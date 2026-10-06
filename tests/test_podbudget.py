import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from podbudget import core


class PodbudgetTest(unittest.TestCase):
    def test_evict_allowed_with_room(self):
        state = core.State(100)
        state.add_workload("A", 10, 2)
        self.assertEqual(state.evict("A", "op1", 0, core.Counter()), "allowed")

    def test_evict_denied_without_budget(self):
        state = core.State(100)
        state.add_workload("A", 2, 2)
        self.assertEqual(state.evict("A", "op1", 0, core.Counter()), "denied")

    def test_two_ops_allowed_with_room(self):
        state = core.State(100)
        state.add_workload("A", 10, 2)
        c = core.Counter()
        first = state.evict("A", "op1", 0, c)
        second = state.evict("A", "op2", 0, c)
        self.assertEqual((first, second), ("allowed", "allowed"))

    def test_workload_stored(self):
        state = core.State(100)
        state.add_workload("A", 5, 1)
        self.assertEqual(state.workloads["A"], (5, 1))

    def test_window_stored(self):
        self.assertEqual(core.State(7).window, 7)

    def test_counter_counts(self):
        state = core.State(100)
        state.add_workload("A", 10, 2)
        c = core.Counter()
        state.evict("A", "op1", 0, c)
        self.assertGreater(c.scanned, 0)


if __name__ == "__main__":
    unittest.main()
