

"""
Configuration Components Module for Config-Presets Extension
配置组件模块 - 用于Config-Presets扩展

This module handles the loading and parsing of custom component configurations
for both txt2img and img2img modes. It provides utilities to read component
IDs from configuration files and handle logging.

该模块处理txt2img和img2img模式的自定义组件配置的加载和解析。
它提供了从配置文件读取组件ID和处理日志的工具。
"""

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


def _parse_config_components(file: list[str] | IO[str], components_ids: list[str] = []) -> list[str]:  # pyright: ignore[reportCallInDefaultInitializer]
    """
    Parse configuration components from a file or list of strings.
    
    从文件或字符串列表中解析配置组件。
    
    This private function reads through lines of text, filters out comments and empty lines,
    and extracts valid component IDs. It's used internally to process configuration files
    that define which UI components should be tracked by the Config-Presets extension.
    
    这个私有函数读取文本行，过滤掉注释和空行，并提取有效的组件ID。
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

    for line in file:
        line = line.strip()
        if not line.startswith("#") and line != "":  # ignore lines that start with # or are empty
            # 忽略以#开头的行或空行
            components_ids.append(line)
            # log_debug(f"Added txt2img custom tracked component: {line}")
            # log_debug(f"添加txt2img自定义跟踪组件：{line}")
    return components_ids


def load_custom_tracked_component_ids(file_path: str, type_name: EnumTypeName, default_config: str) -> list[str]:
    """
    Load custom tracked component IDs from a configuration file.
    
    从配置文件加载自定义跟踪组件ID。
    
    This function attempts to read component IDs from a specified configuration file.
    If the file doesn't exist (first run or deleted), it creates a new file with default
    configuration and logs the action. This ensures the extension always has a valid
    configuration file to work with.
    
    该函数尝试从指定的配置文件中读取组件ID。
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
    components_ids: list[str] = []
    try:
        with open(file_path, "r") as file:
            components_ids = _parse_config_components(file)
    except FileNotFoundError:
        # config file not found
        # 配置文件未找到
        # First time running the extension or it was deleted, so fill it with default values
        # 首次运行扩展或文件被删除，所以用默认值填充
        _write_text_to_file(default_config, file_path)
        log(f"{type_name} custom tracked components config file not found, created default config at {file_path}")
        # log(f"{type_name}自定义跟踪组件配置文件未找到，在{file_path}创建了默认配置")

    return components_ids


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

def load_config_file(file_path: str, type_name: EnumTypeName, default_presets: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Generic function to load configuration presets from JSON file.
    
    通用函数，用于从JSON文件加载配置预设。
    
    This function follows the same pattern as load_custom_tracked_component_ids():
    1. Try to load the JSON file
    2. If the file doesn't exist or is corrupted, use the default presets
    3. Handle different error types appropriately
    4. Log the actions taken
    
    此函数遵循与load_custom_tracked_component_ids()相同的模式：
    1. 尝试加载JSON文件
    2. 如果文件不存在或损坏，使用默认预设
    3. 适当处理不同错误类型
    4. 记录执行的操作
    
    Args:
        file_path (str): Name of the config file / 配置文件名
        type_name (EnumTypeName): Type of configuration (txt2img or img2img) / 配置类型（txt2img或img2img）
        default_presets (dict): Default presets to use if file loading fails / 文件加载失败时使用的默认预设
    
    Returns:
        dict: Dictionary containing configuration presets / 包含配置预设的字典
    """
    try:
        with open(file_path) as file:
            return json.load(file)

    except (FileNotFoundError, JSONDecodeError) as e:
        # JSONDecodeError can happen and prevent Web UI from loading if the json file is malformed
        # JSONDecodeError会在json文件格式错误时发生，并阻止Web UI加载
        
        if e.__class__ == FileNotFoundError:
            # File not found - create with defaults
            # 文件未找到 - 使用默认值创建
            write_json_to_file(default_presets, file_path)
            log(f"{type_name} config file not found. Created default {type_name} config at {file_path}")
        elif e.__class__ == JSONDecodeError:
            # File corrupted - log error and return error preset
            # 文件损坏 - 记录错误并返回错误预设
            log_error(f"failed to load {type_name} config file at {file_path}")
            log_error(f"at line {e.lineno}, col {e.colno}: {e.msg}")
            log_error(f"Loading default presets until you fix the syntax error, or you could delete the file and let it be recreated with default values.")
            return {"ERROR loading your config file! See console for details": {}}

    return default_presets

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