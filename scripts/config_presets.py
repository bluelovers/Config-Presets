# Import necessary modules for Stable Diffusion Web UI extension
# 导入Stable Diffusion Web UI扩展所需的模块
import traceback
from typing import Any
import modules.scripts as scripts  # pyright: ignore[reportMissingImports]
import gradio as gr  # pyright: ignore[reportMissingImports]

from modules.ui_components import ToolButton  # pyright: ignore[reportMissingImports]
from sd_config_presets.config_components import dict_synonyms, load_custom_tracked_component_ids, EnumTypeName, log, log_error, log_critical_error, load_config_file, write_json_to_file
from sd_config_presets.sd_components import save_config, get_config_preset_dropdown_choices
from sd_config_presets.utils import open_file_in_system_app

# Base directory path for the Config-Presets extension
# Contains the full path to the extension folder
# Config-Presets扩展的基础目录路径
# 包含扩展文件夹的完整路径
BASEDIR: str = scripts.basedir()     #C:\path\to\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path

# Configuration file names for different components and modes
# 不同组件和模式的配置文件名
CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = f"{BASEDIR}/config-txt2img-custom-tracked-components.txt"
CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = f"{BASEDIR}/config-img2img-custom-tracked-components.txt"
CONFIG_TXT2IMG_FILE_NAME = f"{BASEDIR}/config-txt2img.json"
CONFIG_IMG2IMG_FILE_NAME = f"{BASEDIR}/config-img2img.json"


def load_txt2img_custom_tracked_component_ids() -> list[str]:
    """
    Load custom tracked component IDs for txt2img mode.
    This function loads component IDs that users want to track in addition to default ones.
    Returns a list of component IDs that should be tracked for presets.
    
    加载txt2img模式的自定义跟踪组件ID。
    此函数加载用户想要跟踪的组件ID，除了默认的组件之外。
    返回应该为预设跟踪的组件ID列表。
    """
    type_name = EnumTypeName.txt2img

    # config file not found
    # First time running the extension or it was deleted, so fill it with default values
    # 配置文件未找到
    # 第一次运行扩展或文件被删除，所以用默认值填充
    txt2img_custom_tracked_components_default_text = f"""# Put custom {type_name} tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
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

# X/Y/Z plot (script):
#script_{type_name}_xyz_plot_x_type
#script_{type_name}_xyz_plot_y_type
#script_{type_name}_xyz_plot_z_type
#script_{type_name}_xyz_plot_x_values
#script_{type_name}_xyz_plot_y_values
#script_{type_name}_xyz_plot_z_values

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

    return load_custom_tracked_component_ids(CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME, EnumTypeName.txt2img, txt2img_custom_tracked_components_default_text)


def load_img2img_custom_tracked_component_ids() -> list[str]:
    """
    Load custom tracked component IDs for img2img mode.
    This function loads component IDs that users want to track in addition to default ones.
    Returns a list of component IDs that should be tracked for presets.
    
    加载img2img模式的自定义跟踪组件ID。
    此函数加载用户想要跟踪的组件ID，除了默认的组件之外。
    返回应该为预设跟踪的组件ID列表。
    """
    type_name = EnumTypeName.img2img

    # config file not found
    # First time running the extension or it was deleted, so fill it with default values
    # 配置文件未找到
    # 第一次运行扩展或文件被删除，所以用默认值填充
    img2img_custom_tracked_components_default_text = f"""# Put custom {type_name} tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
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

# X/Y/Z plot (script):
#script_{type_name}_xyz_plot_x_type
#script_{type_name}_xyz_plot_y_type
#script_{type_name}_xyz_plot_z_type
#script_{type_name}_xyz_plot_x_values
#script_{type_name}_xyz_plot_y_values
#script_{type_name}_xyz_plot_z_values

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

    return load_custom_tracked_component_ids(CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME, EnumTypeName.img2img, img2img_custom_tracked_components_default_text)


def load_txt2img_config_file():
    """
    Load txt2img configuration presets from JSON file.
    If file doesn't exist or is corrupted, creates default presets.
    Returns a dictionary containing all txt2img configuration presets.
    
    从JSON文件加载txt2img配置预设。
    如果文件不存在或损坏，创建默认预设。
    返回包含所有txt2img配置预设的字典。
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
        "None": {},
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

    # Call the generic _load_config_file function with specific parameters
    # 调用通用的_load_config_file函数，传入特定参数
    return load_config_file(CONFIG_TXT2IMG_FILE_NAME, type_name, txt2img_config_presets)


def load_img2img_config_file():
    """
    Load img2img configuration presets from JSON file.
    If file doesn't exist or is corrupted, creates default presets.
    Returns a dictionary containing all img2img configuration presets.
    
    从JSON文件加载img2img配置预设。
    如果文件不存在或损坏，创建默认预设。
    返回包含所有img2img配置预设的字典。
    """
    # Define type name for img2img configuration
    # 为img2img配置定义类型名称
    type_name = EnumTypeName.img2img

    # Default presets for img2img configuration
    # img2img配置的默认预设
    img2img_config_presets = {
        "None": {},
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

    # Call the generic _load_config_file function with specific parameters
    # 调用通用的_load_config_file函数，传入特定参数
    return load_config_file(CONFIG_IMG2IMG_FILE_NAME, type_name, img2img_config_presets)


class Script(scripts.Script):
    """
    Main Script class for the Config-Presets extension.
    This class handles the UI components and logic for saving/loading configuration presets.
    
    Config-Presets扩展的主Script类。
    此类处理用于保存/加载配置预设的UI组件和逻辑。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load custom tracked components
        # 加载自定义跟踪组件
        txt2img_custom_tracked_components_ids = load_txt2img_custom_tracked_component_ids()
        img2img_custom_tracked_components_ids = load_img2img_custom_tracked_component_ids()


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
        self.txt2img_component_ids += txt2img_custom_tracked_components_ids # add the custom tracked components

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
        self.img2img_component_ids += img2img_custom_tracked_components_ids # add the custom tracked components

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
        
        # Mapping between component labels and the actual components in ui.py
        # 组件标签与ui.py中实际组件之间的映射
        self.txt2img_component_map: dict[str, Any] = {k: None for k in self.txt2img_component_ids}  # gets filled up in the after_component() method
        self.img2img_component_map: dict[str, Any] = {k: None for k in self.img2img_component_ids}  # gets filled up in the after_component() method

        # Load txt2img and img2img config files
        # 加载txt2img和img2img配置文件
        self.txt2img_config_presets: dict[str, dict[str, Any]] = load_txt2img_config_file()
        self.img2img_config_presets: dict[str, dict[str, Any]] = load_img2img_config_file()



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
        
        在每个UI组件创建后调用。
        这里我们构建预设管理UI并连接到现有组件。
        """
        # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
        # so we can use the same code for both tabs
        # 为了通用化代码，检测我们是在txt2img标签页还是img2img标签页，然后使用相应的self变量
        # 这样我们可以为两个标签页使用相同的代码
        component_map: dict[str, Any] = None  # pyright: ignore[reportAssignmentType]
        component_ids: list[str] = None  # pyright: ignore[reportAssignmentType]
        config_file_name = None
        custom_tracked_components_config_file_name = None
        optional_ids = None
        synonym_ids = self.synonym_ids
        type_name: EnumTypeName = None  # pyright: ignore[reportAssignmentType]
        if self.is_txt2img:
            component_map = self.txt2img_component_map
            component_ids = self.txt2img_component_ids
            config_file_name = CONFIG_TXT2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            optional_ids = self.txt2img_optional_ids
            type_name = EnumTypeName.txt2img
        else:
            component_map = self.img2img_component_map
            component_ids = self.img2img_component_ids
            config_file_name = CONFIG_IMG2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            optional_ids = self.img2img_optional_ids
            type_name = EnumTypeName.img2img

        #if component.label in self.component_map:
        if component.elem_id in component_map:
            component_map[component.elem_id] = component
            #log_debug(f"found component: {component.elem_id} {component}")

        #if component.elem_id == "script_list": #bottom of the script dropdown
        #脚本下拉菜单底部
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        #不起作用，需要在我们要编辑的所有组件加载后添加
        #if component.elem_id == "open_folder": #bottom of the image gallery
        #图片库底部
        #if component.elem_id == "txt2img_results" or component.elem_id == "img2img_results": #bottom of the image gallery, doesn't work
        #图片库底部，不起作用
        #if component.elem_id == "txt2img_gallery_container" or component.elem_id == "img2img_gallery_container": #bottom of the image gallery, doesn't work
        #图片库底部，不起作用
        if component.elem_id == "txt2img_generation_info_button" or component.elem_id == "img2img_generation_info_button": #very bottom of the txt2img/img2img image gallery
            #txt2img/img2img图片库的最底部

            #log_debug("Creating dropdown values...")
            #log_debug("key/value pairs in component_map:")

            # before we create the dropdown, we need to check if each component was found successfully to prevent errors from bricking the Web UI
            component_map = {k:v for k,v in component_map.items() if v is not None or k not in optional_ids}    # Cleanse missing optional components with optional_ids
            component_ids = [k for k in component_ids if k in component_map]

            # protect against None type components to prevent bricking the UI
            # this check needs to happen after optional_ids are accounted for
            # 防止None类型组件导致UI崩溃
            # 此检查需要在考虑optional_ids后进行
            for component_name, component in component_map.items():
                if component is None:
                    log_error(f"The {type_name} component '{component_name}' could not be processed. This may be because you are running an outdated version of the Config-Presets extension, you included a component ID in the custom tracked components config file that does not exist, it no longer exists (if you updated an extension or Automatic1111), or is an invalid component (if this is the case, you need to manually edit the config file at {custom_tracked_components_config_file_name} or just delete it so it resets to defaults). This extension will not work until this issue is resolved.")
                    return

            # Mark components with type "index" to be transformed
            # 标记类型为"index"的组件以进行转换
            index_type_components = []
            for component in component_map.values():
                #log_debug(component)
                if getattr(component, "type", "No type attr") == "index":
                    # log_debug(component.elem_id)
                    index_type_components.append(component.elem_id)

            preset_values: list[str] = []
            config_presets: dict[str, Any] = None  # pyright: ignore[reportAssignmentType]
            if self.is_txt2img:
                config_presets = self.txt2img_config_presets
            else:
                config_presets = self.img2img_config_presets

            preset_values = list(config_presets.keys())
            # for dropdownValue in config_presets:
            #     preset_values.append(dropdownValue)
            #     #log(f"added \"{dropdownValue}\"")

            fields_checkboxgroup_value = component_ids.copy()
            fields_checkboxgroup = gr.CheckboxGroup(choices=component_ids,
                                                    value=fields_checkboxgroup_value,    #check all checkboxes by default
                                                    label="Fields to save",
                                                    show_label=True,
                                                    interactive=True,
                                                    elem_id="script_config_preset_fields_to_save",
                                                    ).unrender() #we need to define this early on so that it can be used as an input for another function
            # 复选框组值，默认选中所有复选框
            # 复选框组，用于选择要保存的字段

            with gr.Box(elem_id=f"config_preset_wrapper_{type_name}"):
                with gr.Row(elem_id="config_preset_dropdown_row"):

                    def get_config_preset(dropdown_value):
                        config_preset = config_presets[dropdown_value]
                        config_preset = dict_synonyms(config_preset, synonym_ids)  # Add synonyms
                        return config_preset

                    def get_filtered_ids(config_preset):
                        filtered_ids = [id for id in component_ids if
                                        id in config_preset.keys()] or component_ids.copy()
                        return filtered_ids

                    def update_fields_checkboxgroup(dropdown_value):
                        config_preset = get_config_preset(dropdown_value)
                        filtered_ids = get_filtered_ids(config_preset)
                        return gr.update(value=filtered_ids)

                    def config_preset_dropdown_change(dropdown_value, *components_value):
                        config_preset = get_config_preset(dropdown_value)
                        log(f"Changed to: {dropdown_value}")

                        # update component values with user preset
                        current_components = dict(zip(component_map.keys(), components_value))
                        #log_debug("Components before:", current_components)
                        current_components.update(config_preset)

                        # transform necessary components from index to value
                        for component_name, component_value in current_components.items():
                            #log_debug(component_name, component_value)
                            if component_name in index_type_components and type(component_value) == int:
                                    current_components[component_name] = component_map[component_name].choices[component_value]

                                    # A1111 1.6.0 changed radio buttons values into tuples.
                                    # For example, for the "img2img_mask_mode" component it changed from:
                                    #   ['Inpaint masked', 'Inpaint not masked']
                                    #   to
                                    #   [('Inpaint masked', 'Inpaint masked'), ('Inpaint not masked', 'Inpaint not masked')]
                                    # Using a type == tuple check here will ensure compatibility with the older versions.
                                    # A1111 1.6.0将单选按钮值更改为元组。
                                    # 例如，对于"img2img_mask_mode"组件，它从：
                                    #   ['Inpaint masked', 'Inpaint not masked']
                                    #   更改为
                                    #   [('Inpaint masked', 'Inpaint masked'), ('Inpaint not masked', 'Inpaint not masked')]
                                    # 在这里使用type == tuple检查将确保与旧版本的兼容性。
                                    if type(current_components[component_name]) == tuple:
                                        current_components[component_name] = current_components[component_name][0]

                        #log_debug("Components after :", current_components)

                        return list(current_components.values())

                    config_preset_dropdown = gr.Dropdown(
                        label="Config Presets",
                        choices=get_config_preset_dropdown_choices(preset_values),
                        elem_id="config_preset_txt2img_dropdown" if self.is_txt2img else "config_preset_img2img_dropdown",
                    )

                    try:
                        components = list(component_map.values())
                        config_preset_dropdown.change(
                            fn=config_preset_dropdown_change,
                            show_progress=False,
                            inputs=[config_preset_dropdown, *components],
                            outputs=components
                            )
                        config_preset_dropdown.change(
                            fn=update_fields_checkboxgroup,
                            show_progress=False,
                            inputs=[config_preset_dropdown],
                            outputs=[fields_checkboxgroup]
                        )
                    except AttributeError:
                        print(traceback.format_exc())   # prints the exception stacktrace
                        log_critical_error("The Config-Presets extension encountered a fatal error. A component required by this extension no longer exists in the Web UI. This is most likely due to the A1111 Web UI being updated. Try updating the Config-Presets extension. If that doesn't work, please post a bug report at https://github.com/Zyin055/Config-Presets/issues and delete your extensions/Config-Presets folder until an update is published.")


                    def delete_selected_preset(config_preset_name: str):
                        """
                        Delete the selected preset from the configuration.
                        
                        删除选中的预设配置。
                        """
                        if config_preset_name in config_presets.keys():
                            del config_presets[config_preset_name]
                            log(f"deleted: \"{config_preset_name}\"")

                            write_json_to_file(config_presets, config_file_name)

                            preset_keys = list(config_presets.keys())
                            return gr.Dropdown.update(value=preset_keys[len(preset_keys)-1],
                                                        choices=get_config_preset_dropdown_choices(preset_keys),
                                                        )
                        # do nothing if no value is selected
                        return gr.Dropdown.update()
                    
                    def refresh_dropdown_button_click():
                        """
                        Refresh the dropdown by reloading configuration presets from files.
                        
                        通过从文件重新加载配置预设来刷新下拉菜单。
                        """
                        if self.is_txt2img:
                            self.txt2img_config_presets = load_txt2img_config_file()
                            #new_config_presets = self.txt2img_config_presets
                            config_presets.update(self.txt2img_config_presets)
                            preset_values = list(self.txt2img_config_presets.keys())
                        else:
                            self.img2img_config_presets = load_img2img_config_file()
                            #new_config_presets = self.img2img_config_presets
                            config_presets.update(self.img2img_config_presets)
                            preset_values = list(self.img2img_config_presets.keys())
                        
                        return gr.Dropdown.update(choices=get_config_preset_dropdown_choices(preset_values))

                    refresh_dropdown_button = ToolButton(
                        value="🔄",
                        elem_id="script_config_preset_refresh_dropdown_button",
                        visible=False,
                    )
                    refresh_dropdown_button.click(
                        fn=refresh_dropdown_button_click,
                        inputs=[],
                        outputs=[config_preset_dropdown],
                    )

                    trash_button = ToolButton(
                        value="🗑️",
                        elem_id="script_config_preset_trash_button",
                        visible=False,
                    )
                    trash_button.click(
                        fn=delete_selected_preset,
                        inputs=[config_preset_dropdown],
                        outputs=[config_preset_dropdown],
                    )



                    open_config_file_button = ToolButton(
                        value="📂",
                        elem_id="script_config_preset_open_config_file_button",
                        visible=False,
                    )
                    open_config_file_button.click(
                        fn=lambda: open_file_in_system_app(config_file_name),
                        inputs=[],
                        outputs=[],
                    )

                    cancel_button = ToolButton(
                        value="\U000021A9",
                        elem_id="script_config_preset_cancel_save_button",
                        visible=False,
                    )

                    reapply_button = ToolButton(
                        value="📋",
                        elem_id="script_config_preset_reapply_button"
                    )

                    components = list(component_map.values())
                    reapply_button.click(
                        fn=config_preset_dropdown_change,
                        inputs=[config_preset_dropdown, *components],
                        show_progress=False,
                        outputs=components,
                    )
                    reapply_button.click(
                        fn=update_fields_checkboxgroup,
                        inputs=[config_preset_dropdown],
                        show_progress=False,
                        outputs=[fields_checkboxgroup],
                    )

                    add_remove_button = ToolButton(
                        value="🖌️",
                        elem_id="script_config_preset_add_button"
                    )

                with gr.Row() as collapsable_row:
                    collapsable_row.visible = False
                    with gr.Column():
                        with gr.Row():
                            save_textbox = gr.Textbox(
                                label="New preset name",
                                placeholder="Ex: Low quality",
                                max_lines=1,
                                elem_id="script_config_preset_save_textbox",
                            )
                            save_button = ToolButton(
                                value="💾",
                                variant="primary",
                                elem_id="script_config_preset_save_button",
                            )

                            save_button.click(
                                fn=save_config(config_presets, component_map, config_file_name),
                                inputs=list(
                                    [save_textbox] + [fields_checkboxgroup] + [component_map[comp_name] for comp_name in
                                                                                component_ids if
                                                                                component_map[comp_name] is not None]),
                                outputs=[config_preset_dropdown, save_textbox],
                            )

                            def add_remove_button_click(save_textbox_text: str, config_preset_dropdown_value: str):
                                """
                                Handle add/remove button click event.
                                Auto-populate textbox if empty when a preset is selected.
                                
                                处理添加/删除按钮点击事件。
                                如果选择了预设且文本框为空，则自动填充文本框。
                                """
                                if save_textbox_text == "" or save_textbox_text is None:
                                    if config_preset_dropdown_value != "" and config_preset_dropdown_value is not None:
                                        # save textbox is empty, and we have a dropdown value selected
                                        # auto-populate the save textbox so it's easier to overwrite existing config preset
                                        # 保存文本框为空，并且我们选择了下拉菜单值
                                        # 自动填充保存文本框，以便更容易覆盖现有配置预设
                                        return gr.Textbox.update(value=config_preset_dropdown_value)
                                return gr.Textbox.update()


                            def expand_edit_ui():
                                """
                                Expand the edit UI by showing relevant buttons and hiding others.
                                
                                展开编辑UI，显示相关按钮并隐藏其他按钮。
                                """
                                return gr.Row.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=True)

                            def collapse_edit_ui():
                                """
                                Collapse the edit UI by hiding relevant buttons and showing others.
                                
                                折叠编辑UI，隐藏相关按钮并显示其他按钮。
                                """
                                return gr.Row.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=False)

                            add_remove_button.click(
                                fn=add_remove_button_click,
                                inputs=[save_textbox, config_preset_dropdown],
                                outputs=[save_textbox],
                            )
                            add_remove_button.click(
                                fn=expand_edit_ui,
                                inputs=[],
                                outputs=[collapsable_row, refresh_dropdown_button, reapply_button, add_remove_button, trash_button, open_config_file_button, cancel_button],
                            )

                            cancel_button.click(
                                fn=collapse_edit_ui,
                                inputs=[],
                                outputs=[collapsable_row, refresh_dropdown_button, reapply_button, add_remove_button, trash_button, open_config_file_button, cancel_button],
                            )

                        with gr.Row():
                            fields_checkboxgroup.render()

                        with gr.Row():
                            with gr.Column(scale=1):
                                open_custom_tracked_components_config_file_button = gr.Button(
                                    value="📂 Add custom fields...",
                                    elem_id="script_config_preset_open_custom_tracked_components_config",
                                )
                                open_custom_tracked_components_config_file_button.click(
                                    fn=lambda: open_file_in_system_app(custom_tracked_components_config_file_name),
                                    inputs=[],
                                    outputs=[],
                                )
                            with gr.Column(scale=2):
                                pass


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

