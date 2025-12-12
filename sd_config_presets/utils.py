
from os import startfile, path
from platform import system
from subprocess import Popen

from sd_config_presets.config_components import log


def open_file_in_system_app(file_path: str) -> None:
    """
    Open a file using the system's default application.
    
    使用系统默认应用程序打开文件。
    """
    file_path = path.normpath(file_path)

    if not path.exists(file_path):
        log(f'The file at "{file_path}" does not exist.')
        return

    # copied from ui.py:538
    # 从ui.py:538复制
    if system() == "Windows":
        startfile(file_path)
    elif system() == "Darwin":
        Popen(["open", file_path])
    else:
        Popen(["xdg-open", file_path])

