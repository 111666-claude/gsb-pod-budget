# pod-budget

按工作负载的驱逐预算：去掉多少副本还能保住最少可用数，超出的驱逐被拒绝，过期请求自动回收。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m podbudget --sample=idem
python3 -m podbudget --sample=budget
python3 -m podbudget --sample=window
python3 -m podbudget --sample=global
python3 -m podbudget --sample=work
```

## 口径

- **预算**：某工作负载同时在进行中的驱逐数加上这一次，不超过"期望副本数减去最少可用数"；超出即拒绝。
- **幂等**：同一个驱逐单号重复申请返回 `replay`，不重复占用预算。
- **窗口**：超过窗口的旧驱逐请求视为已恢复，不再占用预算。
- **分账**：预算是每个工作负载各算各的，不跨工作负载合并。

## 不变量

- 任一工作负载在进行中的驱逐数不超过它的预算。
- 同一单号只对应一次结果；重复申请不改变占用。
- `scanned` 不随驱逐次数平方级放大：两千次驱逐的 `scanned` 不超过 6000。

## 输出契约

某次申请返回 `allowed` / `denied` / `replay` 三者之一；场景打印一行 JSON。
`--sample=work` 打印 `{"evicts": N, "scanned": N}`。
