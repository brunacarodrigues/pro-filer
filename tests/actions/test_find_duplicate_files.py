from pro_filer.actions.main_actions import find_duplicate_files  # NOQA
import tempfile
import os
import pytest


def test_find_duplicate_files_with_duplicates():
    file1 = tempfile.NamedTemporaryFile(delete=False)
    file2 = tempfile.NamedTemporaryFile(delete=False)

    file1.write(b"Test content")
    file2.write(b"Test content")

    file1.close()
    file2.close()

    context = {"all_files": [file1.name, file2.name]}
    duplicates = find_duplicate_files(context)

    assert (file1.name, file2.name) in duplicates

    os.unlink(file1.name)
    os.unlink(file2.name)


def test_find_duplicate_files_without_duplicates():
    file1 = tempfile.NamedTemporaryFile(delete=False)
    file2 = tempfile.NamedTemporaryFile(delete=False)

    file1.write(b"Test content 1")
    file2.write(b"Test content 2")

    file1.close()
    file2.close()

    context = {"all_files": [file1.name, file2.name]}
    duplicates = find_duplicate_files(context)

    assert len(duplicates) == 0

    os.unlink(file1.name)
    os.unlink(file2.name)


def test_find_duplicate_files_ignore_inexistent_files():
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file_path = file.name

    def _test_ignore_inexistent_files():
        return []

    context = {"all_files": [file_path]}

    try:
        find_duplicate_files(context)
    except FileNotFoundError:
        pytest.fail("A função não deve lançar um erro FileNotFoundError")

    os.unlink(file_path)


def test_find_duplicate_files_with_tmp_path_fixture(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("Test content")
    file2.write_text("Test content")

    context = {"all_files": [str(file1), str(file2)]}
    duplicates = find_duplicate_files(context)

    assert (str(file1), str(file2)) in duplicates


def test_find_duplicate_inexistent_files(tmp_path):
    CONTENT = "file_content"

    dir_1 = tmp_path / "dir_1"
    dir_1.mkdir()
    file1_path = dir_1 / "file1.txt"
    file1_path.write_text(CONTENT)

    context = {
        "all_files": [
            f"{file1_path}",
            "path/no/exist/file1.txt",
        ]
    }

    with pytest.raises(ValueError, match="All files must exist"):
        find_duplicate_files(context)
