import json
import os

import requests

from core.ai_quota import AiQuota
from core.core import env_int, get_device_id, get_fingerprint_id

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemini-2.5-flash-lite"
OPENROUTER_KEY_NAMES = ["OPENROUTER_API_KEY", "openrouter_key", "OPENROUTER_KEY", "OPENROUTER_TOKEN"]
DAILY_AI_LIMIT = env_int("DAILY_AI_LIMIT", 10)
FINGERPRINT_AI_LIMIT = env_int(
    "FINGERPRINT_AI_LIMIT", max(DAILY_AI_LIMIT * 3, DAILY_AI_LIMIT)
)
DAILY_AI_BUDGET = env_int("DAILY_AI_BUDGET", 300)
QUOTA = AiQuota("zodiak", DAILY_AI_LIMIT, FINGERPRINT_AI_LIMIT, DAILY_AI_BUDGET)
QUOTA_NOTICE = "AI Mode Limited. Switching to Standard Prediction."


def get_openrouter_api_key():
    for key_name in OPENROUTER_KEY_NAMES:
        val = os.getenv(key_name)
        if val:
            return val.strip()
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        os.path.join(os.getcwd(), ".env"),
        ".env",
    ]
    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if "=" in line and not line.startswith("#"):
                            k, v = line.split("=", 1)
                            if "openrouter" in k.lower():
                                return v.strip()
            except Exception:
                pass
    return None


def strip_code_fence(content):
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        if content.endswith("```"):
            content = content.rsplit("```", 1)[0]
        content = content.strip()
    if content.startswith("json"):
        content = content[4:].strip()
    return content


def ask_openrouter(api_key, system_prompt, user_prompt, temperature, timeout=9):
    resp = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://zodiak-data-asia.local",
            "X-OpenRouter-Title": "Zodiak Data Asia",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        },
        timeout=timeout,
    )
    if resp.status_code != 200:
        return None
    return json.loads(strip_code_fence(resp.json()["choices"][0]["message"]["content"]))


def check_ai_quota(device_id=None):
    try:
        if not QUOTA.allows(device_id or get_device_id(), get_fingerprint_id()):
            return False, QUOTA_NOTICE
        return True, None
    except Exception:
        return True, None


def increment_ai_quota(device_id=None):
    try:
        QUOTA.record(device_id or get_device_id(), get_fingerprint_id())
    except Exception:
        pass
