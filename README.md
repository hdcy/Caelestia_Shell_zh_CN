# Caelestia Shell 简体中文汉化

将 [Caelestia Shell](https://github.com/caelestia-dots/caelestia) 界面从英文替换为简体中文。

**适配版本：caelestia-shell 2.2.0 / caelestia-cli 1.1.1 / Quickshell-git (latest)**

## 原理

脚本将源目录（`/etc/xdg/quickshell/caelestia`）复制到用户配置目录（`~/.config/quickshell/caelestia`），然后根据 `zh_CN.json` 翻译字典，直接将 QML 文件中的英文字符串替换为中文。Quickshell 会优先加载用户配置目录。

## 文件说明

| 文件 | 说明 |
|---|---|
| `zh_CN.json` | 翻译字典（687 条词条，98 个上下文） |
| `install_zh_CN.py` | Python 汉化脚本（含 9 个 LANG_PATCHES 自动汉化 + `--fix` 2 个 Bug 修复） |
| `TRANSLATION_GUIDE.md` | 翻译词条编写规则（维护者参考） |

## 执行流程

```
[1/2] 复制源文件 → [2/2] zh_CN.json 替换 → LANG_PATCHES (自动) → BUG_FIXES (--fix)
```

| 阶段 | 触发 | 内容 |
|------|------|------|
| zh_CN.json | 自动 | 687 条 qsTr 字符串替换 |
| LANG_PATCHES | 自动 | 运行时间单位 / 天气状态 / 锁屏日期 / 桌面时钟 / 锁定状态 / 电池时间 / 电池功率 汉化（9 条规则） |
| BUG_FIXES | `--fix` | 启动器 Super 键竞态 / Kitty 通知空按钮 修复（2 个修复，共 5 处替换） |

## 快速开始

### Linux 部署

```bash
cd Caelestia_Shell_zh_CN
python install_zh_CN.py
```

脚本会自动检测系统目录并汉化。完成后重启 Caelestia Shell 即可生效。

推荐用法：

```bash
python install_zh_CN.py --force --fix
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `source` (可选) | 源目录路径，默认 `/etc/xdg/quickshell/caelestia` |
| `target` (可选) | 输出目录，默认 `~/.config/quickshell/caelestia` |
| `--dry-run` | 预览模式：只报告将要修改的内容，不实际写入 |
| `--force` | 非交互模式：跳过确认提示，直接删除并重新复制 |
| `--fix` | 汉化后应用 Bug 修复补丁（启动器竞态 + 通知空按钮）。汉化补丁无需此参数，自动执行 |

### 预览模式

caelestia-shell 更新后，可以先预览哪些文件需要重新汉化：

```bash
python install_zh_CN.py --dry-run
```

### 指定源目录

```bash
python install_zh_CN.py /custom/path/to/caelestia
```

### 指定源目录和输出目录

```bash
python install_zh_CN.py /path/to/source /path/to/output
```

## 注意事项

### 在原有目录配置进行汉化

选择保留现有目录（`n`）时，请确保用户配置的目录结构和官方相同。注意：不会从源目录同步新增的 QML 文件，且已汉化的文本因英文原文已不存在，无法重新匹配。

### 重新复制会清空用户配置

选择重新复制（`y`，需二次确认）时，脚本会**删除整个目标目录后重新复制**。如果你在 `~/.config/quickshell/caelestia` 下有自定义配置，请提前备份。

### 不可重复执行

脚本是直接替换英文为中文。已汉化的目录中英文原文已不存在，再次运行会匹配不到任何内容。如需重新汉化（如更新翻译后），请选择重新复制（`y`），或使用 `--force` 跳过交互。

### 源文件不会被修改

脚本只修改输出目录（用户配置目录）中的副本，不会修改 `/etc/xdg/quickshell/caelestia` 下的源文件。

### 依赖

- **Python 3.6+**（Linux 通常预装）
- 无第三方库依赖，仅使用标准库

### 翻译覆盖范围

**98 个 QML 文件，687 条词条 + 2 个 BUG_FIXES（`--fix`）+ 9 个 LANG_PATCHES（自动）**，覆盖：

- 控制中心 / Nexus（网络、蓝牙、音频、外观、任务栏、通知、启动器、仪表盘、语言与地区、服务）
- 锁屏界面
- 顶栏弹出面板（电池、网络、蓝牙、托盘、键盘布局）
- 仪表盘（媒体、性能监控、天气）
- 文件对话框
- 通知、录屏、窗口信息、会话管理等

### 更新翻译后

修改 `zh_CN.json` 后重新运行脚本，选择重新复制即可。翻译字典的编写规则见 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)。

## 贡献翻译

欢迎补充和修正翻译。编辑 `zh_CN.json` 时请遵循 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) 中的规则，确保：

1. 上下文名与 QML 文件名一致
2. `_comment` 字段包含正确的文件路径
3. 英文原文与 QML 源码完全一致（包括空格、大小写、特殊字符）
4. 保留 `%1`、`%2` 等占位符不翻译

可用以下命令验证 JSON 格式：

```bash
python3 -m json.tool zh_CN.json > /dev/null && echo "JSON OK"
```
