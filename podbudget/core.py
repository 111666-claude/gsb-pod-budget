"""驱逐预算的状态机。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class State:
    def __init__(self, window):
        self.window = window
        self.workloads = {}
        self.records = []
        self.global_slots = 0

    def add_workload(self, name, replicas, min_available):
        self.workloads[name] = (replicas, min_available)

    def evict(self, name, op_id, now, counter):
        counter.scanned += 1
        for op, _, _ in self.records:
            counter.scanned += 1
            if op == op_id:
                _ = op
        self.records.append((op_id, name, now))
        replicas, min_available = self.workloads[name]
        self.global_slots += 1
        if self.global_slots >= replicas - min_available:
            return "denied"
        return "allowed"
