#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen


URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
DEFAULT_AUTH_FILE = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
CHINA = timezone(timedelta(hours=8))


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_duration(seconds):
    seconds = int(seconds)
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    days, seconds = divmod(seconds, 86_400)
    hours, seconds = divmod(seconds, 3_600)
    minutes, seconds = divmod(seconds, 60)
    return f"{sign}{days}天 {hours}小时 {minutes}分钟 {seconds}秒"


def format_china_time(value):
    return value.astimezone(CHINA).strftime("%Y-%m-%d %H:%M:%S")


def load_token(auth_file):
    auth = json.loads(auth_file.read_text(encoding="utf-8"))
    return auth["tokens"]["access_token"]


def fetch_credits(token):
    request = Request(
        URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Origin": "https://chatgpt.com",
            "Referer": "https://chatgpt.com/",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def build_result(data):
    now = datetime.now(timezone.utc)
    credits = []
    for index, credit in enumerate(data.get("credits", []), start=1):
        expires_at = parse_time(credit["expires_at"])
        reminder_1_day = expires_at - timedelta(days=1)
        reminder_1_hour = expires_at - timedelta(hours=1)
        credits.append(
            {
                "index": index,
                "remaining": format_duration(expires_at.timestamp() - now.timestamp()),
                "expires_at_utc": expires_at.isoformat(timespec="seconds"),
                "expires_at_china": expires_at.astimezone(CHINA).isoformat(timespec="seconds"),
                "reminders": [
                    {
                        "label": "过期前 1 天",
                        "at_utc": reminder_1_day.isoformat(timespec="seconds"),
                        "at_china": reminder_1_day.astimezone(CHINA).isoformat(timespec="seconds"),
                    },
                    {
                        "label": "过期前 1 小时",
                        "at_utc": reminder_1_hour.isoformat(timespec="seconds"),
                        "at_china": reminder_1_hour.astimezone(CHINA).isoformat(timespec="seconds"),
                    },
                ],
            }
        )
    return {
        "available_count": data.get("available_count", 0),
        "credits": credits,
    }


def print_text(result):
    print(f"Codex 重置次数：{result['available_count']}")
    for credit in result["credits"]:
        expires_at = parse_time(credit["expires_at_china"])
        print(f"第 {credit['index']} 次重置：")
        print(f"  剩余时间：{credit['remaining']}")
        print(f"  过期时间：{format_china_time(expires_at)}（中国时间）")
        print("  提醒时间：")
        for reminder in credit["reminders"]:
            reminder_at = parse_time(reminder["at_china"])
            print(f"    - {reminder['label']}：{format_china_time(reminder_at)}（中国时间）")


def main():
    parser = argparse.ArgumentParser(description="查询 Codex 重置次数、过期时间和提醒时间。")
    parser.add_argument("--auth-file", type=Path, default=DEFAULT_AUTH_FILE)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = build_result(fetch_credits(load_token(args.auth_file)))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
