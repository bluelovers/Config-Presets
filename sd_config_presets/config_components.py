

from enum import Enum, unique
from typing import IO


@unique
class EnumTypeName(Enum):
    txt2img = "txt2img"
    img2img = "img2img"

def log(text: str):
    print(f"[Config Presets] {text}")


def log_error(text: str):
    print(f"[ERROR][Config Presets] {text}")


def log_critical_error(text: str):
    print(f"[ERROR][CRITICAL][Config Presets] {text}")


def _parse_config_components(file: list[str] | IO[str], components_ids: list[str] = []) -> list[str]:  # pyright: ignore[reportCallInDefaultInitializer]
    if (not components_ids):
        components_ids = []

    for line in file:
        line = line.strip()
        if not line.startswith("#") and line != "":  # ignore lines that start with # or are empty
            components_ids.append(line)
            #print(f"Added txt2img custom tracked component: {line}")
    return components_ids


def load_custom_tracked_component_ids(file_path: str, type_name: EnumTypeName, default_config: str) -> list[str]:
    components_ids: list[str] = []
    try:
        with open(file_path, "r") as file:
            components_ids = _parse_config_components(file)
    except FileNotFoundError:
        # config file not found
        # First time running the extension or it was deleted, so fill it with default values
        _write_text_to_file(default_config, file_path)
        log(f"{type_name} custom tracked components config file not found, created default config at {file_path}")

    return components_ids


def _write_text_to_file(text: str, file_path: str):
    with open(file_path, "w") as file:
        file.write(text)  # pyright: ignore[reportUnusedCallResult]

