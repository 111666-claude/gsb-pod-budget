"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "idem":
        state = core.State(100)
        state.add_workload("A", 4, 2)
        c = core.Counter()
        state.evict("A", "op1", 0, c)
        second = state.evict("A", "op1", 0, c)
        third = state.evict("A", "op2", 0, c)
        _line({"second": second, "third": third})
        return 0
    if name == "budget":
        state = core.State(100)
        state.add_workload("A", 3, 2)
        _line({"first": state.evict("A", "op1", 0, core.Counter())})
        return 0
    if name == "window":
        state = core.State(10)
        state.add_workload("A", 3, 2)
        c = core.Counter()
        state.evict("A", "op1", 0, c)
        _line({"second": state.evict("A", "op2", 100, c)})
        return 0
    if name == "global":
        state = core.State(100)
        state.add_workload("A", 3, 2)
        state.add_workload("B", 3, 2)
        c = core.Counter()
        state.evict("A", "op1", 0, c)
        _line({"b": state.evict("B", "op1", 0, c)})
        return 0
    if name == "work":
        state = core.State(10000000)
        state.add_workload("A", 100000, 0)
        c = core.Counter()
        for i in range(2000):
            state.evict("A", "op%04d" % i, i, c)
        _line({"evicts": 2000, "scanned": c.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
