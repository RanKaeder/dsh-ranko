#!/usr/bin/env bash
# 把 persona.md 编译进 dsh profile 的 cordis.patch.yml（幂等，可反复跑）。
#   bash sync.sh                      # 默认写 web profile
#   DSH_HOME=/custom bash sync.sh     # 换 DSH 家目录
#   PROFILE=minimal bash sync.sh      # 换 profile
# 生效要重启 dsh（预设列表只在进程启动时注册）。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
PROFILE="${PROFILE:-web}"
PATCH="$DSH_HOME/profiles/$PROFILE/cordis.patch.yml"
START='# ── 神崎兰子 Agent 预设（兰子语 + 内心对照）'

if [ ! -f "$PATCH" ]; then
  echo "找不到 $PATCH（profile 名对吗？）" >&2
  exit 1
fi

# 先切掉旧段（本预设永远追加在文件末尾，按起始标记截断）
python3 - "$PATCH" "$START" <<'PY'
import sys, pathlib
patch, start = pathlib.Path(sys.argv[1]), sys.argv[2]
txt = patch.read_text(encoding='utf-8')
i = txt.find(start)
if i != -1:
    patch.write_text(txt[:i].rstrip('\n') + '\n', encoding='utf-8')
    print('旧段已移除')
else:
    print('首次写入')
PY

# 记忆插件跟着进去（patch 里用相对路径 ./ranko-grimoire.mjs 引用）
cp "$HERE/grimoire.mjs" "$(dirname "$PATCH")/ranko-grimoire.mjs"
echo "已放入 $(dirname "$PATCH")/ranko-grimoire.mjs"

python3 "$HERE/build.py"
printf '\n' >> "$PATCH"
cat "$HERE/ranko-preset.patch.yml" >> "$PATCH"
echo "已写入 $PATCH"

# 组合校验（有 dsh 才跑）
if command -v dsh >/dev/null 2>&1; then
  if timeout 180 dsh --profile "$PROFILE" --dump-config > /tmp/dump-ranko.txt 2>/tmp/dump-ranko.err; then
    echo "dump-config OK（命中 $(grep -c 神崎兰子 /tmp/dump-ranko.txt) 处）"
  else
    echo "dump-config 失败：" >&2
    tail -5 /tmp/dump-ranko.err >&2
    exit 1
  fi
fi
