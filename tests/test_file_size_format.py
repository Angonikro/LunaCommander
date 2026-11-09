from pathlib import Path
import ast


def formatter():
    source = (Path(__file__).parents[1] / "main.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "format_file_size")
    module = ast.Module(body=[node], type_ignores=[])
    namespace = {}
    exec(compile(module, "main.py", "exec"), namespace)
    return namespace["format_file_size"]


def test_112426_bytes_is_not_shown_as_11_kb():
    assert formatter()(112426) == "110 KB"


def test_integer_values_keep_trailing_zeroes():
    fmt = formatter()
    assert fmt(100 * 1024) == "100 KB"
    assert fmt(1024 * 1024 * 100) == "100 MB"
    assert fmt(1024 * 1024 * 1000) == "1,000 MB"


def test_decimal_values_still_trim_unneeded_zeroes():
    fmt = formatter()
    assert fmt(10 * 1024 + 512) == "10.5 KB"
    assert fmt(1024 + 0) == "1 KB"
