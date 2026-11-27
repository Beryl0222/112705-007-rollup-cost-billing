"""验证演练资料与其输入协议相符。"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from inspect_inputs import DATA, load_schema, load_stream


class InputContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = load_schema()
        self.paths = sorted(DATA.glob("*.jsonl"))

    def test_all_streams_are_readable(self):
        self.assertTrue(self.paths)
        seen = set()
        for path in self.paths:
            with self.subTest(path=path.name):
                records = load_stream(path, self.schema)
                self.assertEqual(records[-1]["seq"], len(records))
                seen.update(record["kind"] for record in records)
        self.assertEqual(seen, set(self.schema))

    def test_reader_rejects_rewound_time(self):
        records = load_stream(self.paths[0], self.schema)
        records[-1]["observed"] = -1
        with TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "观察时间无效"):
                load_stream(path, self.schema)

    def test_reader_rejects_unknown_record_field(self):
        first = load_stream(self.paths[0], self.schema)[0]
        first["payload"]["unknown"] = 1
        with TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text(json.dumps(first), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "内容字段不匹配"):
                load_stream(path, self.schema)


if __name__ == "__main__":
    unittest.main()
