import hashlib
import hmac
import re
import secrets

from core.core import transact

ROOM_CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
ROOM_CODE_LENGTH = 6
ROOM_CODE_ALIASES = str.maketrans({"O": "0", "I": "1", "L": "1"})
COUNTERS_COLLECTION = "room_codes"
FEISTEL_ROUNDS = 8


class RoomCodesExhausted(Exception):
    pass


def code_space(alphabet=ROOM_CODE_ALPHABET, length=ROOM_CODE_LENGTH):
    return len(alphabet) ** length


def half_bits(size):
    bits = max(2, (size - 1).bit_length())
    return (bits + 1) // 2


def round_value(key, round_index, value, mask):
    digest = hmac.new(key, f"{round_index}:{value}".encode("ascii"), hashlib.sha256).digest()
    return int.from_bytes(digest[:8], "big") & mask


def feistel(key, number, half):
    mask = (1 << half) - 1
    left, right = number >> half, number & mask
    for round_index in range(FEISTEL_ROUNDS):
        left, right = right, left ^ round_value(key, round_index, right, mask)
    return (left << half) | right


def permute(key, number, size):
    if not 0 <= number < size:
        raise RoomCodesExhausted()
    half = half_bits(size)
    value = feistel(key, number, half)
    while value >= size:
        value = feistel(key, value, half)
    return value


def encode(number, alphabet=ROOM_CODE_ALPHABET, length=ROOM_CODE_LENGTH):
    base = len(alphabet)
    chars = []
    for _ in range(length):
        number, digit = divmod(number, base)
        chars.append(alphabet[digit])
    return "".join(reversed(chars))


def code_for(key, number, alphabet=ROOM_CODE_ALPHABET, length=ROOM_CODE_LENGTH):
    return encode(permute(key, number, code_space(alphabet, length)), alphabet, length)


def clean_room_code(value):
    if not isinstance(value, str):
        return None
    code = re.sub(r"[\s-]", "", value).upper().translate(ROOM_CODE_ALIASES)
    if len(code) != ROOM_CODE_LENGTH or any(char not in ROOM_CODE_ALPHABET for char in code):
        return None
    return code


def take_number(current):
    if not current:
        key = secrets.token_hex(32)
        return {"next": 1, "key": key}, (0, key)
    number = int(current.get("next", 0))
    if number >= code_space():
        raise RoomCodesExhausted()
    return {"next": number + 1}, (number, current["key"])


def allocate_room_code(client, namespace):
    number, key = transact(client.collection(COUNTERS_COLLECTION).document(namespace), take_number)
    return code_for(bytes.fromhex(key), number)
