
import csv
from io import StringIO
from typing import Any
from sd_config_presets.config_components import log, log_error, write_json_to_file
from modules.sd_samplers import samplers_map, samplers  # pyright: ignore[reportMissingImports]
import gradio as gr  # pyright: ignore[reportMissingImports]
from sd_config_presets.utils import open_file_in_system_app
from modules.ui_components import ToolButton  # pyright: ignore[reportMissingImports]


#def get_config_preset_dropdown_choices(new_config_presets) -> list[str]:
def get_config_preset_dropdown_choices(new_config_presets: list[str]) -> list[str]:
    """
    workaround function for not being able to select new dropdown values after new choices are added to the dropdown in Gradio v3.28.1 (Automatic1111 v1.1.0)
    it's possible they will fix this in Gradio v4
    see: https://github.com/Zyin055/Config-Presets/pull/41
    解决方案函数，用于在Gradio v3.28.1（Automatic1111 v1.1.0）中向下拉菜单添加新选项后无法选择新值的问题
    可能在Gradio v4中会修复此问题
    参见：https://github.com/Zyin055/Config-Presets/pull/41
    """
    new_choices: list[str] = []
    if len(new_config_presets) > 0:
        # if isinstance(new_config_presets, dict):
        #     new_choices.extend(new_config_presets.keys())
        # else: # List assumed.
        #     new_choices.extend(new_config_presets)
        new_choices.extend(new_config_presets)
    return new_choices

def list_to_csv_string(data_list: list[str]) -> str:
    """
    將值列表轉為單個 CSV 字串。

    實作與 scripts/xyz_grid.py（X/Y/Z plot）的 list_to_csv_string 一致，
    使從其 dropdown UI 儲存的值能經 csv_string_to_list_strip() 一致解析。
    """
    with StringIO() as o:
        csv.writer(o).writerow(data_list)
        return o.getvalue().strip()

def save_config(config_presets: dict[str, Any], component_map: dict[str, Any], config_file_name_path: str):
    """
    Save the current values on the UI to a new entry in the config file
    """

    #log_debug("save_config()")
    # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
    def func(new_setting_name: str, fields_to_save_list, *new_setting):
        #log_debug(f"save_config() func() new_setting_name={new_setting_name} *new_setting={new_setting}")
        #log_debug(f"config_presets()={config_presets}")
        #log_debug(f"component_map()={component_map}")
        #log_debug(f"config_file_name()={config_file_name}")

        if new_setting_name == "":
            # do nothing if no label entered in textbox
            # 如果在文本框中没有输入标签，则不执行任何操作
            return gr.Dropdown.update(), gr.Textbox.update()

        new_setting_map: dict[str, Any] = {}    # dict[str, Any]    {"txt2img_steps": 10, ...}
        # 新设置映射字典 - 字符串到任意类型的映射，格式如：{"txt2img_steps": 10, ...}

        #log_debug(f"component_map={component_map}")
        #log_debug(f"new_setting={new_setting}")

        # 組件 ID → 目前 UI 值的映射，用於取得配對的 "{component_id}_dropdown" 元件值
        component_value_map: dict[str, Any] = dict(zip(component_map.keys(), new_setting))

        for i, component_id in enumerate(component_map.keys()):

            if component_id not in fields_to_save_list:
                #log(f"New preset '{new_setting_name}' will not include {component_id}")
                # log(f"新预设'{new_setting_name}'将不包含{component_id}")
                continue

            if component_map[component_id] is not None:
                new_value = new_setting[i]  # this gives the index when the component is a dropdown

                if isinstance(new_value, str) and (component_id == "txt2img_sampling" or component_id == "img2img_sampling" or component_id == "hr_sampler"):
                    if isinstance(new_value, str):  # in A1111 1.6.0(?) the sampler is now returned as a string instead of an integer
                        if new_value == "Use same sampler": # the hr_sampler dropdown has a "Use same sampler" value that doesn't exist in the samplers_map
                            # hr_sampler下拉菜单有一个"Use same sampler"值，在samplers_map中不存在
                            new_setting_map[component_id] = new_value
                        else:
                            new_setting_map[component_id] = samplers_map[new_value.lower()]
                    elif isinstance(new_value, int):
                        new_setting_map[component_id] = samplers[new_value].name
                    else:
                        log_error(f"Unable get sampler name for component: {component_id}")
                        log_error(f"Unknown data type for sampler: {new_value}")
                        # 无法获取组件的采样器名称：{component_id}
                        # 采样器的未知数据类型：{new_value}
                else:
                    if new_value is None or (isinstance(new_value, str) and new_value.strip() == ""):
                        # X/Y/Z plot 在非 csv_mode（dropdown 模式）時，實際值存於配對的 multiselect
                        # "{component_id}_dropdown"、其 textbox 保持空白；
                        # 沿用 xyz_grid.py 的做法，將該 dropdown 選擇儲存為 CSV 字串
                        dropdown_value = component_value_map.get(f"{component_id}_dropdown")
                        if isinstance(dropdown_value, list) and len(dropdown_value) > 0:
                            new_value = list_to_csv_string(dropdown_value)
                    new_setting_map[component_id] = new_value

                #log_debug(f"Saving '{component_id}' as: {new_setting_map[component_id]} ({new_value})")

        #log_debug(f"new_setting_map = {new_setting_map}")

        config_presets.update({new_setting_name: new_setting_map})
        write_json_to_file(config_presets, config_file_name_path)
        # 使用新设置映射更新配置预设
        # 将配置预设写入JSON文件

        # log_debug(f"self.txt2img_config_preset_dropdown.choices before =\n{self.txt2img_config_preset_dropdown.choices}")
        # self.txt2img_config_preset_dropdown.choices = list(config_presets.keys())
        # log_debug(f"self.txt2img_config_preset_dropdown.choices after =\n{self.txt2img_config_preset_dropdown.choices}")

        log(f"Added new preset: {new_setting_name}")
        #log(f"Restarting UI...") # done in _js
        # log(f"添加新预设：{new_setting_name}")
        # log(f"重启UI...") # 在_js中完成

        # update the dropdown with the new config preset
        return gr.Dropdown.update(value=new_setting_name,   
                                  #choices=list(config_presets.keys()),
                                  choices=get_config_preset_dropdown_choices(config_presets.keys()),  # pyright: ignore[reportArgumentType]
                                  ), gr.Textbox.update() # 不清空 New preset name 文字框，保留剛儲存的名稱
                                  # 使用新的配置预设更新下拉菜单

    return func

def createOpenFileInSystemAppButton(value: str, elem_id: str, file_path: str, btnClass: gr.Button | ToolButton = gr.Button, tooltip: str | None = None, *args, **kwargs):
    """
    Create a button that opens a file in the system's default application.
    
    创建一个在系统默认应用程序中打开文件的按钮。
    
    Args:
        value (str): Button display text / 按钮显示文本
        elem_id (str): Element ID for the button / 按钮的元素ID
        file_path (str): Path to the file to open / 要打开的文件路径
        btnClass (gr.Button | ToolButton): Button class to use / 要使用的按钮类
        *args: Additional positional arguments passed to btnClass / 传递给btnClass的额外位置参数
        **kwargs: Additional keyword arguments passed to btnClass / 传递给btnClass的额外关键字参数
    
    Returns:
        btn: The created button instance / 创建的按钮实例
    """
    btn = btnClass(
        value=value,
        elem_id=elem_id,
        tooltip=tooltip,
        *args,
        **kwargs
    )
    btn.click(
        fn=lambda: open_file_in_system_app(file_path),
        inputs=[],
        outputs=[],
    )
    return btn
