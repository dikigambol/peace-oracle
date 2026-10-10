import datetime
import re
import secrets

from core.core import TransactionFailed, get_firestore_client, transact

try:
    from google.api_core.exceptions import AlreadyExists, GoogleAPIError
    from google.cloud.firestore import FieldFilter
except ImportError:
    AlreadyExists = GoogleAPIError = ()
    FieldFilter = None

from .bank import (
    ANSWERS,
    CHAT_CARD_POSITION,
    CHAT_NOT_FOUND,
    CHAT_TTL_DAYS,
    CHAT_TURN_LIMIT,
    CHAT_TURN_LIMIT_NOTE,
    ORIENTATION_LABELS,
    SPREADS,
    TOPICS,
)
from .data import CARDS, DECK_SIZE, TarotError, describe_drawn, draw_cards

CHATS_COLLECTION = "tarot_chats"
CHAT_ID_BYTES = 16
CHAT_ID_ATTEMPTS = 3
CHAT_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{8,64}")
CHAT_TTL = datetime.timedelta(days=CHAT_TTL_DAYS)
PURGE_BATCH = 50


class ChatUnavailable(Exception):
    pass


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def format_moment(moment):
    return moment.isoformat(timespec="seconds")


def chat_ready():
    return get_firestore_client() is not None


def not_found():
    return TarotError(CHAT_NOT_FOUND, 404)


def is_alive(chat, now):
    return chat.get("purge_at", "") > format_moment(now)


class ChatStore:
    def collection(self):
        client = get_firestore_client()
        if client is None:
            raise ChatUnavailable()
        return client.collection(CHATS_COLLECTION)

    def call(self, action):
        try:
            return action()
        except (GoogleAPIError, TransactionFailed) as error:
            raise ChatUnavailable() from error

    def purge(self, now):
        try:
            query = self.collection().where(filter=FieldFilter("purge_at", "<=", format_moment(now))).limit(PURGE_BATCH)
            for doc in query.stream():
                doc.reference.delete()
        except Exception:
            pass

    def create(self, kind, device, context, now=None):
        now = now or utc_now()
        self.purge(now)
        chat = {
            "kind": kind,
            "device_id": device,
            "context": context,
            "messages": [],
            "turns": 0,
            "created_at": format_moment(now),
            "updated_at": format_moment(now),
            "purge_at": format_moment(now + CHAT_TTL),
        }
        for _ in range(CHAT_ID_ATTEMPTS):
            chat_id = secrets.token_urlsafe(CHAT_ID_BYTES)
            try:
                self.call(lambda: self.collection().document(chat_id).create(chat))
            except ChatUnavailable as error:
                if isinstance(error.__cause__, AlreadyExists):
                    continue
                raise
            return {"id": chat_id, **chat}
        raise ChatUnavailable()

    def get(self, chat_id, device, now=None):
        now = now or utc_now()
        if not isinstance(chat_id, str) or not CHAT_ID_PATTERN.fullmatch(chat_id):
            raise not_found()
        snapshot = self.call(lambda: self.collection().document(chat_id).get())
        chat = snapshot.to_dict() if snapshot.exists else None
        if not chat or chat.get("device_id") != device or not is_alive(chat, now):
            raise not_found()
        return {"id": chat_id, **chat}

    def latest(self, device, kind, now=None):
        now = now or utc_now()
        query = self.collection().where(filter=FieldFilter("device_id", "==", device))
        found = self.call(lambda: [(doc.id, doc.to_dict()) for doc in query.stream()])
        alive = [(chat_id, chat) for chat_id, chat in found if chat.get("kind") == kind and is_alive(chat, now)]
        if not alive:
            return None
        chat_id, chat = max(alive, key=lambda item: item[1].get("updated_at", ""))
        return {"id": chat_id, **chat}

    def append(self, chat_id, device, messages, now=None):
        now = now or utc_now()

        def change(current):
            if not current or current.get("device_id") != device or not is_alive(current, now):
                raise not_found()
            turns = int(current.get("turns", 0))
            if turns >= CHAT_TURN_LIMIT:
                raise TarotError(CHAT_TURN_LIMIT_NOTE, 409)
            fields = {
                "messages": list(current.get("messages", [])) + messages,
                "turns": turns + 1,
                "updated_at": format_moment(now),
                "purge_at": format_moment(now + CHAT_TTL),
            }
            return fields, {**current, **fields}

        return {"id": chat_id, **self.call(lambda: transact(self.collection().document(chat_id), change))}


def build_chat_store():
    return ChatStore()


def ensure_room(chat):
    if int(chat.get("turns", 0)) >= CHAT_TURN_LIMIT:
        raise TarotError(CHAT_TURN_LIMIT_NOTE, 409)


def card_key(card):
    return {"slug": card["slug"], "reversed": bool(card["reversed"])}


def reading_context(reading):
    return {
        "question": reading["question"],
        "topic": reading["topic"]["key"],
        "spread": reading["spread"]["key"],
        "spread_name": reading["spread"]["name"],
        "cards": [{**card_key(card), "position": card["position"]["label"]} for card in reading["cards"]],
    }


def answer_context(result):
    return {"question": result["question"], "card": card_key(result["card"]), "answer": result["answer"]["key"]}


def describe_key(key, topic, position=None):
    return describe_drawn(CARDS[key["slug"]], key["reversed"], topic, {"label": position} if position else None)


def draw_chat_card(rng=None):
    rng = rng or secrets.SystemRandom()
    (card, reversed_), = draw_cards([rng.randrange(DECK_SIZE)], True, rng)
    return {"slug": card["slug"], "reversed": reversed_}


def chat_scene(chat, card_key_for_turn=None):
    context = chat.get("context") or {}
    kind = chat["kind"]
    if kind == "bacaan":
        topic = context["topic"]
        return {
            "question": context.get("question", ""),
            "topic": {"key": topic, **TOPICS[topic]},
            "spread": {"key": context["spread"], "name": context.get("spread_name") or SPREADS[context["spread"]]["name"]},
            "cards": [describe_key(card, topic, card["position"]) for card in context["cards"]],
        }
    if kind == "yatidak":
        answer_key = context["answer"]
        return {
            "question": context.get("question", ""),
            "card": describe_key(context["card"], "umum"),
            "answer": {"key": answer_key, **ANSWERS[answer_key]},
        }
    return {"card": describe_key(card_key_for_turn, "umum", CHAT_CARD_POSITION) if card_key_for_turn else None}


def public_card(key):
    card = CARDS[key["slug"]]
    return {
        "slug": card["slug"],
        "name": card["name"],
        "name_id": card["name_id"],
        "reversed": key["reversed"],
        "orientation_label": ORIENTATION_LABELS[key["reversed"]],
    }


def public_message(message):
    shown = {"role": message["role"], "text": message["text"]}
    if message.get("card"):
        shown["card"] = public_card(message["card"])
    if message.get("note"):
        shown["note"] = message["note"]
    if message.get("source"):
        shown["source"] = message["source"]
    return shown


def public_chat(chat):
    return {
        "id": chat["id"],
        "kind": chat["kind"],
        "turns": int(chat.get("turns", 0)),
        "turn_limit": CHAT_TURN_LIMIT,
        "messages": [public_message(message) for message in chat.get("messages", [])],
    }


def user_message(text, now=None):
    return {"role": "user", "text": text, "at": format_moment(now or utc_now())}


def peramal_message(reply, card=None, now=None):
    message = {
        "role": "peramal",
        "text": reply["text"],
        "source": reply["source"],
        "note": reply["note"],
        "at": format_moment(now or utc_now()),
    }
    if card:
        message["card"] = card
    return message
