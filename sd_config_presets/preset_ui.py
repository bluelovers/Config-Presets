"""
設定預設 UI 顯示層 (Config Presets UI Display Layer)

以元件偵測層 (component_tracker.py) 解析出的結果
建立 Config Presets 的 Gradio 介面：
下拉選單、欄位複選框組、儲存/刪除/重新整理等工具按鈕，
並掛載載入/儲存/刪除/重新整理等事件處理閉包。

本層不負責元件偵測：元件資料由 ComponentTracker.resolve() 傳入，
設定檔路徑與「是否保留內建預設」的 Settings 選項皆由呼叫端提供。
"""

import traceback
from typing import Any, Callable

import gradio as gr  # pyright: ignore[reportMissingImports]
from modules.ui_components import ToolButton  # pyright: ignore[reportMissingImports]

from sd_config_presets.component_tracker import ResolvedComponents
from sd_config_presets.config_components import dict_synonyms, is_reserved_preset_name, log, log_critical_error, write_json_to_file, RESERVED_PRESET_NAME  # pyright: ignore[reportMissingImports]
from sd_config_presets.config_file.preset_loaders import load_txt2img_config_file, load_img2img_config_file, build_config_presets  # pyright: ignore[reportMissingImports]
from sd_config_presets.sd_components import createOpenFileInSystemAppButton, save_config, get_config_preset_dropdown_choices  # pyright: ignore[reportMissingImports]
from sd_config_presets.config_components import EnumTypeName


class ConfigPresetUI:
    """
    Config Presets 的 UI 顯示層。

    由呼叫端 (Script.after_component) 傳入偵測層解析結果與預設集合，
    build() 負責建立 Gradio 元件並掛載事件處理。
    """

    def __init__(
        self,
        type_name: EnumTypeName,
        resolved: ResolvedComponents,
        config_presets: dict[str, dict[str, Any]],
        custom_config_presets: dict[str, dict[str, Any]],
        default_config_presets: dict[str, dict[str, Any]],
        synonym_ids: list[tuple[str, str]],
        config_file_name: str,
        custom_tracked_components_config_file_name: str,
        keep_builtin_config_presets_enabled: Callable[[], bool],
    ):
        """
        Args:
            type_name: tab 類型 (txt2img 或 img2img)
            resolved: 偵測層解析結果（乾淨的 component_map / component_ids / index 型別清單）
            config_presets: 顯示用預設集合（內建＋自訂，同名以自訂覆蓋內建）
            custom_config_presets: 自訂專用集合（寫入設定檔）
            default_config_presets: 內建預設集合，重新整理時用於重建顯示集合
            synonym_ids: 載入預設時可互換的同義詞 ID 對照
            config_file_name: 自訂預設 JSON 檔路徑
            custom_tracked_components_config_file_name: 自訂追蹤元件設定檔路徑
            keep_builtin_config_presets_enabled: 讀取 Settings 選項的回呼，重新整理時重新讀取
        """
        self.type_name = type_name
        self.is_txt2img = type_name == EnumTypeName.txt2img
        self.component_map = resolved.component_map
        self.component_ids = resolved.component_ids
        self.index_type_components = resolved.index_type_components
        self.config_presets = config_presets
        self.custom_config_presets = custom_config_presets
        self.default_config_presets = default_config_presets
        self.synonym_ids = synonym_ids
        self.config_file_name = config_file_name
        self.custom_tracked_components_config_file_name = custom_tracked_components_config_file_name
        self.keep_builtin_config_presets_enabled = keep_builtin_config_presets_enabled

    def get_config_preset(self, dropdown_value: str) -> dict[str, Any]:
        """
        取得下拉選單選取的預設，並套用同義詞 ID。
        """
        config_preset = self.config_presets[dropdown_value]
        config_preset = dict_synonyms(config_preset, self.synonym_ids)  # Add synonyms
        return config_preset

    def get_filtered_ids(self, config_preset: dict[str, Any]) -> list[str]:
        """
        回傳預設中實際包含的追蹤元件 ID；預設沒有任何追蹤欄位時回傳全部。
        """
        filtered_ids = [id for id in self.component_ids if
                        id in config_preset.keys()] or self.component_ids.copy()
        return filtered_ids

    def update_fields_checkboxgroup(self, dropdown_value: str):
        """
        依選取預設包含的欄位更新「Fields to save」複選框組。
        """
        config_preset = self.get_config_preset(dropdown_value)
        filtered_ids = self.get_filtered_ids(config_preset)
        return gr.update(value=filtered_ids)

    def config_preset_dropdown_change(self, dropdown_value: str, *components_value):
        """
        下拉選單選取變更時，將預設值套用到各追蹤元件。
        """
        config_preset = self.get_config_preset(dropdown_value)
        log(f"Changed to: {dropdown_value}")

        # update component values with user preset
        current_components = dict(zip(self.component_map.keys(), components_value))
        #log_debug("Components before:", current_components)
        current_components.update(config_preset)

        # transform necessary components from index to value
        for component_name, component_value in current_components.items():
            #log_debug(component_name, component_value)
            if component_name in self.index_type_components and type(component_value) == int:
                    current_components[component_name] = self.component_map[component_name].choices[component_value]

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

    def delete_selected_preset(self, config_preset_name: str):
        """
        刪除選取的自訂預設；內建預設與保留項不可刪除。

        删除选中的自定义预设；内建预设与保留项不可删除。
        """
        if is_reserved_preset_name(config_preset_name):
            log(f"The '{RESERVED_PRESET_NAME}' preset is reserved and can not be deleted")
            return gr.Dropdown.update()

        if config_preset_name in self.custom_config_presets:
            del self.custom_config_presets[config_preset_name]     # 僅刪除自訂來源
            self.config_presets.pop(config_preset_name, None)      # 同步移除顯示項
            log(f"deleted: \"{config_preset_name}\"")

            write_json_to_file(self.custom_config_presets, self.config_file_name)

            preset_keys = list(self.config_presets.keys())
            return gr.Dropdown.update(value=preset_keys[len(preset_keys)-1],
                                        choices=get_config_preset_dropdown_choices(preset_keys),
                                        )

        log(f"\"{config_preset_name}\" is a built-in preset and can not be deleted")
        # do nothing if no value is selected
        return gr.Dropdown.update()

    def refresh_dropdown_button_click(self):
        """
        從設定檔重新載入自訂預設，並依目前 Settings 選項重建顯示集合。
        """
        if self.is_txt2img:
            (_, reloaded_custom_presets) = load_txt2img_config_file(self.config_file_name)
        else:
            (_, reloaded_custom_presets) = load_img2img_config_file(self.config_file_name)

        # 以原地更新維持各閉包共享的 dict 參照不變
        self.custom_config_presets.clear()
        self.custom_config_presets.update(reloaded_custom_presets)
        self.config_presets.clear()
        self.config_presets.update(build_config_presets(self.default_config_presets, self.custom_config_presets, self.keep_builtin_config_presets_enabled()))

        preset_values = list(self.config_presets.keys())
        return gr.Dropdown.update(choices=get_config_preset_dropdown_choices(preset_values))

    @staticmethod
    def update_save_textbox(dropdown_value: str):
        """
        將 Config Presets 下拉選單的選取值同步到 New preset name 文字框。
        """
        if dropdown_value is None or dropdown_value == "":
            return gr.Textbox.update()
        return gr.Textbox.update(value=dropdown_value)

    @staticmethod
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

    @staticmethod
    def expand_edit_ui():
        """
        Expand the edit UI by showing relevant buttons and hiding others.

        展开编辑UI，显示相关按钮并隐藏其他按钮。
        """
        return gr.Row.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=True)

    @staticmethod
    def collapse_edit_ui():
        """
        Collapse the edit UI by hiding relevant buttons and showing others.

        折叠编辑UI，隐藏相关按钮并显示其他按钮。
        """
        return gr.Row.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=True), gr.Button.update(visible=True), gr.Button.update(visible=False), gr.Button.update(visible=False), gr.Button.update(visible=False)

    def build(self):
        """
        建立 Config Presets 的 Gradio 介面並掛載事件處理。

        對應原 after_component() 的 UI 建構區段；在 generation info 按鈕（圖庫最底部）
        建立時呼叫，使本區塊位於所有追蹤元件之後。
        """
        #log_debug("Creating dropdown values...")
        #log_debug("key/value pairs in component_map:")

        preset_values = list(self.config_presets.keys())

        fields_checkboxgroup_value = self.component_ids.copy()
        fields_checkboxgroup = gr.CheckboxGroup(choices=self.component_ids,
                                                value=fields_checkboxgroup_value,    #check all checkboxes by default
                                                label="Fields to save",
                                                show_label=True,
                                                interactive=True,
                                                elem_id="script_config_preset_fields_to_save",
                                                ).unrender() #we need to define this early on so that it can be used as an input for another function
        # 复选框组值，默认选中所有复选框
        # 复选框组，用于选择要保存的字段

        with gr.Box(elem_id=f"config_preset_wrapper_{self.type_name.value}"):
            with gr.Row(elem_id="config_preset_dropdown_row"):

                config_preset_dropdown = gr.Dropdown(
                    label="Config Presets",
                    choices=get_config_preset_dropdown_choices(preset_values),
                    elem_id="config_preset_txt2img_dropdown" if self.is_txt2img else "config_preset_img2img_dropdown",
                )

                try:
                    components = list(self.component_map.values())
                    config_preset_dropdown.change(
                        fn=self.config_preset_dropdown_change,
                        show_progress=False,
                        inputs=[config_preset_dropdown, *components],
                        outputs=components
                        )
                    config_preset_dropdown.change(
                        fn=self.update_fields_checkboxgroup,
                        show_progress=False,
                        inputs=[config_preset_dropdown],
                        outputs=[fields_checkboxgroup]
                    )
                except AttributeError:
                    print(traceback.format_exc())   # prints the exception stacktrace
                    log_critical_error("The Config-Presets extension encountered a fatal error. A component required by this extension no longer exists in the Web UI. This is most likely due to the A1111 Web UI being updated. Try updating the Config-Presets extension. If that doesn't work, please post a bug report at https://github.com/Zyin055/Config-Presets/issues and delete your extensions/Config-Presets folder until an update is published.")

                refresh_dropdown_button = ToolButton(
                    value="🔄",
                    elem_id="script_config_preset_refresh_dropdown_button",
                    visible=False,
                )
                refresh_dropdown_button.click(
                    fn=self.refresh_dropdown_button_click,
                    inputs=[],
                    outputs=[config_preset_dropdown],
                )

                trash_button = ToolButton(
                    value="🗑️",
                    elem_id="script_config_preset_trash_button",
                    visible=False,
                )
                trash_button.click(
                    fn=self.delete_selected_preset,
                    inputs=[config_preset_dropdown],
                    outputs=[config_preset_dropdown],
                )

                open_config_file_button = createOpenFileInSystemAppButton(
                    btnClass=ToolButton,
                    value="📂",
                    tooltip="Open config file in system app",
                    elem_id="script_config_preset_open_config_file_button",
                    visible=False,
                    file_path=self.config_file_name
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

                components = list(self.component_map.values())
                reapply_button.click(
                    fn=self.config_preset_dropdown_change,
                    inputs=[config_preset_dropdown, *components],
                    show_progress=False,
                    outputs=components,
                )
                reapply_button.click(
                    fn=self.update_fields_checkboxgroup,
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
                            fn=save_config(self.config_presets, self.custom_config_presets, self.component_map, self.config_file_name),
                            inputs=list(
                                [save_textbox] + [fields_checkboxgroup] + [self.component_map[comp_name] for comp_name in
                                                                            self.component_ids if
                                                                            self.component_map[comp_name] is not None]),
                            outputs=[config_preset_dropdown, save_textbox],
                        )

                        # Config Presets 選取變更時（含儲存、刪除後的自動切換）同步 New preset name
                        config_preset_dropdown.change(
                            fn=self.update_save_textbox,
                            show_progress=False,
                            inputs=[config_preset_dropdown],
                            outputs=[save_textbox],
                        )

                        add_remove_button.click(
                            fn=self.add_remove_button_click,
                            inputs=[save_textbox, config_preset_dropdown],
                            outputs=[save_textbox],
                        )
                        add_remove_button.click(
                            fn=self.expand_edit_ui,
                            inputs=[],
                            outputs=[collapsable_row, refresh_dropdown_button, reapply_button, add_remove_button, trash_button, open_config_file_button, cancel_button],
                        )

                        cancel_button.click(
                            fn=self.collapse_edit_ui,
                            inputs=[],
                            outputs=[collapsable_row, refresh_dropdown_button, reapply_button, add_remove_button, trash_button, open_config_file_button, cancel_button],
                        )

                    with gr.Row():
                        fields_checkboxgroup.render()

                    with gr.Row():
                        with gr.Column(scale=1):
                            createOpenFileInSystemAppButton(
                                btnClass=gr.Button,
                                value="📂 Add custom fields...",
                                tooltip="Add custom fields to the custom tracked components config",
                                elem_id="script_config_preset_open_custom_tracked_components_config",
                                file_path=self.custom_tracked_components_config_file_name
                            )
                        with gr.Column(scale=2):
                            pass
