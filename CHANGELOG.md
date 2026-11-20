# Change Log

All notable changes to this project will be documented in this file.
See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.

# 1.0.0 (2026-11-20)


### BREAKING CHANGES

* **ui:** 將預設配置 UI 邏輯拆分為偵測層與顯示層



### 🐛　Bug Fixes

* [#84](https://github.com/bluelovers/Config-Presets/issues/84) only saved item is checked ([8054584](https://github.com/bluelovers/Config-Presets/commit/80545847313d828f33aaf13ce7ad315b18f49f07))
* broken radio-button in v1.6 ([#62](https://github.com/bluelovers/Config-Presets/issues/62)) ([1f02069](https://github.com/bluelovers/Config-Presets/commit/1f020691cbc83a9203f91a193d870b4d2ee8485c))
* **config:** 調整預設配置保留選項的初始狀態 ([735a720](https://github.com/bluelovers/Config-Presets/commit/735a7206bcd3562092eef81782b1e00b83c9d49a))
* **config:** 修正枚举值使用并清理代码格式 ([5fa16db](https://github.com/bluelovers/Config-Presets/commit/5fa16db48ac15b4b8c40deb4822b762c442e8448))
* **core:** 引入派生元件機制以支援自動化欄位追蹤 ([f1ae56e](https://github.com/bluelovers/Config-Presets/commit/f1ae56e14519ea2f84d65743a967feb0e708634b))
* **ui:** 優化 X/Y/Z plot 預設值套用機制與安全性 ([d8ab9b8](https://github.com/bluelovers/Config-Presets/commit/d8ab9b8a6f5118d08df02ac2af96f697e0159b30))
* **ui:** 修正刪除預設值時的 UI 狀態與勾選邏輯 ([ba832f0](https://github.com/bluelovers/Config-Presets/commit/ba832f0a036011d78dd8661dea4c6e96235e3af7))
* **ui:** 修正 first_group_ids 的型別定義錯誤 ([5e09e24](https://github.com/bluelovers/Config-Presets/commit/5e09e249bddfd839c145d6d6892b466497be9bc8))
* **ui:** 防止保留名稱「None」被自動填充至預設名稱文字框 ([53ec5c4](https://github.com/bluelovers/Config-Presets/commit/53ec5c45edd2f7e29b5af13820864b0b696a5c93))


### ✨　Features

* add "Reapply" button ([#64](https://github.com/bluelovers/Config-Presets/issues/64)) ([b82ce63](https://github.com/bluelovers/Config-Presets/commit/b82ce634a27323edaa331743db6e6738a8f0487c))
* keep unset component value ([#23](https://github.com/bluelovers/Config-Presets/issues/23)) ([6ce6a28](https://github.com/bluelovers/Config-Presets/commit/6ce6a2865488a7f3e6485f0644bbacdcdff3391b))
* **config:** 新增 `--configpresets-dir` 參數以支援外部設定檔路徑 ([743f264](https://github.com/bluelovers/Config-Presets/commit/743f264f08d891c68538dbe271211a86fff725cd))
* **config:** 支援 X/Y/Z plot 多選下拉框的自動追蹤與儲存 ([481d39b](https://github.com/bluelovers/Config-Presets/commit/481d39bd01e49ef30e07a2f05c9512a6d87c0fce))
* **ui:** 支援透過 `##@` 語法在自訂追蹤元件設定檔中建立摺疊分組 ([0a96c06](https://github.com/bluelovers/Config-Presets/commit/0a96c068bdd8465e82c67ae55e57a165090ac7d5))


### 📦　Code Refactoring

* **compat:** 抽離 CSV 轉換邏輯並優化 X/Y/Z plot 數據同步 ([b088a73](https://github.com/bluelovers/Config-Presets/commit/b088a73371af513f8022a33d61999b5e6b640de3))
* **config:** 優化分組解析邏輯與移除冗餘程式碼 ([bfebfae](https://github.com/bluelovers/Config-Presets/commit/bfebfae03c2ee2680283b18041ded4d8d175e40b))
* **config:** 提取自訂追蹤元件預設標頭生成邏輯 ([455676b](https://github.com/bluelovers/Config-Presets/commit/455676bf74168fcc5ef79a94c7d08ada27ed1912))
* **config:** 模組化配置載入邏輯並解耦設定檔處理 ([d1b5d05](https://github.com/bluelovers/Config-Presets/commit/d1b5d05ddc803bf4580e453730008ad517168271))
* **config:** 優化保留預設名稱的判斷邏輯與管理機制 ([a8290b6](https://github.com/bluelovers/Config-Presets/commit/a8290b659ed3357385f5b347a4bd7fdb624ea106))
* **config:** 實作內建與自訂預設分離機制並新增 Settings 選項 ([56a5dfe](https://github.com/bluelovers/Config-Presets/commit/56a5dfedb540dcab2ce61e12b613c0ef084f6ee1))
* **config:** 添加类型提示并更新 pyright 配置 ([98b9290](https://github.com/bluelovers/Config-Presets/commit/98b929023ea3cbd830ec0e6f41a28dc56d52d0d8))
* **config:** 移动 dict_synonyms 函数并添加类型提示 ([93d8e1b](https://github.com/bluelovers/Config-Presets/commit/93d8e1b8ed2615fce9de09a1e49434b5fb87d053))
* **config:** 将文件打开功能提取到单独的工具模块 ([cbd81d7](https://github.com/bluelovers/Config-Presets/commit/cbd81d79a045815a8d2b0e96bdea030b5d4e17ec))
* **config:** 引入 type_name 变量以简化条件判断逻辑 ([f9e5059](https://github.com/bluelovers/Config-Presets/commit/f9e50595c9d5e55598eaec8459f5fc2be81d3635))
* **config:** 重构配置预设，将函数移至单独模块并添加类型提示 ([3e7807b](https://github.com/bluelovers/Config-Presets/commit/3e7807b24a6d5c6edd6a3397894c32f9c75ce9ca))
* **config:** 为 json_data 参数添加类型提示 ([ee1c158](https://github.com/bluelovers/Config-Presets/commit/ee1c158756cf2a12be8c3db1b5073cc474a30aef))
* **config:** 重构配置文件加载逻辑为通用函数 ([f873655](https://github.com/bluelovers/Config-Presets/commit/f8736555e7258a1b2a29e2b30983b27189889f2b))
* **config:** 替换打印语句为日志函数 ([e67e55b](https://github.com/bluelovers/Config-Presets/commit/e67e55b13d5923ff5e9f82dc8a4962347f6e17d0))
* **config:** 使用变量替换硬编码的类型名称 ([6c5d5dd](https://github.com/bluelovers/Config-Presets/commit/6c5d5dd373cbf9dd55af4c0b724ef21d20d76459))
* **config:** 重构配置组件加载逻辑 ([3b6c38a](https://github.com/bluelovers/Config-Presets/commit/3b6c38a9ef3319ff486f47f6b457f7ac8ab824b0))
* **core:** 隔離派生元件與追蹤清單以優化儲存機制 ([5cb2578](https://github.com/bluelovers/Config-Presets/commit/5cb25782815919799416e14edf4a31cff4f15a91))
* **pyright:** 移除 pyright 忽略注释并更新配置 ([96e9318](https://github.com/bluelovers/Config-Presets/commit/96e93189d51d9b89d3976f4bcb29299e444c40ca))
* **ui:** 調整編輯介面展開時的按鈕顯示邏輯 ([674155a](https://github.com/bluelovers/Config-Presets/commit/674155adff3aac50bdd07da83b14b9fae332643a))
* **ui:** 優化「Fields to save」區塊的渲染邏輯與分組判斷 ([a36b226](https://github.com/bluelovers/Config-Presets/commit/a36b226a91331440c1bd76daa56b83959d0d8399))
* **ui:** 優化追蹤元件分組解析邏輯與 UI 呈現方式 ([bd6d2bf](https://github.com/bluelovers/Config-Presets/commit/bd6d2bf4bd115c9d72d209f663849cc4fd4ab925))
* **ui:** 將預設配置 UI 邏輯拆分為偵測層與顯示層 ([4c33078](https://github.com/bluelovers/Config-Presets/commit/4c330788b0acd7e7352763fbb485c27230725cd3))
* **ui:** 優化配置預設值介面之互動邏輯與狀態同步 ([f42c027](https://github.com/bluelovers/Config-Presets/commit/f42c0274c08ba23189f41b0095e8c8cf657b6d07))
* **ui:** 提取文件打开按钮创建为可重用函数 ([3edf0cc](https://github.com/bluelovers/Config-Presets/commit/3edf0ccae501e1ca1f1549dfd9c59154b7a4ee81))


### 📚　Documentation

* 更新 README.md 以說明專案來源與支援的 Forge 版本 ([3329a43](https://github.com/bluelovers/Config-Presets/commit/3329a43ed2f9a0e1ec5848b69ee31abafaf49199))
* **config:** 为配置预设模块添加详细中文注释和文档字符串 ([4b7da1f](https://github.com/bluelovers/Config-Presets/commit/4b7da1f280202b40e5a5adb1668e283469fac629))
* **ui:** 更新關於「Fields to save」分組邏輯的術語定義與文件說明 ([cea9338](https://github.com/bluelovers/Config-Presets/commit/cea93389554ff5c6435370e4557ef8ad660b82af))


### 💎　Styles

* **config:** 修复配置文件缩进格式问题 ([719beef](https://github.com/bluelovers/Config-Presets/commit/719beeff4e4d655e87284c45452fb8f229ef508d))
* **ui:** 將設定檔欄位分組預設改為展開狀態 ([c04651d](https://github.com/bluelovers/Config-Presets/commit/c04651d6e778eac68ea5c8def5bb48e79ad775d4))


### 🛠　Build System

* 新增 package.json 以建立專案管理基礎 ([55f274f](https://github.com/bluelovers/Config-Presets/commit/55f274f74733afbe13a8471957388f2911dc5a5c))


### ♻️　Chores

* **gitignore:** 添加.*和__pycache__到忽略文件 ([18b7ec4](https://github.com/bluelovers/Config-Presets/commit/18b7ec4ee45820ea3cb9ded33b1fb97cb6863c6b))


### 🔖　Miscellaneous

* . ([7a1aab7](https://github.com/bluelovers/Config-Presets/commit/7a1aab79a371c5be10a8165c02f9cd61999b3360))
* added IDs for img2img soft inpainting ([b154e2d](https://github.com/bluelovers/Config-Presets/commit/b154e2d7d5edb21735278c13dced6696f5b7a0f4)), closes [#90](https://github.com/bluelovers/Config-Presets/issues/90)
* Forge control_step_slider ([9295577](https://github.com/bluelovers/Config-Presets/commit/92955772d5576d3c12051744e20fa2ec7fd20393)), closes [#91](https://github.com/bluelovers/Config-Presets/issues/91)
* Update config_presets.py ([c315d2e](https://github.com/bluelovers/Config-Presets/commit/c315d2e9aab560b85a8f26a237d14c6c39e220cb)), closes [#txt2](https://github.com/bluelovers/Config-Presets/issues/txt2) [#93](https://github.com/bluelovers/Config-Presets/issues/93)
* Update README.md ([02a834a](https://github.com/bluelovers/Config-Presets/commit/02a834a33c435271ac9255847953a69de8a74a6b))
* additions for Forge's Flux model support ([014daac](https://github.com/bluelovers/Config-Presets/commit/014daacab85c84c39b27d4ac40bd401ce2d0c882))
* Update README.md ([96e9f77](https://github.com/bluelovers/Config-Presets/commit/96e9f774ff386ad25253b8da05bc0e5be352dce7))
* ADetailer hidden enabled checkbox ([2d7c381](https://github.com/bluelovers/Config-Presets/commit/2d7c381dab18966fd68a1b41ddb4bedf9d8b68f0)), closes [#86](https://github.com/bluelovers/Config-Presets/issues/86)
* fix for ADetailer's update ([6254faa](https://github.com/bluelovers/Config-Presets/commit/6254faa81a598ffb856a921a428d60690716c537)), closes [#86](https://github.com/bluelovers/Config-Presets/issues/86)
* Update config_presets.py ([19ca616](https://github.com/bluelovers/Config-Presets/commit/19ca61676b96fd04d38be6617fb80c8e3f508375)), closes [#81](https://github.com/bluelovers/Config-Presets/issues/81)
* Update README.md ([1351554](https://github.com/bluelovers/Config-Presets/commit/1351554778253087d76fb3a768a0dffa3579e166))
* fixed backwards compatibility issue ([268da43](https://github.com/bluelovers/Config-Presets/commit/268da434ef2831f56dd5dafc27a79911cc3b3791)), closes [#80](https://github.com/bluelovers/Config-Presets/issues/80)
* Update README.md ([56e7bd9](https://github.com/bluelovers/Config-Presets/commit/56e7bd99dbdac09c097e1a7825c5ca6f9f50e38f))
* A1111 1.9.0 update ([54904a8](https://github.com/bluelovers/Config-Presets/commit/54904a8f8858d92d56990e35efefa17cb4d06241))
* add synonyms for multidiffusion upscaler ([99a8476](https://github.com/bluelovers/Config-Presets/commit/99a8476c37cb512c6f51e124e0a9a0223bf57962)), closes [#78](https://github.com/bluelovers/Config-Presets/issues/78)
* Update README.md ([ca6e888](https://github.com/bluelovers/Config-Presets/commit/ca6e8888c9f84c25150ce3b3454fbdaaa680603a))
* improved config file error handling ([58d6cc3](https://github.com/bluelovers/Config-Presets/commit/58d6cc32341530ac0483c031c6c124ae0ec72ebb))
* Update README.md ([4578200](https://github.com/bluelovers/Config-Presets/commit/45782006d4e7f211656d7168cff37f1bb997b834))
* smaller buttons, added refresh button, updated presets ([6675175](https://github.com/bluelovers/Config-Presets/commit/6675175d4ed90c7af942cd30050124ad8569fd69))
* Update README.md ([48cd226](https://github.com/bluelovers/Config-Presets/commit/48cd226ad99fbd4cf365669c1c38d2e9d912fc48))
* Update README.md ([d6b5432](https://github.com/bluelovers/Config-Presets/commit/d6b54327dbe8e65963cb00d9307d26e95c534f88))
* fix for "Use same sampler" sampler dropdown value ([ab2ff57](https://github.com/bluelovers/Config-Presets/commit/ab2ff579d60b9a1c58839a67dbc0ea6586abce19)), closes [#75](https://github.com/bluelovers/Config-Presets/issues/75)
* Update README.md ([165bc50](https://github.com/bluelovers/Config-Presets/commit/165bc505f0e0e1324f09dd0535c1ee822f4a4c61))
* fix save preset bug, JSON checks ([f7d5a7a](https://github.com/bluelovers/Config-Presets/commit/f7d5a7a9a83dba925bf2da32b00f0a5fe86731b2)), closes [#63](https://github.com/bluelovers/Config-Presets/issues/63) [#70](https://github.com/bluelovers/Config-Presets/issues/70)
* multidiffusion-upscaler (Tiled Diffusion, Tiled VAE) changed IDs ([0ff35ea](https://github.com/bluelovers/Config-Presets/commit/0ff35ea638b7e00fcb65672984b3f4b5489ea8b8)), closes [#69](https://github.com/bluelovers/Config-Presets/issues/69)
* ADetailer extension changed IDs _2nd ([74d21ba](https://github.com/bluelovers/Config-Presets/commit/74d21bae6275abce7e9f2b8c1e5d6911caeaeeda))
* ADetailer extension changed IDs ([d3ecee6](https://github.com/bluelovers/Config-Presets/commit/d3ecee690ce61e4e5312493d3a9bb80d08abc06d))
* Update README.md ([6b1bc20](https://github.com/bluelovers/Config-Presets/commit/6b1bc209bb0a19ee8dad0c81f44b1186f19c4035))
* added Ultimate SD Upscale IDs #51 ([305c23a](https://github.com/bluelovers/Config-Presets/commit/305c23a0475ce9a898618ac9b611af5ba7ad4992)), closes [#51](https://github.com/bluelovers/Config-Presets/issues/51)
* Update README.md ([87dd00d](https://github.com/bluelovers/Config-Presets/commit/87dd00d336bbca60df9454a9418738994535efd2))
* Update README.md ([9e6c4d8](https://github.com/bluelovers/Config-Presets/commit/9e6c4d8d40946450eee68f4431af408fb448bb57))
* Update README.md ([69ae22e](https://github.com/bluelovers/Config-Presets/commit/69ae22e20b4da2343ca23878dd9c6458a0bbdf30))
* fixes for A1111 1.6.0 ([f4677f7](https://github.com/bluelovers/Config-Presets/commit/f4677f7f0e51992e2ac3b487db313164feea0449)), closes [#56](https://github.com/bluelovers/Config-Presets/issues/56) [#58](https://github.com/bluelovers/Config-Presets/issues/58)
* fix typo `txt2txt` -> `txt2img` (#57) ([08aaf66](https://github.com/bluelovers/Config-Presets/commit/08aaf664f628bb6bdbf3ec4211fbd736d4a8821c)), closes [#57](https://github.com/bluelovers/Config-Presets/issues/57)
* Optional components. ([#55](https://github.com/bluelovers/Config-Presets/issues/55)) ([d3e2353](https://github.com/bluelovers/Config-Presets/commit/d3e23532d452b7aa4ef98fec35ac247b0aa155cc))
* edited default presets ([0f0f25c](https://github.com/bluelovers/Config-Presets/commit/0f0f25c37e5049cb01d71b823127a80a1c41cb90))
* Updates to automatically generated config text files. (#48) ([6fee8ff](https://github.com/bluelovers/Config-Presets/commit/6fee8ff706faddfe6dc70bff3e285e4223dd4d7b)), closes [#48](https://github.com/bluelovers/Config-Presets/issues/48)
* added hires prompt to default config file ([f99171b](https://github.com/bluelovers/Config-Presets/commit/f99171bf89a7d08e514d5491f579110df2eeb97d))
* Update README.md ([405c4d3](https://github.com/bluelovers/Config-Presets/commit/405c4d3ecd554f4b26a61d73d7ce18074b505505))
* added ADetailer IDs to custom component config ([72df7d7](https://github.com/bluelovers/Config-Presets/commit/72df7d7a3dfc542c6dbaed4a2bbe4ea546cd9eb1))
* Auto fix bad ControlNet component ID ([f91c65b](https://github.com/bluelovers/Config-Presets/commit/f91c65b54d2781735252290d8befdf530d80dd85)), closes [#45](https://github.com/bluelovers/Config-Presets/issues/45)
* auto populate new config preset name, add new IDs to default config ([1c4f88d](https://github.com/bluelovers/Config-Presets/commit/1c4f88d706edff3efe365836fd0edbbd65a2243b))
* Update README.md ([5e3cc9d](https://github.com/bluelovers/Config-Presets/commit/5e3cc9d3a5210e5d35a9d65c17122fec7e2f5b8f))
* Update README.md ([6256e17](https://github.com/bluelovers/Config-Presets/commit/6256e1704e743aa24e52dac01142f93df220879e))
* Update README.md ([b222f9a](https://github.com/bluelovers/Config-Presets/commit/b222f9ad36c4a63a5789f9e1eb3c08a5bb26d5e9))
* Update README.md ([cf2f82e](https://github.com/bluelovers/Config-Presets/commit/cf2f82eae6274fc8d429e0ae6115ddfd465d03ae))
* added ControlNet component IDs to default tracked components config file ([314036f](https://github.com/bluelovers/Config-Presets/commit/314036f333abebe289ad023135e917fb0f6606a7))
* update delete button icon ([b433fb4](https://github.com/bluelovers/Config-Presets/commit/b433fb49bc973ddcdf8e0269de37a4a95c27ef13))
* Update README.md ([4fddb6d](https://github.com/bluelovers/Config-Presets/commit/4fddb6d0cbd8d5be7c39e2472aa4cc1516764672))
* add img2img_scale to default config file ([5584055](https://github.com/bluelovers/Config-Presets/commit/55840552554b8024e1fe24d0b69e2e2bf6a54711))
* Preset auto refresh. (#41) ([5f9af27](https://github.com/bluelovers/Config-Presets/commit/5f9af2777a7c041560777c141fc52a46c6baeab1)), closes [#41](https://github.com/bluelovers/Config-Presets/issues/41)
* Update README.md ([1683ad6](https://github.com/bluelovers/Config-Presets/commit/1683ad6e6489096322fab759b2525899759b7129))
* Update README.md ([b655bf1](https://github.com/bluelovers/Config-Presets/commit/b655bf141c24ace808a147126e28954c0b9d5e3c))
* update config file instructions ([fe22565](https://github.com/bluelovers/Config-Presets/commit/fe22565b78b73b872f367294f14f02074e016360))
* Update README.md ([851add5](https://github.com/bluelovers/Config-Presets/commit/851add5fe2b922a6447983d39793fc048549aac4))
* Update README.md ([84fe880](https://github.com/bluelovers/Config-Presets/commit/84fe880363707860758751dee5c67f4868d9f0ff))
* Added custom field tracking ([fe3176c](https://github.com/bluelovers/Config-Presets/commit/fe3176c77fdb4ee50ff0c03f668fc16c5ce1589a)), closes [#28](https://github.com/bluelovers/Config-Presets/issues/28) [#31](https://github.com/bluelovers/Config-Presets/issues/31) [#32](https://github.com/bluelovers/Config-Presets/issues/32) [#33](https://github.com/bluelovers/Config-Presets/issues/33) [#34](https://github.com/bluelovers/Config-Presets/issues/34)
* tweak default presets ([5c8a867](https://github.com/bluelovers/Config-Presets/commit/5c8a867c99c153947cbda71b0dd16fb7b8b8b92a))
* renamed the "Default" preset to "None" which doesn't do anything ([6a1aa7b](https://github.com/bluelovers/Config-Presets/commit/6a1aa7b027817c5e5551605ec4be47fd351d17e4))
* tweaked default presets for large resolutions ([b0052a9](https://github.com/bluelovers/Config-Presets/commit/b0052a999f7d4fe868fc9daa2b8e350dd25bef92))
* added icons to some buttons ([854ca2f](https://github.com/bluelovers/Config-Presets/commit/854ca2ff04d07266178cc5166a6239499e776fe2))
* Update README.md ([1b952e2](https://github.com/bluelovers/Config-Presets/commit/1b952e263563605cd9d3d66c5fc02ada4a245ad6))
* Update README.md ([abe250a](https://github.com/bluelovers/Config-Presets/commit/abe250ad3898a4d4803bdaf04709275712265c6b))
* default value tweaks ([54080bf](https://github.com/bluelovers/Config-Presets/commit/54080bfe7300660ed54560d413eafcb517ac3105))
* fix bad comment ([d4e4a10](https://github.com/bluelovers/Config-Presets/commit/d4e4a108a7d6bf31853749d8693cb9356d4051d7))
* remove duplicate "txt2img_hr_scale" ([bd09d4f](https://github.com/bluelovers/Config-Presets/commit/bd09d4f39899717e1756129b7041a9c2e6fe8b21))
* Update README.md ([cba40c9](https://github.com/bluelovers/Config-Presets/commit/cba40c9706539521d256a1db4325c1be08a10633))
* Added ability to ignore fields, preset default tweaks ([eb366cc](https://github.com/bluelovers/Config-Presets/commit/eb366cc9cb56c578f978cbe52c645cd0f75746b6)), closes [#27](https://github.com/bluelovers/Config-Presets/issues/27) [#6](https://github.com/bluelovers/Config-Presets/issues/6)
* Update .gitignore ([d1c8d6f](https://github.com/bluelovers/Config-Presets/commit/d1c8d6f4cbef15c034a677db5626551012fd437b))
* Update README.md ([89abe60](https://github.com/bluelovers/Config-Presets/commit/89abe60897641fb8a957ca0cb72ab3b44331f415))
* Update README.md ([f852f8d](https://github.com/bluelovers/Config-Presets/commit/f852f8df5b36b945a1fdf9d69043a0f31a6cbd41))
* Update README.md ([8928e49](https://github.com/bluelovers/Config-Presets/commit/8928e49330dea3abbcaaf7c93c95e1d6b4d460d1))
* Added style.css ([c4cab05](https://github.com/bluelovers/Config-Presets/commit/c4cab058e1947858eb97149c6ea01ac54821b281)), closes [#22](https://github.com/bluelovers/Config-Presets/issues/22)
* Added 768x768, 1080p, 1440p, and 4k presets ([fcb2d57](https://github.com/bluelovers/Config-Presets/commit/fcb2d5740854d784c626e2255f5a683e62c8f040))
* Update README.md ([eb3abef](https://github.com/bluelovers/Config-Presets/commit/eb3abef5601cbda9679e42c8e9f002672f6c5254))
* fix sampler not being saved for new presets ([63ef7b0](https://github.com/bluelovers/Config-Presets/commit/63ef7b09fbb41af56211e2fb0f514f7f38ebf275))
* Update README.md ([850fe07](https://github.com/bluelovers/Config-Presets/commit/850fe07d55b80d471130370c8ab50a5e9a9a48d2))
* Update README.md ([c8c42cf](https://github.com/bluelovers/Config-Presets/commit/c8c42cf6873a7197b2b56f4835454e1727a7859b))
* Update README.md ([fb94c8d](https://github.com/bluelovers/Config-Presets/commit/fb94c8d59437cca9022e7d3dd87586ec44b08350))
* massive backend updates ([98a922a](https://github.com/bluelovers/Config-Presets/commit/98a922ac5ccb59d653accdcc58997beb31bcd72c)), closes [#16](https://github.com/bluelovers/Config-Presets/issues/16)
* Update README.md ([ae73d03](https://github.com/bluelovers/Config-Presets/commit/ae73d038df048660fe914706f9a7c33c70c93468))
* Update README.md ([bca4772](https://github.com/bluelovers/Config-Presets/commit/bca4772b6a791577e6ac186e593393f86142945a))
* Update README.md ([7bb06a7](https://github.com/bluelovers/Config-Presets/commit/7bb06a7620478452dd62b3a87f0ac0f986dd3b6c))
* Update README.md ([7986826](https://github.com/bluelovers/Config-Presets/commit/7986826a36792e52830f6a1b0f3e0230e02bbdb5))
* Update README.md ([8230dcb](https://github.com/bluelovers/Config-Presets/commit/8230dcb72f9ab56d6ff0e5db0a8ceaa28c39a6d9))
* Update README.md ([da63276](https://github.com/bluelovers/Config-Presets/commit/da63276b4bb290b930fa8a35ed0d9430ecc35e14))
* Update README.md ([c41d634](https://github.com/bluelovers/Config-Presets/commit/c41d6344eee81b8aa15232de9bfc2e19189de304))
* final touches ([aa58d65](https://github.com/bluelovers/Config-Presets/commit/aa58d6579a5886913300bd722739b660f31199e1))
* Update README.md ([baa36af](https://github.com/bluelovers/Config-Presets/commit/baa36af7632292027b5fff2b68db449798c168a5))
* img2img tab support ([c84d4b6](https://github.com/bluelovers/Config-Presets/commit/c84d4b61a083f40f3e104021dbdc9c1b3d7d04e7))
* Added save/delete functionality in the UI for config presets ([6d6c466](https://github.com/bluelovers/Config-Presets/commit/6d6c4660718291cd21a95becc09dea94f98f9db9))
* Update README.md ([4503743](https://github.com/bluelovers/Config-Presets/commit/4503743faf4023a000343af85a6091218e6ff466))
* Update README.md ([5883ffa](https://github.com/bluelovers/Config-Presets/commit/5883ffa296e814a5e871f1efc8d79cfd4b9edba8))
* Update README.md ([2ac60d4](https://github.com/bluelovers/Config-Presets/commit/2ac60d43f94cf784414212694d8b191c0001fc9b))
* Update README.md ([a6c9149](https://github.com/bluelovers/Config-Presets/commit/a6c9149bd44f6bca22a9f0f605f9074730a455f8))
* Removed config.json ([721e612](https://github.com/bluelovers/Config-Presets/commit/721e6129b06a9ec372cf6e8fb9e199e329e522ab))
* Create config.json on first load ([24639a5](https://github.com/bluelovers/Config-Presets/commit/24639a5c7cf87eeb4ac9b61e4df6e093fafb5720))
* Update README.md ([d675098](https://github.com/bluelovers/Config-Presets/commit/d6750987ab80147750ab4c386f2a960b18f3a13a))
* Update README.md ([797c4bd](https://github.com/bluelovers/Config-Presets/commit/797c4bd928a25b7fbbcc180181e9db38a872e7ff))
* Update README.md ([5036218](https://github.com/bluelovers/Config-Presets/commit/5036218ac27f67777a1581084f151a95218ea143))
* use / instead of \ for config file path ([24801fc](https://github.com/bluelovers/Config-Presets/commit/24801fc3f1ce6ad15333b7bb473e6d1be915bda6)), closes [#7](https://github.com/bluelovers/Config-Presets/issues/7)
* Update README.md ([3208f3e](https://github.com/bluelovers/Config-Presets/commit/3208f3eccd50f67fd59d1bd087efecf6555f6dea))
* Added Firstpass width/height ([1992e1e](https://github.com/bluelovers/Config-Presets/commit/1992e1eed76bda3de93719faf8d82c7c5ac9afa1))
* Update README.md ([0fe5fc5](https://github.com/bluelovers/Config-Presets/commit/0fe5fc5383a272d2819cf1bdbba2ea4885eef78c))
* edited gerschel's pr ([30f96f8](https://github.com/bluelovers/Config-Presets/commit/30f96f8c52a62d2d3df800d2178336478de3b4ad))
* Fixed missing back slash, brought others to parity ([624f16e](https://github.com/bluelovers/Config-Presets/commit/624f16e8d1c081a0a38fb2462a017811cd3c9b33))
* Refactor, made it work with img2img ([318de88](https://github.com/bluelovers/Config-Presets/commit/318de88d009264cde3b3e88ef4da6923cc620e82))
* Update README.md ([258c347](https://github.com/bluelovers/Config-Presets/commit/258c347a0c968c28ded80e39d0e42ec4cf10ab19))
* Update README.md ([d9e56da](https://github.com/bluelovers/Config-Presets/commit/d9e56da0458f4ea9df0019062fa78069b29b01dd))
* Update README.md ([e0845cd](https://github.com/bluelovers/Config-Presets/commit/e0845cd6b9daf875ffa565ccedab18249d007b22))
* Initial commit ([8c90a92](https://github.com/bluelovers/Config-Presets/commit/8c90a927c08edbe30db1d252629fcfadbee4be12))
