

"""
Configuration Components Module for Config-Presets Extension
配置组件模块 - 用于Config-Presets扩展

This module handles the loading and parsing of custom component configurations
for both txt2img and img2img modes. It provides utilities to read component
IDs from configuration files and handle logging.

该模块处理txt2img和img2img模式的自定义组件配置的加载和解析。
它提供了从配置文件读取组件ID和处理日志的工具。
"""

from dataclasses import dataclass
from enum import Enum, unique
import json
from typing import IO, Any
from json import JSONDecodeError


@unique
class EnumTypeName(Enum):
    """
    Enumeration for different configuration type names.
    Used to distinguish between txt2img and img2img modes.

    不同配置类型名称的枚举。
    用于区分txt2img和img2img模式。
    """
    txt2img = "txt2img"  # Text-to-image mode / 文本到图像模式
    img2img = "img2img"  # Image-to-image mode / 图像到图像模式

def log(text: str):
    """
    Print a standard log message with Config Presets prefix.

    打印带有Config Presets前缀的标准日志消息。

    Args:
        text (str): The message to log / 要记录的消息
    """
    print(f"[Config Presets] {text}")


def log_error(text: str):
    """
    Print an error message with Config Presets prefix.

    打印带有Config Presets前缀的错误消息。

    Args:
        text (str): The error message to log / 要记录的错误消息
    """
    print(f"[ERROR][Config Presets] {text}")


def log_critical_error(text: str):
    """
    Print a critical error message with Config Presets prefix.
    Used for severe errors that may prevent the extension from functioning.

    打印带有Config Presets前缀的严重错误消息。
    用于可能阻止扩展正常运行的严重错误。

    Args:
        text (str): The critical error message to log / 要记录的严重错误消息
    """
    print(f"[ERROR][CRITICAL][Config Presets] {text}")


def log_debug(text: str):
    print(f"[DEBUG][Config Presets] {text}")


# 追蹤元件分組標記 (group marker)：##@ <label> 開啟分組、##@ 關閉分組，@ 的數量代表層級
TRACKED_GROUP_MARKER: str = "##@"


@dataclass
class TrackedComponentGroup:
    """
    追蹤元件設定檔中 ##@ ... ##@ 區塊定義的分組 (group)。

    分組會將追蹤清單切割：標記之前的元件 ID 屬根層，區塊內的屬本分組，
    關閉標記之後的元件 ID 回到根層；分組可多層巢狀。

    Attributes:
        label (str): 分組標題，顯示於 UI 摺疊區塊的標頭
        items (list[TrackedComponentItem]): 分組內容，依序為元件 ID (str) 與巢狀分組
    """
    label: str
    items: list["TrackedComponentItem"]


# 一個分組項目：元件 ID (str) 或分組 (TrackedComponentGroup)
TrackedComponentItem = str | TrackedComponentGroup


def _parse_tracked_component_items(file: list[str] | IO[str]) -> list[TrackedComponentItem]:
    """
    Parse tracked components into an ordered tree with ##@ group markers.

    將追蹤元件解析為含 ##@ 分組標記的有序樹狀結構。

    分組語法 (group syntax)，每多一個 @ 則多一層：
        ##@ <label>   開啟分組 (open a group at level 1)；##@@ <label> 為 level 2
        ##@           關閉分組 (close a group at level 1)；##@@ 為 level 2

    以單一 # 開頭的行為註解 (comment)、空白行忽略；
    標記層級不符時記錄錯誤並略過該行，檔案結尾未關閉的分組記錄錯誤後視為已關閉。

    Args:
        file (list[str] | IO[str]): File object or list of strings to parse / 要解析的文件对象或字符串列表

    Returns:
        list[TrackedComponentItem]: 依序排列的元件 ID 與分組 / ordered component IDs and groups
    """
    root: list[TrackedComponentItem] = []
    open_groups: list[TrackedComponentGroup] = []   # 目前開啟的分組；index 即層級 - 1

    def current_items() -> list[TrackedComponentItem]:
        return open_groups[-1].items if len(open_groups) > 0 else root

    for raw_line in file:
        line = raw_line.strip()
        if line == "":
            continue

        if line.startswith(TRACKED_GROUP_MARKER):
            rest = line[len(TRACKED_GROUP_MARKER):]
            at_count = 0
            while at_count < len(rest) and rest[at_count] == "@":
                at_count += 1
            level = 1 + at_count
            label = rest[at_count:].strip()

            if label != "":
                # 開啟分組：層級必須緊接目前層級
                if level != len(open_groups) + 1:
                    log_error(f"Invalid group marker '{line}': expected level {len(open_groups) + 1} at this position, ignoring it")
                    continue
                group = TrackedComponentGroup(label=label, items=[])
                current_items().append(group)
                open_groups.append(group)
            else:
                # 關閉分組：關閉該層及其內層（內層未關閉時視為一併關閉）
                if level > len(open_groups):
                    log_error(f"Invalid group marker '{line}': no open group at level {level}, ignoring it")
                    continue
                del open_groups[level - 1:]
            continue

        if line.startswith("#"):
            continue    # 註解 (comment)

        current_items().append(line)

    if len(open_groups) > 0:
        labels = ", ".join(f"'{group.label}'" for group in open_groups)
        log_error(f"Group marker(s) left unclosed at end of file: {labels}, treating them as closed")

    return root


def flatten_tracked_component_items(items: list[TrackedComponentItem]) -> list[str]:
    """
    將樹狀結構攤平為元件 ID 清單，維持檔案中的排列順序。

    Args:
        items (list[TrackedComponentItem]): 分組解析結果 / parsed group items

    Returns:
        list[str]: 全部元件 ID（含巢狀分組）/ all component IDs including nested groups
    """
    component_ids: list[str] = []
    for item in items:
        if isinstance(item, str):
            component_ids.append(item)
        else:
            component_ids.extend(flatten_tracked_component_items(item.items))
    return component_ids


def _parse_config_components(file: list[str] | IO[str], components_ids: list[str] = []) -> list[str]:  # pyright: ignore[reportCallInDefaultInitializer]
    """
    Parse configuration components from a file or list of strings.

    从文件或字符串列表中解析配置组件。

    This private function parses the file with group markers (##@) and flattens
    the result to a plain component ID list. It's used internally to process
    configuration files that define which UI components should be tracked by
    the Config-Presets extension.

    这个私有函数以分组标记（##@）解析文件后攤平为纯组件ID列表。
    它在内部用于处理定义Config-Presets扩展应该跟踪哪些UI组件的配置文件。

    Args:
        file (list[str] | IO[str]): File object or list of strings to parse / 要解析的文件对象或字符串列表
        components_ids (list[str], optional): Existing list of component IDs to append to.
                                             Defaults to empty list.
                                             要追加的现有组件ID列表，默认为空列表。

    Returns:
        list[str]: List of parsed component IDs / 解析出的组件ID列表

    Note:
        Ignores lines starting with '#' (comments) and empty lines.
        忽略以'#'开头的行（注释）和空行。
    """
    if (not components_ids):
        components_ids = []

    components_ids.extend(flatten_tracked_component_items(_parse_tracked_component_items(file)))
    return components_ids


def load_custom_tracked_component_items(file_path: str, type_name: EnumTypeName, default_config: str) -> list[TrackedComponentItem]:
    """
    Load custom tracked components (with ##@ group structure) from a configuration file.

    从配置文件加载自定义跟踪组件（含 ##@ 分组结构）。

    This function attempts to parse component IDs and groups from a specified
    configuration file. If the file doesn't exist (first run or deleted), it
    creates a new file with default configuration and logs the action.

    该函数尝试从指定的配置文件中解析组件ID与分组。
    如果文件不存在（首次运行或已删除），它会创建一个包含默认配置的新文件并记录此操作。

    Args:
        file_path (str): Path to the configuration file / 配置文件的路径
        type_name (EnumTypeName): Type of configuration (txt2img or img2img) / 配置类型（txt2img或img2img）
        default_config (str): Default configuration content to write if file doesn't exist /
                              如果文件不存在时要写入的默认配置内容

    Returns:
        list[TrackedComponentItem]: 解析結果；檔案剛建立時為空列表
                                    / parsed items; empty list if the file was just created
    """
    try:
        with open(file_path, "r") as file:
            return _parse_tracked_component_items(file)
    except FileNotFoundError:
        # config file not found
        # 配置文件未找到
        # First time running the extension or it was deleted, so fill it with default values
        # 首次运行扩展或文件被删除，所以用默认值填充
        _write_text_to_file(default_config, file_path)
        log(f"{type_name.value} custom tracked components config file not found, created default config at {file_path}")

    return []


def load_custom_tracked_component_ids(file_path: str, type_name: EnumTypeName, default_config: str) -> list[str]:
    """
    Load custom tracked component IDs from a configuration file.

    从配置文件加载自定义跟踪组件ID（攤平 ##@ 分组结构后的清单）。

    This function attempts to read component IDs from a specified configuration file.
    If the file doesn't exist (first run or deleted), it creates a new file with default
    configuration and logs the action. This ensures the extension always has a valid
    configuration file to work with.

    该函数尝试从指定的配置文件中读取组件ID（攤平分组结构）。
    如果文件不存在（首次运行或已删除），它会创建一个包含默认配置的新文件
    并记录此操作。这确保扩展始终有有效的配置文件可以使用。

    Args:
        file_path (str): Path to the configuration file / 配置文件的路径
        type_name (EnumTypeName): Type of configuration (txt2img or img2img) / 配置类型（txt2img或img2img）
        default_config (str): Default configuration content to write if file doesn't exist /
                              如果文件不存在时要写入的默认配置内容

    Returns:
        list[str]: List of component IDs loaded from the file or empty list if file was just created
                  / 从文件加载的组件ID列表，如果文件刚创建则为空列表

    Side Effects:
        - Creates the configuration file with default content if it doesn't exist
        - Logs the file creation action
        - 如果文件不存在，则使用默认内容创建配置文件
        - 记录文件创建操作
    """
    return flatten_tracked_component_items(load_custom_tracked_component_items(file_path, type_name, default_config))


def _write_text_to_file(text: str, file_path: str):
    """
    Write text content to a file, overwriting any existing content.

    将文本内容写入文件，覆盖任何现有内容。

    This is a private helper function used internally to create configuration
    files with default content when they don't exist. It writes the provided
    text to the specified file path in write mode.

    这是一个私有辅助函数，在内部用于在配置文件不存在时创建包含
    默认内容的文件。它以写入模式将提供的文本写入指定的文件路径。

    Args:
        text (str): Text content to write to the file / 要写入文件的文本内容
        file_path (str): Path where the file should be created/overwritten / 应创建/覆盖文件的路径

    Side Effects:
        - Creates or overwrites the file at the specified path
        - 在指定路径创建或覆盖文件

    Note:
        Uses write mode ('w') which will overwrite existing files.
        使用写入模式('w')，这将覆盖现有文件。
    """
    with open(file_path, "w") as file:
        file.write(text)

def write_json_to_file(json_data: Any, file_path: str):
    """
    Write JSON data to a file with proper indentation.

    将JSON数据以适当的缩进写入文件。
    """
    with open(file_path, "w") as file:
        file.write(json.dumps(json_data, indent=2))

# 保留預設名稱：永遠置頂、不可儲存、不可刪除、不寫入任何設定檔
RESERVED_PRESET_NAME = "None"


def is_reserved_preset_name(name: str) -> bool:
    """
    判斷名稱是否為保留預設（None），不區分大小寫。
    """
    return isinstance(name, str) and name.casefold() == RESERVED_PRESET_NAME.casefold()


def strip_reserved_preset(presets: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    無視並剔除集合中的保留預設（None），不區分大小寫。
    """
    return {name: value for name, value in presets.items() if not is_reserved_preset_name(name)}

def load_config_file(file_path: str, type_name: EnumTypeName) -> dict[str, dict[str, Any]]:
    """
    從 JSON 檔載入自訂預設 (custom presets)，與內建預設脫鉤。

    此函式僅負責讀取使用者的自訂預設：
    1. 嘗試載入 JSON 檔
    2. 檔案不存在時建立空的自訂預設檔（內建預設不再寫入使用者設定檔）
    3. 檔案損壞時記錄錯誤並回傳錯誤預設

    Args:
        file_path (str): 設定檔路徑 / config file path
        type_name (EnumTypeName): txt2img 或 img2img

    Returns:
        dict: 僅含檔案內容的自訂預設 / custom presets loaded from the file only
    """
    try:
        with open(file_path) as file:
            return json.load(file)

    except (FileNotFoundError, JSONDecodeError) as e:
        # JSONDecodeError can happen and prevent Web UI from loading if the json file is malformed
        # JSONDecodeError会在json文件格式错误时发生，并阻止Web UI加载

        if e.__class__ == FileNotFoundError:
            # 自訂預設與內建預設脫鉤：首次執行建立空的自訂預設檔
            write_json_to_file({}, file_path)
            log(f"{type_name.value} config file not found. Created empty {type_name.value} custom presets at {file_path}")
        elif e.__class__ == JSONDecodeError:
            # File corrupted - log error and return error preset
            # 文件损坏 - 记录错误并返回错误预设
            log_error(f"failed to load {type_name.value} config file at {file_path}")
            log_error(f"at line {e.lineno}, col {e.colno}: {e.msg}")
            log_error(f"Loading default presets until you fix the syntax error, or you could delete the file and let it be recreated with default values.")
            return {"ERROR loading your config file! See console for details": {}}

    return {}

def dict_synonyms(d: dict[str, Any], lsyn: list[tuple[str, str]] ):
    """
    Adds synonyms to keys in a given dictionary.

    lsyn = [(key1,key2..), (key3,key4..) ...]
    Key2 will receive the value of key1 if it exists and vice versa.
    If both key3 and key4 exist, then they'll keep their old values.
    If two keys have values and a third doesn't, then it will be assigned to one of the two randomly.
    One liner partly written by a chatbot.

    为给定字典中的键添加同义词。

    lsyn = [(key1,key2..), (key3,key4..) ...]
    如果key1存在，key2将接收key1的值，反之亦然。
    如果key3和key4都存在，它们将保持旧值。
    如果两个键有值而第三个没有，那么它将被随机分配给其中一个。
    单行代码部分由聊天机器人编写。
    """
    d2: dict[str, Any] = {key: d[existing_key] # Get existing value.
          for syn in lsyn # Loop over synonyms.
          for key in syn # Loop over each key in the set.
          for existing_key in syn  # Find existing key to copy from.
          if existing_key in d and key not in d} # Only if the key doesn't exist already.
    d2.update(d) # Add back all existing keys.
    return d2