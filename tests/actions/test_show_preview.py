from pro_filer.actions.main_actions import show_preview  # NOQA


def test_show_preview_no_files_or_dirs(capsys):
    context = {"all_files": [], "all_dirs": []}

    show_preview(context)
    captured = capsys.readouterr()

    assert captured.out.strip() == "Found 0 files and 0 directories"


def test_show_preview_with_files_and_dirs(capsys):
    context = {
        "all_files": ["file1.txt", "file2.txt", "file3.txt"],
        "all_dirs": ["dir1", "dir2", "dir3"]
    }

    show_preview(context)
    captured = capsys.readouterr()

    expected_output = (
        "Found 3 files and 3 directories\n"
        "First 5 files: ['file1.txt', 'file2.txt', 'file3.txt']\n"
        "First 5 directories: ['dir1', 'dir2', 'dir3']"
    )

    assert captured.out.strip() == expected_output


def test_show_preview_only_files(capsys):
    context = {
        "all_files": ["file1.txt", "file2.txt", "file3.txt"],
        "all_dirs": []
    }

    show_preview(context)
    captured = capsys.readouterr()

    expected_output = (
        "Found 3 files and 0 directories\n"
        "First 5 files: ['file1.txt', 'file2.txt', 'file3.txt']\n"
    )

    assert captured.out == expected_output


def test_show_preview_only_dirs(capsys):
    context = {
        "all_files": [],
        "all_dirs": ["dir1", "dir2", "dir3"]
    }

    show_preview(context)
    captured = capsys.readouterr()

    expected_output = (
        "Found 0 files and 3 directories\n"
        "First 5 directories: ['dir1', 'dir2', 'dir3']"
    )

    assert captured.out.strip() == expected_output
