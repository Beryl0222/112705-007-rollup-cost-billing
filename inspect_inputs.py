"""读取演练事件文件并检查外层记录和字段类型。"""

from collections import Counter
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
FIELD_TYPES = {"s": str, "i": int, "a": list, "b": bool}
RECORD_KEYS = {"seq", "observed", "kind", "payload"}


def load_schema():
    """返回演练允许的记录类型与字段表。"""
    return json.loads((DATA / "schema.json").read_text(encoding="utf-8"))


def load_stream(path, schema):
    """按原始到达顺序读取一份演练记录。"""
    records = []
    last_time = -1
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            location = f"{path.name} 第 {line_number} 行"
            if type(record) is not dict or set(record) != RECORD_KEYS:
                raise ValueError(f"{location}缺少预期的事件字段")
            if type(record["seq"]) is not int or record["seq"] != line_number:
                raise ValueError(f"{location}事件序号不连续")
            observed = record["observed"]
            if type(observed) is not int or observed < 0 or observed < last_time:
                raise ValueError(f"{location}的观察时间无效")
            kind = record["kind"]
            if type(kind) is not str or kind not in schema:
                raise ValueError(f"{location}的记录类型无效")
            payload = record["payload"]
            fields = schema[kind]
            if type(payload) is not dict or set(payload) != set(fields):
                raise ValueError(f"{location}的内容字段不匹配")
            for key, declared_type in fields.items():
                if type(payload[key]) is not FIELD_TYPES[declared_type]:
                    raise ValueError(f"{location}的 {key} 类型不匹配")
            records.append(record)
            last_time = observed
    if not records:
        raise ValueError(f"{path.name}没有事件")
    return records


def main():
    """列出每份演练输入的记录类型与数量。"""
    schema = load_schema()
    for path in sorted(DATA.glob("*.jsonl")):
        records = load_stream(path, schema)
        counts = Counter(record["kind"] for record in records)
        kinds = "，".join(f"{kind} {count}" for kind, count in sorted(counts.items()))
        print(f"{path.name} 共 {len(records)} 条（{kinds}）")


if __name__ == "__main__":
    main()
