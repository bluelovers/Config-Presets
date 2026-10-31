"""
擴充功能命令列參數預載：註冊 --configpresets-dir，
指定設定檔（config-txt2img.json、custom tracked components 等）所在資料夾，
預設仍為本擴充功能目錄。WebUI 啟動解析 COMMANDLINE_ARGS 前會載入本檔並呼叫 preload(parser)，
使多個 WebUI 安裝得共享同一份自訂預設。
"""

from pathlib import Path


def preload(parser):
    parser.add_argument("--configpresets-dir", type=Path, help="[Extension][Config-Presets] Path to directory with Config Presets configuration files (use forward slashes or double backslashes). Default config files will be created if none exist.", default=None)
