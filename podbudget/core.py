"""驱逐预算的状态机。"""

from collections import deque


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class State:
    def __init__(self, window):
        self.window = window
        self.workloads = {}
        self.records = {}
        self.ops = {}

    def add_workload(self, name, replicas, min_available):
        self.workloads[name] = (replicas, min_available)

    def _reclaim(self, name, now, counter):
        records = self.records.setdefault(name, deque())
        while records and now - records[0][1] > self.window:
            counter.scanned += 1
            op_id, _ = records.popleft()
            self.ops.pop((name, op_id), None)
        return records

    def evict(self, name, op_id, now, counter):
        counter.scanned += 1
        records = self._reclaim(name, now, counter)
        key = (name, op_id)
        if key in self.ops:
            _, ts = self.ops[key]
            if now - ts <= self.window:
                return "replay"
            self.ops.pop(key, None)
        replicas, min_available = self.workloads[name]
        if len(records) + 1 > replicas - min_available:
            return "denied"
        records.append((op_id, now))
        self.ops[(name, op_id)] = (name, now)
        return "allowed"
