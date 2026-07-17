# Caelestia Shell 简体中文汉化

将 [Caelestia Shell](https://github.com/caelestia-dots/caelestia) 界面从英文替换为简体中文。

**适配版本：caelestia-shell 2.2.0 / caelestia-cli 1.1.1**

## 原理

脚本从 `/etc/xdg/quickshell/caelestia` 复制 QML 文件到 `~/.config/quickshell/caelestia`，根据 `zh_CN.json` 翻译字典直接替换英文字符串。Quickshell 优先加载用户配置目录。

## 文件说明

| 文件 | 说明 |
|---|---|
| `zh_CN.json` | 翻译字典（687 条词条，98 个上下文） |
| `install_zh_CN.py` | 汉化脚本（9 个 LANG_PATCHES + `--fix` 2 个 Bug 修复） |
| `TRANSLATION_GUIDE.md` | 翻译词条编写规则 |

## 执行流程

```
[1/2] 复制源文件 → [2/2] zh_CN.json 替换 → LANG_PATCHES → BUG_FIXES (--fix)
```

| 阶段 | 触发 | 内容 |
|------|------|------|
| zh_CN.json | 自动 | 687 条 qsTr 字符串替换 |
| LANG_PATCHES | 自动 | 运行时间 / 天气 / 锁屏日期 / 桌面时钟 / 锁键状态 / 电池时间 汉化（9 条） |
| BUG_FIXES | `--fix` | 启动器 Super 键竞态 / Kitty 通知空按钮（2 个修复，5 处替换） |

## 快速开始

```bash
cd Caelestia_Shell_zh_CN
python install_zh_CN.py --force --fix
```

caelestia-shell 更新后重新执行即可。

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--dry-run` | 预览模式，只报告不写入 |
| `--force` | 跳过确认，直接删除并重新复制 |
| `--fix` | 应用 Bug 修复补丁 |

## 覆盖范围

**98 个 QML 文件，687 条词条**，覆盖：

- 控制中心（网络、蓝牙、音频、外观、任务栏、通知、启动器、仪表盘、语言、服务）
- 锁屏界面
- 顶栏弹出面板（电池、网络、蓝牙、托盘、键盘布局）
- 仪表盘（媒体、性能监控、天气）
- 文件对话框、通知、录屏、窗口信息、会话管理

## 注意事项

- 重新执行需用 `--force`，否则已汉化的文本无法再次匹配
- 源文件（`/etc/xdg/`）不会被修改
- 依赖 Python 3.6+，无第三方库

翻译词条修改参考 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)。
