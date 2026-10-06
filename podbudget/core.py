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
        self._active = {}
        self._queue = {}
        self._inflight = {}

    def add_workload(self, name, replicas, min_available):
        self.workloads[name] = (replicas, min_available)

    def _reclaim_expired(self, name, now, counter):
        queue = self._queue.get(name)
        if queue is None:
            return
        active = self._active[name]
        while queue:
            counter.scanned += 1
            ts, op_id = queue[0]
            if now - ts <= self.window:
                break
            queue.popleft()
            del active[op_id]
            self._inflight[name] -= 1

    def evict(self, name, op_id, now, counter):
        counter.scanned += 1
        self._reclaim_expired(name, now, counter)
        active = self._active.setdefault(name, {})
        if op_id in active:
            return "replay"
        replicas, min_available = self.workloads[name]
        if self._inflight.get(name, 0) + 1 > replicas - min_available:
            return "denied"
        active[op_id] = now
        self._queue.setdefault(name, deque()).append((now, op_id))
        self._inflight[name] = self._inflight.get(name, 0) + 1
        return "allowed"
