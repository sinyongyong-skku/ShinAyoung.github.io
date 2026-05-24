# Nourish 🌿

> wholesome ingredients, honest recipes

식재료를 선택하거나 검색하면 맞춤 레시피를 보여주는 Streamlit 웹 앱.

---

## 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 열기

---

## 앱 이름 바꾸기
`app.py` 상단의 두 줄만 수정하면 전체 반영됩니다:
```python
APP_NAME = "Nourish"          # ← 여기만 바꾸면 됨
APP_TAGLINE = "wholesome ingredients, honest recipes"
```

---

## 식재료 추가하기
`INGREDIENTS` 리스트에 아래 형식으로 항목을 추가하세요:

```python
{
    "id": "고유ID",
    "icon": "🥦",
    "name": "한국어 이름",
    "name_en": "English Name",
    "desc": "짧은 설명",
    "badge": "뱃지 텍스트",
    "tags": ["태그1", "태그2"],
    "nutrition": {"칼로리": "...", "단백질": "..."},
    "recipes": [
        {
            "title": "레시피 이름",
            "time": "20분",
            "kcal": "300 kcal",
            "difficulty": "쉬움",  # 쉬움 / 보통 / 어려움
            "steps": [
                "1단계 설명",
                "2단계 설명",
            ]
        }
    ]
}
```

---

## 파일 구조
```
nourish_app/
├── app.py            # 메인 앱
├── requirements.txt  # 패키지 목록
└── README.md         # 이 파일
```
