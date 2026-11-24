from pathlib import Path
import ast
import os


def clipboard_matcher():
    source = (Path(__file__).parents[1] / "main.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    main_class = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Main")
    method = next(n for n in main_class.body if isinstance(n, ast.FunctionDef) and n.name == "_clipboard_matches_internal_selection")
    module = ast.Module(body=[method], type_ignores=[])
    namespace = {"Path": Path, "os": os}
    exec(compile(module, "main.py", "exec"), namespace)
    return namespace[method.name]


class Pane:
    def __init__(self, path, remote=False, archive_file=None):
        self.path = str(path)
        self.remote = remote
        self.archive_file = archive_file


class App:
    _clipboard_matches_internal_selection = clipboard_matcher()

    def __init__(self, clip):
        self.clip = clip


def test_internal_clipboard_matches_uri_list_after_private_mime_is_stripped(tmp_path):
    (tmp_path / "one.txt").write_text("one")
    (tmp_path / "two.txt").write_text("two")
    app = App((Pane(tmp_path), [("one.txt", False), ("two.txt", False)], True))
    assert app._clipboard_matches_internal_selection([
        str(tmp_path / "one.txt"), str(tmp_path / "two.txt")
    ])


def test_internal_clipboard_does_not_claim_an_unrelated_external_selection(tmp_path):
    (tmp_path / "one.txt").write_text("one")
    (tmp_path / "other.txt").write_text("other")
    app = App((Pane(tmp_path), [("one.txt", False)], False))
    assert not app._clipboard_matches_internal_selection([str(tmp_path / "other.txt")])


def test_remote_internal_clipboard_does_not_depend_on_local_uri_list():
    app = App((Pane("/remote", remote=True), [("one.txt", False)], True))
    assert app._clipboard_matches_internal_selection([])


def test_internal_clipboard_uses_original_source_directory_after_navigation(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "picked.txt").write_text("payload")
    pane = Pane(tmp_path / "elsewhere")
    app = App((pane, [("picked.txt", False)], False))
    app.clip_source_path = str(source)
    assert app._clipboard_matches_internal_selection([str(source / "picked.txt")])
