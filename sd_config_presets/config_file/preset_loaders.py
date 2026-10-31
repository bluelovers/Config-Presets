"""
內建預設定義與設定檔載入模組
Built-in preset definitions and config file loaders

承載 txt2img/img2img 的內建預設 (built-in presets) 字典、
自訂預設 (custom presets) 的載入函式，以及 UI 顯示用集合的合併函式。

本模組不依賴 WebUI 腳本層：設定檔路徑與「是否保留內建預設」的
Settings 選項值皆由呼叫端傳入。
"""

from typing import Any

from sd_config_presets.config_components import EnumTypeName, RESERVED_PRESET_NAME, load_config_file, strip_reserved_preset


def load_txt2img_config_file(file_path: str) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    載入 txt2img 的內建預設預設檔與自訂預設（兩者脫鉤）。

    Args:
        file_path (str): 自訂預設 JSON 檔路徑（由呼叫端以擴充功能目錄組出）

    Returns:
        tuple: (內建預設預設檔, 自訂預設；"None" 為保留項，已自設定檔剔除)
    """
    # Define type name for txt2img configuration
    # 为txt2img配置定义类型名称
    type_name = EnumTypeName.txt2img

    # Note: "txt2img_enable_hr" was changed to "txt2img_hr-checkbox" in A1111 1.6.0 (8/31/2023), but we keep it
    # as "txt2img_enable_hr" in config file so that newer version of Config Presets will work with older
    # versions of A1111. This is handled at runtime with synonyms.
    # 注意："txt2img_enable_hr"在A1111 1.6.0 (8/31/2023)中更改为"txt2img_hr-checkbox"，但我们在配置文件中
    # 保持为"txt2img_enable_hr"，以便Config Presets的更新版本能与旧版A1111兼容。这在运行时通过同义词处理。

    # Default presets for txt2img configuration
    # txt2img配置的默认预设
    txt2img_config_presets = {
        "SD1.5 - 512x512": {
            "txt2img_width": 512,
            "txt2img_height": 512,
        },
        "SD2.1 - 768x768": {
            "txt2img_width": 768,
            "txt2img_height": 768,
        },
        "SDXL --- 1024x1024": {
            "txt2img_width": 1024,
            "txt2img_height": 1024,
        },
        "SDXL --- 1024x1024 with Refiner": {
            "txt2img_width": 1024,
            "txt2img_height": 1024,
            "txt2img_enable-checkbox": True,
        },
        "Flux.1 Dev - 256x256 to 1920x1080 (0.1 to 2.0 megapixels), 20 steps, CFG 1, Distilled CFG 3.5, Euler Simple": {
            "txt2img_width": 1024,
            "txt2img_height": 1024,
            "txt2img_sampling": "Euler",
            "txt2img_scheduler": "Simple",
            "txt2img_distilled_cfg_scale": 3.5,
            "txt2img_cfg_scale": 1,
            "txt2img_steps": 20,
        },
        "Flux.1 Schnell - 256x256 to 1920x1080 (0.1 to 2.0 megapixels), 4 steps, CFG 1, Distilled CFG 3.5, Euler Simple": {
            "txt2img_width": 1024,
            "txt2img_height": 1024,
            "txt2img_sampling": "Euler",
            "txt2img_scheduler": "Simple",
            "txt2img_distilled_cfg_scale": 3.5,
            "txt2img_cfg_scale": 1,
            "txt2img_steps": 4,
        },
        "High res ----------- [Hires fix - Upscale by: 2, Denoising: 0.3, Hires steps: 10]": {
            "txt2img_enable_hr": True,
            "txt2img_hr_scale": 2,
            "txt2img_hires_steps": 10,
            "txt2img_denoising_strength": 0.3,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 1,
        },
        "SD1.5 Low quality ------ steps: 10, batch size: 4, DPM++ 2M": {
            "txt2img_sampling": "DPM++ 2M",
            "txt2img_steps": 10,
            "txt2img_enable_hr": False,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 4,
        },
        "SD1.5 Medium quality - steps: 15, batch size: 4, DPM++ 2M": {
            "txt2img_sampling": "DPM++ 2M",
            "txt2img_steps": 15,
            "txt2img_enable_hr": False,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 4,
        },
        "SD1.5 High quality ------ steps: 30, batch size: 4, DPM++ 2S a": {
            "txt2img_sampling": "DPM++ 2S a",
            "txt2img_steps": 30,
            "txt2img_enable_hr": False,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 4,
        },
        "SD1.5 - 1080p --- 432x768 -> 1920x1080, [Hires fix - Upscale by: 2.5, Denoising: 0.4, Hires steps: 10]": {
            # 2x 960x536, 2.5x 768x432, 3x 640x360
            "txt2img_width": 768,
            "txt2img_height": 432,
            "txt2img_enable_hr": True,
            "txt2img_hr_scale": 2.5,
            "txt2img_hires_steps": 10,
            "txt2img_denoising_strength": 0.4,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 1,
        },
        "SD1.5 - 1440p --- 432x768 -> 2560x1440, [Hires fix - Upscale by: 3.3334, Denoising: 0.35, Hires steps: 10]": {
            # 2x 1024x720, 2.5x 1024x576, 3.3334x 768x432, 4x 640x360
            "txt2img_width": 768,
            "txt2img_height": 432,
            "txt2img_enable_hr": True,
            "txt2img_hr_scale": 3.3334,
            "txt2img_hires_steps": 10,
            "txt2img_denoising_strength": 0.35,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 1,
        },
        "SD1.5 - 4k -------- 432x768 -> 3840x2160, [Upscale by: 5, Denoising: 0.3, Hires steps: 15]": {
            # 2x 1420x1080, 2.5x 1536x864, 3x 1280x720, 5x 768x432, 6x 640x360
            "txt2img_width": 768,
            "txt2img_height": 432,
            "txt2img_enable_hr": True,
            "txt2img_hr_scale": 5,
            "txt2img_hires_steps": 15,
            "txt2img_denoising_strength": 0.3,
            "txt2img_batch_count": 1,
            "txt2img_batch_size": 1,
        },
    }

    # 自訂預設與內建預設脫鉤；無視設定檔中的保留項（不區分大小寫）
    custom_config_presets = load_config_file(file_path, type_name)
    custom_config_presets = strip_reserved_preset(custom_config_presets)
    return txt2img_config_presets, custom_config_presets


def load_img2img_config_file(file_path: str) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    載入 img2img 的內建預設預設檔與自訂預設（兩者脫鉤）。

    Args:
        file_path (str): 自訂預設 JSON 檔路徑（由呼叫端以擴充功能目錄組出）

    Returns:
        tuple: (內建預設預設檔, 自訂預設；"None" 為保留項，已自設定檔剔除)
    """
    # Define type name for img2img configuration
    # 为img2img配置定义类型名称
    type_name = EnumTypeName.img2img

    # Default presets for img2img configuration
    # img2img配置的默认预设
    img2img_config_presets = {
        "Low denoising ------- denoising: 0.25, steps: 20, DPM++ 2M": {
            "img2img_sampling": "DPM++ 2M",
            "img2img_steps": 20,
            #"img2img_width": 512,
            #"img2img_height": 512,
            #"img2img_batch_count": 1,
            #"img2img_batch_size": 1,
            #"img2img_cfg_scale": 7,
            "img2img_denoising_strength": 0.25,
        },
        "Medium denoising -- denoising: 0.40, steps: 20, DPM++ 2M": {
            "img2img_sampling": "DPM++ 2M",
            "img2img_steps": 20,
            #"img2img_width": 512,
            #"img2img_height": 512,
            #"img2img_batch_count": 1,
            #"img2img_batch_size": 1,
            #"img2img_cfg_scale": 7,
            "img2img_denoising_strength": 0.40,
        },
        "High denoising ------- denoising: 0.75, steps: 30, DPM++ 2M": {
            "img2img_sampling": "DPM++ 2M",
            "img2img_steps": 30,
            #"img2img_width": 512,
            #"img2img_height": 512,
            #"img2img_batch_count": 1,
            #"img2img_batch_size": 1,
            #"img2img_cfg_scale": 7,
            "img2img_denoising_strength": 0.75,
        },
    }

    # 自訂預設與內建預設脫鉤；無視設定檔中的保留項（不區分大小寫）
    custom_config_presets = load_config_file(file_path, type_name)
    custom_config_presets = strip_reserved_preset(custom_config_presets)
    return img2img_config_presets, custom_config_presets


def build_config_presets(default_presets: dict[str, dict[str, Any]], custom_config_presets: dict[str, dict[str, Any]], keep_builtin: bool) -> dict[str, dict[str, Any]]:
    """
    建立 UI 顯示用的預設集合：內建預設與自訂預設脫鉤，同名時以自訂覆蓋內建。

    Args:
        default_presets (dict): 內建預設集合 / built-in presets
        custom_config_presets (dict): 自訂預設集合 / custom presets
        keep_builtin (bool): 具有自訂預設時是否保留內建預設（由呼叫端讀取 Settings 選項）；
                             沒有任何自訂預設時一律顯示內建預設

    Returns:
        dict: 合併後的顯示用集合；保留項 "None" 永遠置頂且不可變更
    """
    merged_presets: dict[str, dict[str, Any]] = {RESERVED_PRESET_NAME: {}}
    if keep_builtin or len(custom_config_presets) == 0:
        merged_presets.update(default_presets)
    merged_presets.update(custom_config_presets)
    return merged_presets
