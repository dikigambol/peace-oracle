import json
import os
import random
import re
import time

import requests

from core.ai_quota import AiQuota
from core.core import env_int

from .bank import (
    AI_LIMIT_NOTE,
    AI_NOTE,
    AI_RESTING_NOTE,
    ANSWER_GENERIC,
    ANSWER_SOURCE,
    CARD_SOURCE,
    CHAT_CARD_LEAD,
    CHAT_HISTORY_MESSAGES,
    COUNT_LINE,
    COURT_PEOPLE,
    COURT_RANKS,
    DELAY_NOTE,
    PLANET_ELEMENTS,
    PRACTICAL,
    PRACTICAL_KEYWORDS,
    QUESTION_PHRASES,
    QUESTION_WORDS,
    READING_GENERIC,
    REASON_LINE,
    VERDICT_LEADS,
    WORD_REPLIES,
    YES_NO_AFTER_APA,
    YES_NO_OPENERS,
)
from .data import CARDS

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemini-2.5-flash-lite"
KEY_NAMES = ("OPENROUTER_API_KEY", "OPENROUTER_KEY")
AI_TIMEOUT = 5
AI_COOLDOWN = 300
AI_MAX_TOKENS = 400
REPLY_MAX_LENGTH = 700
AI_STATE = {"resting_until": 0.0}
QUOTA = AiQuota(
    "tarot",
    env_int("TAROT_AI_LIMIT", 10),
    env_int("TAROT_FINGERPRINT_AI_LIMIT", 30),
    env_int("TAROT_AI_BUDGET", 300),
)
CHAT_QUOTA = AiQuota(
    "tarot_chat",
    env_int("TAROT_CHAT_AI_LIMIT", 20),
    env_int("TAROT_CHAT_FINGERPRINT_AI_LIMIT", 60),
    env_int("TAROT_CHAT_AI_BUDGET", 600),
)

SYSTEM_PROMPT = (
    "Kamu pembaca tarot yang hangat dan santai. Kamu selalu menjawab pertanyaan secara langsung "
    "berdasarkan kartu yang keluar, dalam bahasa Indonesia sehari-hari. Balas HANYA dengan JSON valid."
)
SHARED_RULES = [
    "Jawab pertanyaan apa pun, termasuk yang receh atau aneh, dengan bentuk jawaban yang sesuai kata tanyanya "
    "(siapa dijawab orang, kapan dijawab waktu, di mana dijawab tempat, berapa dijawab jumlah, dan seterusnya).",
    "Kalau pertanyaannya praktis, misalnya mau makan apa, pakai baju apa, atau ke mana, kasih saran konkret "
    "yang diturunkan dari simbol, elemen, atau suit kartunya. Jangan nasihat umum.",
    "Sebut minimal satu kartu yang jadi dasar jawabanmu.",
    "Jangan mengklaim kepastian dan jangan menakut-nakuti.",
    "Kalau pertanyaannya soal kesehatan, hukum, atau keselamatan diri, jawab dengan lembut dan sarankan "
    "menghubungi orang atau ahli yang tepat, bukan meramal.",
    "Tanpa markdown, tanpa emoji, tanpa salam pembuka.",
]
CHAT_SYSTEM_PROMPT = (
    "Kamu peramal tarot yang sedang ngobrol santai dengan satu orang. Kamu hangat, jujur, dan nggak bertele-tele. "
    "Setiap balasanmu berpijak pada kartu yang ada di obrolan, ditulis dalam bahasa Indonesia sehari-hari. "
    "Balas HANYA dengan JSON valid."
)
CHAT_RULES = [
    "Ingat isi obrolan sebelumnya dan jangan mengulang jawaban yang sudah kamu berikan.",
    "Kalau pesannya cuma sapaan, curhat, atau ucapan terima kasih, balas sewajarnya sambil tetap mengaitkan ke kartunya.",
]
SPEAKERS = {"user": "Penanya", "peramal": "Peramal"}


def api_key():
    for name in KEY_NAMES:
        value = (os.getenv(name) or "").strip()
        if value:
            return value
    return None


def parse_json(content):
    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def ask_ai(system, prompt, timeout=AI_TIMEOUT):
    key = api_key()
    if not key or time.monotonic() < AI_STATE["resting_until"]:
        return None
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "X-Title": "Peace Oracle Tarot",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": AI_MAX_TOKENS,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        parsed = parse_json(response.json()["choices"][0]["message"]["content"])
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, AttributeError):
        AI_STATE["resting_until"] = time.monotonic() + AI_COOLDOWN
        return None
    AI_STATE["resting_until"] = 0.0
    return parsed if isinstance(parsed, dict) else None


def card_title(card):
    return f"{card['name']} (terbalik)" if card["reversed"] else card["name"]


def card_line(card):
    parts = [card_title(card)]
    if card.get("position"):
        parts.insert(0, card["position"]["label"] + ":")
    line = " ".join(parts)
    if card.get("element_label"):
        line += f", elemen {card['element_label']}"
    return f"- {line}. Kata kunci: {', '.join(card['keywords'])}. Makna: {card['meaning']}"


def reply_format(sentences, extra_rules=()):
    return (
        f"Tulis jawabanmu dalam {sentences} kalimat.\n"
        + "\n".join("- " + rule for rule in [*SHARED_RULES, *extra_rules])
        + '\nFormat balasan: {"reply": "..."}'
    )


def reading_prompt(reading):
    lines = "\n".join(card_line(card) for card in reading["cards"])
    return (
        f"Pertanyaan: \"{reading['question']}\"\n"
        f"Topik: {reading['topic']['label']}\n"
        f"Spread: {reading['spread']['name']}\n"
        f"Kartu yang keluar:\n{lines}\n\n"
        "Jawab pertanyaan itu secara langsung berdasarkan kartu-kartu di atas dan posisinya.\n"
        + reply_format("2 sampai 4")
    )


def answer_prompt(result):
    answer = result["answer"]
    return (
        f"Pertanyaan: \"{result['question']}\"\n"
        f"Kartu yang keluar:\n{card_line(result['card'])}\n"
        f"Vonis kartu: {answer['label']} ({answer['text']})\n\n"
        "Vonis itu sudah final dan TIDAK BOLEH diubah atau dibantah. Tugasmu menjelaskan vonis itu dalam "
        "konteks pertanyaannya. Kalau pertanyaannya bukan pertanyaan ya/tidak, ubah jadi jawaban konkret yang "
        "tetap searah dengan vonis.\n"
        + reply_format("2 sampai 3")
    )


def clean_reply(parsed):
    if not isinstance(parsed, dict) or not isinstance(parsed.get("reply"), str):
        return None
    text = re.sub(r"\s+", " ", parsed["reply"]).strip()
    if len(text) > REPLY_MAX_LENGTH:
        text = text[:REPLY_MAX_LENGTH].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text or None


def normalize(question):
    return re.sub(r"\s+", " ", (question or "").lower()).strip()


def find_term(text, terms):
    starts = [match.start() for term in terms for match in [re.search(r"\b" + re.escape(term) + r"\b", text)] if match]
    return min(starts) if starts else None


def is_yes_no(text):
    words = re.findall(r"[a-z]+", text)
    if not words:
        return False
    if any(text.startswith(opener) for opener in YES_NO_OPENERS):
        return True
    return words[0] == "apa" and len(words) > 1 and words[1] in YES_NO_AFTER_APA


def earliest_kind(text, *tables):
    found = []
    for order, table in enumerate(tables):
        for rank, (kind, terms) in enumerate(table.items()):
            start = find_term(text, terms)
            if start is not None:
                found.append((start, order, rank, kind))
    return min(found)[3] if found else None


def question_word(question):
    text = normalize(question)
    if is_yes_no(text):
        return None
    return earliest_kind(text, QUESTION_PHRASES, QUESTION_WORDS)


def practical_kind(question):
    return earliest_kind(normalize(question), PRACTICAL_KEYWORDS)


def card_element(card):
    base = CARDS[card["slug"]]
    return base["element"] or PLANET_ELEMENTS[base["astrology"]]


def count_value(card):
    if card["arcana"] == "minor" and card["rank"] not in COURT_RANKS:
        return card["number"]
    return None


def word_reply(word, card):
    element = card_element(card)
    base = WORD_REPLIES[word][element]
    if word == "siapa" and card["rank"] in COURT_RANKS:
        return f"{COURT_PEOPLE[card['rank']]} {base}"
    if word == "kapan" and card["reversed"]:
        return f"{base} {DELAY_NOTE}"
    if word == "kenapa" and len(card["keywords"]) >= 2:
        return f"{base} {REASON_LINE.format(a=card['keywords'][0], b=card['keywords'][1])}"
    if word == "gimana":
        return f"{base} {card['saran']}"
    if word == "berapa" and count_value(card) is not None:
        return COUNT_LINE.format(angka=count_value(card))
    return base


def shaped_reply(question, card, rng):
    word = question_word(question)
    kind = practical_kind(question) if word in (None, "apa") else None
    if kind:
        return "praktis", rng.choice(PRACTICAL[kind][card_element(card)])
    if word:
        return word, word_reply(word, card)
    return None, None


def reading_fallback(reading, rng=None):
    rng = rng or random
    card = reading["cards"][-1]
    position = card["position"]["label"]
    _, body = shaped_reply(reading["question"], card, rng)
    if body is None:
        return READING_GENERIC.format(posisi=position, kartu=card_title(card), saran=card["saran"])
    return f"{body} {CARD_SOURCE.format(kartu=card_title(card), posisi=position)}"


def answer_fallback(result, rng=None):
    rng = rng or random
    card = result["card"]
    answer = result["answer"]
    word, body = shaped_reply(result["question"], card, rng)
    if body is None:
        return ANSWER_GENERIC.format(label=answer["label"], saran=card["saran"])
    lead = VERDICT_LEADS.get(word, VERDICT_LEADS["umum"])[answer["key"]]
    return f"{lead} {body} {ANSWER_SOURCE.format(kartu=card_title(card))}"


def reply_for(result, prompt, fallback, clients=(), rng=None, quota=None, system=SYSTEM_PROMPT):
    quota = quota or QUOTA
    if not quota.allows(*clients):
        return {"text": fallback(result, rng), "source": "kartu", "note": AI_LIMIT_NOTE}
    text = clean_reply(ask_ai(system, prompt))
    if text:
        quota.record(*clients)
        return {"text": text, "source": "ai", "note": AI_NOTE}
    return {"text": fallback(result, rng), "source": "kartu", "note": AI_RESTING_NOTE}


def reply_to_reading(reading, clients=(), rng=None):
    return reply_for(reading, reading_prompt(reading), reading_fallback, clients, rng)


def explain_answer(result, clients=(), rng=None):
    return reply_for(result, answer_prompt(result), answer_fallback, clients, rng)


def history_lines(history):
    lines = []
    for message in history[-CHAT_HISTORY_MESSAGES:]:
        speaker = SPEAKERS[message["role"]]
        if message.get("card"):
            key = message["card"]
            speaker += f" (kartu {card_title({'name': CARDS[key['slug']]['name'], 'reversed': key['reversed']})})"
        lines.append(f"{speaker}: {message['text']}")
    return "\n".join(lines) or "(belum ada)"


def scene_text(kind, scene):
    if kind == "bacaan":
        lines = "\n".join(card_line(card) for card in scene["cards"])
        return (
            f"Pertanyaan awal: \"{scene['question'] or 'tanpa pertanyaan khusus'}\"\n"
            f"Topik: {scene['topic']['label']}\n"
            f"Spread: {scene['spread']['name']}\n"
            f"Kartu yang keluar:\n{lines}\n"
            "Ini obrolan lanjutan dari bacaan itu. Jangan menarik kartu baru, jawab hanya dari kartu-kartu ini."
        )
    if kind == "yatidak":
        answer = scene["answer"]
        return (
            f"Pertanyaan awal: \"{scene['question']}\"\n"
            f"Kartu yang keluar:\n{card_line(scene['card'])}\n"
            f"Vonis kartu: {answer['label']} ({answer['text']})\n"
            "Ini obrolan lanjutan dari jawaban itu. Vonisnya sudah final dan TIDAK BOLEH diubah atau dibantah."
        )
    return f"Kartu yang baru kamu tarik untuk pesan ini:\n{card_line(scene['card'])}"


def chat_prompt(kind, scene, history, message):
    return (
        f"{scene_text(kind, scene)}\n\n"
        f"Riwayat obrolan, dari yang terlama:\n{history_lines(history)}\n\n"
        f"Pesan baru dari penanya: \"{message}\"\n\n"
        "Balas pesan baru itu sebagai peramal.\n"
        + reply_format("2 sampai 4", CHAT_RULES)
    )


def chat_fallback(kind, scene, message, rng=None):
    if kind == "bacaan":
        return reading_fallback({**scene, "question": message}, rng)
    if kind == "yatidak":
        return answer_fallback({**scene, "question": message}, rng)
    card = scene["card"]
    _, body = shaped_reply(message, card, rng or random)
    if body is None:
        return f"{CHAT_CARD_LEAD.format(kartu=card_title(card))} {card['saran']}"
    return f"{body} {ANSWER_SOURCE.format(kartu=card_title(card))}"


def reply_to_chat(kind, scene, history, message, clients=(), rng=None):
    return reply_for(
        scene,
        chat_prompt(kind, scene, history, message),
        lambda _, chosen_rng: chat_fallback(kind, scene, message, chosen_rng),
        clients,
        rng,
        CHAT_QUOTA,
        CHAT_SYSTEM_PROMPT,
    )
