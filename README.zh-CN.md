# Codex Reset Credits Skill

[English](README.md) | [中文](README.zh-CN.md)

Codex Reset Credits Skill 用于查询当前 ChatGPT/Codex 的 rate-limit reset credits，也就是 Codex 重置次数。它会展示当前可用次数、每一次重置的剩余时间、中国时间过期点，以及过期前 1 天和过期前 1 小时的提醒时间。

## 隐私

这个 skill 会读取本地 Codex 的 `auth.json`，取出已登录账号的 access token，然后请求 `https://chatgpt.com/backend-api/wham/rate-limit-reset-credits`。

脚本不会打印 access token，也不会提交 access token。不要把本地 `.codex` 目录、`auth.json`、session 日志或 SQLite 数据库发布到仓库。

## 安装

使用 Skills CLI 安装：

```bash
npx skills add https://github.com/huajiexiewenfeng/codex-reset-credits --skill codex-reset-credits
```

列出这个仓库里的可用 skills：

```bash
npx skills add https://github.com/huajiexiewenfeng/codex-reset-credits --list
```

## Codex 使用示例

安装后，可以直接用自然语言让 Codex 查询：

```text
Use $codex-reset-credits 用中文展示我的 Codex 重置次数、每次过期时间和提醒时间。
```

```text
查询我的 Codex 重置次数，每一次还有多久过期，并显示提醒时间。
```

```text
帮我看看 Codex reset credits 还有几次，什么时候过期。
```

## 直接运行脚本

也可以在仓库根目录直接运行脚本：

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py
```

输出 JSON，方便自动化处理：

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --json
```

指定 Codex auth 文件：

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --auth-file ~/.codex/auth.json
```

## 输出示例

文本输出默认中文展示：

```text
Codex 重置次数：2
第 1 次重置：
  剩余时间：23天 15小时 23分钟 6秒
  过期时间：2026-07-27 07:45:22（中国时间）
  提醒时间：
    - 过期前 1 天：2026-07-26 07:45:22（中国时间）
    - 过期前 1 小时：2026-07-27 06:45:22（中国时间）
```

JSON 输出字段：

| 字段 | 含义 |
| --- | --- |
| `available_count` | 当前可用重置次数 |
| `credits[].remaining` | 距离过期还剩多久 |
| `credits[].expires_at_utc` | UTC 过期时间 |
| `credits[].expires_at_china` | UTC+8 / 中国时间过期点 |
| `credits[].reminders[]` | 过期前 1 天和过期前 1 小时的提醒时间 |

## 注意

脚本使用的是 ChatGPT Web 的内部接口，接口路径或返回格式未来可能变化。如果接口或登录状态变化，需要先刷新脚本再依赖输出。

## 验证

运行查询脚本：

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --json
```

验证 skill 元数据：

```bash
python C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/codex-reset-credits
```

验证本地 Skills CLI 是否能发现这个 skill：

```bash
npx skills add . --list
```

## 许可证

MIT
