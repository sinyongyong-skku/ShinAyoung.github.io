import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path
import base64

# ── 앱 이름 ───────────────────────────────────────────────────────────
APP_NAME = "Bloomy"
APP_SUB  = "작은 습관이 나를 피우는 중 🌸"

# ── 데이터 저장 경로 ──────────────────────────────────────────────────
DATA_DIR = Path("bloomy_data")
DATA_DIR.mkdir(exist_ok=True)
PROFILE_FILE = DATA_DIR / "profile.json"
WEIGHT_FILE  = DATA_DIR / "weight_log.json"
MEAL_FILE    = DATA_DIR / "meal_log.json"

def load_json(path):
    if path.exists():
        try: return json.loads(path.read_text(encoding="utf-8"))
        except: return {}
    return {}

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── 매일 달라지는 좋은 말 (날짜 기반) ───────────────────────────────
QUOTES = [
    {"text": "오늘 하루도 나를 위해 살아가는 것, 그것으로 충분해요.", "author": "오늘의 Bloomy", "emoji": "🌸"},
    {"text": "완벽하지 않아도 괜찮아요. 어제보다 조금 나아진 오늘이면 돼요.", "author": "오늘의 Bloomy", "emoji": "🌱"},
    {"text": "네 몸은 네가 생각하는 것보다 훨씬 더 강해요.", "author": "오늘의 Bloomy", "emoji": "💪"},
    {"text": "The secret of getting ahead is getting started.", "author": "Mark Twain", "emoji": "✨"},
    {"text": "작은 변화들이 모여 큰 기적이 돼요.", "author": "오늘의 Bloomy", "emoji": "🦋"},
    {"text": "Take care of your body. It's the only place you have to live.", "author": "Jim Rohn", "emoji": "🏡"},
    {"text": "오늘 먹은 것이 내일의 나를 만들어요.", "author": "오늘의 Bloomy", "emoji": "🥗"},
    {"text": "비교하지 마세요. 어제의 나와만 비교하면 돼요.", "author": "오늘의 Bloomy", "emoji": "🪞"},
    {"text": "Progress, not perfection.", "author": "오늘의 Bloomy", "emoji": "📈"},
    {"text": "당신이 포기하지 않는 한, 실패는 없어요.", "author": "오늘의 Bloomy", "emoji": "🌟"},
    {"text": "건강은 목적지가 아니라 여정이에요.", "author": "오늘의 Bloomy", "emoji": "🛤️"},
    {"text": "You don't have to be great to start, but you have to start to be great.", "author": "Zig Ziglar", "emoji": "🚀"},
    {"text": "오늘 하루를 버텨준 나에게 박수 👏", "author": "오늘의 Bloomy", "emoji": "👏"},
    {"text": "몸이 힘들 때일수록 마음을 먼저 토닥여줘요.", "author": "오늘의 Bloomy", "emoji": "🤍"},
    {"text": "Your body hears everything your mind says.", "author": "Naomi Judd", "emoji": "🧠"},
    {"text": "천천히 가도 괜찮아요. 멈추지만 않으면 돼요.", "author": "오늘의 Bloomy", "emoji": "🐢"},
    {"text": "오늘의 땀이 내일의 자신감이 돼요.", "author": "오늘의 Bloomy", "emoji": "💧"},
    {"text": "Believe in yourself and all that you are.", "author": "Christian D. Larson", "emoji": "🌈"},
    {"text": "꽃이 피려면 비가 필요하듯, 변화에는 노력이 필요해요.", "author": "오늘의 Bloomy", "emoji": "🌺"},
    {"text": "나를 사랑하는 것이 다이어트의 시작이에요.", "author": "오늘의 Bloomy", "emoji": "💗"},
    {"text": "오늘 잘 먹고 잘 자고 잘 움직인 당신, 최고예요.", "author": "오늘의 Bloomy", "emoji": "⭐"},
    {"text": "It always seems impossible until it's done.", "author": "Nelson Mandela", "emoji": "🏆"},
    {"text": "한 걸음씩, 한 끼씩, 한 숨씩.", "author": "오늘의 Bloomy", "emoji": "👣"},
    {"text": "내 몸은 내 가장 소중한 집이에요.", "author": "오늘의 Bloomy", "emoji": "🏠"},
    {"text": "변화는 하루아침에 오지 않지만, 매일 오고 있어요.", "author": "오늘의 Bloomy", "emoji": "🌅"},
    {"text": "You are stronger than you think.", "author": "오늘의 Bloomy", "emoji": "💎"},
    {"text": "오늘 하루를 선물처럼 사용해요.", "author": "오늘의 Bloomy", "emoji": "🎁"},
    {"text": "건강한 몸에 건강한 마음이 깃들어요.", "author": "오늘의 Bloomy", "emoji": "🧘"},
    {"text": "포기하고 싶을 때가 가장 가까운 순간이에요.", "author": "오늘의 Bloomy", "emoji": "🔆"},
    {"text": "Every day is a fresh start.", "author": "오늘의 Bloomy", "emoji": "🌤️"},
    {"text": "작은 나를 응원해요, 매일매일.", "author": "오늘의 Bloomy", "emoji": "📣"},
    {"text": "오늘도 여기까지 온 나, 정말 대단해요.", "author": "오늘의 Bloomy", "emoji": "🎖️"},
    {"text": "물 한 잔이 몸을 살려요. 지금 마셔봐요 💧", "author": "오늘의 Bloomy", "emoji": "💧"},
    {"text": "완벽한 식단보다 지속 가능한 식단이 더 좋아요.", "author": "오늘의 Bloomy", "emoji": "🥦"},
    {"text": "잠을 잘 자는 것도 다이어트예요.", "author": "오늘의 Bloomy", "emoji": "🌙"},
    {"text": "Rest when you're weary. Refresh and renew yourself.", "author": "오늘의 Bloomy", "emoji": "🛌"},
    {"text": "나의 속도로, 나의 방식으로.", "author": "오늘의 Bloomy", "emoji": "🎵"},
    {"text": "오늘의 선택이 한 달 후의 나를 만들어요.", "author": "오늘의 Bloomy", "emoji": "📅"},
    {"text": "You've got this. 할 수 있어요!", "author": "오늘의 Bloomy", "emoji": "🤜"},
    {"text": "꾸준함이 재능을 이겨요.", "author": "오늘의 Bloomy", "emoji": "🏅"},
    {"text": "오늘 하루 수고했어요. 정말로.", "author": "오늘의 Bloomy", "emoji": "🫶"},
    {"text": "건강해지는 과정을 즐겨요, 결과만 보지 말고.", "author": "오늘의 Bloomy", "emoji": "🎠"},
    {"text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "emoji": "⏰"},
    {"text": "내 몸에게 오늘도 고마워요.", "author": "오늘의 Bloomy", "emoji": "🙏"},
    {"text": "행복한 마음이 건강한 몸을 만들어요.", "author": "오늘의 Bloomy", "emoji": "😊"},
    {"text": "숫자에 집착하지 마요. 느낌을 봐요.", "author": "오늘의 Bloomy", "emoji": "🎈"},
    {"text": "오늘 하루 딱 한 가지만 잘하면 충분해요.", "author": "오늘의 Bloomy", "emoji": "☝️"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "emoji": "🌊"},
    {"text": "나를 위한 선택을 해요. 남이 아닌 나를 위해.", "author": "오늘의 Bloomy", "emoji": "💝"},
    {"text": "봄이 오듯, 변화도 반드시 와요.", "author": "오늘의 Bloomy", "emoji": "🌷"},
    {"text": "조급해하지 마요. 꽃은 강요한다고 피지 않아요.", "author": "오늘의 Bloomy", "emoji": "🌸"},
    {"text": "내가 나를 응원하는 것이 가장 강한 동력이에요.", "author": "오늘의 Bloomy", "emoji": "🔥"},
    {"text": "오늘의 나는 어제보다 분명히 성장했어요.", "author": "오늘의 Bloomy", "emoji": "📊"},
    {"text": "Eat well, move often, sleep enough, repeat.", "author": "오늘의 Bloomy", "emoji": "🔄"},
    {"text": "힘든 날도 괜찮아요. 내일 다시 시작하면 돼요.", "author": "오늘의 Bloomy", "emoji": "🌙"},
    {"text": "나는 매일 조금씩 더 나아지고 있어요.", "author": "오늘의 Bloomy", "emoji": "🌱"},
    {"text": "Your health is an investment, not an expense.", "author": "오늘의 Bloomy", "emoji": "💰"},
    {"text": "오늘 마신 물 한 잔이 피부를 빛나게 해요.", "author": "오늘의 Bloomy", "emoji": "✨"},
    {"text": "몸을 사랑하는 방식으로 움직여요.", "author": "오늘의 Bloomy", "emoji": "💃"},
    {"text": "결과가 보이지 않아도, 변화는 이미 시작됐어요.", "author": "오늘의 Bloomy", "emoji": "🌿"},
    {"text": "오늘도 여기 있는 당신이 자랑스러워요.", "author": "오늘의 Bloomy", "emoji": "🌟"},
]

# 귀여운 SVG 일러스트 (날짜마다 다른 그림)
ILLUSTRATIONS = [
    # 꽃
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <circle cx="60" cy="60" r="18" fill="#FFB7C5"/>
      <ellipse cx="60" cy="32" rx="10" ry="16" fill="#FFD6E0" opacity="0.9"/>
      <ellipse cx="60" cy="88" rx="10" ry="16" fill="#FFD6E0" opacity="0.9"/>
      <ellipse cx="32" cy="60" rx="16" ry="10" fill="#FFD6E0" opacity="0.9"/>
      <ellipse cx="88" cy="60" rx="16" ry="10" fill="#FFD6E0" opacity="0.9"/>
      <ellipse cx="40" cy="40" rx="10" ry="16" fill="#FFC2D1" opacity="0.8" transform="rotate(45 40 40)"/>
      <ellipse cx="80" cy="40" rx="10" ry="16" fill="#FFC2D1" opacity="0.8" transform="rotate(-45 80 40)"/>
      <ellipse cx="40" cy="80" rx="10" ry="16" fill="#FFC2D1" opacity="0.8" transform="rotate(-45 40 80)"/>
      <ellipse cx="80" cy="80" rx="10" ry="16" fill="#FFC2D1" opacity="0.8" transform="rotate(45 80 80)"/>
      <circle cx="60" cy="60" r="12" fill="#FFF0F5"/>
      <circle cx="56" cy="57" r="2.5" fill="#FFB7C5"/>
      <circle cx="64" cy="57" r="2.5" fill="#FFB7C5"/>
      <circle cx="60" cy="64" r="2" fill="#FFB7C5"/>
    </svg>""",
    # 새싹
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <rect x="57" y="60" width="6" height="40" rx="3" fill="#8DBE8D"/>
      <ellipse cx="60" cy="55" rx="22" ry="28" fill="#B8DABA" opacity="0.85"/>
      <ellipse cx="42" cy="65" rx="18" ry="22" fill="#A8D4A8" opacity="0.7" transform="rotate(-20 42 65)"/>
      <ellipse cx="78" cy="65" rx="18" ry="22" fill="#A8D4A8" opacity="0.7" transform="rotate(20 78 65)"/>
      <ellipse cx="60" cy="38" rx="12" ry="16" fill="#D4EED4" opacity="0.9"/>
      <circle cx="52" cy="58" r="3" fill="#fff" opacity="0.4"/>
      <circle cx="68" cy="48" r="2" fill="#fff" opacity="0.4"/>
    </svg>""",
    # 별
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <polygon points="60,18 68,45 97,45 74,62 82,89 60,73 38,89 46,62 23,45 52,45" fill="#FFD6A5"/>
      <polygon points="60,28 66,46 85,46 71,57 76,75 60,64 44,75 49,57 35,46 54,46" fill="#FFE8C2"/>
      <circle cx="60" cy="55" r="8" fill="#FFF4E0"/>
      <circle cx="32" cy="30" r="5" fill="#FFD6E0" opacity="0.7"/>
      <circle cx="88" cy="28" r="4" fill="#FFD6E0" opacity="0.6"/>
      <circle cx="22" cy="75" r="3" fill="#C8E6C9" opacity="0.7"/>
      <circle cx="98" cy="80" r="4" fill="#C8E6C9" opacity="0.6"/>
    </svg>""",
    # 나비
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="38" cy="48" rx="28" ry="20" fill="#F8C8D4" opacity="0.85" transform="rotate(-20 38 48)"/>
      <ellipse cx="82" cy="48" rx="28" ry="20" fill="#F8C8D4" opacity="0.85" transform="rotate(20 82 48)"/>
      <ellipse cx="40" cy="75" rx="20" ry="16" fill="#FFD6E0" opacity="0.75" transform="rotate(15 40 75)"/>
      <ellipse cx="80" cy="75" rx="20" ry="16" fill="#FFD6E0" opacity="0.75" transform="rotate(-15 80 75)"/>
      <ellipse cx="60" cy="60" rx="5" ry="22" fill="#8B7B8B" opacity="0.6"/>
      <circle cx="60" cy="38" r="5" fill="#6B5B6B" opacity="0.7"/>
      <line x1="55" y1="36" x2="42" y2="22" stroke="#6B5B6B" stroke-width="1.5" opacity="0.6"/>
      <line x1="65" y1="36" x2="78" y2="22" stroke="#6B5B6B" stroke-width="1.5" opacity="0.6"/>
      <circle cx="42" cy="22" r="2" fill="#FFB7C5"/>
      <circle cx="78" cy="22" r="2" fill="#FFB7C5"/>
    </svg>""",
    # 무지개
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <path d="M15 80 Q60 20 105 80" stroke="#FFB3BA" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M22 80 Q60 28 98 80" stroke="#FFD6A5" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M29 80 Q60 36 91 80" stroke="#FFF0A5" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M36 80 Q60 44 84 80" stroke="#C8E6C9" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M43 80 Q60 52 77 80" stroke="#B3D9FF" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M50 80 Q60 60 70 80" stroke="#D4B3FF" stroke-width="8" fill="none" stroke-linecap="round"/>
      <circle cx="30" cy="90" r="10" fill="white" opacity="0.9"/>
      <circle cx="25" cy="88" r="8" fill="white" opacity="0.9"/>
      <circle cx="90" cy="90" r="10" fill="white" opacity="0.9"/>
      <circle cx="95" cy="88" r="8" fill="white" opacity="0.9"/>
    </svg>""",
    # 달과 별
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <circle cx="55" cy="60" r="28" fill="#FFE4A0"/>
      <circle cx="68" cy="52" r="22" fill="#FFF4E0"/>
      <circle cx="30" cy="30" r="4" fill="#FFD6A5" opacity="0.8"/>
      <circle cx="90" cy="25" r="3" fill="#FFD6A5" opacity="0.7"/>
      <circle cx="95" cy="70" r="4" fill="#FFD6A5" opacity="0.6"/>
      <circle cx="20" cy="80" r="3" fill="#FFD6A5" opacity="0.7"/>
      <polygon points="85,45 87,51 93,51 88,55 90,61 85,57 80,61 82,55 77,51 83,51" fill="#FFE4A0" opacity="0.9"/>
      <polygon points="25,50 26,54 30,54 27,57 28,61 25,58 22,61 23,57 20,54 24,54" fill="#FFE4A0" opacity="0.8"/>
    </svg>""",
    # 물방울
    """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
      <path d="M60 20 Q85 50 85 70 Q85 92 60 92 Q35 92 35 70 Q35 50 60 20Z" fill="#ADE8F4" opacity="0.85"/>
      <path d="M60 30 Q78 55 78 68 Q78 84 60 84 Q42 84 42 68 Q42 55 60 30Z" fill="#CAF0F8" opacity="0.7"/>
      <ellipse cx="50" cy="55" rx="6" ry="10" fill="white" opacity="0.35" transform="rotate(-20 50 55)"/>
      <circle cx="42" cy="35" r="6" fill="#ADE8F4" opacity="0.6"/>
      <circle cx="85" cy="40" r="5" fill="#B5EAF5" opacity="0.5"/>
      <circle cx="30" cy="70" r="4" fill="#ADE8F4" opacity="0.5"/>
    </svg>""",
]

def get_today_quote():
    day_of_year = date.today().timetuple().tm_yday
    return QUOTES[day_of_year % len(QUOTES)]

def get_today_illustration():
    day_of_year = date.today().timetuple().tm_yday
    return ILLUSTRATIONS[day_of_year % len(ILLUSTRATIONS)]

def calc_bmi(weight, height_cm):
    h = height_cm / 100
    return round(weight / (h * h), 1)

def bmi_label(bmi):
    if bmi < 18.5: return "저체중", "#74B9FF"
    elif bmi < 23:  return "정상", "#55EFC4"
    elif bmi < 25:  return "과체중", "#FDCB6E"
    else:           return "비만", "#FF7675"

def can_record_weight(weight_log):
    """1주일에 한 번만 기록 가능 여부"""
    if not weight_log: return True, 0
    last_date_str = sorted(weight_log.keys())[-1]
    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
    days_since = (date.today() - last_date).days
    if days_since >= 7: return True, 0
    return False, 7 - days_since

# ── 페이지 설정 ───────────────────────────────────────────────────────
st.set_page_config(page_title=APP_NAME, page_icon="🌸", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Nunito',sans-serif!important;}
#MainMenu,header,footer{visibility:hidden;}
.stApp{background:linear-gradient(160deg,#FFF5F8 0%,#F0FFF4 50%,#FFF5F8 100%);}

/* 헤더 */
.app-header{text-align:center;padding:28px 0 8px;}
.app-logo{font-size:38px;margin-bottom:4px;}
.app-name{font-size:28px;font-weight:700;color:#D4829A;letter-spacing:-0.5px;}
.app-sub{font-size:13px;color:#A8C5A0;margin-top:2px;}

/* 오늘의 명언 카드 */
.quote-card{
    background:linear-gradient(135deg,#FFF0F5 0%,#F0FFF4 100%);
    border-radius:20px;border:1.5px solid #F8C8D8;
    padding:28px 24px;text-align:center;margin-bottom:20px;
    box-shadow:0 4px 20px rgba(212,130,154,0.12);
}
.quote-illust{display:flex;justify-content:center;margin-bottom:14px;}
.quote-illust svg{width:90px;height:90px;}
.quote-date{font-size:11px;color:#C4A0B0;margin-bottom:8px;letter-spacing:0.05em;}
.quote-text{font-size:16px;font-weight:600;color:#5A4060;line-height:1.65;margin-bottom:8px;}
.quote-author{font-size:12px;color:#C4A0B0;}
.quote-emoji{font-size:28px;margin-bottom:8px;display:block;}

/* 섹션 카드 */
.section-card{
    background:white;border-radius:18px;
    border:1.5px solid #F0E8F0;padding:22px 20px;
    margin-bottom:16px;box-shadow:0 2px 12px rgba(180,160,200,0.08);
}
.section-title{font-size:16px;font-weight:700;color:#5A4060;margin-bottom:4px;}
.section-sub{font-size:12px;color:#B0A0B8;margin-bottom:16px;}

/* 프로필 정보 */
.profile-row{display:flex;gap:10px;margin-bottom:12px;}
.profile-item{flex:1;background:#FFF5F8;border-radius:12px;padding:14px;text-align:center;border:1px solid #F8C8D8;}
.profile-val{font-size:20px;font-weight:700;color:#D4829A;}
.profile-lbl{font-size:11px;color:#C4A0B0;margin-top:2px;}

/* BMI 뱃지 */
.bmi-badge{display:inline-block;padding:4px 14px;border-radius:99px;font-size:12px;font-weight:600;}

/* 체중 기록 */
.weight-entry{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#FFF8FC;border-radius:10px;margin-bottom:6px;border:1px solid #F0E0EA;}
.w-date{font-size:12px;color:#B0A0B8;}
.w-val{font-size:15px;font-weight:700;color:#D4829A;}
.w-change-up{font-size:11px;color:#FF7675;font-weight:600;}
.w-change-down{font-size:11px;color:#55EFC4;font-weight:600;}
.w-change-same{font-size:11px;color:#B0A0B8;}

/* 식사 기록 */
.meal-entry{background:#F8FFF8;border-radius:12px;padding:14px;margin-bottom:10px;border:1px solid #D4EDD4;}
.meal-header{display:flex;justify-content:space-between;margin-bottom:6px;}
.meal-date{font-size:11px;color:#A0C0A0;}
.meal-type{font-size:12px;font-weight:600;color:#6DAA6D;}
.meal-note{font-size:13px;color:#5A7A5A;line-height:1.5;}
.meal-img{width:100%;border-radius:10px;margin-top:8px;max-height:220px;object-fit:cover;}

/* 잠금 배너 */
.lock-banner{background:linear-gradient(135deg,#FFF0F5,#F5F0FF);border-radius:14px;padding:20px;text-align:center;border:1.5px dashed #D4B0D4;}
.lock-icon{font-size:32px;margin-bottom:8px;}
.lock-text{font-size:14px;font-weight:600;color:#9070A0;}
.lock-sub{font-size:12px;color:#C0A0C8;margin-top:4px;}

/* 목표 달성률 */
.goal-bar-wrap{background:#F5EDF5;border-radius:99px;height:12px;margin:8px 0;}
.goal-bar{height:12px;border-radius:99px;background:linear-gradient(90deg,#FFB7C5,#D4829A);}

/* 버튼 */
.stButton>button{
    background:linear-gradient(135deg,#F8A0B8,#D4829A)!important;
    color:white!important;border:none!important;border-radius:12px!important;
    font-family:'Nunito',sans-serif!important;font-size:14px!important;
    font-weight:600!important;padding:10px 20px!important;
    box-shadow:0 3px 12px rgba(212,130,154,0.3)!important;
}
.stButton>button:hover{background:linear-gradient(135deg,#F490A8,#C47288)!important;}

/* 입력 */
.stTextInput>div>div>input,.stTextArea textarea,.stNumberInput>div>div>input{
    border:1.5px solid #F0D8E8!important;border-radius:10px!important;
    background:#FFFAFD!important;font-family:'Nunito',sans-serif!important;
    font-size:14px!important;color:#5A4060!important;
}
.stTextInput label,.stTextArea label,.stNumberInput label,.stSelectbox label{
    color:#9070A0!important;font-size:13px!important;font-weight:600!important;
}
.stSelectbox>div>div{
    border:1.5px solid #F0D8E8!important;border-radius:10px!important;
    background:#FFFAFD!important;color:#5A4060!important;
}
.stTabs [data-baseweb="tab-list"]{gap:6px;background:transparent;}
.stTabs [data-baseweb="tab"]{
    font-family:'Nunito',sans-serif!important;font-size:13px!important;
    font-weight:600!important;color:#C4A0B8!important;
    padding:8px 18px!important;border-radius:10px!important;background:#FFF5F8!important;
}
.stTabs [aria-selected="true"]{background:#F8C8D8!important;color:#D4829A!important;}
.stFileUploader>div{border:1.5px dashed #F0D8E8!important;border-radius:12px!important;background:#FFFAFD!important;}
.stFileUploader label{color:#9070A0!important;font-size:13px!important;font-weight:600!important;}
.stRadio label{color:#7A6080!important;font-size:13px!important;}
div[data-testid="stMetricValue"]{color:#D4829A!important;font-family:'Nunito',sans-serif!important;}
</style>
""", unsafe_allow_html=True)

# ── 세션 & 데이터 로드 ────────────────────────────────────────────────
if "profile" not in st.session_state:
    st.session_state.profile = load_json(PROFILE_FILE)
if "weight_log" not in st.session_state:
    st.session_state.weight_log = load_json(WEIGHT_FILE)
if "meal_log" not in st.session_state:
    st.session_state.meal_log = load_json(MEAL_FILE)

# ════════════════════════════════════════════════════════════════════
# 온보딩 — 프로필 없으면 먼저 설정
# ════════════════════════════════════════════════════════════════════
if not st.session_state.profile:
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">🌸</div>
        <div class="app-name">Bloomy</div>
        <div class="app-sub">나만의 건강 다이어리를 시작해봐요</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="quote-card" style="margin-bottom:24px;">
        <span class="quote-emoji">👋</span>
        <div class="quote-text">안녕하세요! 먼저 기본 정보를 알려주세요.<br>딱 한 번만 입력하면 돼요 🌸</div>
    </div>""", unsafe_allow_html=True)

    with st.form("onboarding"):
        nickname = st.text_input("닉네임", placeholder="예: 꽃봉오리, 쭈니, 하루 🌸")
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("키 (cm)", min_value=140.0, max_value=200.0, value=163.0, step=0.5)
            current_weight = st.number_input("현재 몸무게 (kg)", min_value=30.0, max_value=150.0, value=58.0, step=0.1)
        with col2:
            goal_weight = st.number_input("목표 몸무게 (kg)", min_value=30.0, max_value=150.0, value=53.0, step=0.1)
            goal_weeks = st.number_input("목표 기간 (주)", min_value=4, max_value=52, value=12, step=1)

        submitted = st.form_submit_button("🌸 Bloomy 시작하기", use_container_width=True)

        if submitted:
            if not nickname:
                st.warning("닉네임을 입력해주세요!")
            else:
                profile = {
                    "nickname": nickname,
                    "height": height,
                    "start_weight": current_weight,
                    "goal_weight": goal_weight,
                    "goal_weeks": goal_weeks,
                    "start_date": str(date.today()),
                }
                st.session_state.profile = profile
                save_json(PROFILE_FILE, profile)

                # 시작 체중 기록
                weight_log = {str(date.today()): current_weight}
                st.session_state.weight_log = weight_log
                save_json(WEIGHT_FILE, weight_log)

                st.success(f"환영해요, {nickname}님! 🌸 Bloomy가 시작됐어요!")
                st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════
# 메인 앱
# ════════════════════════════════════════════════════════════════════
profile    = st.session_state.profile
weight_log = st.session_state.weight_log
meal_log   = st.session_state.meal_log

# 헤더
st.markdown(f"""
<div class="app-header">
    <div class="app-logo">🌸</div>
    <div class="app-name">Bloomy</div>
    <div class="app-sub">안녕하세요, {profile.get('nickname','친구')}님 🌿</div>
</div>""", unsafe_allow_html=True)

# ── 오늘의 명언 ───────────────────────────────────────────────────────
quote = get_today_quote()
illust = get_today_illustration()
today_str = date.today().strftime("%Y년 %m월 %d일")

st.markdown(f"""
<div class="quote-card">
    <div class="quote-illust">{illust}</div>
    <div class="quote-date">✦ {today_str} 오늘의 메시지 ✦</div>
    <div class="quote-text">"{quote['text']}"</div>
    <div class="quote-author">— {quote['author']}</div>
</div>""", unsafe_allow_html=True)

# ── 탭 ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🏠 홈", "⚖️ 체중", "🥗 식사", "👤 프로필"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — 홈 (요약)
# ════════════════════════════════════════════════════════════════════
with tab1:
    # 현재 체중 & BMI
    sorted_weights = sorted(weight_log.items())
    current_w = sorted_weights[-1][1] if sorted_weights else profile["start_weight"]
    bmi = calc_bmi(current_w, profile["height"])
    bmi_text, bmi_color = bmi_label(bmi)
    goal_w = profile["goal_weight"]
    start_w = profile["start_weight"]

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">나의 현황 ✨</div>
        <div class="profile-row">
            <div class="profile-item">
                <div class="profile-val">{current_w}kg</div>
                <div class="profile-lbl">현재 체중</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{goal_w}kg</div>
                <div class="profile-lbl">목표 체중</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{bmi}</div>
                <div class="profile-lbl">BMI <span class="bmi-badge" style="background:{bmi_color}22;color:{bmi_color};">{bmi_text}</span></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 목표 달성률
    total_to_lose = abs(start_w - goal_w)
    lost_so_far   = abs(start_w - current_w)
    progress = min(int((lost_so_far / total_to_lose * 100) if total_to_lose > 0 else 0), 100)
    remaining = round(abs(current_w - goal_w), 1)

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">목표까지 {remaining}kg 남았어요 🎯</div>
        <div class="section-sub">시작 {start_w}kg → 목표 {goal_w}kg</div>
        <div class="goal-bar-wrap">
            <div class="goal-bar" style="width:{progress}%"></div>
        </div>
        <div style="text-align:right;font-size:12px;color:#D4829A;font-weight:700;margin-top:4px;">{progress}% 달성 🌸</div>
    </div>""", unsafe_allow_html=True)

    # 최근 식사 기록 요약
    today_meals = {k: v for k, v in meal_log.items() if k.startswith(str(date.today()))}
    meal_count  = len(today_meals)
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">오늘의 식사 기록 🥗</div>
        <div class="section-sub">오늘 기록한 식사: {meal_count}끼</div>
        {'<div style="text-align:center;font-size:13px;color:#B0A0B8;padding:12px 0;">아직 오늘 식사를 기록하지 않았어요<br>식사 탭에서 기록해봐요! 🌿</div>' if meal_count == 0 else ''}
    </div>""", unsafe_allow_html=True)

    if today_meals:
        for key, meal in list(today_meals.items())[-2:]:
            mtype = meal.get("type","")
            mnote = meal.get("note","")
            mimg  = meal.get("img_b64","")
            mmime = meal.get("mime","image/jpeg")
            img_html = f'<img class="meal-img" src="data:{mmime};base64,{mimg}"/>' if mimg else ""
            st.markdown(f"""
            <div class="meal-entry">
                <div class="meal-header">
                    <span class="meal-type">{mtype}</span>
                    <span class="meal-date">오늘</span>
                </div>
                <div class="meal-note">{mnote}</div>
                {img_html}
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 2 — 체중 기록 (1주일 1회)
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">⚖️ 체중 기록</div>
        <div class="section-sub">1주일에 딱 한 번만 기록해요 — 매일 재면 오히려 스트레스예요! 🌸</div>
    </div>""", unsafe_allow_html=True)

    can_record, days_left = can_record_weight(weight_log)

    if can_record:
        with st.form("weight_form"):
            new_weight = st.number_input("오늘 몸무게 (kg)", min_value=30.0, max_value=150.0,
                                          value=float(sorted(weight_log.items())[-1][1]) if weight_log else profile["start_weight"],
                                          step=0.1)
            memo = st.text_input("한마디 (선택)", placeholder="예: 이번 주 운동 열심히 했어요! 💪")
            submitted = st.form_submit_button("🌸 기록하기", use_container_width=True)
            if submitted:
                key = str(date.today())
                weight_log[key] = new_weight
                if memo:
                    weight_log[key + "_memo"] = memo
                st.session_state.weight_log = weight_log
                save_json(WEIGHT_FILE, weight_log)
                # 변화량 계산
                sorted_w = [(k, v) for k, v in sorted(weight_log.items()) if not k.endswith("_memo")]
                if len(sorted_w) >= 2:
                    prev_w = sorted_w[-2][1]
                    diff = round(new_weight - prev_w, 1)
                    if diff < 0:
                        st.success(f"🎉 지난 주보다 {abs(diff)}kg 빠졌어요! 정말 잘하고 있어요!")
                    elif diff > 0:
                        st.info(f"💗 {diff}kg 늘었지만 괜찮아요. 다음 주를 기대해봐요!")
                    else:
                        st.info("🌸 지난 주와 같아요. 유지도 대단한 거예요!")
                else:
                    st.success("🌸 첫 체중을 기록했어요!")
                st.rerun()
    else:
        st.markdown(f"""
        <div class="lock-banner">
            <div class="lock-icon">🔒</div>
            <div class="lock-text">다음 기록까지 {days_left}일 남았어요</div>
            <div class="lock-sub">1주일에 한 번 기록하는 게 Bloomy의 특별한 규칙이에요 🌸<br>매일 재는 것보다 훨씬 건강한 방법이에요!</div>
        </div>""", unsafe_allow_html=True)

    # 체중 기록 목록
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:15px;font-weight:700;color:#5A4060;margin-bottom:10px;">📈 체중 변화 기록</div>', unsafe_allow_html=True)

    sorted_w = [(k, v) for k, v in sorted(weight_log.items(), reverse=True) if not k.endswith("_memo")]
    if not sorted_w:
        st.markdown('<div style="text-align:center;color:#C4A0B0;font-size:13px;padding:20px;">아직 기록이 없어요</div>', unsafe_allow_html=True)
    else:
        for idx, (wdate, wval) in enumerate(sorted_w):
            memo_key = wdate + "_memo"
            memo_txt = weight_log.get(memo_key, "")
            # 변화량
            if idx < len(sorted_w) - 1:
                prev_val = sorted_w[idx + 1][1]
                diff = round(wval - prev_val, 1)
                if diff < 0:
                    change_html = f'<span class="w-change-down">▼ {abs(diff)}kg</span>'
                elif diff > 0:
                    change_html = f'<span class="w-change-up">▲ {diff}kg</span>'
                else:
                    change_html = '<span class="w-change-same">— 유지</span>'
            else:
                change_html = '<span class="w-change-same">시작</span>'
            d = datetime.strptime(wdate, "%Y-%m-%d").strftime("%Y.%m.%d")
            memo_html = f'<div style="font-size:11px;color:#A0C0A0;margin-top:3px;">{memo_txt}</div>' if memo_txt else ""
            st.markdown(f"""
            <div class="weight-entry">
                <div>
                    <div class="w-date">{d}</div>
                    {memo_html}
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    {change_html}
                    <div class="w-val">{wval}kg</div>
                </div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 3 — 식사 기록 (매일 자유롭게)
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">🥗 식사 기록</div>
        <div class="section-sub">매일 자유롭게 기록해요 — 사진과 한마디로 나만의 식사 일기!</div>
    </div>""", unsafe_allow_html=True)

    with st.form("meal_form"):
        meal_type = st.selectbox("식사 종류", ["🌅 아침", "☀️ 점심", "🌙 저녁", "🍪 간식", "☕ 음료"])
        meal_note = st.text_area("오늘 뭐 먹었어요?", placeholder="예: 현미밥에 된장국, 샐러드 먹었어요! 생각보다 맛있었어요 😋", height=90)
        meal_photo = st.file_uploader("사진 첨부 (선택)", type=["jpg","jpeg","png"])
        meal_submit = st.form_submit_button("🌸 기록하기", use_container_width=True)

        if meal_submit:
            now_key = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            entry = {
                "type": meal_type,
                "note": meal_note,
                "img_b64": "",
                "mime": "",
                "time": datetime.now().strftime("%Y.%m.%d %H:%M"),
            }
            if meal_photo:
                entry["img_b64"] = base64.b64encode(meal_photo.read()).decode()
                ext = meal_photo.name.split(".")[-1].lower()
                entry["mime"] = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            meal_log[now_key] = entry
            st.session_state.meal_log = meal_log
            save_json(MEAL_FILE, meal_log)
            st.success("🌿 식사 기록이 저장됐어요!")
            st.rerun()

    # 식사 기록 목록
    st.markdown('<div style="font-size:15px;font-weight:700;color:#5A4060;margin:16px 0 10px;">📔 식사 일기</div>', unsafe_allow_html=True)

    filter_date = st.date_input("날짜 선택", value=date.today())
    filter_str  = str(filter_date)
    filtered_meals = {k: v for k, v in sorted(meal_log.items(), reverse=True) if k.startswith(filter_str)}

    if not filtered_meals:
        st.markdown('<div style="text-align:center;color:#C4A0B0;font-size:13px;padding:24px;">이 날의 식사 기록이 없어요 🌿</div>', unsafe_allow_html=True)
    else:
        for key, meal in filtered_meals.items():
            img_html = ""
            if meal.get("img_b64"):
                img_html = f'<img class="meal-img" src="data:{meal["mime"]};base64,{meal["img_b64"]}"/>'
            st.markdown(f"""
            <div class="meal-entry">
                <div class="meal-header">
                    <span class="meal-type">{meal.get('type','')}</span>
                    <span class="meal-date">{meal.get('time','')}</span>
                </div>
                <div class="meal-note">{meal.get('note','')}</div>
                {img_html}
            </div>""", unsafe_allow_html=True)

            del_col = st.columns([5,1])[1]
            with del_col:
                if st.button("삭제", key=f"del_meal_{key}"):
                    del meal_log[key]
                    st.session_state.meal_log = meal_log
                    save_json(MEAL_FILE, meal_log)
                    st.rerun()

# ════════════════════════════════════════════════════════════════════
# TAB 4 — 프로필
# ════════════════════════════════════════════════════════════════════
with tab4:
    sorted_weights_all = [(k,v) for k,v in sorted(weight_log.items()) if not k.endswith("_memo")]
    current_w_now = sorted_weights_all[-1][1] if sorted_weights_all else profile["start_weight"]
    bmi_now = calc_bmi(current_w_now, profile["height"])
    bmi_text_now, bmi_color_now = bmi_label(bmi_now)

    st.markdown(f"""
    <div class="section-card" style="text-align:center;">
        <div style="font-size:48px;margin-bottom:8px;">🌸</div>
        <div style="font-size:20px;font-weight:700;color:#D4829A;">{profile.get('nickname','나')}님</div>
        <div style="font-size:12px;color:#C4A0B0;margin-top:4px;">Bloomy 시작일: {profile.get('start_date','')}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">기본 정보</div>
        <div class="profile-row">
            <div class="profile-item">
                <div class="profile-val">{profile['height']}cm</div>
                <div class="profile-lbl">키</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{current_w_now}kg</div>
                <div class="profile-lbl">현재 체중</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{bmi_now}</div>
                <div class="profile-lbl">BMI</div>
            </div>
        </div>
        <div style="text-align:center;margin-top:4px;">
            <span class="bmi-badge" style="background:{bmi_color_now}22;color:{bmi_color_now};font-size:13px;padding:5px 16px;">{bmi_text_now}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">목표 설정 🎯</div>
        <div class="profile-row">
            <div class="profile-item">
                <div class="profile-val">{profile['start_weight']}kg</div>
                <div class="profile-lbl">시작 체중</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{profile['goal_weight']}kg</div>
                <div class="profile-lbl">목표 체중</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{profile['goal_weeks']}주</div>
                <div class="profile-lbl">목표 기간</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 통계
    total_meals = len([k for k in meal_log.keys()])
    total_weight_records = len(sorted_weights_all)
    start_date = datetime.strptime(profile.get("start_date", str(date.today())), "%Y-%m-%d").date()
    days_running = (date.today() - start_date).days + 1

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">나의 기록 통계 📊</div>
        <div class="profile-row">
            <div class="profile-item">
                <div class="profile-val">{days_running}일</div>
                <div class="profile-lbl">Bloomy와 함께한 날</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{total_meals}끼</div>
                <div class="profile-lbl">식사 기록</div>
            </div>
            <div class="profile-item">
                <div class="profile-val">{total_weight_records}회</div>
                <div class="profile-lbl">체중 기록</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 프로필 초기화
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with st.expander("⚙️ 설정"):
        st.warning("아래 버튼을 누르면 모든 데이터가 삭제돼요. 신중하게 눌러주세요!")
        if st.button("🗑 처음부터 다시 시작", use_container_width=True):
            for f in [PROFILE_FILE, WEIGHT_FILE, MEAL_FILE]:
                if f.exists(): f.unlink()
            st.session_state.clear()
            st.rerun()

st.markdown("""
<div style="text-align:center;font-size:11px;color:#C4A0B0;margin-top:40px;padding-bottom:20px;">
    Bloomy 🌸 · 작은 습관이 나를 피우는 중 · SKKU Art Project
</div>""", unsafe_allow_html=True)
