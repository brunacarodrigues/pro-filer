from pro_filer.actions.main_actions import show_disk_usage  # NOQA
from unittest.mock import Mock, patch


def test_show_disk_usage_empty_files_list(capsys):
    context = {"all_files": []}

    show_disk_usage(context)
    captured = capsys.readouterr()

    expected_output = "Total size: 0\n"
    assert captured.out == expected_output


def test_show_disk_usage_all_files(capsys, tmp_path):
    file1 = tmp_path / "tmp_epub.txt"
    file2 = tmp_path / "tmp_txt.txt"
    file3 = tmp_path / "tmp_icon.txt"

    CONTENT1 = "content.svg"
    CONTENT2 = "content.pdf.xls"
    CONTENT3 = "content.txts"

    file1.write_text(CONTENT1)
    file2.write_text(CONTENT2)
    file3.write_text(CONTENT3)

    mock_get_printable_file_path = Mock(return_value="/content/")

    context = {"all_files": [file1, file2, file3]}
    expected_output = (
        "'/content/':"
        "                                                           15 (39%)\n"
        "'/content/':"
        "                                                           12 (31%)\n"
        "'/content/':"
        "                                                           11 (28%)\n"
        "Total size: 38\n"
    )
    with patch(
        "pro_filer.actions.main_actions._get_printable_file_path",
        mock_get_printable_file_path,
    ):
        show_disk_usage(context)
        captured = capsys.readouterr()
        assert captured.out == expected_output
