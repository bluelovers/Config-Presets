"""
X/Y/Z plot 值的 CSV 轉換相容層 (Compatibility)。

收拢 csv → list、list → csv 的轉換邏輯：
- list_to_csv_string 與 scripts/xyz_grid.py 的同名實作一致；
- csv_string_to_list_strip 優先借用 xyz_grid 的現成實作（lazy import），
  借不到才退回逗號切分，避免在此重寫解析邏輯。
"""

import csv
from io import StringIO
from typing import Any


def list_to_csv_string(data_list: list[str]) -> str:
    """
    將值列表轉為單個 CSV 字串。

    實作與 scripts/xyz_grid.py（X/Y/Z plot）的 list_to_csv_string 一致，
    使從其 dropdown UI 儲存的值能經 csv_string_to_list_strip() 一致解析。
    """
    with StringIO() as o:
        csv.writer(o).writerow(data_list)
        return o.getvalue().strip()


def csv_string_to_list_strip(data_str: str) -> list[str]:
    """
    將 CSV 字串解析為值列表；優先借用 xyz_grid.py 的同名實作，借不到才逗號切分。

    於呼叫當下 lazy import，避免模組載入期依賴 xyz_grid 是否已註冊。
    """
    try:
        from scripts.xyz_grid import csv_string_to_list_strip as parse_csv
    except Exception:
        try:
            from xyz_grid import csv_string_to_list_strip as parse_csv
        except Exception:
            parse_csv = None  # type: ignore[assignment]
    if parse_csv is not None:
        return parse_csv(data_str)
    return [value.strip() for value in data_str.split(",") if value.strip() != ""]


def split_csv_text_and_list(owner_value: Any) -> tuple[Any, list[str]]:
    """
    將預設儲存的擁有者值拆成雙寫兩邊：(文字框 CSV 值, 多選框列表值)。

    list 值轉 CSV 寫文字框、原列表給多選框；非空字串原樣留文字框並解析出列表；
    空值／None 文字框維持原值、多選框清空。
    """
    if isinstance(owner_value, list):
        return list_to_csv_string(owner_value), owner_value
    if isinstance(owner_value, str) and owner_value.strip() != "":
        return owner_value, csv_string_to_list_strip(owner_value)
    return owner_value, []


def resolve_saved_csv_value(textbox_value: Any, derived_value: Any) -> Any:
    """
    儲存時決定落盤值：配對多選框為非空列表時以其轉 CSV 為準，否則沿用文字框值。

    雙寫後文字框可能留著舊串，先判定多選框才能存到下拉模式的後改；
    文字模式的後改會被同一次雙寫的舊多選蓋掉（測試性取捨）。
    """
    if isinstance(derived_value, list) and len(derived_value) > 0:
        return list_to_csv_string(derived_value)
    return textbox_value
