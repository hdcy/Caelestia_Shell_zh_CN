#!/usr/bin/env python3
"""
Caelestia Shell 汉化脚本 (直接替换模式)
用法:
  python install_zh_CN.py                              # Linux 自动检测
  python install_zh_CN.py /path/to/caelestia           # 指定源目录
  python install_zh_CN.py . ./test_output              # 指定源+输出 (Windows 测试)
"""

import argparse, json, os, sys, shutil, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "zh_CN.json")
PROJECT_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
LINUX_SOURCE = "/etc/xdg/quickshell/caelestia"
LINUX_TARGET = os.path.expanduser("~/.config/quickshell/caelestia")

# 支持的属性列表（包括 name）
SUPPORTED_PROPS = [
    "label", "description", "text", "title",
    "summary", "placeholderText", "toolTip", "name"
]

def to_qml_literal(s):
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\t", "\\t")
    s = s.replace("\r", "\\r")
    return s


def parse_comment_paths(comment):
    """从 _comment 字段提取文件的相对路径列表
    支持两种格式:
      单文件: "描述 → modules/controlcenter/audio/AudioPane.qml"
      合并:   "⚠ 合并: modules/.../A.qml + modules/.../B.qml"
    """
    paths = []
    if "\u2192" in comment:
        path = comment.split("\u2192")[-1].strip()
        if path.endswith(".qml"):
            paths.append(path)
    elif ":" in comment or "\uff1a" in comment:
        after = re.split(r"[:\uff1a]", comment, maxsplit=1)[-1].strip()
        for part in after.split("+"):
            p = part.strip()
            if p.endswith(".qml"):
                paths.append(p)
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Caelestia Shell 简体中文汉化脚本"
    )
    parser.add_argument("source", nargs="?", help="源目录路径（默认自动检测）")
    parser.add_argument("target", nargs="?", default=LINUX_TARGET, help="输出目录（默认 ~/.config/quickshell/caelestia）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式：只报告将要修改的内容，不实际写入文件")
    parser.add_argument("--force", action="store_true", help="非交互模式：跳过所有确认提示，直接删除并重新复制")
    args = parser.parse_args()

    source_arg = args.source
    target_dir = args.target
    is_dry_run = args.dry_run
    is_force = args.force

    print("=== Caelestia Shell 汉化脚本 ===")
    if is_dry_run:
        print("  [预览模式 — 不会修改任何文件]")
    print()

    print(f"脚本位置:     {SCRIPT_DIR}")
    print(f"翻译字典:     {JSON_FILE}")
    print(f"项目根目录:   {PROJECT_ROOT}")
    print(f"输出目录:     {target_dir}")
    print()

    # 检查翻译字典
    if not os.path.isfile(JSON_FILE):
        print(f"错误: 找不到翻译字典 {JSON_FILE}")
        return 1
    print("[✓] 翻译字典已找到")

    # 确定源目录
    source_conf = None
    if source_arg:
        if os.path.isdir(source_arg) and os.path.isfile(os.path.join(source_arg, "shell.qml")):
            source_conf = source_arg
        else:
            print(f"错误: 指定路径无效或不包含 shell.qml: {source_arg}")
            return 1
    else:
        for candidate in [LINUX_SOURCE, LINUX_SOURCE.lower(),
                         "/usr/share/quickshell/Caelestia", "/usr/share/quickshell/caelestia",
                         PROJECT_ROOT]:
            if os.path.isdir(candidate) and os.path.isfile(os.path.join(candidate, "shell.qml")):
                source_conf = candidate
                break

    if not source_conf:
        print()
        print("错误: 找不到 Caelestia Shell 源文件！")
        print("用法: python install_zh_CN.py /path/to/caelestia [输出目录]")
        return 1

    print(f"[✓] 源目录: {source_conf}")
    print()

    # ========== [1/2] 准备输出目录 ==========
    print("[1/2] 准备输出目录...")

    abs_target = os.path.abspath(target_dir)
    abs_source = os.path.abspath(source_conf)

    def _ignore_target(directory, contents):
        """copytree 时跳过输出目录自身，防止递归套娃"""
        ignored = set()
        for item in contents:
            item_abs = os.path.normcase(os.path.abspath(os.path.join(directory, item)))
            if item_abs == os.path.normcase(abs_target):
                ignored.add(item)
            if item in (".git", "__pycache__", "node_modules"):
                ignored.add(item)
        return ignored

    def _do_copy():
        os.makedirs(os.path.dirname(os.path.abspath(target_dir)), exist_ok=True)
        shutil.copytree(source_conf, target_dir, ignore=_ignore_target)

    if os.path.isdir(target_dir):
        print(f"    已存在: {target_dir}")
        print("    从源目录重新复制 (已汉化的目录无法再次匹配英文原文)")

        if is_dry_run:
            print("    [预览] 将删除目标目录并从源目录重新复制")
        elif is_force:
            shutil.rmtree(target_dir)
            _do_copy()
            print("    已重新复制（--force 模式）。")
        else:
            print("      y) 重新复制 (⚠ 会删除目标目录下所有用户自定义文件)")
            print("      n) 保留现有目录 (⚠ 新文件不会同步、已汉化文本无法重新匹配)")
            choice = input("    选项 [y/n] (默认 n): ").strip().lower()

            if choice == 'y':
                confirm = input("    ⚠ 确认删除整个目录？此操作不可逆 [y/N]: ").strip().lower()
                if confirm == 'y':
                    shutil.rmtree(target_dir)
                    _do_copy()
                    print("    已重新复制。")
                else:
                    print("    已取消删除，将在现有目录上汉化。")
                    print("    注意：不会从源目录同步新文件，已汉化文本可能无法重新匹配。")
            else:
                print("    保留现有目录。")
                print("    注意：不会从源目录同步新文件，已汉化文本可能无法重新匹配。")
    else:
        if is_dry_run:
            print(f"    [预览] 将从 {source_conf} 复制到 {target_dir}")
        else:
            _do_copy()
            print("    已从源目录复制。")

    if not os.path.isfile(os.path.join(target_dir, "shell.qml")):
        print(f"    错误: {target_dir}/shell.qml 不存在")
        return 1
    print("    [✓] 输出目录就绪")
    print()

    # ========== [2/2] 替换英文为中文 ==========
    print("[2/2] 替换英文为中文...")

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 构建两层映射:
    #   path_map:  精确相对路径 → [(ctx, src, trans), ...]  (依据 _comment 路径)
    #   fname_map: 文件名兜底   → [(ctx, src, trans), ...]  (无 _comment 时回退)
    path_map = {}
    fname_map = {}
    all_entries = set()

    for ctx, entries in data.items():
        if ctx.startswith("_") or not isinstance(entries, dict):
            continue

        comment = data.get(f"_comment_{ctx}", "")
        target_paths = parse_comment_paths(comment)

        pairs = [(src, trans) for src, trans in entries.items()
                 if not src.startswith("_") and src != trans]

        if target_paths:
            for path in target_paths:
                norm = path.replace("\\", "/")
                path_map.setdefault(norm, [])
                for src, trans in pairs:
                    path_map[norm].append((ctx, src, trans))
                    all_entries.add((ctx, src))
        else:
            fname = ctx + ".qml"
            fname_map.setdefault(fname, [])
            for src, trans in pairs:
                fname_map[fname].append((ctx, src, trans))
                all_entries.add((ctx, src))

    entry_count = len(all_entries)
    path_count = len(path_map)
    fname_count = len(fname_map)
    print(f"    已加载 {path_count + fname_count} 个目标文件 ({path_count} 精确路径 + {fname_count} 文件名兜底), {entry_count} 条词条")
    print(f"    扫描: {target_dir}")
    if is_dry_run:
        print()
        print("    --- 预览：以下是将要修改的文件 ---")
    else:
        print()

    total_files = 0
    total_subs = 0
    matched_entries = set()

    for root, dirs, files in os.walk(target_dir):
        for fname in files:
            if not fname.endswith(".qml"):
                continue

            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, target_dir).replace("\\", "/")

            entries_for_file = path_map.get(rel, [])
            matched_by_fallback = False
            if not entries_for_file:
                entries_for_file = fname_map.get(fname, [])
                if entries_for_file:
                    matched_by_fallback = True
            if not entries_for_file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"    [!] 无法读取: {filepath} ({e})")
                continue

            original = content
            file_subs = 0

            for ctx, src, trans in entries_for_file:
                src_esc = to_qml_literal(src)
                trans_esc = to_qml_literal(trans)
                entry_key = (ctx, src)
                matched = False

                # 模式1: qsTr("source") -> qsTr("translation")
                old = f'qsTr("{src_esc}")'
                new = f'qsTr("{trans_esc}")'
                if old in content:
                    count = content.count(old)
                    file_subs += count
                    content = content.replace(old, new)
                    matched = True

                # 模式2: qsTr(`source`) -> qsTr(`translation`)
                if not matched:
                    old = f"qsTr(`{src}`)"
                    new = f"qsTr(`{trans}`)"
                    if old in content:
                        count = content.count(old)
                        file_subs += count
                        content = content.replace(old, new)
                        matched = True

                # 模式3: 裸字符串属性 (支持 name/label/description/text 等)
                if not matched:
                    for prop in SUPPORTED_PROPS:
                        # 匹配 prop: "value" 格式
                        old = f'{prop}: "{src_esc}"'
                        new = f'{prop}: "{trans_esc}"'
                        if old in content:
                            count = content.count(old)
                            file_subs += count
                            content = content.replace(old, new)
                            matched = True
                            break
                        
                        # 匹配 prop: 'value' 格式（单引号）
                        old_single = f"{prop}: '{src}'"
                        new_single = f"{prop}: '{trans}'"
                        if old_single in content:
                            count = content.count(old_single)
                            file_subs += count
                            content = content.replace(old_single, new_single)
                            matched = True
                            break

                # 模式4: JSON 中的 name 字段（启动器配置专用）
                # 匹配格式: "name": "Calculator" 或 name: "Calculator"
                if not matched:
                    patterns = [
                        (f'"{src}"', f'"{trans}"'),      # "name": "Calculator"
                        (f"'{src}'", f"'{trans}'"),      # 'name': 'Calculator'
                        (f': {src}', f': {trans}'),      # 无引号的情况
                    ]
                    for old, new in patterns:
                        if old in content:
                            # 确保是 name 字段的值
                            # 简单检查前面是否有 name 或 "name"
                            if re.search(rf'name\s*:\s*{re.escape(old)}', content):
                                count = content.count(old)
                                file_subs += count
                                content = content.replace(old, new)
                                matched = True
                                break

                # 模式5: 直接匹配不带属性名的字符串（兜底）
                if not matched:
                    # 只匹配行首或冒号后的独立字符串
                    patterns = [
                        (f'"{src_esc}"', f'"{trans_esc}"'),
                        (f"'{src}'", f"'{trans}'"),
                    ]
                    for old, new in patterns:
                        if old in content:
                            # 确保不是其他单词的一部分
                            if re.search(rf'[:=]\s*{re.escape(old)}', content):
                                count = content.count(old)
                                file_subs += count
                                content = content.replace(old, new)
                                matched = True
                                break

                if matched:
                    matched_entries.add(entry_key)

            if content != original:
                if is_dry_run:
                    print(f"    [预览] {rel} ({file_subs} 处)" + (" ⚠ 文件名兜底" if matched_by_fallback else ""))
                else:
                    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                        f.write(content)
                    print(f"    [+] {rel} ({file_subs} 处)" + (" ⚠ 文件名兜底" if matched_by_fallback else ""))
                total_files += 1
                total_subs += file_subs

    truly_missed = []
    seen = set()
    for entries in list(path_map.values()) + list(fname_map.values()):
        for ctx, src, trans in entries:
            key = (ctx, src)
            if key not in matched_entries and key not in seen:
                seen.add(key)
                truly_missed.append((ctx, src))

    print()
    print("=== 结果 ===")
    if is_dry_run:
        print(f"  预览修改: {total_files} 个文件")
        print(f"  预览替换: {total_subs} 处")
        print(f"  词条: {entry_count} 条中 {len(matched_entries)} 条可命中")
        if total_files == 0:
            print()
            print("  [!] 没有可修改的文件 — 可能已经汉化过，或翻译字典需要更新")
    else:
        print(f"  修改: {total_files} 个文件")
        print(f"  替换: {total_subs} 处")
        print(f"  词条: {entry_count} 条中 {len(matched_entries)} 条命中")

    if total_files == 0 and not is_dry_run:
        print()
        print("  [!] 没有文件被修改, 可能原因:")
        print("    - 输出目录中没有匹配的 QML 文件")
        print("    - 已经汉化过了 (建议选选项1重新复制)")

    if truly_missed:
        print()
        print(f"  [!] 未匹配词条 ({len(truly_missed)} 条):")
        for ctx, src in truly_missed[:30]:
            s = src[:50] + "..." if len(src) > 50 else src
            comment = data.get(f"_comment_{ctx}", "")
            paths = parse_comment_paths(comment)
            loc = ", ".join(paths) if paths else ctx + ".qml"
            print(f"      - [{ctx}] \"{s}\"  (应在 {loc})")
        if len(truly_missed) > 30:
            print(f"      ... 还有 {len(truly_missed) - 30} 条")

    # 保存翻译字典到输出目录（仅作快照归档，Quickshell 不会读取此文件；方便排查当前使用的是哪个版本的字典）
    if not is_dry_run:
        trans_dir = os.path.join(target_dir, "assets", "translations")
        os.makedirs(trans_dir, exist_ok=True)
        shutil.copy2(JSON_FILE, trans_dir)

    if is_dry_run:
        print()
        print("=== 预览完成 === 使用 python install_zh_CN.py 正式运行汉化。")
    else:
        print()
        print("=== 完成！重启 Caelestia Shell 即可生效 ===")
        print("提示: 修改 zh_CN.json 后重新运行此脚本")

    # 兜底路径报告
    if fname_map:
        fallback_files = {fname for fname in fname_map}
        print()
        print(f"  💡 提示: {len(fname_map)} 个上下文使用了文件名兜底匹配（无 _comment 路径），")
        print(f"     若发现翻译错误，建议为以下文件补充 _comment 字段：")
        for f in sorted(fallback_files)[:10]:
            print(f"       - {f}")
        if len(fallback_files) > 10:
            print(f"       ... 还有 {len(fallback_files) - 10} 个")

    return 0


if __name__ == "__main__":
    main()
