from pro_filer.actions.main_actions import show_details  # NOQA
import os
from datetime import datetime


def test_show_details_file_exists(capsys, tmp_path):
    # Crie um arquivo temporário para o teste
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Test content")

    context = {"base_path": str(file_path)}

    show_details(context)
    captured = capsys.readouterr()

    # Obtém o tamanho do arquivo e a data de modificação
    file_size = os.path.getsize(file_path)
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

    expected_output = (
        f"File name: test_file.txt\n"
        f"File size in bytes: {file_size}\n"
        f"File type: file\n"
        f"File extension: .txt\n"
        f"Last modified date: {mod_time}"
    )

    assert captured.out.strip() == expected_output


def test_show_details_file_not_exists(capsys, tmp_path):
    file_path = tmp_path / "non_existent_file.txt"

    context = {"base_path": str(file_path)}

    show_details(context)
    captured = capsys.readouterr()

    expected_output = "File 'non_existent_file.txt' does not exist"

    assert captured.out.strip() == expected_output


def test_show_details_directory(capsys, tmp_path):
    # Crie um diretório temporário para o teste
    dir_path = tmp_path / "test_dir"
    os.mkdir(dir_path)

    context = {"base_path": str(dir_path)}

    show_details(context)
    captured = capsys.readouterr()

    expected_output = (
        f"File name: test_dir\n"
        f"File size in bytes: {os.path.getsize(dir_path)}\n"
        f"File type: directory\n"
        f"File extension: [no extension]\n"
        f"Last modified date: {datetime.today().date()}"
    )

    assert captured.out.strip() == expected_output
