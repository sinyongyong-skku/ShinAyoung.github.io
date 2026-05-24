import streamlit as st
import requests

# ── 앱 이름 설정 (여기만 바꾸면 전체 반영) ──────────────────────────
APP_NAME = "Nourish"
APP_TAGLINE = "wholesome ingredients, honest recipes"

# ── 페이지 설정 ───────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 전역 CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* 배경 */
.stApp { background-color: #F7F5F0; }

/* 상단 Streamlit 기본 헤더 숨김 */
#MainMenu, header, footer { visibility: hidden; }

/* 네비게이션 바 */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 14px;
    border-bottom: 1px solid #E2DDD4;
    margin-bottom: 36px;
}
.nav-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 24px;
    color: #2C3A1E;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-logo-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #4A7C3F;
    display: inline-block;
}
.nav-tagline {
    font-size: 12px;
    color: #8A9980;
    letter-spacing: 0.06em;
    font-style: italic;
}

/* 히어로 섹션 */
.hero-section {
    background: #EEF0E8;
    border-radius: 16px;
    padding: 40px 36px;
    margin-bottom: 32px;
    border: 1px solid #DDE0D4;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    color: #4A7C3F;
    margin-bottom: 8px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: #2C3A1E;
    line-height: 1.25;
    margin-bottom: 10px;
}
.hero-sub {
    font-size: 15px;
    color: #6B7A60;
    margin-bottom: 0;
    line-height: 1.6;
}

/* 섹션 헤더 */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #2C3A1E;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 13px;
    color: #8A9980;
    margin-bottom: 20px;
}

/* 식재료 카드 */
.ingr-card {
    background: #FFFFFF;
    border: 1px solid #E2DDD4;
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    height: 100%;
}
.ingr-card:hover {
    border-color: #4A7C3F;
    background: #F2F7EF;
}
.ingr-card.selected {
    border-color: #2C3A1E;
    background: #EEF5E9;
}
.ingr-card-icon { font-size: 28px; margin-bottom: 8px; }
.ingr-card-name {
    font-weight: 500;
    font-size: 14px;
    color: #2C3A1E;
    margin-bottom: 4px;
}
.ingr-card-desc {
    font-size: 11px;
    color: #8A9980;
    line-height: 1.4;
}
.ingr-badge {
    display: inline-block;
    margin-top: 8px;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 99px;
    background: #EEF5E9;
    color: #2C5F21;
    border: 1px solid #C5DDB8;
}

/* 레시피 카드 */
.recipe-card {
    background: #FFFFFF;
    border: 1px solid #E2DDD4;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
}
.recipe-title {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #2C3A1E;
    margin-bottom: 8px;
}
.recipe-meta {
    display: flex;
    gap: 16px;
    font-size: 12px;
    color: #8A9980;
    margin-bottom: 14px;
}
.recipe-meta span { display: flex; align-items: center; gap: 4px; }
.recipe-step {
    display: flex;
    gap: 12px;
    padding: 8px 0;
    border-top: 1px solid #F0ECE4;
    font-size: 13px;
    color: #5A6650;
    line-height: 1.5;
    align-items: flex-start;
}
.recipe-step:first-child { border-top: none; }
.step-num {
    min-width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #4A7C3F;
    color: white;
    font-size: 10px;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

/* 태그 칩 */
.quick-tag {
    display: inline-block;
    font-size: 12px;
    padding: 5px 12px;
    border-radius: 99px;
    border: 1px solid #D8D3C8;
    color: #6B7A60;
    background: white;
    cursor: pointer;
    margin: 3px;
}
.quick-tag:hover { border-color: #4A7C3F; color: #2C3A1E; }

/* Streamlit 버튼 커스터마이즈 */
.stButton > button {
    background-color: #2C3A1E !important;
    color: #F7F5F0 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background-color: #4A7C3F !important;
}

/* 검색창 */
.stTextInput > div > div > input {
    border: 1px solid #D8D3C8 !important;
    border-radius: 8px !important;
    background: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4A7C3F !important;
    box-shadow: 0 0 0 3px rgba(74,124,63,0.1) !important;
}

/* 선택된 식재료 칩 */
.selected-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EEF5E9;
    color: #2C5F21;
    border: 1px solid #C5DDB8;
    border-radius: 99px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}

/* 알림 박스 */
.empty-state {
    text-align: center;
    padding: 48px 24px;
    background: #FFFFFF;
    border: 1px dashed #D8D3C8;
    border-radius: 12px;
    color: #8A9980;
    font-size: 14px;
}
.empty-state-icon { font-size: 36px; margin-bottom: 12px; }

/* 구분선 */
.divider {
    height: 1px;
    background: #E2DDD4;
    margin: 28px 0;
}
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────────────
INGREDIENTS = [
    {
        "id": "quinoa",
        "icon": "🌾",
        "name": "퀴노아",
        "name_en": "Quinoa",
        "desc": "완전단백질 슈퍼씨앗",
        "badge": "글루텐프리",
        "tags": ["단백질", "통곡물"],
        "nutrition": {"칼로리": "120 kcal/100g", "단백질": "4.4g", "식이섬유": "2.8g"},
        "recipes": [
            {
                "title": "퀴노아 샐러드 볼",
                "time": "20분",
                "kcal": "310 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "퀴노아 1컵을 물 2컵에 넣고 약불에서 15분 끓인 뒤 뚜껑을 덮고 5분 뜸 들인다",
                    "오이, 방울토마토, 적양파를 작게 썬다",
                    "레몬즙 2큰술, 올리브오일 1큰술, 소금·후추로 드레싱을 만든다",
                    "모든 재료를 섞고 파슬리나 민트 잎을 올려 완성한다",
                ]
            },
            {
                "title": "퀴노아 리조또",
                "time": "30분",
                "kcal": "380 kcal",
                "difficulty": "보통",
                "steps": [
                    "채수(또는 닭육수) 3컵을 따뜻하게 준비한다",
                    "팬에 버터를 두르고 다진 양파와 마늘을 볶다가 퀴노아를 넣어 1분 더 볶는다",
                    "육수를 조금씩 부어가며 15분간 중불에서 저으며 익힌다",
                    "파마산 치즈 2큰술, 버터 1큰술을 넣어 크리미하게 만들고 후추로 마무리한다",
                ]
            },
        ]
    },
    {
        "id": "avocado",
        "icon": "🥑",
        "name": "아보카도",
        "name_en": "Avocado",
        "desc": "건강한 단일불포화지방",
        "badge": "비타민E",
        "tags": ["건강지방", "비타민"],
        "nutrition": {"칼로리": "160 kcal/100g", "지방": "14.7g", "칼륨": "485mg"},
        "recipes": [
            {
                "title": "아보카도 토스트",
                "time": "10분",
                "kcal": "280 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "통곡물빵을 토스터에 노릇하게 굽는다",
                    "잘 익은 아보카도를 반으로 갈라 씨를 제거하고 포크로 으깬다",
                    "레몬즙 1작은술, 소금·후추를 넣어 버무린 뒤 빵 위에 바른다",
                    "반숙 달걀, 치아씨드, 홍고추 플레이크를 올려 완성한다",
                ]
            },
            {
                "title": "과카몰리",
                "time": "8분",
                "kcal": "150 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "잘 익은 아보카도 2개를 으깬다",
                    "토마토, 적양파, 고수(실란트로)를 잘게 썬다",
                    "라임즙, 소금, 큐민 1/4작은술을 넣고 잘 섞는다",
                    "토르티야 칩이나 채소 스틱과 함께 서브한다",
                ]
            },
        ]
    },
    {
        "id": "salmon",
        "icon": "🐟",
        "name": "연어",
        "name_en": "Salmon",
        "desc": "오메가-3 고함량 생선",
        "badge": "단백질 25g",
        "tags": ["단백질", "오메가3"],
        "nutrition": {"칼로리": "208 kcal/100g", "단백질": "20g", "오메가3": "2.3g"},
        "recipes": [
            {
                "title": "연어 포케 볼",
                "time": "15분",
                "kcal": "450 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "현미밥 또는 흰쌀밥을 볼에 담는다",
                    "신선한 연어를 큐브 모양으로 썰어 간장 1큰술, 참기름 1작은술, 생강즙으로 5분 마리네이드한다",
                    "에다마메, 오이, 당근, 아보카도를 준비한다",
                    "밥 위에 재료를 올리고 스리라차 마요네즈, 깨를 뿌려 완성한다",
                ]
            },
            {
                "title": "허브 구운 연어",
                "time": "20분",
                "kcal": "390 kcal",
                "difficulty": "보통",
                "steps": [
                    "연어 필레에 올리브오일, 다진 마늘, 레몬즙, 딜·파슬리를 바른다",
                    "오븐을 200도로 예열하고 연어를 12분 굽는다",
                    "아스파라거스나 브로콜리를 함께 오븐에 넣어 굽는다",
                    "레몬 슬라이스와 신선한 허브를 올려 마무리한다",
                ]
            },
        ]
    },
    {
        "id": "tofu",
        "icon": "🫘",
        "name": "두부",
        "name_en": "Tofu",
        "desc": "식물성 완전단백질",
        "badge": "저칼로리",
        "tags": ["채식", "단백질"],
        "nutrition": {"칼로리": "76 kcal/100g", "단백질": "8g", "칼슘": "350mg"},
        "recipes": [
            {
                "title": "순두부 된장국",
                "time": "20분",
                "kcal": "180 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "멸치와 다시마로 육수를 10분 끓인 뒤 건더기를 건진다",
                    "된장 2큰술을 풀고 애호박, 버섯, 두부를 넣는다",
                    "순두부를 큼직하게 뜯어 넣고 5분 더 끓인다",
                    "청양고추와 파를 썰어 넣고 불을 끈다",
                ]
            },
            {
                "title": "두부 스테이크",
                "time": "15분",
                "kcal": "220 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "단단한 두부를 2cm 두께로 썰어 키친타올로 물기를 제거한다",
                    "간장 2큰술, 꿀 1큰술, 다진 마늘, 참기름으로 소스를 만든다",
                    "달군 팬에 올리브오일을 두르고 두부 양면을 각 3분씩 노릇하게 굽는다",
                    "소스를 부어 1분 조리고 깨와 파를 얹어 완성한다",
                ]
            },
        ]
    },
    {
        "id": "blueberry",
        "icon": "🫐",
        "name": "블루베리",
        "name_en": "Blueberry",
        "desc": "항산화 슈퍼푸드",
        "badge": "비타민C",
        "tags": ["항산화", "비타민"],
        "nutrition": {"칼로리": "57 kcal/100g", "비타민C": "9.7mg", "식이섬유": "2.4g"},
        "recipes": [
            {
                "title": "블루베리 스무디 볼",
                "time": "8분",
                "kcal": "260 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "냉동 블루베리 1컵과 바나나 1개를 블렌더에 넣는다",
                    "그릭요거트 1/2컵을 넣고 걸쭉하게 블렌딩한다",
                    "볼에 담고 그래놀라, 신선 블루베리, 치아씨드를 올린다",
                    "꿀을 살짝 드리즐하여 완성한다",
                ]
            },
            {
                "title": "블루베리 오트밀",
                "time": "10분",
                "kcal": "310 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "귀리 1/2컵을 물 또는 식물성 우유 1컵에 넣고 5분 끓인다",
                    "블루베리 1/3컵을 넣고 2분 더 가열해 과일이 살짝 터지게 한다",
                    "시나몬 1/4작은술을 넣어 향을 더한다",
                    "나머지 블루베리, 견과류, 메이플시럽으로 토핑하여 완성한다",
                ]
            },
        ]
    },
    {
        "id": "lentil",
        "icon": "🌱",
        "name": "렌틸콩",
        "name_en": "Lentils",
        "desc": "식이섬유 + 철분의 보고",
        "badge": "채식",
        "tags": ["채식", "철분"],
        "nutrition": {"칼로리": "116 kcal/100g", "단백질": "9g", "철분": "3.3mg"},
        "recipes": [
            {
                "title": "렌틸 수프",
                "time": "35분",
                "kcal": "290 kcal",
                "difficulty": "쉬움",
                "steps": [
                    "양파, 마늘, 당근을 올리브오일에 5분 볶는다",
                    "붉은 렌틸콩 1컵, 채수 4컵, 큐민·파프리카·강황을 넣는다",
                    "약불에서 25분 뭉근히 끓인다",
                    "핸드블렌더로 반쯤 갈아 걸쭉하게 만들고 레몬즙, 파슬리로 마무리한다",
                ]
            },
            {
                "title": "렌틸 커리",
                "time": "30분",
                "kcal": "350 kcal",
                "difficulty": "보통",
                "steps": [
                    "팬에 커리 페이스트 2큰술을 볶아 향을 낸다",
                    "코코넛밀크 1캔과 렌틸콩 1컵을 넣는다",
                    "약불에서 20분 졸이며 렌틸이 부드러워질 때까지 익힌다",
                    "시금치를 넣고 2분 더 가열한 뒤 밥이나 난과 함께 낸다",
                ]
            },
        ]
    },
]

QUICK_TAGS = ["퀴노아", "아보카도", "연어", "두부", "블루베리", "렌틸콩"]

# ── 세션 상태 초기화 ──────────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state.selected = set()
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ── 헬퍼 함수 ────────────────────────────────────────────────────────
def toggle_ingredient(ingr_id):
    if ingr_id in st.session_state.selected:
        st.session_state.selected.discard(ingr_id)
    else:
        st.session_state.selected.add(ingr_id)

def search_and_add(query):
    query = query.strip()
    if not query:
        return
    for ing in INGREDIENTS:
        if query in ing["name"] or query in ing["name_en"].lower() or query.lower() in ing["name_en"].lower():
            st.session_state.selected.add(ing["id"])
            st.session_state.search_query = ""
            return
    st.session_state.search_query = ""

# ── 네비게이션 ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-logo">
        <span class="nav-logo-dot"></span>
        {APP_NAME}
    </div>
    <div class="nav-tagline">{APP_TAGLINE}</div>
</div>
""", unsafe_allow_html=True)

# ── 히어로 섹션 ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <p class="hero-eyebrow">🌿 GOOD FOOD STARTS HERE</p>
    <h1 class="hero-title">냉장고 속 재료로<br>오늘 뭘 만들까?</h1>
    <p class="hero-sub">가진 식재료를 선택하거나 검색하면 맞춤 레시피를 찾아드려요</p>
</div>
""", unsafe_allow_html=True)

# ── 검색 ──────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input(
        label="검색",
        placeholder="식재료 검색 (예: 두부, 아보카도, salmon...)",
        label_visibility="collapsed",
        key="search_input",
    )
with col_btn:
    if st.button("검색", use_container_width=True):
        search_and_add(query)
        st.rerun()

if query and st.session_state.get("search_input") != "":
    if st.session_state.get("_last_query") != query:
        st.session_state["_last_query"] = query

# 퀵태그
st.markdown('<div style="margin: 8px 0 24px;">', unsafe_allow_html=True)
tag_cols = st.columns(len(QUICK_TAGS))
for i, tag in enumerate(QUICK_TAGS):
    with tag_cols[i]:
        if st.button(tag, key=f"qtag_{tag}", use_container_width=True):
            search_and_add(tag)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── 식재료 그리드 ────────────────────────────────────────────────────
st.markdown('<p class="section-header">오늘의 추천 식재료</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">카드를 클릭해 선택하세요 — 여러 개 선택 가능해요</p>', unsafe_allow_html=True)

cols = st.columns(3)
for i, ing in enumerate(INGREDIENTS):
    is_selected = ing["id"] in st.session_state.selected
    card_class = "ingr-card selected" if is_selected else "ingr-card"
    check = "✓ " if is_selected else ""

    with cols[i % 3]:
        st.markdown(f"""
        <div class="{card_class}">
            <div class="ingr-card-icon">{ing['icon']}</div>
            <div class="ingr-card-name">{check}{ing['name']}</div>
            <div class="ingr-card-desc">{ing['desc']}</div>
            <span class="ingr-badge">{ing['badge']}</span>
        </div>
        """, unsafe_allow_html=True)

        label = f"{'✓ 선택됨' if is_selected else '선택하기'} — {ing['name']}"
        if st.button(label, key=f"ing_{ing['id']}", use_container_width=True):
            toggle_ingredient(ing["id"])
            st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── 레시피 섹션 ───────────────────────────────────────────────────────
st.markdown('<p class="section-header">레시피</p>', unsafe_allow_html=True)

if st.session_state.selected:
    # 선택된 식재료 칩
    selected_names = [ing["name"] for ing in INGREDIENTS if ing["id"] in st.session_state.selected]
    chips_html = "".join([f'<span class="selected-chip">🌿 {n}</span>' for n in selected_names])
    st.markdown(f'<div style="margin-bottom:20px;">{chips_html}</div>', unsafe_allow_html=True)

    col_clear = st.columns([4, 1])[1]
    with col_clear:
        if st.button("선택 초기화", use_container_width=True):
            st.session_state.selected.clear()
            st.rerun()

    # 매칭 레시피 출력
    matched = [ing for ing in INGREDIENTS if ing["id"] in st.session_state.selected]
    for ing in matched:
        for recipe in ing["recipes"]:
            diff_color = {"쉬움": "#2C5F21", "보통": "#7A5C00", "어려움": "#8B0000"}.get(recipe["difficulty"], "#555")
            steps_html = "".join([
                f'<div class="recipe-step"><span class="step-num">{j+1}</span><span>{step}</span></div>'
                for j, step in enumerate(recipe["steps"])
            ])
            st.markdown(f"""
            <div class="recipe-card">
                <div class="recipe-title">{recipe['title']}</div>
                <div class="recipe-meta">
                    <span>⏱ {recipe['time']}</span>
                    <span>🔥 {recipe['kcal']}</span>
                    <span>🌿 {ing['name']}</span>
                    <span style="color:{diff_color}; font-weight:500;">● {recipe['difficulty']}</span>
                </div>
                <div>{steps_html}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🥗</div>
        위에서 식재료를 선택하거나 검색하면<br>맞춤 레시피가 여기에 나타나요
    </div>
    """, unsafe_allow_html=True)

# ── 푸터 ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top: 60px; padding: 24px 0; border-top: 1px solid #E2DDD4; text-align: center; font-size: 12px; color: #8A9980;">
    {APP_NAME} · {APP_TAGLINE}
</div>
""", unsafe_allow_html=True)
