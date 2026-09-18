NAYIN_BANK = {
    0: {"hanzi": "海中金", "name": "Emas dalam Laut", "element": "logam"},
    1: {"hanzi": "爐中火", "name": "Api dalam Tungku", "element": "api"},
    2: {"hanzi": "大林木", "name": "Kayu Hutan Besar", "element": "kayu"},
    3: {"hanzi": "路旁土", "name": "Tanah Tepi Jalan", "element": "tanah"},
    4: {"hanzi": "劍鋒金", "name": "Emas Mata Pedang", "element": "logam"},
    5: {"hanzi": "山頭火", "name": "Api Puncak Gunung", "element": "api"},
    6: {"hanzi": "澗下水", "name": "Air Jurang", "element": "air"},
    7: {"hanzi": "城頭土", "name": "Tanah Benteng Kota", "element": "tanah"},
    8: {"hanzi": "白蠟金", "name": "Emas Lilin Putih", "element": "logam"},
    9: {"hanzi": "楊柳木", "name": "Kayu Dedalu", "element": "kayu"},
    10: {"hanzi": "泉中水", "name": "Air Mata Air", "element": "air"},
    11: {"hanzi": "屋上土", "name": "Tanah Atap Rumah", "element": "tanah"},
    12: {"hanzi": "霹靂火", "name": "Api Petir", "element": "api"},
    13: {"hanzi": "松柏木", "name": "Kayu Pinus dan Cemara", "element": "kayu"},
    14: {"hanzi": "長流水", "name": "Air Sungai Panjang", "element": "air"},
    15: {"hanzi": "沙中金", "name": "Emas dalam Pasir", "element": "logam"},
    16: {"hanzi": "山下火", "name": "Api Kaki Gunung", "element": "api"},
    17: {"hanzi": "平地木", "name": "Kayu Dataran", "element": "kayu"},
    18: {"hanzi": "壁上土", "name": "Tanah Dinding", "element": "tanah"},
    19: {"hanzi": "金箔金", "name": "Emas Lembaran", "element": "logam"},
    20: {"hanzi": "覆燈火", "name": "Api Lampu Bertudung", "element": "api"},
    21: {"hanzi": "天河水", "name": "Air Sungai Langit", "element": "air"},
    22: {"hanzi": "大驛土", "name": "Tanah Jalan Raya", "element": "tanah"},
    23: {"hanzi": "釵釧金", "name": "Emas Perhiasan", "element": "logam"},
    24: {"hanzi": "桑柘木", "name": "Kayu Murbei", "element": "kayu"},
    25: {"hanzi": "大溪水", "name": "Air Sungai Besar", "element": "air"},
    26: {"hanzi": "沙中土", "name": "Tanah dalam Pasir", "element": "tanah"},
    27: {"hanzi": "天上火", "name": "Api Langit", "element": "api"},
    28: {"hanzi": "石榴木", "name": "Kayu Delima", "element": "kayu"},
    29: {"hanzi": "大海水", "name": "Air Samudra", "element": "air"},
}

STEM_RELATION_BANK = {
    (0, 5): {
        "kind": "he",
        "hanzi": "甲己合",
        "label": "Berpadu jadi Tanah",
        "text": "Batang tahun 甲 dan 己 berpadu jadi Tanah. Yang berprinsip bertemu yang telaten, dan kesepakatan kalian cenderung tahan lama.",
    },
    (1, 6): {
        "kind": "he",
        "hanzi": "乙庚合",
        "label": "Berpadu jadi Logam",
        "text": "Batang tahun 乙 dan 庚 berpadu jadi Logam. Kelenturan bertemu ketegasan, dan dari situ keputusan yang jelas biasanya lahir.",
    },
    (2, 7): {
        "kind": "he",
        "hanzi": "丙辛合",
        "label": "Berpadu jadi Air",
        "text": "Batang tahun 丙 dan 辛 berpadu jadi Air. Keterbukaan bertemu ketelitian, dan kalian saling melembutkan cara masing-masing.",
    },
    (3, 8): {
        "kind": "he",
        "hanzi": "丁壬合",
        "label": "Berpadu jadi Kayu",
        "text": "Batang tahun 丁 dan 壬 berpadu jadi Kayu. Kedalaman bertemu keluwesan — hubungan yang romantis sekaligus rumit.",
    },
    (4, 9): {
        "kind": "he",
        "hanzi": "戊癸合",
        "label": "Berpadu jadi Api",
        "text": "Batang tahun 戊 dan 癸 berpadu jadi Api. Ketenangan bertemu kepekaan; beda cara pandang sering terasa, tapi justru itu yang merekatkan.",
    },
    (0, 6): {
        "kind": "chong",
        "hanzi": "甲庚冲",
        "label": "Berbenturan",
        "text": "Batang tahun 甲 dan 庚 berbenturan. Dua kehendak keras yang sama-sama tidak mau membelok lebih dulu.",
    },
    (1, 7): {
        "kind": "chong",
        "hanzi": "乙辛冲",
        "label": "Berbenturan",
        "text": "Batang tahun 乙 dan 辛 berbenturan. Yang satu menyesuaikan, yang satu menuntut standar; gesekannya halus tapi terus-menerus.",
    },
    (2, 8): {
        "kind": "chong",
        "hanzi": "丙壬冲",
        "label": "Berbenturan",
        "text": "Batang tahun 丙 dan 壬 berbenturan. Yang satu terbuka terang-terangan, yang satu menyimpan, dan keduanya merasa tidak terbaca.",
    },
    (3, 9): {
        "kind": "chong",
        "hanzi": "丁癸冲",
        "label": "Berbenturan",
        "text": "Batang tahun 丁 dan 癸 berbenturan. Sama-sama peka dan sama-sama memendam, jadi salah pahamnya dalam dan lama.",
    },
}

STEM_NEUTRAL = {
    "kind": "netral",
    "hanzi": "干無合冲",
    "label": "Netral",
    "text": "Batang tahun kalian tidak berpadu maupun berbenturan. Lapisan langitnya diam, jadi yang menentukan tetap relasi cabang dan elemennya.",
}

NAYIN_RELATION_BANK = {
    "setara": "Nayin kalian sama-sama {element}. Cara kalian memandang rezeki dan rasa aman mirip, termasuk titik butanya.",
    "memberi": "Nayin {self_name} menghidupi {other_name}. Dalam urusan jangka panjang, kamu lebih sering jadi pihak yang menopang.",
    "menerima": "Nayin {other_name} menghidupi {self_name}. Dalam urusan jangka panjang, kamu lebih sering jadi pihak yang ditopang.",
    "menekan": "Nayin {self_name} mengekang {other_name}. Kamu cenderung jadi penentu arah saat keputusan besar diambil.",
    "ditekan": "Nayin {other_name} mengekang {self_name}. Kamu cenderung mengalah saat keputusan besar diambil.",
}
