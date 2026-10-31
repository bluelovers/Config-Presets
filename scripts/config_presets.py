# Import necessary modules for Stable Diffusion Web UI extension
# 导入Stable Diffusion Web UI扩展所需的模块
import os
from typing import Any
import modules.scripts as scripts  # pyright: ignore[reportMissingImports]
import gradio as gr  # pyright: ignore[reportMissingImports]

from modules import shared, script_callbacks  # pyright: ignore[reportMissingImports]
from sd_config_presets.config_components import load_custom_tracked_component_items, flatten_tracked_component_items, EnumTypeName, TrackedComponentItem, log, log_error
from sd_config_presets.config_file.preset_loaders import load_txt2img_config_file, load_img2img_config_file, build_config_presets
from sd_config_presets.component_tracker import ComponentTracker
from sd_config_presets.preset_ui import ConfigPresetUI

# Base directory path for the Config-Presets extension
# Contains the full path to the extension folder
# Config-Presets扩展的基础目录路径
# 包含扩展文件夹的完整路径
BASEDIR: str = scripts.basedir()     #C:\path\to\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path

# 設定檔資料夾：預設為擴充功能目錄；可用 --configpresets-dir 指向其他資料夾（在 preload.py 註冊），
# 讓多個 WebUI 安裝共享同一份自訂設定檔；路徑不存在時回退預設並記錄錯誤
config_folder = BASEDIR
if getattr(shared.cmd_opts, "configpresets_dir", None):
    if os.path.exists(shared.cmd_opts.configpresets_dir):
        config_folder = str(shared.cmd_opts.configpresets_dir)   # COMMANDLINE_ARGS: --configpresets-dir "C:/path/to/folder", setup in preload.py
        log(f"Will load config files at: {config_folder}")
    else:
        log_error(f"The directory set with --configpresets-dir in COMMANDLINE_ARGS {shared.cmd_opts.configpresets_dir} does not exist, using default directory at {config_folder}")

# Configuration file names for different components and modes
# 不同组件和模式的配置文件名
CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = f"{config_folder}/config-txt2img-custom-tracked-components.txt"
CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = f"{config_folder}/config-img2img-custom-tracked-components.txt"
CONFIG_TXT2IMG_FILE_NAME = f"{config_folder}/config-txt2img.json"
CONFIG_IMG2IMG_FILE_NAME = f"{config_folder}/config-img2img.json"

# WebUI Settings 的 Config Presets 區段與選項鍵
CONFIG_PRESETS_SETTINGS_SECTION = ("config_presets", "Config Presets")
CONFIG_PRESETS_KEEP_BUILTIN_OPTION_KEY = "config_presets_keep_builtin_presets"


def keep_builtin_config_presets_enabled() -> bool:
    """
    讀取 WebUI Settings 選項：具有自訂預設時是否保留內建預設。
    """
    return getattr(shared.opts, CONFIG_PRESETS_KEEP_BUILTIN_OPTION_KEY, False)


def on_ui_settings():
    """
    向 WebUI Settings 註冊 Config Presets 選項。
    """
    shared.opts.add_option(
        CONFIG_PRESETS_KEEP_BUILTIN_OPTION_KEY,
        shared.OptionInfo(
            False,
            "Keep built-in default presets when custom presets exist",
            gr.Checkbox,
            {"interactive": True},
            section=CONFIG_PRESETS_SETTINGS_SECTION,
        ),
    )


script_callbacks.on_ui_settings(on_ui_settings)


def load_txt2img_custom_tracked_component_items() -> list[TrackedComponentItem]:
    """
    Load custom tracked components (with ##@ group structure) for txt2img mode.
    This function loads component IDs that users want to track in addition to default ones,
    preserving their collapsible group layout.
    Returns a list of component IDs and groups that should be tracked for presets.

    加载txt2img模式的自定义跟踪组件（含 ##@ 分组结构）。
    此函数加载用户想要跟踪的组件ID，除了默认的组件之外，并保留其分组层级。
    返回应该为预设跟踪的组件ID与分组列表。
    """
    type_name = EnumTypeName.txt2img.value

    # config file not found
    # First time running the extension or it was deleted, so fill it with default values
    # 配置文件未找到
    # 第一次运行扩展或文件被删除，所以用默认值填充
    txt2img_custom_tracked_components_default_text = f"""# Put custom {type_name} tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
# Wrap related IDs with "##@ <label>" ... "##@" to show them inside a collapsible group in the Fields to save section.
# Component IDs can be found in the HTML (id="..."), in modules/ui.py (elem_id="..."), or in an extensions python code. IDs like "component-5890" won't work because the number at the end will change each startup.
# Entering an invalid component ID here will cause this extension to error and not load. Components that do not have a value associated with them, such as tabs and accordions, are not supported.
# Note that components on the top row of the UI cannot be added here, such as "setting_sd_model_checkpoint", "setting_sd_vae", and "setting_CLIP_stop_at_last_layers".

# Other fields:
#{type_name}_prompt
#{type_name}_neg_prompt
#{type_name}_styles
#{type_name}_seed
#{type_name}_subseed_show
#{type_name}_subseed
#{type_name}_subseed_strength
#{type_name}_seed_resize_from_w
#{type_name}_seed_resize_from_h
#{type_name}_tiling
#{type_name}_hr_resize_x
#{type_name}_hr_resize_y
#hr_sampler
#hires_prompt
#hires_neg_prompt

# Script dropdown:
#script_list

##@ X/Y/Z plot (script):
script_{type_name}_xyz_plot_x_type
script_{type_name}_xyz_plot_y_type
script_{type_name}_xyz_plot_z_type
script_{type_name}_xyz_plot_x_values
script_{type_name}_xyz_plot_y_values
script_{type_name}_xyz_plot_z_values

##@

# Latent Couple (extension):
#cd_{type_name}_divisions
#cd_{type_name}_positions
#cd_{type_name}_weights
#cd_{type_name}_end_at_this_step

# Forge - ControlNet Integrated:
#{type_name}_controlnet_ControlNet-0_controlnet_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_control_step_slider

# ControlNet (extension):
#{type_name}_controlnet_ControlNet-0_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-0_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-0_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-0_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-0_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-0_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-0_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-0_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-0_controlnet_automatically_send_generated_images_checkbox

#{type_name}_controlnet_ControlNet-1_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-1_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-1_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-1_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-1_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-1_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-1_controlnet_automatically_send_generated_images_checkbox

#{type_name}_controlnet_ControlNet-2_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-2_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-2_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-2_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-2_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-2_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-2_controlnet_automatically_send_generated_images_checkbox

# Tiled Diffusion (extension)
#MD-t2i-enabled-checkbox
#MD-t2i-overwrite-image-size
#MD-overwrite-width-t2i
#MD-overwrite-height-t2i
#MD-t2i-method
#MD-t2i-control-tensor-cpu
#MD-t2i-latent-tile-width
#MD-t2i-latent-tile-height
#MD-t2i-latent-tile-overlap
#MD-t2i-latent-tile-batch-size
# Tiled Diffusion - Region Prompt Control
#MD-t2i-enable-bbox-control
#MD-t2i-draw-background
#MD-t2i-cfg-name
# Tiled Diffusion - Region Prompt Control - Region 1
#MD-bbox-t2i-0-enable
#MD-t2i-0-blend-mode
#MD-t2i-0-feather
#MD-t2i-0-x
#MD-t2i-0-y
#MD-t2i-0-w
#MD-t2i-0-h
#MD-t2i-0-prompt
#MD-t2i-0-neg-prompt
#MD-t2i-0-seed
# Tiled Diffusion - Region Prompt Control - Region 2
#MD-bbox-t2i-1-enable
#MD-t2i-1-blend-mode
#MD-t2i-1-feather
#MD-t2i-1-x
#MD-t2i-1-y
#MD-t2i-1-w
#MD-t2i-1-h
#MD-t2i-1-prompt
#MD-t2i-1-neg-prompt
#MD-t2i-1-seed
# Tiled Diffusion - Region Prompt Control - Region 3
#MD-bbox-t2i-2-enable
#MD-t2i-2-blend-mode
#MD-t2i-2-feather
#MD-t2i-2-x
#MD-t2i-2-y
#MD-t2i-2-w
#MD-t2i-2-h
#MD-t2i-2-prompt
#MD-t2i-2-neg-prompt
#MD-t2i-2-seed
# Tiled Diffusion - Tiled VAE
#MDV-t2i-enabled-checkbox
#MD-t2i-vae2gpu
#MD-t2i-enc-size
#MD-t2i-dec-size
#MD-t2i-fastenc
#MD-t2i-fastenc-colorfix
#MD-t2i-fastdec

# ADetailer (extension)
#script_{type_name}_adetailer_ad_main_accordion-checkbox
# ADetailer - 1st tab
#script_{type_name}_adetailer_ad_model
#script_{type_name}_adetailer_ad_prompt
#script_{type_name}_adetailer_ad_negative_prompt
# ADetailer - 1st tab - Detection
#script_{type_name}_adetailer_ad_confidence
#script_{type_name}_adetailer_ad_mask_min_ratio
#script_{type_name}_adetailer_ad_mask_max_ratio
# ADetailer - 1st tab - Mask Preprocessing
#script_{type_name}_adetailer_ad_x_offset
#script_{type_name}_adetailer_ad_y_offset
#script_{type_name}_adetailer_ad_dilate_erode
#script_{type_name}_adetailer_ad_mask_merge_invert
# ADetailer - 1st tab - Inpainting
#script_{type_name}_adetailer_ad_mask_blur
#script_{type_name}_adetailer_ad_denoising_strength
#script_{type_name}_adetailer_ad_inpaint_only_masked
#script_{type_name}_adetailer_ad_inpaint_only_masked_padding
#script_{type_name}_adetailer_ad_use_inpaint_width_height
#script_{type_name}_adetailer_ad_inpaint_width
#script_{type_name}_adetailer_ad_inpaint_height
#script_{type_name}_adetailer_ad_use_steps
#script_{type_name}_adetailer_ad_steps
#script_{type_name}_adetailer_ad_use_cfg_scale
#script_{type_name}_adetailer_ad_cfg_scale
#script_{type_name}_adetailer_ad_use_checkpoint
#script_{type_name}_adetailer_ad_use_vae
#script_{type_name}_adetailer_ad_use_sampler
#script_{type_name}_adetailer_ad_sampler
#script_{type_name}_adetailer_ad_scheduler
#script_{type_name}_adetailer_ad_use_noise_multiplier
#script_{type_name}_adetailer_ad_noise_multiplier
#script_{type_name}_adetailer_ad_use_clip_skip
#script_{type_name}_adetailer_ad_clip_skip
#script_{type_name}_adetailer_ad_restore_face
# ADetailer - 1st tab - ControlNet
#script_{type_name}_adetailer_ad_controlnet_model
#script_{type_name}_adetailer_ad_controlnet_weight
#script_{type_name}_adetailer_ad_controlnet_guidance_start
#script_{type_name}_adetailer_ad_controlnet_guidance_end
# ADetailer - 2nd tab
#script_{type_name}_adetailer_ad_model_2nd
#script_{type_name}_adetailer_ad_prompt_2nd
#script_{type_name}_adetailer_ad_negative_prompt_2nd
# ADetailer - 2nd tab - Detection
#script_{type_name}_adetailer_ad_confidence_2nd
#script_{type_name}_adetailer_ad_mask_min_ratio_2nd
#script_{type_name}_adetailer_ad_mask_max_ratio_2nd
# ADetailer - 2nd tab - Mask Preprocessing
#script_{type_name}_adetailer_ad_x_offset_2nd
#script_{type_name}_adetailer_ad_y_offset_2nd
#script_{type_name}_adetailer_ad_dilate_erode_2nd
#script_{type_name}_adetailer_ad_mask_merge_invert_2nd
# ADetailer - 2nd tab - Inpainting
#script_{type_name}_adetailer_ad_mask_blur_2nd
#script_{type_name}_adetailer_ad_denoising_strength_2nd
#script_{type_name}_adetailer_ad_inpaint_only_masked_2nd
#script_{type_name}_adetailer_ad_inpaint_only_masked_padding_2nd
#script_{type_name}_adetailer_ad_use_inpaint_width_height_2nd
#script_{type_name}_adetailer_ad_inpaint_width_2nd
#script_{type_name}_adetailer_ad_inpaint_height_2nd
#script_{type_name}_adetailer_ad_use_steps_2nd
#script_{type_name}_adetailer_ad_steps_2nd
#script_{type_name}_adetailer_ad_use_cfg_scale_2nd
#script_{type_name}_adetailer_ad_cfg_scale_2nd
#script_{type_name}_adetailer_ad_use_checkpoint_2nd
#script_{type_name}_adetailer_ad_use_vae_2nd
#script_{type_name}_adetailer_ad_use_sampler_2nd
#script_{type_name}_adetailer_ad_sampler_2nd
#script_{type_name}_adetailer_ad_scheduler_2nd
#script_{type_name}_adetailer_ad_use_noise_multiplier_2nd
#script_{type_name}_adetailer_ad_noise_multiplier_2nd
#script_{type_name}_adetailer_ad_use_clip_skip_2nd
#script_{type_name}_adetailer_ad_clip_skip_2nd
#script_{type_name}_adetailer_ad_restore_face_2nd
# ADetailer - 2nd tab - ControlNet
#script_{type_name}_adetailer_ad_controlnet_model_2nd
#script_{type_name}_adetailer_ad_controlnet_weight_2nd
#script_{type_name}_adetailer_ad_controlnet_guidance_start_2nd
#script_{type_name}_adetailer_ad_controlnet_guidance_end_2nd
"""

    return load_custom_tracked_component_items(CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME, EnumTypeName.txt2img, txt2img_custom_tracked_components_default_text)


def load_img2img_custom_tracked_component_items() -> list[TrackedComponentItem]:
    """
    Load custom tracked components (with ##@ group structure) for img2img mode.
    This function loads component IDs that users want to track in addition to default ones,
    preserving their collapsible group layout.
    Returns a list of component IDs and groups that should be tracked for presets.

    加载img2img模式的自定义跟踪组件（含 ##@ 分组结构）。
    此函数加载用户想要跟踪的组件ID，除了默认的组件之外，并保留其分组层级。
    返回应该为预设跟踪的组件ID与分组列表。
    """
    type_name = EnumTypeName.img2img.value

    # config file not found
    # First time running the extension or it was deleted, so fill it with default values
    # 配置文件未找到
    # 第一次运行扩展或文件被删除，所以用默认值填充
    img2img_custom_tracked_components_default_text = f"""# Put custom {type_name} tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
# Wrap related IDs with "##@ <label>" ... "##@" to show them inside a collapsible group in the Fields to save section.
# Component IDs can be found in the HTML (id="..."), in modules/ui.py (elem_id="..."), or in an extensions python code. IDs like "component-5890" won't work because the number at the end will change each startup.
# Entering an invalid component ID here will cause this extension to error and not load. Components that do not have a value associated with them, such as tabs and accordions, are not supported.
# Note that components on the top row of the UI cannot be added here, such as "setting_sd_model_checkpoint", "setting_sd_vae", and "setting_CLIP_stop_at_last_layers".

# Other fields:
#{type_name}_prompt
#{type_name}_neg_prompt
#{type_name}_mask_mode
#{type_name}_mask_blur
#{type_name}_mask_alpha
#{type_name}_inpainting_fill
#{type_name}_inpaint_full_res
#{type_name}_inpaint_full_res_padding
#resize_mode
#{type_name}_scale
#{type_name}_seed
#{type_name}_subseed_show
#{type_name}_subseed
#{type_name}_subseed_strength
#{type_name}_seed_resize_from_w
#{type_name}_seed_resize_from_h
#{type_name}_tiling
#{type_name}_batch_input_dir
#{type_name}_batch_output_dir
#{type_name}_batch_inpaint_mask_dir

# Soft Inpainting:
#soft_inpainting_enabled-checkbox
#mask_blend_power
#mask_blend_scale
#inpaint_detail_preservation
#composite_mask_influence
#composite_difference_threshold
#composite_difference_contrast

# Script dropdown:
#script_list

##@ X/Y/Z plot (script):
script_{type_name}_xyz_plot_x_type
script_{type_name}_xyz_plot_y_type
script_{type_name}_xyz_plot_z_type
script_{type_name}_xyz_plot_x_values
script_{type_name}_xyz_plot_y_values
script_{type_name}_xyz_plot_z_values

##@

# Loopback (script):
#script_loopback_loops
#script_loopback_final_denoising_strength

# SD upscale (script):
#script_sd_upscale_overlap
#script_sd_upscale_scale_factor
#script_sd_upscale_upscaler_index

# Latent Couple (extension):
#cd_{type_name}_divisions
#cd_{type_name}_positions
#cd_{type_name}_weights
#cd_{type_name}_end_at_this_step

# Forge - ControlNet Integrated:
#{type_name}_controlnet_ControlNet-0_controlnet_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_control_step_slider

# ControlNet (extension):
#{type_name}_controlnet_ControlNet-0_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-0_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-0_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-0_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-0_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-0_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-0_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-0_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-0_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-0_controlnet_automatically_send_generated_images_checkbox

#{type_name}_controlnet_ControlNet-1_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-1_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-1_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-1_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-1_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-1_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-1_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-1_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-1_controlnet_automatically_send_generated_images_checkbox

#{type_name}_controlnet_ControlNet-2_controlnet_enable_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_low_vram_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_pixel_perfect_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_preprocessor_preview_checkbox
#{type_name}_controlnet_ControlNet-2_controlnet_type_filter_radio
#{type_name}_controlnet_ControlNet-2_controlnet_preprocessor_dropdown
#{type_name}_controlnet_ControlNet-2_controlnet_model_dropdown
#{type_name}_controlnet_ControlNet-2_controlnet_control_weight_slider
#{type_name}_controlnet_ControlNet-2_controlnet_start_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_ending_control_step_slider
#{type_name}_controlnet_ControlNet-2_controlnet_control_mode_radio
#{type_name}_controlnet_ControlNet-2_controlnet_resize_mode_radio
#{type_name}_controlnet_ControlNet-2_controlnet_automatically_send_generated_images_checkbox

# Tiled Diffusion (extension)
#MD-i2i-enabled-checkbox
#MD-i2i-keep-input-size
#MD-i2i-method
#MD-i2i-control-tensor-cpu
#MD-i2i-latent-tile-width
#MD-i2i-latent-tile-height
#MD-i2i-latent-tile-overlap
#MD-i2i-latent-tile-batch-size
#MD-i2i-upscaler-index
#MD-i2i-upscaler-factor
# Tiled Diffusion - Noise Inversion
#MD-i2i-noise-inverse
#MD-i2i-noise-inverse-steps
#MD-i2i-noise-inverse-retouch
#MD-i2i-noise-inverse-renoise-strength
#MD-i2i-noise-inverse-renoise-kernel
# Tiled Diffusion - Region Prompt Control
#MD-i2i-enable-bbox-control
#MD-i2i-draw-background
#MD-i2i-cfg-name
# Tiled Diffusion - Region Prompt Control - Region 1
#MD-bbox-i2i-0-enable
#MD-i2i-0-blend-mode
#MD-i2i-0-feather
#MD-i2i-0-x
#MD-i2i-0-y
#MD-i2i-0-w
#MD-i2i-0-h
#MD-i2i-0-prompt
#MD-i2i-0-neg-prompt
#MD-i2i-0-seed
# Tiled Diffusion - Region Prompt Control - Region 2
#MD-bbox-i2i-1-enable
#MD-i2i-1-blend-mode
#MD-i2i-1-feather
#MD-i2i-1-x
#MD-i2i-1-y
#MD-i2i-1-w
#MD-i2i-1-h
#MD-i2i-1-prompt
#MD-i2i-1-neg-prompt
#MD-i2i-1-seed
# Tiled Diffusion - Region Prompt Control - Region 3
#MD-bbox-i2i-2-enable
#MD-i2i-2-blend-mode
#MD-i2i-2-feather
#MD-i2i-2-x
#MD-i2i-2-y
#MD-i2i-2-w
#MD-i2i-2-h
#MD-i2i-2-prompt
#MD-i2i-2-neg-prompt
#MD-i2i-2-seed
# Tiled Diffusion - Tiled VAE
#MDV-i2i-enabled-checkbox
#MD-i2i-vae2gpu
#MD-i2i-enc-size
#MD-i2i-dec-size
#MD-i2i-fastenc
#MD-i2i-fastenc-colorfix
#MD-i2i-fastdec

# StableSR (extension)
#SR Model does not have an ID as of June 1 2023
#StableSR-scale
#StableSR-color-fix
#StableSR-save-original
#StableSR-pure-noise

# ADetailer (extension)
#script_{type_name}_adetailer_ad_main_accordion-checkbox
# ADetailer - 1st tab
#script_{type_name}_adetailer_ad_model
#script_{type_name}_adetailer_ad_prompt
#script_{type_name}_adetailer_ad_negative_prompt
# ADetailer - 1st tab - Detection
#script_{type_name}_adetailer_ad_confidence
#script_{type_name}_adetailer_ad_mask_min_ratio
#script_{type_name}_adetailer_ad_mask_max_ratio
# ADetailer - 1st tab - Mask Preprocessing
#script_{type_name}_adetailer_ad_x_offset
#script_{type_name}_adetailer_ad_y_offset
#script_{type_name}_adetailer_ad_dilate_erode
#script_{type_name}_adetailer_ad_mask_merge_invert
# ADetailer - 1st tab - Inpainting
#script_{type_name}_adetailer_ad_mask_blur
#script_{type_name}_adetailer_ad_denoising_strength
#script_{type_name}_adetailer_ad_inpaint_full_res
#script_{type_name}_adetailer_ad_inpaint_full_res_padding
#script_{type_name}_adetailer_ad_use_inpaint_width_height
#script_{type_name}_adetailer_ad_inpaint_width
#script_{type_name}_adetailer_ad_inpaint_height
#script_{type_name}_adetailer_ad_use_steps
#script_{type_name}_adetailer_ad_steps
#script_{type_name}_adetailer_ad_use_cfg_scale
#script_{type_name}_adetailer_ad_cfg_scale
#script_{type_name}_adetailer_ad_use_checkpoint
#script_{type_name}_adetailer_ad_use_vae
#script_{type_name}_adetailer_ad_use_sampler
#script_{type_name}_adetailer_ad_sampler
#script_{type_name}_adetailer_ad_scheduler
#script_{type_name}_adetailer_ad_use_noise_multiplier
#script_{type_name}_adetailer_ad_noise_multiplier
#script_{type_name}_adetailer_ad_use_clip_skip
#script_{type_name}_adetailer_ad_clip_skip
#script_{type_name}_adetailer_ad_restore_face
# ADetailer - 1st tab - ControlNet
#script_{type_name}_adetailer_ad_controlnet_model
#script_{type_name}_adetailer_ad_controlnet_weight
#script_{type_name}_adetailer_ad_controlnet_guidance_start
#script_{type_name}_adetailer_ad_controlnet_guidance_end
# ADetailer - 2nd tab
#script_{type_name}_adetailer_ad_model_2nd
#script_{type_name}_adetailer_ad_prompt_2nd
#script_{type_name}_adetailer_ad_negative_prompt_2nd
# ADetailer - 2nd tab - Detection
#script_{type_name}_adetailer_ad_confidence_2nd
#script_{type_name}_adetailer_ad_mask_min_ratio_2nd
#script_{type_name}_adetailer_ad_mask_max_ratio_2nd
# ADetailer - 2nd tab - Mask Preprocessing
#script_{type_name}_adetailer_ad_x_offset_2nd
#script_{type_name}_adetailer_ad_y_offset_2nd
#script_{type_name}_adetailer_ad_dilate_erode_2nd
#script_{type_name}_adetailer_ad_mask_merge_invert_2nd
# ADetailer - 2nd tab - Inpainting
#script_{type_name}_adetailer_ad_mask_blur_2nd
#script_{type_name}_adetailer_ad_denoising_strength_2nd
#script_{type_name}_adetailer_ad_inpaint_full_res_2nd
#script_{type_name}_adetailer_ad_inpaint_full_res_padding_2nd
#script_{type_name}_adetailer_ad_use_inpaint_width_height_2nd
#script_{type_name}_adetailer_ad_inpaint_width_2nd
#script_{type_name}_adetailer_ad_inpaint_height_2nd
#script_{type_name}_adetailer_ad_use_steps_2nd
#script_{type_name}_adetailer_ad_steps_2nd
#script_{type_name}_adetailer_ad_use_cfg_scale_2nd
#script_{type_name}_adetailer_ad_cfg_scale_2nd
#script_{type_name}_adetailer_ad_use_checkpoint_2nd
#script_{type_name}_adetailer_ad_use_vae_2nd
#script_{type_name}_adetailer_ad_use_sampler_2nd
#script_{type_name}_adetailer_ad_sampler_2nd
#script_{type_name}_adetailer_ad_scheduler_2nd
#script_{type_name}_adetailer_ad_use_noise_multiplier_2nd
#script_{type_name}_adetailer_ad_noise_multiplier_2nd
#script_{type_name}_adetailer_ad_use_clip_skip_2nd
#script_{type_name}_adetailer_ad_clip_skip_2nd
#script_{type_name}_adetailer_ad_restore_face_2nd
# ADetailer - 2nd tab - ADetailer ControlNet
#script_{type_name}_adetailer_ad_controlnet_model_2nd
#script_{type_name}_adetailer_ad_controlnet_weight_2nd
#script_{type_name}_adetailer_ad_controlnet_guidance_start_2nd
#script_{type_name}_adetailer_ad_controlnet_guidance_end_2nd

# Ultimate SD Upscale
#ultimateupscale_target_size_type
#ultimateupscale_custom_width
#ultimateupscale_custom_height
#ultimateupscale_custom_scale
#ultimateupscale_upscaler_index
#ultimateupscale_redraw_mode
#ultimateupscale_tile_width
#ultimateupscale_tile_height
#ultimateupscale_mask_blur
#ultimateupscale_padding
#ultimateupscale_seams_fix_type
#ultimateupscale_seams_fix_denoise
#ultimateupscale_seams_fix_width
#ultimateupscale_seams_fix_mask_blur
#ultimateupscale_seams_fix_padding
#ultimateupscale_save_upscaled_image
#ultimateupscale_save_seams_fix_image
"""

    return load_custom_tracked_component_items(CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME, EnumTypeName.img2img, img2img_custom_tracked_components_default_text)


class Script(scripts.Script):
    """
    Main Script class for the Config-Presets extension.
    This class handles the UI components and logic for saving/loading configuration presets.

    Config-Presets扩展的主Script类。
    此类处理用于保存/加载配置预设的UI组件和逻辑。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load custom tracked components (含 ##@ 分組結構，分組由顯示層渲染為摺疊區塊)
        # 加载自定义跟踪组件（含 ##@ 分组结构）
        txt2img_custom_tracked_items = load_txt2img_custom_tracked_component_items()
        img2img_custom_tracked_items = load_img2img_custom_tracked_component_items()


        # These are the settings from the UI that are saved for each preset
        # 这些是每个预设保存的UI设置
        # These are the settings from the UI that are saved for each preset
        self.txt2img_component_ids: list[str] = [
            "txt2img_sampling",
            "txt2img_scheduler",        # added in A1111 1.9.0 (Schedule type)
            "txt2img_steps",
            "txt2img_width",
            "txt2img_height",
            "txt2img_batch_count",
            "txt2img_batch_size",
            "txt2img_restore_faces",
            "txt2img_enable_hr",        # removed in A1111 1.6.0
            "txt2img_hr-checkbox",      # added in A1111 1.6.0
            "txt2img_hr_scale",
            "txt2img_hr_upscaler",
            "txt2img_hires_steps",
            "txt2img_denoising_strength",
            "txt2img_cfg_scale",
            "txt2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner)
            "txt2img_switch_at",        # added in A1111 1.6.0 (Refiner switch at)

            # IDs below are only available in specific WebUIs (they must also be added to self.txt2img_optional_ids):

            # vladmandic/automatic (SD.Next) https://github.com/vladmandic/automatic
            "txt2img_sampling_alt",     # Equiv to txt2img_hr_upscaler
            "txt2img_steps_alt",        # Equiv to txt2img_hires_steps
            "txt2img_show_batch",
            "txt2img_show_seed",
            "txt2img_show_advanced",
            "txt2img_show_second_pass", # Replaces txt2img_enable_hr in Vlad's

            # lllyasviel/stable-diffusion-webui-forge (Forge) https://github.com/lllyasviel/stable-diffusion-webui-forge
            "txt2img_distilled_cfg_scale",  # Flux model's CFG
        ]
        self.txt2img_component_ids += flatten_tracked_component_items(txt2img_custom_tracked_items) # add the custom tracked components

        self.img2img_component_ids: list[str] = [
            "img2img_sampling",
            "img2img_scheduler",        # added in A1111 1.9.0 (Schedule type)
            "img2img_steps",
            "img2img_width",
            "img2img_height",
            "img2img_batch_count",
            "img2img_batch_size",
            "img2img_cfg_scale",
            "img2img_denoising_strength",
            "img2img_restore_faces",
            "img2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner)
            "img2img_switch_at",        # added in A1111 1.6.0 (Refiner switch at)

            # IDs below are only available in specific WebUIs (they must also be added to self.img2img_optional_ids):

            # vladmandic/automatic (SD.Next) https://github.com/vladmandic/automatic
            "img2img_show_seed",
            "img2img_show_resize",
            "img2img_show_batch",
            "img2img_show_denoise",
            "img2img_show_advanced",

            # lllyasviel/stable-diffusion-webui-forge (Forge) https://github.com/lllyasviel/stable-diffusion-webui-forge
            "img2img_distilled_cfg_scale",  # Flux model's CFG
        ]
        self.img2img_component_ids += flatten_tracked_component_items(img2img_custom_tracked_items) # add the custom tracked components

        # Optional IDs don't crash the extension if no associated component is found.
        # These could be legacy IDs from older versions of the Web UI/extensions, or IDs from another UI (Vlad's SD.Next).
        # IDs put here also need to be put in the above txt2img_component_ids and img2img_component_ids arrays.
        # 可选ID在找不到关联组件时不会导致扩展崩溃。
        # 这些可能是Web UI/扩展旧版本的遗留ID，或来自其他UI（Vlad的SD.Next）的ID。
        # 放在这里的ID也需要放入上面的txt2img_component_ids和img2img_component_ids数组中。
        self.txt2img_optional_ids: list[str] = [
            "txt2img_restore_faces",    # removed in A1111 1.6.0
            "txt2img_enable_hr",        # removed in A1111 1.6.0, and replaced in Vlad's SD.Next
            "txt2img_hr-checkbox",      # added in A1111 1.6.0
            "txt2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner accordion)
            "txt2img_switch_at",        # added in A1111 1.6.0 (Refiner Switch at)
            "txt2img_scheduler",        # added in A1111 1.9.0 (Schedule type)

            "txt2img_hires_steps",      # Replaced in Vlad's SD.Next

            # vladmandic/automatic (SD.Next) https://github.com/vladmandic/automatic
            "txt2img_sampling_alt",
            "txt2img_steps_alt",
            "txt2img_show_batch",
            "txt2img_show_seed",
            "txt2img_show_advanced",
            "txt2img_show_second_pass",

            # lllyasviel/stable-diffusion-webui-forge (Forge) https://github.com/lllyasviel/stable-diffusion-webui-forge
            "txt2img_distilled_cfg_scale",  # Flux model's CFG

            # IDs below are only for extensions:
            "controlnet_control_mod_radio",
            "controlnet_control_mode_radio",
        ]
        self.img2img_optional_ids: list[str] = [
            "img2img_restore_faces",    # removed in A1111 1.6.0
            "img2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner accordion)
            "img2img_switch_at",        # added in A1111 1.6.0 (Refiner Switch at)
            "img2img_scheduler",        # added in A1111 1.9.0 (Schedule type)

            # vladmandic/automatic (SD.Next) https://github.com/vladmandic/automatic
            "img2img_show_seed",
            "img2img_show_resize",
            "img2img_show_batch",
            "img2img_show_denoise",
            "img2img_show_advanced",

            # lllyasviel/stable-diffusion-webui-forge (Forge) https://github.com/lllyasviel/stable-diffusion-webui-forge
            "img2img_distilled_cfg_scale",  # Flux model's CFG

            # IDs below are only for extensions:
            "controlnet_control_mod_radio",
            "controlnet_control_mode_radio",
        ]

        # Synonymous IDs are interchangeable at load time.
        # 同义词ID在加载时可以互换。
        self.synonym_ids: list[tuple[str, str]] = [
            ("txt2img_hires_steps", "txt2img_steps_alt"),                       # Vlad's SD.Next Hires fix steps
            ("txt2img_enable_hr", "txt2img_show_second_pass"),                  # Vlad's SD.Next Hires fix enable
            ("controlnet_control_mod_radio", "controlnet_control_mode_radio"),  # ControlNet component renamed on 5/26/2023 due to typo.
            ("txt2img_enable_hr", "txt2img_hr-checkbox"),                       # Automatic1111 1.6.0 changed ID for Hires fix checkbox

            # ADetailer changed IDs 6/04/2023
                # https://github.com/Bing-su/adetailer/commit/3702d196b35fc9f0bcb7fcfbc0aa8f8fea5fbcdf
            ("script_txt2img_adetailer_ad_inpaint_full_res", "script_txt2img_adetailer_ad_inpaint_only_masked"),
            ("script_txt2img_adetailer_ad_inpaint_full_res_padding", "script_txt2img_adetailer_ad_inpaint_only_masked_padding"),
            ("script_txt2img_adetailer_ad_inpaint_full_res_2nd", "script_txt2img_adetailer_ad_inpaint_only_masked_2nd"),
            ("script_txt2img_adetailer_ad_inpaint_full_res_padding_2nd", "script_txt2img_adetailer_ad_inpaint_only_masked_padding_2nd"),

            # multidiffusion-upscaler-for-automatic1111 (Tiled Diffusion, Tiled VAE) changed IDs 5/25/2023
                # https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/commit/f54e190b13dcf0f975f174b7b9f20efb5eba4952
                # https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/commit/acc3666ee833b4b6dde05a38c22185d273aa067f
                # https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/commit/2473d6b005a516fb4bd51b331abd04b0289fdf07
            ("tiledvae-t2i-enable", "MD-t2i-enable"),
            ("tiledvae-t2i-vae2gpu", "MD-t2i-vae2gpu"),
            ("tiledvae-t2i-enc-size", "MD-t2i-enc-size"),
            ("tiledvae-t2i-dec-size", "MD-t2i-dec-size"),
            ("tiledvae-t2i-fastenc", "MD-t2i-fastenc"),
            ("tiledvae-t2i-fastenc-colorfix", "MD-t2i-fastenc-colorfix"),
            ("tiledvae-t2i-fastdec", "MD-t2i-fastdec"),
            ("tiledvae-i2i-enable", "MD-i2i-enable"),
            ("tiledvae-i2i-vae2gpu", "MD-i2i-vae2gpu"),
            ("tiledvae-i2i-enc-size", "MD-i2i-enc-size"),
            ("tiledvae-i2i-dec-size", "MD-i2i-dec-size"),
            ("tiledvae-i2i-fastenc", "MD-i2i-fastenc"),
            ("tiledvae-i2i-fastenc-colorfix", "MD-i2i-fastenc-colorfix"),
            ("tiledvae-i2i-fastdec", "MD-i2i-fastdec"),

            # multidiffusion-upscaler-for-automatic1111 changed IDs 3/28/2024
                # https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/commit/0d88a384c7e60ed81e5dba7ecf4ce927d062ee63
                # Note: MD-i2i-enabled (see the d) is for "Tiled Difusion" tab, MDV-i2i-enabled is for "Tiled VAE" tab (previously MD-i2i-enable)
                # 3/30/2024 commit made these obsolete
            #("MD-t2i-enable", "MDV-t2i-enabled"),
            #("MD-i2i-enable", "MDV-i2i-enabled"),

            # multidiffusion-upscaler-for-automatic1111 changed IDs 3/30/2024
                # https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/commit/8f924dc6efce47ede615f01cca011b1ab0c54c96
            ("MD-t2i-enabled", "MD-t2i-enabled-checkbox"),
            ("MD-i2i-enabled", "MD-i2i-enabled-checkbox"),
            ("MDV-t2i-enabled", "MDV-t2i-enabled-checkbox"),
            ("MDV-i2i-enabled", "MDV-i2i-enabled-checkbox"),

            # ADetailer changed IDs 6/01/2024
                # Moved the enable checkbox to the accordion, and added individual enable checkboxes for each tab
                # https://github.com/Bing-su/adetailer/commit/a479f60f405481a37c98c1b08534610de9e9e05b
            ("script_txt2img_adetailer_ad_enable", "script_txt2img_adetailer_ad_main_accordion-checkbox"),
            ("script_img2img_adetailer_ad_enable", "script_img2img_adetailer_ad_main_accordion-checkbox"),
        ]

        # 元件偵測層：component_map 與 X/Y/Z plot 下拉框錨點狀態由 ComponentTracker 管理，
        # 於 after_component() 依序登記 WebUI 建立的元件
        # (gets filled up in the after_component() method)
        self.txt2img_component_tracker = ComponentTracker(
            type_name=EnumTypeName.txt2img,
            component_ids=self.txt2img_component_ids,
            optional_ids=self.txt2img_optional_ids,
            synonym_ids=self.synonym_ids,
            custom_tracked_components_config_file_name=CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME,
        )
        self.img2img_component_tracker = ComponentTracker(
            type_name=EnumTypeName.img2img,
            component_ids=self.img2img_component_ids,
            optional_ids=self.img2img_optional_ids,
            synonym_ids=self.synonym_ids,
            custom_tracked_components_config_file_name=CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME,
        )

        # ##@ 分組樹狀結構：供顯示層將自訂追蹤元件渲染為可摺疊區塊
        self.txt2img_tracked_component_items: list[TrackedComponentItem] = txt2img_custom_tracked_items
        self.img2img_tracked_component_items: list[TrackedComponentItem] = img2img_custom_tracked_items

        # 載入 txt2img/img2img 的內建預設與自訂預設（兩者脫鉤）
        (self.txt2img_default_config_presets, self.txt2img_custom_config_presets) = load_txt2img_config_file(CONFIG_TXT2IMG_FILE_NAME)
        (self.img2img_default_config_presets, self.img2img_custom_config_presets) = load_img2img_config_file(CONFIG_IMG2IMG_FILE_NAME)

        # UI 顯示用集合：同名時以自訂預設覆蓋內建預設；儲存/刪除只作用於自訂集合
        self.txt2img_config_presets: dict[str, dict[str, Any]] = build_config_presets(self.txt2img_default_config_presets, self.txt2img_custom_config_presets, keep_builtin_config_presets_enabled())
        self.img2img_config_presets: dict[str, dict[str, Any]] = build_config_presets(self.img2img_default_config_presets, self.img2img_custom_config_presets, keep_builtin_config_presets_enabled())



    def title(self):
        """
        Return the title of the script shown in the UI.
        返回在UI中显示的脚本标题
        """
        return "Config Presets"

    def show(self, is_img2img):
        """
        Return when this script should be visible. AlwaysVisible hides it from the Scripts dropdown.
        返回脚本应该何时可见。AlwaysVisible将其从Scripts下拉菜单中隐藏
        """
        return scripts.AlwaysVisible    # hide this script in the Scripts dropdown

    def after_component(self, component, **kwargs):
        """
        Called after each UI component is created.
        This is where we build our preset management UI and hook into existing components.

        职责分为两层：
        - 侦测层 (ComponentTracker)：基于 component 的属性登记追踪元件，触发元件出现时解析出UI 所需资料
        - 显示层 (ConfigPresetUI)：以解析结果建立 Config Presets 的 Gradio 介面

        在每个UI组件创建后调用。
        这里我们构建预设管理UI并连接到现有组件。
        """
        # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
        # so we can use the same code for both tabs
        # 为了通用化代码，检测我们是在txt2img标签页还是img2img标签页，然后使用相应的self变量
        # 这样我们可以为两个标签页使用相同的代码
        tracker = self.txt2img_component_tracker if self.is_txt2img else self.img2img_component_tracker

        # 偵測層：登記目前元件；觸發元件（圖庫最底部的 generation info 按鈕）出現時才繼續建立 UI
        #if component.elem_id == "txt2img_generation_info_button" or component.elem_id == "img2img_generation_info_button": #very bottom of the txt2img/img2img image gallery
        #txt2img/img2img图片库的最底部
        if not tracker.register_component(component):
            return

        # 偵測層解析：剔除缺失的可選元件；必備元件缺失時記錄錯誤並放棄建立 UI（防止None类型组件导致UI崩溃）
        resolved = tracker.resolve()
        if resolved is None:
            return

        if self.is_txt2img:
            config_presets = self.txt2img_config_presets
            custom_config_presets = self.txt2img_custom_config_presets
            default_config_presets = self.txt2img_default_config_presets
            config_file_name = CONFIG_TXT2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            tracked_component_items = self.txt2img_tracked_component_items
        else:
            config_presets = self.img2img_config_presets
            custom_config_presets = self.img2img_custom_config_presets
            default_config_presets = self.img2img_default_config_presets
            config_file_name = CONFIG_IMG2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            tracked_component_items = self.img2img_tracked_component_items

        # 顯示層：建立 Config Presets UI（下拉選單、欄位複選框組、工具按鈕與事件處理）
        ConfigPresetUI(
            type_name=EnumTypeName.txt2img if self.is_txt2img else EnumTypeName.img2img,
            resolved=resolved,
            config_presets=config_presets,
            custom_config_presets=custom_config_presets,
            default_config_presets=default_config_presets,
            synonym_ids=self.synonym_ids,
            config_file_name=config_file_name,
            custom_tracked_components_config_file_name=custom_tracked_components_config_file_name,
            keep_builtin_config_presets_enabled=keep_builtin_config_presets_enabled,
            tracked_component_items=tracked_component_items,
        ).build()


    def ui(self, is_img2img: bool):
        """
        Placeholder for UI creation. Not used in this extension.

        UI创建的占位符。此扩展中未使用。
        """
        pass

    def run(self, p, *args):
        """
        Placeholder for script execution. Not used in this extension.

        脚本执行的占位符。此扩展中未使用。
        """
        pass

