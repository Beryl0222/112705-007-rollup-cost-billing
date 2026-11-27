# Rollup 批次发布成本的归属与计费

合成 Rollup 发布器与一层回执对账资料。 每个 JSONL 文件都是独立的演练时钟。资料约定见 [输入协议](docs/input.md)。

使用 Python 3.11.2 和标准库。在项目根目录核验资料格式。

```sh
python3 inspect_inputs.py
python3 -m unittest discover -s tests -v
```

检查程序只负责读取和核对输入格式，运行后显示每个演练文件所包含的记录。演练资料位于 `data/`。

- `data/one-publish.jsonl`
- `data/operator-repost.jsonl`
