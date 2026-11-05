#!/usr/bin/env python3
"""把 persona.md 编译成 dsh profile patch 片段（ranko-preset.patch.yml）。

- 人设正文每行加 16 空格缩进，塞进 dsh-persona 的 prefix（block scalar）。
- 产物 ranko-preset.patch.yml / cordis.patch.yml 是生成物，别手改。
- 改人设请改 persona.md，然后重跑本脚本或 sync.sh。
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

persona = (HERE / 'persona.md').read_text(encoding='utf-8').rstrip('\n')
body = '\n'.join(('                ' + ln) if ln.strip() else '' for ln in persona.split('\n'))

frag = '''
# ── 神崎兰子 Agent 预设（兰子语 + 内心对照）──────────────────────────────────
# 人设正文来自同目录 persona.md（由 build.py 生成，改人设请改那里再重跑 build.py / sync.sh）。
# 预设本体 = 官方极简工具面（持久 shell + 文件读写 + 检索）+ 兰子人设。
# 人设走 dsh-persona 的 prefix，complete: true 会把其它 section 丢掉，所以人设必须整段内联。
- insert:
    - id: preset-神崎兰子Agent预设
      name: '@deepseek-ai/dsh-agent-preset'
      config:
        id: 神崎兰子Agent预设
        name: 神崎兰子Agent预设
        description: '中二病兰子语人设：每段兰子腔下面配一行「▸ 内心」真实解释，信息一个字不丢；先干活再表演。工具面同官方极简（持久 shell + 文件读写 + 检索）。'
        order: 9
        plugins:
          - id: persona
            name: '@deepseek-ai/dsh-persona'
            config:
              prefix: |-
''' + body + '''
              complete: true
              includeRuntimeContext: false
          # 闇之魔導書：把 dark-grimoire.md 注册成提示变量 {{dark_grimoire}}（读），
          # 并注册写入工具 engrave_grimoire（写）。插件文件随包走，sync.sh 会把它
          # 复制到 profile 目录，所以这里用相对路径 ./ranko-grimoire.mjs。
          - id: ranko-grimoire
            name: ./ranko-grimoire.mjs
            config:
              file: dark-grimoire.md
              variableName: dark_grimoire
              toolName: engrave_grimoire
              maxChars: 16000
              turnLimit: 80
              detailLimit: 5
          - id: agent-instructions
            name: '@deepseek-ai/dsh-agent-instructions'
            config:
              maxBytes: 65536
          - id: tool-fs
            name: '@deepseek-ai/dsh-tool-fs'
          - id: tool-fs-search
            name: '@deepseek-ai/dsh-tool-fs-search'
            config:
              sampleOverCapGlobResults: false
          - id: persistent-shell
            name: cordis:group
            group: true
            isolate:
              terminals: true
            config:
              - id: pty
                name: '@deepseek-ai/dsh-terminal'
              - id: terminal-bash
                name: '@deepseek-ai/dsh-terminal-bash'
                disabled: !!js process.platform === 'win32'
                config:
                  timeoutMs: 300000
              - id: persistent-bash
                name: '@deepseek-ai/dsh-tool-bash-persistent'
                disabled: !!js process.platform === 'win32'
                config:
                  timeoutMs: 300000
              - id: terminal-pwsh
                name: '@deepseek-ai/dsh-terminal-bash'
                disabled: !!js process.platform !== 'win32'
                config:
                  shellDialect: pwsh
                  timeoutMs: 300000
              - id: persistent-pwsh
                name: '@deepseek-ai/dsh-tool-pwsh-persistent'
                disabled: !!js process.platform !== 'win32'
                config:
                  timeoutMs: 300000
'''

END = '# ── /神崎兰子 Agent 预设 ──\n'
out = frag.lstrip('\n').rstrip('\n') + '\n' + END
(HERE / 'ranko-preset.patch.yml').write_text(out, encoding='utf-8')
(HERE / 'cordis.patch.yml').write_text(out, encoding='utf-8')
print(f'frag bytes {len(out)} -> ranko-preset.patch.yml / cordis.patch.yml')
