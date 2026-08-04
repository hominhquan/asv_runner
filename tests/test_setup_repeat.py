# asv#966: setup must restore state before each timed sample when number>1
# would otherwise run the stmt multiple times under one setup.

import os
import sys
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from asv_runner.benchmarks.time import TimeBenchmark  # noqa: E402


class TestSetupBeforeEachSample(unittest.TestCase):
    def test_setup_restores_state_across_samples(self):
        """Reproducer from asv#966: mutating setup must not fail timing."""

        class Suite:
            number = 10  # would re-mutate without re-setup if number>1
            repeat = 5
            warmup_time = 0
            min_run_count = 1
            rounds = 1
            processes = 1

            def setup(self):
                self.x = []

            def time_1(self):
                assert len(self.x) == 0
                self.x.append(0)

            def time_2(self):
                assert len(self.x) == 0

        suite = Suite()
        b = TimeBenchmark(
            "Suite.time_1",
            suite.time_1,
            [suite.time_1, suite],
        )
        b.do_setup()
        result = b.run()
        self.assertEqual(result["number"], 1)
        self.assertGreaterEqual(len(result["samples"]), 1)

    def test_auto_number_allowed_without_setup(self):
        def time_fast():
            return 1 + 1

        time_fast.number = 0  # auto
        time_fast.repeat = 2
        time_fast.warmup_time = 0
        time_fast.sample_time = 0.001
        time_fast.min_run_count = 1
        time_fast.rounds = 1
        time_fast.processes = 1

        b = TimeBenchmark("m.time_fast", time_fast, [time_fast])
        b.do_setup()
        result = b.run()
        # Without setup, auto number may be > 1 for a tiny function.
        self.assertGreaterEqual(result["number"], 1)
        self.assertGreaterEqual(len(result["samples"]), 1)


if __name__ == "__main__":
    unittest.main()
