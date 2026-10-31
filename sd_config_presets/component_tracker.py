"""
元件偵測層 (Component Detection Layer)

追蹤 WebUI 依序建立的 Gradio 元件：比對追蹤清單後將元件收進 component_map、
以前一個元件為錨點自動捕獲 X/Y/Z plot 的 values 多選下拉框，
並在觸發元件出現時解析出 UI 顯示層所需的乾淨資料。

本層只依賴元件物件的屬性 (elem_id / multiselect / label / type)，
不建立任何 Gradio 元件；UI 建構由顯示層 (preset_ui.py) 負責。
"""

from dataclasses import dataclass
from typing import Any

from sd_config_presets.config_components import EnumTypeName, log_error  # pyright: ignore[reportMissingImports]


# 觸發建立 Config Presets UI 的元件：txt2img/img2img 圖庫最底部的 generation info 按鈕
# (very bottom of the txt2img/img2img image gallery)
TRIGGER_COMPONENT_IDS: tuple[str, ...] = ("txt2img_generation_info_button", "img2img_generation_info_button")

# X/Y/Z plot 配對下拉框的 ID 後綴 (companion dropdown suffix)
XYZ_VALUES_DROPDOWN_SUFFIX: str = "_dropdown"


def is_xyz_values_textbox_id(component_id: str) -> bool:
    """
    判斷是否為 X/Y/Z plot 的 values 文字框 ID（*_xyz_plot_*_values）。

    此類元件的下一個 multiselect 會被自動捕獲為其配對下拉框。
    """
    return component_id.endswith("_values") and "_xyz_plot_" in component_id


def xyz_values_dropdown_id(base_id: str) -> str:
    """
    由 X/Y/Z plot values 文字框 ID 建立其配對多選下拉框 ID。
    """
    return f"{base_id}{XYZ_VALUES_DROPDOWN_SUFFIX}"


@dataclass(frozen=True)
class ResolvedComponents:
    """
    偵測層解析結果：已剔除缺失可選元件的映射與追蹤清單。

    Args:
        component_map: 元件 ID → Gradio 元件；必備元件缺失時不會產出此結果
        component_ids: 實際追蹤到的元件 ID 順序清單，驅動 UI 輸入/輸出順序
        index_type_components: 型別為 "index" 的元件 ID，載入預設時需轉換為實際值
        derived_component_owner_ids: 派生元件表 {派生 ID: 擁有者 ID}；
                                     派生 ID 由機制自動建立、從屬於擁有者，
                                     不是獨立的設定欄位（顯示層不顯示、儲存隨擁有者）
    """

    component_map: dict[str, Any]
    component_ids: list[str]
    index_type_components: list[str]
    derived_component_owner_ids: dict[str, str]


class ComponentTracker:
    """
    單一 tab (txt2img 或 img2img) 的元件偵測器。

    WebUI 每建立一個元件即呼叫 register_component() 登記：
    元件 ID 在追蹤清單中即收進 component_map；
    當觸發元件 (generation info 按鈕) 出現時回傳 True，
    呼叫端再以 resolve() 取得 UI 顯示層所需資料。
    """

    def __init__(
        self,
        type_name: EnumTypeName,
        component_ids: list[str],
        optional_ids: list[str],
        synonym_ids: list[tuple[str, str]],
        custom_tracked_components_config_file_name: str,
    ):
        """
        Args:
            type_name: tab 類型 (txt2img 或 img2img)
            component_ids: 要追蹤的元件 ID 清單（含自訂追蹤元件），由呼叫端組出並共享引用
            optional_ids: 缺失時不致錯的可選元件 ID 清單
            synonym_ids: 載入預設時可互換的同義詞 ID 對照
            custom_tracked_components_config_file_name: 自訂追蹤元件設定檔路徑，僅用於錯誤提示
        """
        self.type_name = type_name
        self.component_ids: list[str] = component_ids
        self.optional_ids: list[str] = optional_ids
        self.synonym_ids: list[tuple[str, str]] = synonym_ids
        self.custom_tracked_components_config_file_name = custom_tracked_components_config_file_name

        # Mapping between component labels and the actual components in ui.py
        # 組件標籤與 ui.py 中實際組件之間的映射，於 register_component() 依序填入
        self.component_map: dict[str, Any] = {k: None for k in self.component_ids}

        # 派生元件表 {派生 ID: 擁有者 ID}：機制自動建立、從屬於擁有者的追蹤 ID。
        # 不是獨立的設定欄位，由顯示層與儲存層查表區分（未來機制一律經 track_derived_component 登錄）
        self.derived_component_owner_ids: dict[str, str] = {}

        # X/Y/Z plot 的 values 多選下拉框 (multiselect dropdown) 沒有 elem_id，無法以 ID 追蹤；
        # 以前一個建立的 "*_values" textbox 為錨點自動捕獲
        self._pending_xyz_dropdown_base_id: str | None = None
        self._pending_xyz_dropdown_label: str | None = None

    def track_derived_component(self, component: Any, derived_id: str, owner_id: str):
        """
        登記派生元件：自動建立、僅供機制內部取值使用，不作為獨立設定欄位。

        派生 ID 納入 component_map / component_ids 正常追蹤（作為事件輸入），
        同時登錄派生表；顯示層不將其渲染為可勾選欄位，
        儲存層使其隨擁有者一併進出預設。未來的自動捕獲機制（不只 X/Y/Z plot）
        都應經由此表登錄，避免與獨立設定值混淆。

        Args:
            component: WebUI 剛建立的 Gradio 元件
            derived_id: 派生 ID（如 script_*_values_dropdown）
            owner_id: 擁有者元件 ID，派生欄位從屬於它
        """
        self.component_map[derived_id] = component     # 重建 UI 時覆蓋為新元件
        if derived_id not in self.component_ids:
            self.component_ids.append(derived_id)      # 自動納入追蹤，無需使用者設定
        self.derived_component_owner_ids[derived_id] = owner_id

    def is_trigger_component(self, component: Any) -> bool:
        """
        判斷元件是否為觸發建立 Config Presets UI 的 generation info 按鈕。
        """
        return component.elem_id in TRIGGER_COMPONENT_IDS

    def register_component(self, component: Any) -> bool:
        """
        偵測並登記單一元件。

        Args:
            component: WebUI 剛建立的 Gradio 元件

        Returns:
            bool: 是否為觸發建立 Config Presets UI 的元件
        """
        # X/Y/Z plot 的 values 多選下拉框緊鄰在其 "*_values" textbox 之後建立（見 xyz_grid.py）；
        # 以前一個元件為錨點捕獲，並以 multiselect 與 label 特徵驗證，驗證失敗即放棄（維持原有行為）
        if self._pending_xyz_dropdown_base_id is not None:
            if getattr(component, "multiselect", False) is True and getattr(component, "label", None) == self._pending_xyz_dropdown_label:
                # 配對下拉框是派生欄位：隨其 "*_values" 文字框，不作為獨立設定值顯示
                self.track_derived_component(
                    component,
                    derived_id=xyz_values_dropdown_id(self._pending_xyz_dropdown_base_id),
                    owner_id=self._pending_xyz_dropdown_base_id,
                )
            self._pending_xyz_dropdown_base_id = None
            self._pending_xyz_dropdown_label = None

        #if component.label in self.component_map:
        if component.elem_id in self.component_map:
            self.component_map[component.elem_id] = component
            #log_debug(f"found component: {component.elem_id} {component}")
            if is_xyz_values_textbox_id(component.elem_id):
                # 下一個建立的元件即為其多選下拉框，先記下錨點
                self._pending_xyz_dropdown_base_id = component.elem_id
                self._pending_xyz_dropdown_label = getattr(component, "label", None)

        return self.is_trigger_component(component)

    def resolve(self) -> ResolvedComponents | None:
        """
        解析追蹤結果供 UI 顯示層使用。

        建立 UI 前先檢查每個元件是否成功取得，避免缺件導致 WebUI 崩潰：
        1. 剔除 optional_ids 中缺失 (None) 的可選元件
        2. 必備元件缺失時記錄錯誤並回傳 None（UI 不建立）

        Returns:
            ResolvedComponents | None: 解析結果；必備元件缺失時為 None
        """
        # Cleanse missing optional components with optional_ids
        # 剔除缺失的可選元件
        component_map: dict[str, Any] = {k: v for k, v in self.component_map.items() if v is not None or k not in self.optional_ids}
        component_ids: list[str] = [k for k in self.component_ids if k in component_map]

        # protect against None type components to prevent bricking the UI
        # this check needs to happen after optional_ids are accounted for
        # 防止None类型组件导致UI崩溃
        # 此检查需要在考虑optional_ids后进行
        for component_name, component in component_map.items():
            if component is None:
                log_error(f"The {self.type_name.value} component '{component_name}' could not be processed. This may be because you are running an outdated version of the Config-Presets extension, you included a component ID in the custom tracked components config file that does not exist, it no longer exists (if you updated an extension or Automatic1111), or is an invalid component (if this is the case, you need to manually edit the config file at {self.custom_tracked_components_config_file_name} or just delete it so it resets to defaults). This extension will not work until this issue is resolved.")
                return None

        # Mark components with type "index" to be transformed
        # 标记类型为"index"的组件以进行转换
        index_type_components: list[str] = [
            component.elem_id
            for component in component_map.values()
            if getattr(component, "type", "No type attr") == "index"
        ]

        return ResolvedComponents(
            component_map=component_map,
            component_ids=component_ids,
            index_type_components=index_type_components,
            derived_component_owner_ids=dict(self.derived_component_owner_ids),
        )
