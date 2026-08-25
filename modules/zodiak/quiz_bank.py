import json
import requests, os
from .horoscope_bank import get_openrouter_api_key
from .ai_limiter import increment_ai_quota

PARTNER_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "category": "Komunikasi & Konflik",
        "question": "Kalau ada miskomunikasi atau masalah dalam hubungan, siapa yang biasanya ngajak ngobrol duluan?",
        "options": [
            "Aku duluan, gengsi nggak penting kalau soal perasaan.",
            "Dia dong, aku mau liat inisiatif dia dulu.",
            "Tergantung siapa yang salah, kudu adil!",
            "Cooling down dulu masing-masing, baru ngobrol tenang.",
        ],
    },
    {
        "id": 2,
        "category": "Respon Chat & Kabar",
        "question": "Gimana respon kamu kalau partner bales chat-nya lama padahal statusnya online?",
        "options": [
            "Santai aja, mungkin lagi sibuk atau repot urusan lain.",
            "Berpikir positif dulu, nanti baru nanya baik-baik.",
            "Langsung to the point nanya kenapa balesnya lama.",
            "Bales cuek atau lama balik biar ngerasain!",
        ],
    },
    {
        "id": 3,
        "category": "Ide Kencan Impian",
        "question": "Ide weekend atau date impian paling ideal buat kalian berdua?",
        "options": [
            "Deep talk santai di coffee shop estetik & tenang.",
            "Nonton bioskop atau main arcade games seru bareng.",
            "Kulineran street food hunting & jalan-jalan sore.",
            "Nonton marathon di rumah sambil order makanan favorit.",
        ],
    },
    {
        "id": 4,
        "category": "Love Language Utama",
        "question": "Bentuk 'Love Language' apa yang paling bikin kamu merasa dicintai?",
        "options": [
            "Quality Time (Waktu berkualitas berdua tanpa terdistraksi HP).",
            "Words of Affirmation (Pujian, kabar hangat, & perhatian verbal).",
            "Acts of Service (Tindakan nyata & bantuan tanpa diminta).",
            "Physical Touch / Gifts (Sentuhan hangat atau kejutan manis).",
        ],
    },
    {
        "id": 5,
        "category": "Apresiasi Pencapaian",
        "question": "Gimana cara favoritmu merayakan pencapaian sekecil apapun dari partner?",
        "options": [
            "Kasih kejutan makanan kesukaannya atau hadiah kecil.",
            "Puji setinggi langit dan bangga-banggain ke temen.",
            "Ajak makan enak bareng buat ngerayain momen itu.",
            "Kasih pelukan hangat & kata-kata apresiasi mendalam.",
        ],
    },
    {
        "id": 6,
        "category": "Penyelesaian Beda Pendapat",
        "question": "Kalau lagi beda pendapat soal hal penting, gimana cara kalian menyelesaikannya?",
        "options": [
            "Diskusi dingin pakai logika sampai ketemu jalan tengah.",
            "Ngalah dulu dan ikutin mau partner demi kedamaian.",
            "Masing-masing ungkapin perasaan jujur tanpa ditutup-tutupi.",
            "Ambil waktu istirahat sebentar, baru evaluasi bareng kemudian.",
        ],
    },
    {
        "id": 7,
        "category": "Hal Ilfil / Red Flag",
        "question": "Sikap atau kebiasaan apa yang paling bisa bikin kamu ilfil sama partner?",
        "options": [
            "Ga jujur / suka bohong walau untuk hal sepele.",
            "Sikap kasar, tidak sopan, atau kurang menghargai orang lain.",
            "Cuek banget / ga ada kabar seharian tanpa kejelasan.",
            "Posesif berlebihan dan terlalu mengekang kebebasan.",
        ],
    },
    {
        "id": 8,
        "category": "Personal Space & Me Time",
        "question": "Gimana pandangan kamu soal kesibukan & 'me time' masing-masing?",
        "options": [
            "Sangat penting! Masing-masing harus punya ruang & mimpi.",
            "Penting, tapi tetap wajib rajin kasih update kabar.",
            "Pengennya selalu nempel berdua setiap ada waktu luang.",
            "Fleksibel aja, menyesuaikan ritme kesibukan masing-masing.",
        ],
    },
    {
        "id": 9,
        "category": "Kebanggaan pada Partner",
        "question": "Hal apa yang paling bikin kamu merasa paling bangga punya partner seperti dia?",
        "options": [
            "Sifatnya yang dewasa, sabar, dan selalu mendukung mimpiku.",
            "Kelakuannya yang lucu, humoris, dan selalu bikin tersenyum.",
            "Pekerja keras, bertanggung jawab, dan punya visi jelas.",
            "Perhatian detail dan selalu ingat hal-hal kecil tentangku.",
        ],
    },
    {
        "id": 10,
        "category": "Visi Hubungan Masa Depan",
        "question": "Impian terbesar untuk arah hubungan kalian di masa depan?",
        "options": [
            "Tumbuh bareng jadi versi terbaik & sukses bersama.",
            "Punya hubungan yang tenang, harmonis, & bebas drama.",
            "Bisa keliling dunia / petualangan bareng menikmati hidup.",
            "Menuju jenjang yang lebih serius & membangun masa depan.",
        ],
    },
]


def calculate_quiz_match(host_answers, partner_answers):
    """
    Menghitung persentase kecocokan jawaban antara Host & Partner (0-100%)
    """
    if (
        not host_answers
        or not partner_answers
        or len(host_answers) != len(partner_answers)
    ):
        return 50, []
    exact_matches = 0
    breakdown = []
    for i in range(len(host_answers)):
        q = PARTNER_QUIZ_QUESTIONS[i]
        h_idx = int(host_answers[i])
        p_idx = int(partner_answers[i])
        is_match = h_idx == p_idx
        if is_match:
            exact_matches += 1
        breakdown.append(
            {
                "question_id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "host_answer": (
                    q["options"][h_idx] if 0 <= h_idx < len(q["options"]) else "-"
                ),
                "partner_answer": (
                    q["options"][p_idx] if 0 <= p_idx < len(q["options"]) else "-"
                ),
                "is_match": is_match,
            }
        )
    total_q = len(PARTNER_QUIZ_QUESTIONS)
    match_score = int(round((exact_matches / total_q) * 100))
    final_score = max(40, match_score)
    return final_score, breakdown


def get_ai_couple_quiz_analysis(
    host_name, host_sign, partner_name, partner_sign, match_score, breakdown
):
    """
    Memanggil AI OpenRouter untuk membuat ulasan kecocokan pasangan yang seru, Gen Z, hangat, dan kocak
    berdasarkan zodiak & hasil 10 jawaban quiz.
    """
    from .data import ZODIAC_DATA

    h_sign_name = ZODIAC_DATA.get(host_sign.lower(), {}).get(
        "name", host_sign.capitalize()
    )
    p_sign_name = ZODIAC_DATA.get(partner_sign.lower(), {}).get(
        "name", partner_sign.capitalize()
    )
    matches_count = sum(1 for b in breakdown if b["is_match"])
    diff_count = len(breakdown) - matches_count
    same_answers_str = (
        ", ".join(
            [
                f"'{b['category']}': {b['host_answer']}"
                for b in breakdown
                if b["is_match"]
            ][:2]
        )
        or "Banyak kesamaan vibe"
    )
    diff_answers_str = (
        ", ".join(
            [
                f"'{b['category']}': ({host_name}: {b['host_answer']} vs {partner_name}: {b['partner_answer']})"
                for b in breakdown
                if not b["is_match"]
            ][:2]
        )
        or "Saling melengkapi perbedaan"
    )
    api_key = get_openrouter_api_key()
    if not api_key:
        return {
            "verdict": f"Pasangan {h_sign_name} & {p_sign_name} ini punya chemistry yang unik banget!",
            "vibe_headline": f"Kecocokan Vibe {match_score}%: Kombinasi Manis & Penuh Kejutan!",
            "strengths": f"{host_name} dan {partner_name} sama-sama punya pandangan selaras di banyak hal penting.",
            "challenge": f"Perbedaan sudut pandang bisa jadi bumbu penyedap hubungan asalkan tetap saling terbuka.",
            "couple_tip": "Tetap pertahankan komunikasi jujur dan luangkan waktu berkualitas berdua!",
        }
    prompt = f"""Kamu adalah pakar astrologi & relationship consultant Gen Z yang ramah, humoris, cerdas, dan hangat.
Buatkan analisis kecocokan pasangan berikut berdasarkan ZODIAK dan HASIL 10 PERTANYAAN QUIZ PARTNER:
- Host: **{host_name}** ({h_sign_name})
- Partner: **{partner_name}** ({p_sign_name})
- Skor Kembaran Jawaban Quiz: **{match_score}%** ({matches_count} jawaban persis sama, {diff_count} jawaban beda)
- Contoh Kesamaan Jawaban: {same_answers_str}
- Contoh Perbedaan Jawaban: {diff_answers_str}
Buatkan ulasan dalam format JSON valid persis dengan struktur berikut (tanpa teks/markdown lain):
{{ 
  "vibe_headline": "1 kalimat headline paling menarik & kocak tentang dinamika chemistry {host_name} ({h_sign_name}) & {partner_name} ({p_sign_name}).",
  "verdict": "2-3 kalimat ulasan umum chemistry hubungan mereka yang hangat, relatable, dan seru.",
  "strengths": "1-2 kalimat kekuatan utama hubungan mereka dari gabungan zodiak & kecocokan quiz.",
  "challenge": "1-2 kalimat potensi tantangan / hal lucu yang perlu disesuaikan dengan santai.",
  "couple_tip": "1 kalimat tips hubungan paling berharga & manis untuk mereka berdua."
}} """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zodiak-data-asia.local",
        "X-OpenRouter-Title": "Zodiak Data Asia",
    }
    try:
        payload = {
            "model": "google/gemini-2.5-flash-lite",
            "messages": [
                {
                    "role": "system",
                    "content": "Kamu adalah ahli analisis hubungan & astrologi Gen Z yang humoris, hangat, dan komunikatif. Kembalikan respons HANYA dalam format JSON valid.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
        }
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=9,
        )
        if resp.status_code == 200:
            res_data = resp.json()
            content = res_data["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                if content.endswith("```"):
                    content = content.rsplit("```", 1)[0]
                content = content.strip()
            if content.startswith("json"):
                content = content[4:].strip()
            parsed = json.loads(content)
            if all(
                k in parsed
                for k in [
                    "vibe_headline",
                    "verdict",
                    "strengths",
                    "challenge",
                    "couple_tip",
                ]
            ):
                increment_ai_quota()
                return parsed
    except Exception:
        pass
    return {
        "vibe_headline": f"Kecocokan Vibe {match_score}%: Kombinasi {h_sign_name} & {p_sign_name} Yang Seru!",
        "verdict": f"{host_name} dan {partner_name} punya daya tarik kosmik yang unik. Perpaduan karakter {h_sign_name} dan {p_sign_name} bikin hubungan gak pernah ngebosenin!",
        "strengths": f"Kalian sama-sama punya kecocokan jawaban di {matches_count} aspek penting dalam hubungan.",
        "challenge": "Perbedaan persepsi kecil justru bikin kalian saling melengkapi satu sama lain.",
        "couple_tip": "Terus luangkan waktu berkualitas berdua dan selalu apresiasi hal-hal kecil!",
    }
