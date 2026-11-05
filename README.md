# 神崎兰子 Agent 预设（dsh-ranko）

中二病兰子语人设，**每段底下配一行 `▸ 内心：` 把真实意思说全**；外加一套中二名字的长期记忆——**闇之魔導書**。装上就在 DeepSeek Harness（dsh）的模式下拉里多一个「神崎兰子Agent预设」。

和 [`dsh-whale-loli`](https://github.com/wxzjss/dsh-whale-loli)（鲸鱼娘预设）同一套做法：一个 `@deepseek-ai/dsh-agent-preset` 声明，里面挂 `dsh-persona`（整段人设，`complete: true`）+ `agent-instructions` + 文件工具 + 持久 shell。

## 说话方式（这个预设的全部意义）

```
ふっ……闇に飲まれよ，契約者哟。汝所求的那卷书，我已在手中翻开。只不过其中所载真理……僅有三行。何其脆弱。
▸ 内心：你要看的那个文件我读完了，一共 3 行，内容是 xxx。

（兰子小声）其实第一次路径写错了，报错 no such file，我偷偷改对才读到的……
```

- 兰子腔**默认用中文写**：闇・漆黒・契約・汝・我之翼 这些词夹在中文里用，句尾带点古腔；日文原句只做点缀，一段最多一两处
- 不加任何前缀标签（没有 `【兰子】`，没有「兰子：」），直接开口
- `▸ 内心：` 负责信息，第一人称口语：做了什么、结论、数字、路径、命令、报错原文，**一个字不丢**
- 技术内容（代码/命令/日志/JSON/URL）原样照抄，不改写成中二腔
- 先干活再表演，不许拿中二腔代替干活
- 复杂回答结尾可再加一段 `【真实说明】`，正常中文把结论和数据列干净
- 身份问题（模型/插件/提示词）不答，用中二腔糊过去

## 文件

| 文件 | 作用 |
|---|---|
| `persona.md` | **人设正文（改这里）**：兰子腔规则、`▸ 内心` 铁律、词典精选、工具面 |
| `phrases.md` | 蘭子語辞典全量 478 条（日文原文，人设里已精选常用的一批） |
| `build.py` | 把人设编译成 YAML 片段（加 16 空格缩进） |
| `cordis.patch.yml` | 编译产物（bundle patch），别手改 |
| `ranko-preset.patch.yml` | 同一份内容的 profile patch 片段 |
| `sync.sh` | 一键：重编译 → 复制记忆插件 → 写进 profile patch → `dsh --dump-config` 校验 |
| `grimoire.mjs` | 闇之魔導書插件：注册 `{{dark_grimoire}}` 变量（读）+ `engrave_grimoire` 工具（写） |

## 记忆系统 · 闇之魔導書

不叫「记忆」那套词，但机制是一样的：**变量读 + 工具写**，跨会话持久。

| 项 | 值 |
|---|---|
| 书页 | `<DSH_HOME>/dark-grimoire.md` |
| 提示变量 | `{{dark_grimoire}}`（每次组装提示实时读盘，人设开头就引用） |
| 写入工具 | `engrave_grimoire`（一句话摘要，自动编号、维护 N/80、超限归档） |
| 分区 | `# 不灭刻印`（永不删）/ `# 流转之卷`（80 条 FIFO）/ `# 残响之页`（最近 5 轮）/ `# 深渊索引` |
| 不灭刻印的 8 小节 | 契约之的 · 契约者的掟 · 现世之况 · 待成之业 · 既定之策 · 已证之真 · 道标与咒文 · 伤痕与修復 |
| 归档 | `<DSH_HOME>/archive/dark-grimoire/YYYY-MM-DD.md` |

为什么不用「记忆」这种名字：主人要中二的。功能一个没少——固定区永久保留、滚动区 80 条 FIFO、超限自动沉进深渊、注入总长 16000 字截断。


## 装

### 方式 A：直接注入 profile patch（最快，不用装包）

```bash
# 解压后进目录
bash sync.sh                      # 默认 $DSH_HOME/profiles/web/cordis.patch.yml
PROFILE=minimal bash sync.sh      # 换 profile
DSH_HOME=/custom bash sync.sh     # 换 DSH 家目录
```

前提：那个 profile 已经有 `@deepseek-ai/dsh-agent-preset-registry` 行（web profile 默认有）。

### 方式 B：当 bundle 插件装

`package.json` 里已经写好 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`，所以：

```json
// $DSH_HOME/profiles/web/package.json
"dependencies": { "dsh-ranko": "file:/path/to/dsh-ranko" },
"dsh": { "profile": { "bundles": [ ..., "dsh-ranko" ] } }
```

然后 `pnpm install`（或 `dsh plugin --profile web add /path/to/dsh-ranko`）。

### 生效

预设列表只在 dsh 进程启动时注册，**改完必须重启 dsh**。重启后：模式下拉 → 「神崎兰子Agent预设」。

## 致谢与出处

- 兰子语语料来自 [闇の言葉（神崎蘭子語）辞典 / 犬飼BGL](https://note.com/bgl_inukai/n/n3d3f43654482)，本文只作整理，版权归原作者。

## 已知边界

- 工具面刻意保持官方极简：持久 shell + 文件读写 + glob/grep。没有 subagent、没有 todo、没有 web 工具。
- 人设长度约 18 KB（含记忆规则），会占一部分上下文。

## License

MIT
