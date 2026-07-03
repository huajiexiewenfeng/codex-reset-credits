# Codex Reset Credits Skill

[English](README.md) | [中文](README.zh-CN.md)

Codex Reset Credits Skill checks the current ChatGPT/Codex rate-limit reset credits from local Codex auth state. It reports the available reset count, each credit's remaining time, expiry time in China time, and reminder times for 1 day and 1 hour before expiry.

## Privacy

This skill reads the local Codex `auth.json` file to obtain the stored access token, then calls `https://chatgpt.com/backend-api/wham/rate-limit-reset-credits`.

It does not print or commit the access token. Do not publish your local `.codex` directory, `auth.json`, session logs, or SQLite databases.

## Install

Install the skill with Skills CLI:

```bash
npx skills add https://github.com/huajiexiewenfeng/codex-reset-credits --skill codex-reset-credits
```

List available skills from the repository:

```bash
npx skills add https://github.com/huajiexiewenfeng/codex-reset-credits --list
```

## Codex Usage Examples

After installation, ask Codex for your reset credit status in plain language:

```text
Use $codex-reset-credits to show my current Codex reset credits and reminder times.
```

```text
查询我的 Codex 重置次数，每一次还有多久过期，并显示提醒时间。
```

```text
Show my Codex reset credits in Chinese, including expiry time and reminders.
```

## Direct Script Examples

Run the bundled query script directly from the repository root:

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py
```

Output machine-readable JSON:

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --json
```

Use a specific Codex auth file:

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --auth-file ~/.codex/auth.json
```

## Output

Text output is Chinese-first:

```text
Codex 重置次数：2
第 1 次重置：
  剩余时间：23天 15小时 23分钟 6秒
  过期时间：2026-07-27 07:45:22（中国时间）
  提醒时间：
    - 过期前 1 天：2026-07-26 07:45:22（中国时间）
    - 过期前 1 小时：2026-07-27 06:45:22（中国时间）
```

The JSON output includes:

| Field | Meaning |
| --- | --- |
| `available_count` | Number of available reset credits |
| `credits[].remaining` | Remaining time before expiry |
| `credits[].expires_at_utc` | Expiry time in UTC |
| `credits[].expires_at_china` | Expiry time in UTC+8 / China time |
| `credits[].reminders[]` | Reminder schedule at 1 day and 1 hour before expiry |

## Notes

The backend endpoint is an internal ChatGPT web endpoint and may change. If the endpoint or auth format changes, refresh the script before relying on the output.

## Verify

Run the query script:

```bash
python -B skills/codex-reset-credits/scripts/query_reset_credits.py --json
```

Run quick validation:

```bash
python C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/codex-reset-credits
```

Verify local Skills CLI metadata:

```bash
npx skills add . --list
```

## License

MIT
