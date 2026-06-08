import streamlit as st
import base64
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import requests

APP_NAME = "Nourish"
APP_TAGLINE_EN = "wholesome ingredients, honest recipes"
APP_TAGLINE_KO = "건강한 식재료, 정직한 레시피"

DATA_DIR = Path("nourish_data")
POSTS_FILE = DATA_DIR / "community_posts.json"
DIARY_FILE = DATA_DIR / "diary_entries.json"
INGREDIENTS_FILE = DATA_DIR / "custom_ingredients.json"
DATA_DIR.mkdir(exist_ok=True)

def load_json(path, default):
    if path.exists():
        try: return json.loads(path.read_text(encoding="utf-8"))
        except: return default
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

T = {
    "en": {
        "tab1":"🌿 Home","tab2":"🥦 Ingredients","tab3":"🍳 Recipes",
        "tab4":"📸 Share","tab5":"📔 My Diary",
        "search_placeholder":"Search by name, effect, category (EN/KR)...",
        "search_btn":"Search 🔍","close_search":"Close ✕",
        "no_result":"No results for","featured_title":"Featured Ingredients",
        "featured_sub":"Click a card to view details","all_ingr":"All Ingredients",
        "key_benefits":"KEY BENEFITS","nutrition":"NUTRITION (per 100g)",
        "recipes_for":"Recipes with","recipe_title":"Browse Recipes",
        "recipe_search_ph":"Search recipe or ingredient...","select_recipe":"— Select a recipe —",
        "share_title":"Community Food Share","share_sub":"Share your homemade dishes",
        "upload_title":"Upload Your Dish","upload_sub":"Add a photo and details",
        "nickname":"Nickname","recipe_name":"Recipe Name","note":"Your note",
        "share_btn":"🌿 Share","share_success":"Shared!",
        "share_warn_nick":"Please enter a nickname.",
        "share_warn_recipe":"Please enter a recipe name.",
        "share_warn_photo":"Please upload a photo.",
        "diary_title":"My Cooking Diary","diary_sub":"Record your cooking journey",
        "diary_date":"Date","diary_meal":"Meal Name","diary_note":"Diary Entry",
        "diary_mood":"How did it taste?","diary_submit":"💚 Save Entry",
        "health_score_btn":"🤖 Get AI Health Score",
        "ai_add_title":"Add Ingredient with AI",
        "ai_add_btn":"✨ Generate & Add",
        "ai_ingredient_name":"Ingredient name (EN or KO)",
        "goal_chart_title":"🎯 Nutrient Radar by Health Goal",
        "goal_chart_sub":"Select a goal to compare top ingredients",
        "home_stats_ingr":"Ingredients","home_stats_recipe":"Recipes",
        "home_stats_users":"Community Posts",
        "copy_link":"🔗 Copy","insta_share":"📷 Instagram",
        "difficulty":{"Easy":"Easy","Medium":"Medium","Hard":"Hard"},
    },
    "ko": {
        "tab1":"🌿 홈","tab2":"🥦 식재료","tab3":"🍳 레시피",
        "tab4":"📸 공유","tab5":"📔 나의 일기",
        "search_placeholder":"이름, 효능, 카테고리 검색 (영어/한국어)...",
        "search_btn":"검색 🔍","close_search":"닫기 ✕",
        "no_result":"검색 결과 없음:","featured_title":"오늘의 추천 식재료",
        "featured_sub":"카드를 클릭하면 자세한 정보가 나와요","all_ingr":"전체 식재료",
        "key_benefits":"주요 효능","nutrition":"영양 성분 (100g 기준)",
        "recipes_for":"관련 레시피","recipe_title":"레시피 탐색",
        "recipe_search_ph":"레시피 또는 식재료 검색...","select_recipe":"— 레시피를 선택해주세요 —",
        "share_title":"음식 사진 공유","share_sub":"직접 만든 요리를 공유해요",
        "upload_title":"나의 요리 올리기","upload_sub":"사진과 간단한 정보를 입력해주세요",
        "nickname":"닉네임","recipe_name":"레시피 이름","note":"한마디",
        "share_btn":"🌿 공유하기","share_success":"사진이 공유됐어요!",
        "share_warn_nick":"닉네임을 입력해주세요.",
        "share_warn_recipe":"레시피 이름을 입력해주세요.",
        "share_warn_photo":"사진을 업로드해주세요.",
        "diary_title":"나의 요리 일기","diary_sub":"오늘의 요리 이야기를 기록해요",
        "diary_date":"날짜","diary_meal":"요리 이름","diary_note":"일기",
        "diary_mood":"맛은 어땠나요?","diary_submit":"💚 저장하기",
        "health_score_btn":"🤖 AI 건강 점수 받기",
        "ai_add_title":"AI로 식재료 추가",
        "ai_add_btn":"✨ AI로 생성·추가",
        "ai_ingredient_name":"식재료 이름 (한국어/영어)",
        "goal_chart_title":"🎯 건강 목표별 영양소 레이더",
        "goal_chart_sub":"목표를 선택하면 추천 식재료를 비교할 수 있어요",
        "home_stats_ingr":"가지 식재료","home_stats_recipe":"개 레시피",
        "home_stats_users":"커뮤니티 게시물",
        "copy_link":"🔗 링크 복사","insta_share":"📷 인스타 공유",
        "difficulty":{"Easy":"쉬움","Medium":"보통","Hard":"어려움"},
    }
}

def t(key, sub=None):
    lang = st.session_state.get("lang","en")
    base = T[lang].get(key, T["en"].get(key, key))
    if sub and isinstance(base, dict):
        return base.get(sub, sub)
    return base

FEATURED = ["quinoa","avocado","salmon","tofu","blueberry","lentil","kale","beet"]

NUTRIENT_SCORES = {
    "quinoa":[8,6,5,2,1,4,3],"avocado":[3,9,2,8,5,7,2],
    "salmon":[10,0,4,0,10,6,4],"tofu":[7,1,4,0,3,4,10],
    "blueberry":[1,5,1,10,1,10,1],"lentil":[8,10,9,2,1,5,3],
    "spinach":[5,7,8,9,2,9,4],"sweetpotato":[3,6,2,7,0,8,3],
    "egg":[9,0,4,0,4,3,5],"broccoli":[5,6,3,10,1,10,5],
    "oats":[7,10,5,0,2,5,4],"kimchi":[2,4,2,7,1,10,3],
    "garlic":[4,4,3,6,0,9,3],"banana":[2,5,1,6,0,5,1],
    "chickpea":[7,9,7,2,1,5,6],"almond":[8,9,5,0,4,8,6],
    "greek_yogurt":[10,0,1,0,1,3,10],"turmeric":[3,8,5,2,2,10,3],
    "walnut":[6,6,4,1,10,8,3],"chia":[7,10,7,1,9,7,10],
    "kale":[5,8,6,10,1,10,7],"beet":[3,5,4,7,0,9,2],
    "ginger":[2,3,2,5,0,10,2],"sardine":[10,0,6,0,9,4,10],
    "kefir":[7,0,1,1,1,5,10],"mango":[1,3,1,10,0,8,2],
    "pomegranate":[1,4,1,10,0,10,1],"hemp_seeds":[9,5,7,1,8,6,5],
    "tuna":[10,0,5,0,6,3,3],"edamame":[8,7,5,3,2,5,6],
    "sweet_potato":[3,6,2,7,0,8,3],"walnuts":[6,6,4,1,10,8,3],
}

HEALTH_GOALS_EN = {
    "🧠 Brain":["salmon","walnut","blueberry","egg","chia","turmeric","sardine","hemp_seeds"],
    "❤️ Heart":["salmon","avocado","walnut","oats","garlic","chia","sardine","pomegranate"],
    "💪 Muscle":["salmon","egg","greek_yogurt","tofu","chickpea","lentil","quinoa","sardine"],
    "🌿 Gut":["kimchi","greek_yogurt","kefir","lentil","oats","chia","garlic","edamame"],
    "🛡️ Immunity":["broccoli","spinach","blueberry","garlic","kale","turmeric","pomegranate","mango"],
    "⚖️ Weight":["tofu","lentil","broccoli","spinach","oats","greek_yogurt","chia","egg"],
    "🦴 Bone":["tofu","greek_yogurt","chia","kale","sardine","kefir","almond","broccoli"],
    "✨ Skin":["avocado","blueberry","almond","turmeric","salmon","pomegranate","mango","walnut"],
}
HEALTH_GOALS_KO = {
    "🧠 뇌건강":["salmon","walnut","blueberry","egg","chia","turmeric","sardine","hemp_seeds"],
    "❤️ 심장":["salmon","avocado","walnut","oats","garlic","chia","sardine","pomegranate"],
    "💪 근육":["salmon","egg","greek_yogurt","tofu","chickpea","lentil","quinoa","sardine"],
    "🌿 장건강":["kimchi","greek_yogurt","kefir","lentil","oats","chia","garlic","edamame"],
    "🛡️ 면역":["broccoli","spinach","blueberry","garlic","kale","turmeric","pomegranate","mango"],
    "⚖️ 다이어트":["tofu","lentil","broccoli","spinach","oats","greek_yogurt","chia","egg"],
    "🦴 뼈건강":["tofu","greek_yogurt","chia","kale","sardine","kefir","almond","broccoli"],
    "✨ 피부":["avocado","blueberry","almond","turmeric","salmon","pomegranate","mango","walnut"],
}

RECIPE_IMAGES = {
    "Quinoa Salad Bowl":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&q=80",
    "Avocado Toast":"https://images.unsplash.com/photo-1541519227354-08fa5d50c820?w=500&q=80",
    "Salmon Poke Bowl":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80",
    "Blueberry Smoothie Bowl":"https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=500&q=80",
    "Lentil Soup":"https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80",
    "Kale Caesar Salad":"https://images.unsplash.com/photo-1512852939750-1305098529bf?w=500&q=80",
    "Roasted Beet Salad":"https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500&q=80",
    "Overnight Oats":"https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=500&q=80",
    "Mango Salsa":"https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=500&q=80",
    "Hummus":"https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500&q=80",
    "Chia Seed Pudding":"https://images.unsplash.com/photo-1571748982800-fa51082c2224?w=500&q=80",
    "Greek Yogurt Parfait":"https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&q=80",
    "Golden Milk":"https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500&q=80",
    "Kimchi Fried Rice":"https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500&q=80",
    "Banana Bread":"https://images.unsplash.com/photo-1605471021234-6fa53b8e8e34?w=500&q=80",
    "Garlic Butter Shrimp":"https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80",
    "Walnut Brownies":"https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80",
    "default":"https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=500&q=80",
}
INGREDIENTS = [
  {"id":"quinoa","icon":"🌾","name":"Quinoa","name_ko":"퀴노아","name_en":"quinoa",
   "short":"Complete protein super seed","short_ko":"완전단백질 슈퍼씨앗",
   "badge":"Gluten-Free","badge_ko":"글루텐프리","category":"Whole Grain","category_ko":"통곡물",
   "description":"Quinoa is the only grain containing all 9 essential amino acids. Native to the Andes, it is naturally gluten-free and packed with minerals.",
   "description_ko":"퀴노아는 곡물 중 유일하게 9가지 필수아미노산을 모두 함유한 완전단백질 식품이에요. 글루텐이 없어 밀 알레르기가 있는 분들도 안심하고 먹을 수 있어요.",
   "effects":["Blood sugar control","Muscle recovery","Digestion","Satiety","Energy"],
   "effects_ko":["혈당 조절","근육 회복","소화 개선","포만감","에너지 공급"],
   "nutrition":{"Calories":"120kcal","Protein":"4.4g","Fiber":"2.8g","Carbs":"21.3g","Fat":"1.9g","Iron":"1.5mg"},
   "recipes":[
     {"title":"Quinoa Salad Bowl","title_ko":"퀴노아 샐러드 볼","time":"20 min","kcal":"310kcal","difficulty":"Easy",
      "steps":["Cook 1 cup quinoa in 2 cups water 15 min","Slice cucumber, tomatoes, red onion","Make dressing: lemon, olive oil, salt, pepper","Toss everything together"],
      "steps_ko":["퀴노아 1컵을 물 2컵에 15분 끓인다","오이, 방울토마토, 적양파를 썬다","드레싱: 레몬즙, 올리브오일, 소금, 후추","모두 섞어 완성한다"]},
     {"title":"Quinoa Breakfast Bowl","title_ko":"퀴노아 아침 볼","time":"10 min","kcal":"270kcal","difficulty":"Easy",
      "steps":["Mix cooked quinoa 1:1 with Greek yogurt","Stir in honey and cinnamon","Top with blueberries and almonds","Garnish with mint"],
      "steps_ko":["익힌 퀴노아와 그릭요거트를 1:1로 섞는다","꿀과 시나몬을 넣어 섞는다","블루베리와 아몬드를 올린다","민트잎으로 마무리한다"]},
     {"title":"Quinoa Stuffed Peppers","title_ko":"퀴노아 스터프드 파프리카","time":"40 min","kcal":"350kcal","difficulty":"Medium",
      "steps":["Cut tops off peppers, remove seeds","Mix quinoa, black beans, corn, tomato sauce","Fill peppers and top with cheese","Bake 200°C for 25 min"],
      "steps_ko":["파프리카 윗부분을 잘라 씨를 제거한다","퀴노아, 블랙빈, 옥수수, 토마토소스를 섞는다","파프리카에 채우고 치즈를 올린다","200도에서 25분 굽는다"]},
     {"title":"Quinoa Vegetable Soup","title_ko":"퀴노아 채소 수프","time":"30 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Sauté onion, carrot, celery in olive oil","Add 4 cups broth and quinoa","Simmer 20 min on low","Finish with salt, pepper, parsley"],
      "steps_ko":["양파, 당근, 셀러리를 올리브오일에 볶는다","채수 4컵과 퀴노아를 넣는다","약불에서 20분 끓인다","소금, 후추, 파슬리로 마무리한다"]},
   ]},
  {"id":"avocado","icon":"🥑","name":"Avocado","name_ko":"아보카도","name_en":"avocado",
   "short":"Healthy monounsaturated fats","short_ko":"건강한 단일불포화지방",
   "badge":"Vitamin E","badge_ko":"비타민E","category":"Healthy Fats","category_ko":"건강지방",
   "description":"Rich in heart-healthy monounsaturated fats and potassium. Contains twice the potassium of a banana.",
   "description_ko":"'숲속의 버터'라 불릴 만큼 크리미한 식감과 풍부한 영양을 자랑해요. 심장 건강에 좋은 단일불포화지방산이 풍부하고 칼륨 함량이 바나나의 2배예요.",
   "effects":["Heart health","Skin care","Blood pressure","Nutrient absorption","Anti-inflammatory"],
   "effects_ko":["심장 건강","피부 미용","혈압 조절","영양소 흡수","항염증"],
   "nutrition":{"Calories":"160kcal","Protein":"2.0g","Fiber":"6.7g","Carbs":"8.5g","Fat":"14.7g","Potassium":"485mg"},
   "recipes":[
     {"title":"Avocado Toast","title_ko":"아보카도 토스트","time":"10 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Toast whole grain bread","Mash avocado with lemon, salt, pepper","Spread on toast","Top with poached egg and chia seeds"],
      "steps_ko":["통곡물빵을 굽는다","아보카도를 레몬즙, 소금, 후추와 으깬다","빵에 듬뿍 바른다","반숙 달걀과 치아씨드를 올린다"]},
     {"title":"Guacamole","title_ko":"과카몰리","time":"8 min","kcal":"150kcal","difficulty":"Easy",
      "steps":["Mash 2 ripe avocados","Add tomato, red onion, cilantro","Add lime juice, salt, cumin","Serve with tortilla chips"],
      "steps_ko":["잘 익은 아보카도 2개를 으깬다","토마토, 적양파, 고수를 썬다","라임즙, 소금, 큐민을 넣는다","토르티야 칩과 함께 낸다"]},
     {"title":"Avocado Chocolate Mousse","title_ko":"아보카도 초콜릿 무스","time":"15 min","kcal":"240kcal","difficulty":"Easy",
      "steps":["Blend avocado, cocoa powder, honey","Add splash of almond milk","Add vanilla extract","Top with raspberries and mint"],
      "steps_ko":["아보카도, 코코아, 꿀을 블렌더에 넣는다","아몬드밀크를 조금 넣어 크리미하게 간다","바닐라 에센스를 넣는다","라즈베리와 민트를 올린다"]},
     {"title":"Avocado Caesar Pasta","title_ko":"아보카도 시저 파스타","time":"20 min","kcal":"460kcal","difficulty":"Medium",
      "steps":["Blend avocado, lemon, garlic, olive oil, parmesan","Cook pasta in salted water","Toss pasta with dressing","Top with arugula and croutons"],
      "steps_ko":["아보카도, 레몬, 마늘, 올리브오일, 파마산으로 드레싱을 만든다","파스타를 소금물에 삶는다","따뜻한 파스타에 드레싱을 넣어 버무린다","루꼴라와 크루통을 올린다"]},
   ]},
  {"id":"salmon","icon":"🐟","name":"Salmon","name_ko":"연어","name_en":"salmon",
   "short":"High omega-3 fatty fish","short_ko":"오메가-3 고함량 생선",
   "badge":"20g Protein","badge_ko":"단백질 20g","category":"Seafood","category_ko":"해산물",
   "description":"One of the best sources of omega-3 EPA and DHA. Excellent for brain, heart, and reducing inflammation.",
   "description_ko":"오메가-3 지방산의 가장 좋은 공급원 중 하나예요. EPA와 DHA가 풍부해 뇌 건강, 심혈관 건강, 염증 억제에 탁월해요.",
   "effects":["Brain health","Heart protection","Reduces inflammation","Immunity","Bone strength"],
   "effects_ko":["뇌 건강","심혈관 보호","염증 억제","면역력","뼈 강화"],
   "nutrition":{"Calories":"208kcal","Protein":"20.0g","Fiber":"0g","Carbs":"0g","Fat":"13.0g","Omega-3":"2.3g"},
   "recipes":[
     {"title":"Salmon Poke Bowl","title_ko":"연어 포케 볼","time":"15 min","kcal":"450kcal","difficulty":"Easy",
      "steps":["Place brown rice in bowl","Marinate salmon in soy, sesame oil, ginger 5 min","Prepare edamame, cucumber, avocado","Top rice and drizzle sriracha mayo"],
      "steps_ko":["현미밥을 볼에 담는다","연어를 간장, 참기름, 생강즙에 5분 재운다","에다마메, 오이, 아보카도를 준비한다","밥 위에 올리고 스리라차 마요를 뿌린다"]},
     {"title":"Herb-Baked Salmon","title_ko":"허브 오븐 구이 연어","time":"22 min","kcal":"390kcal","difficulty":"Medium",
      "steps":["Coat salmon with olive oil, garlic, lemon, dill","Bake at 200°C for 12 min","Roast asparagus alongside","Finish with lemon and parsley"],
      "steps_ko":["연어에 올리브오일, 마늘, 레몬즙, 딜을 바른다","200도에서 12분 굽는다","아스파라거스를 함께 굽는다","레몬, 파슬리로 마무리한다"]},
     {"title":"Miso Glazed Salmon","title_ko":"미소 연어 구이","time":"20 min","kcal":"350kcal","difficulty":"Easy",
      "steps":["Mix miso, mirin, soy sauce, honey for glaze","Coat salmon, marinate 15 min","Pan-fry 4 min each side","Serve with steamed rice"],
      "steps_ko":["미소, 미린, 간장, 꿀로 글레이즈를 만든다","연어에 바르고 15분 재운다","팬에서 양면 4분씩 굽는다","따뜻한 밥과 함께 낸다"]},
     {"title":"Salmon Cream Pasta","title_ko":"연어 크림파스타","time":"25 min","kcal":"520kcal","difficulty":"Medium",
      "steps":["Cook pasta in salted water","Pan-sear salmon in butter, then flake","Add cream, parmesan, lemon for sauce","Toss pasta, finish with dill and capers"],
      "steps_ko":["파스타를 소금물에 삶는다","버터에 연어를 굽다가 부순다","생크림, 파마산, 레몬즙으로 소스를 만든다","파스타를 넣어 섞고 딜, 케이퍼로 마무리한다"]},
   ]},
  {"id":"tofu","icon":"🫘","name":"Tofu","name_ko":"두부","name_en":"tofu",
   "short":"Plant-based complete protein","short_ko":"식물성 완전단백질",
   "badge":"Low Calorie","badge_ko":"저칼로리","category":"Plant Protein","category_ko":"식물성단백질",
   "description":"Made from soybeans — low in calories yet rich in protein and calcium. Perfect for weight management and bone health.",
   "description_ko":"콩을 갈아 만든 식물성 단백질의 대표 식품이에요. 칼로리가 낮으면서도 단백질이 풍부해 다이어트식으로 완벽하고 칼슘도 높아요.",
   "effects":["Weight management","Bone strength","Muscle maintenance","Lower cholesterol","Hormone balance"],
   "effects_ko":["다이어트","뼈 강화","근육 유지","콜레스테롤 감소","호르몬 균형"],
   "nutrition":{"Calories":"76kcal","Protein":"8.0g","Fiber":"0.3g","Carbs":"1.9g","Fat":"4.8g","Calcium":"350mg"},
   "recipes":[
     {"title":"Tofu Steak","title_ko":"두부 스테이크","time":"15 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Slice tofu 2cm, pat dry","Make sauce: soy, honey, garlic, sesame oil","Pan-fry both sides 3 min until golden","Pour sauce over, top with sesame, scallions"],
      "steps_ko":["두부를 2cm로 썰어 물기를 제거한다","소스: 간장, 꿀, 마늘, 참기름","팬에 양면 3분씩 노릇하게 굽는다","소스를 붓고 깨, 파를 얹는다"]},
     {"title":"Mapo Tofu","title_ko":"마파두부","time":"20 min","kcal":"280kcal","difficulty":"Medium",
      "steps":["Stir-fry ground pork","Add doubanjiang, garlic, ginger","Add tofu, broth, soy sauce","Thicken with cornstarch, finish with scallions"],
      "steps_ko":["돼지고기 다짐육을 볶는다","두반장, 마늘, 생강을 넣는다","두부, 육수, 간장을 넣는다","전분물로 걸쭉하게, 파로 마무리한다"]},
     {"title":"Turmeric Tofu Scramble","title_ko":"강황 두부 스크램블","time":"12 min","kcal":"200kcal","difficulty":"Easy",
      "steps":["Crumble tofu, squeeze moisture","Sauté olive oil and garlic","Add tofu, turmeric, cumin, salt; stir-fry","Fold in spinach and cherry tomatoes"],
      "steps_ko":["두부를 손으로 부숴 물기를 제거한다","올리브오일, 마늘을 볶는다","두부, 강황, 큐민, 소금을 넣고 볶는다","시금치, 방울토마토를 넣어 마무리한다"]},
     {"title":"Crispy Tofu Bowl","title_ko":"크리스피 두부 볼","time":"25 min","kcal":"320kcal","difficulty":"Easy",
      "steps":["Press tofu dry, cut into cubes","Toss in cornstarch, salt, pepper","Air-fry or pan-fry until crispy","Serve over rice with broccoli and peanut sauce"],
      "steps_ko":["두부를 눌러 물기를 빼고 큐브로 자른다","전분, 소금, 후추를 묻힌다","에어프라이어나 팬에서 바삭하게 굽는다","밥 위에 브로콜리, 땅콩소스와 함께 올린다"]},
   ]},
  {"id":"blueberry","icon":"🫐","name":"Blueberry","name_ko":"블루베리","name_en":"blueberry",
   "short":"Antioxidant superfood","short_ko":"항산화 슈퍼푸드",
   "badge":"Vitamin C","badge_ko":"비타민C","category":"Berries","category_ko":"베리류",
   "description":"Packed with anthocyanin antioxidants for brain health and anti-aging. Neutralise free radicals and protect against cognitive decline.",
   "description_ko":"안토시아닌이라는 강력한 항산화 색소로 가득 차 있어요. 뇌 건강과 기억력 개선에 효과적이고 활성산소를 제거해 노화를 늦춰줘요.",
   "effects":["Antioxidant","Brain health","Anti-aging","Blood sugar control","Eye protection"],
   "effects_ko":["항산화","뇌 건강","노화 방지","혈당 조절","시력 보호"],
   "nutrition":{"Calories":"57kcal","Protein":"0.7g","Fiber":"2.4g","Carbs":"14.5g","Fat":"0.3g","Vitamin C":"9.7mg"},
   "recipes":[
     {"title":"Blueberry Smoothie Bowl","title_ko":"블루베리 스무디 볼","time":"8 min","kcal":"260kcal","difficulty":"Easy",
      "steps":["Blend frozen blueberries and banana","Add Greek yogurt, blend thick","Top with granola and chia seeds","Drizzle with honey"],
      "steps_ko":["냉동 블루베리와 바나나를 블렌딩한다","그릭요거트를 넣고 걸쭉하게 만든다","그래놀라와 치아씨드를 올린다","꿀을 드리즐한다"]},
     {"title":"Blueberry Chia Jam","title_ko":"블루베리 치아씨드 잼","time":"15 min","kcal":"40kcal","difficulty":"Easy",
      "steps":["Boil blueberries, honey, lemon juice","Simmer stirring 10 min","Off heat, stir in chia seeds","Cool and refrigerate in jar"],
      "steps_ko":["블루베리, 꿀, 레몬즙을 냄비에서 끓인다","10분 저으며 졸인다","불을 끄고 치아씨드를 넣는다","식혀서 유리병에 냉장 보관한다"]},
     {"title":"Blueberry Pancakes","title_ko":"블루베리 팬케이크","time":"20 min","kcal":"310kcal","difficulty":"Easy",
      "steps":["Mash banana, mix with eggs and oat flour","Fold blueberries into batter","Cook both sides over low heat","Top with maple syrup"],
      "steps_ko":["바나나를 으깨고 달걀, 귀리가루를 섞는다","블루베리를 반죽에 넣는다","팬에 약불로 양면을 굽는다","메이플시럽을 올린다"]},
     {"title":"Blueberry Yogurt Ice Bars","title_ko":"블루베리 요거트 아이스바","time":"10 min+4h","kcal":"90kcal","difficulty":"Easy",
      "steps":["Mix Greek yogurt, honey, vanilla","Mash blueberries, swirl into yogurt","Pour into ice bar molds","Freeze 4+ hours"],
      "steps_ko":["그릭요거트, 꿀, 바닐라를 섞는다","블루베리를 으깨 섞는다","아이스바 틀에 붓고 막대를 꽂는다","냉동실에 4시간 이상 얼린다"]},
   ]},
  {"id":"lentil","icon":"🌱","name":"Lentils","name_ko":"렌틸콩","name_en":"lentils",
   "short":"Fiber and iron powerhouse","short_ko":"식이섬유·철분의 보고",
   "badge":"Vegan","badge_ko":"채식","category":"Legumes","category_ko":"콩류",
   "description":"One of the world's oldest crops — high in protein, iron, and fiber. Improves gut health and prevents blood sugar spikes.",
   "description_ko":"세계에서 가장 오래된 재배 작물 중 하나로, 단백질과 철분이 특히 풍부해요. 식이섬유 함량이 매우 높아 장 건강을 개선하고 혈당 급등을 막아줘요.",
   "effects":["Gut health","Blood sugar control","Anaemia prevention","Satiety","Prenatal health"],
   "effects_ko":["장 건강","혈당 조절","빈혈 예방","포만감","임산부 건강"],
   "nutrition":{"Calories":"116kcal","Protein":"9.0g","Fiber":"7.9g","Carbs":"20.1g","Fat":"0.4g","Iron":"3.3mg"},
   "recipes":[
     {"title":"Lentil Soup","title_ko":"렌틸 수프","time":"35 min","kcal":"290kcal","difficulty":"Easy",
      "steps":["Sauté onion, garlic, carrot in olive oil","Add lentils, broth, cumin, paprika","Simmer 25 min","Partially blend, finish with lemon"],
      "steps_ko":["양파, 마늘, 당근을 올리브오일에 볶는다","렌틸콩, 채수, 큐민, 파프리카를 넣는다","약불에서 25분 끓인다","핸드블렌더로 반쯤 갈고 레몬즙으로 마무리한다"]},
     {"title":"Lentil Curry","title_ko":"렌틸 커리","time":"30 min","kcal":"350kcal","difficulty":"Medium",
      "steps":["Fry curry paste","Add coconut milk and lentils","Simmer 20 min","Stir in spinach 2 min, serve with rice"],
      "steps_ko":["커리 페이스트를 볶아 향을 낸다","코코넛밀크와 렌틸콩을 넣는다","약불에서 20분 졸인다","시금치를 2분 가열한 뒤 밥과 낸다"]},
     {"title":"Lentil Tacos","title_ko":"렌틸 타코","time":"25 min","kcal":"320kcal","difficulty":"Easy",
      "steps":["Season lentils with cumin, paprika, garlic","Warm tortillas","Prepare avocado, tomato, lettuce","Layer lentils and veggies with salsa"],
      "steps_ko":["렌틸콩을 큐민, 파프리카, 마늘로 볶는다","토르티야를 데운다","아보카도, 토마토, 양상추를 준비한다","토르티야에 렌틸, 채소, 살사를 올린다"]},
     {"title":"Lentil Spinach Stew","title_ko":"렌틸 시금치 스튜","time":"30 min","kcal":"260kcal","difficulty":"Easy",
      "steps":["Sauté onion, garlic, tomato in olive oil","Add lentils and broth, simmer 20 min","Stir in large handful of spinach","Finish with lemon and smoked paprika"],
      "steps_ko":["양파, 마늘, 토마토를 볶는다","렌틸콩과 육수를 넣고 20분 끓인다","시금치를 듬뿍 넣는다","레몬즙과 훈제 파프리카로 마무리한다"]},
   ]},
  {"id":"kale","icon":"🌿","name":"Kale","name_ko":"케일","name_en":"kale",
   "short":"Most nutrient-dense leafy green","short_ko":"영양소 밀도 1위 채소",
   "badge":"Vitamin K","badge_ko":"비타민K","category":"Vegetables","category_ko":"채소",
   "description":"One of the most nutrient-dense foods on the planet. Packed with vitamins C, K, A, plus powerful antioxidants kaempferol and quercetin.",
   "description_ko":"지구상에서 가장 영양소 밀도가 높은 식품 중 하나예요. 비타민 C, K, A와 함께 켐페롤, 케르세틴 항산화 성분이 풍부해요.",
   "effects":["Bone strength","Eye health","Anti-cancer","Heart health","Detox"],
   "effects_ko":["뼈 강화","눈 건강","항암","심장 건강","해독"],
   "nutrition":{"Calories":"49kcal","Protein":"4.3g","Fiber":"3.6g","Carbs":"8.8g","Fat":"0.9g","Vitamin K":"817μg"},
   "recipes":[
     {"title":"Kale Caesar Salad","title_ko":"케일 시저 샐러드","time":"15 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Massage kale with olive oil and salt 2 min","Make Caesar dressing with anchovy, garlic, lemon, parmesan","Toss kale with dressing","Top with croutons and parmesan"],
      "steps_ko":["케일을 올리브오일과 소금으로 2분 마사지한다","안초비, 마늘, 레몬, 파마산으로 시저 드레싱을 만든다","케일과 드레싱을 버무린다","크루통과 파마산을 올린다"]},
     {"title":"Kale Chips","title_ko":"케일 칩","time":"20 min","kcal":"80kcal","difficulty":"Easy",
      "steps":["Tear kale, remove stems","Toss with olive oil and salt","Spread on baking sheet","Bake 160°C for 12–15 min until crispy"],
      "steps_ko":["케일을 뜯어 줄기를 제거한다","올리브오일과 소금으로 버무린다","베이킹 시트에 한 겹으로 편다","160도에서 12~15분 바삭하게 굽는다"]},
     {"title":"Kale Smoothie","title_ko":"케일 스무디","time":"5 min","kcal":"140kcal","difficulty":"Easy",
      "steps":["Add 2 kale leaves, banana, apple to blender","Add almond milk and lemon juice","Blend until smooth","Add ice if desired"],
      "steps_ko":["케일 2잎, 바나나, 사과를 블렌더에 넣는다","아몬드밀크와 레몬즙을 넣는다","곱게 간다","원하면 얼음을 넣어 마신다"]},
     {"title":"Kale White Bean Soup","title_ko":"케일 화이트빈 수프","time":"30 min","kcal":"240kcal","difficulty":"Easy",
      "steps":["Sauté onion, garlic, carrot in olive oil","Add white beans, broth, thyme, simmer 15 min","Stir in kale, cook 5 min","Season with salt, pepper, lemon"],
      "steps_ko":["양파, 마늘, 당근을 올리브오일에 볶는다","화이트빈, 채수, 타임을 넣고 15분 끓인다","케일을 넣고 5분 더 끓인다","소금, 후추, 레몬즙으로 마무리한다"]},
   ]},
  {"id":"beet","icon":"🫚","name":"Beet","name_ko":"비트","name_en":"beet",
   "short":"Nitrate-rich endurance booster","short_ko":"질산염·혈류 개선 식품",
   "badge":"Blood Flow","badge_ko":"혈류 개선","category":"Vegetables","category_ko":"채소",
   "description":"Rich in nitrates that improve blood flow and athletic endurance. Betalain pigments are powerful antioxidants.",
   "description_ko":"질산염이 풍부해 체내에서 산화질소로 변환되어 혈류를 개선하고 운동 지구력을 높여줘요. 비탈라인 색소는 강력한 항산화 성분이에요.",
   "effects":["Blood flow","Athletic performance","Liver detox","Heart health","Anti-inflammatory"],
   "effects_ko":["혈류 개선","운동 능력","간 해독","심장 건강","항염증"],
   "nutrition":{"Calories":"43kcal","Protein":"1.6g","Fiber":"2.8g","Carbs":"9.6g","Fat":"0.2g","Folate":"109μg"},
   "recipes":[
     {"title":"Roasted Beet Salad","title_ko":"구운 비트 샐러드","time":"45 min","kcal":"180kcal","difficulty":"Easy",
      "steps":["Wrap beets in foil, roast 200°C 40 min","Cool, peel, and slice","Arrange with arugula and goat cheese","Drizzle with balsamic glaze and walnuts"],
      "steps_ko":["비트를 호일로 싸서 200도에서 40분 굽는다","식혀서 껍질을 벗기고 슬라이스한다","루꼴라, 염소 치즈와 함께 담는다","발사믹 글레이즈와 호두를 뿌린다"]},
     {"title":"Beet Hummus","title_ko":"비트 훔무스","time":"15 min","kcal":"160kcal","difficulty":"Easy",
      "steps":["Roast or boil beet until tender","Blend with chickpeas, tahini, garlic, lemon","Season with salt and cumin","Serve with pita or vegetables"],
      "steps_ko":["비트를 구워서 부드럽게 만든다","병아리콩, 타히니, 마늘, 레몬과 함께 간다","소금과 큐민으로 간한다","피타빵이나 채소와 함께 낸다"]},
     {"title":"Beet Ginger Smoothie","title_ko":"비트 생강 스무디","time":"5 min","kcal":"130kcal","difficulty":"Easy",
      "steps":["Add cooked beet, apple, ginger to blender","Add orange juice and cinnamon","Blend until smooth","Serve over ice"],
      "steps_ko":["익힌 비트, 사과, 생강을 블렌더에 넣는다","오렌지즙과 시나몬 한 꼬집을 넣는다","곱게 간다","얼음 위에 서브한다"]},
     {"title":"Beet Pasta","title_ko":"비트 파스타","time":"25 min","kcal":"360kcal","difficulty":"Medium",
      "steps":["Blend roasted beet with ricotta, garlic, parmesan","Cook pasta in salted water","Toss hot pasta with beet sauce","Top with walnuts and fresh basil"],
      "steps_ko":["구운 비트, 리코타, 마늘, 파마산으로 소스를 만든다","파스타를 소금물에 삶는다","따뜻한 파스타와 비트 소스를 섞는다","호두와 바질을 올린다"]},
   ]},
  {"id":"spinach","icon":"🥬","name":"Spinach","name_ko":"시금치","name_en":"spinach",
   "short":"Iron and folate powerhouse","short_ko":"철분·엽산의 녹색 보고",
   "badge":"Low Calorie","badge_ko":"저칼로리","category":"Vegetables","category_ko":"채소",
   "description":"Rich in iron, folate, vitamins K and A. Lutein protects eye health, magnesium aids sleep. Only 23 kcal per 100g.",
   "description_ko":"철분, 엽산, 비타민 K, A가 풍부하고 칼로리는 매우 낮아요. 루테인이 눈 건강을 지켜주고, 마그네슘이 수면에 도움을 줘요.",
   "effects":["Anaemia prevention","Eye health","Bone strength","Digestion","Skin care"],
   "effects_ko":["빈혈 예방","눈 건강","뼈 강화","소화 개선","피부 미용"],
   "nutrition":{"Calories":"23kcal","Protein":"2.9g","Fiber":"2.2g","Carbs":"3.6g","Fat":"0.4g","Iron":"2.7mg"},
   "recipes":[
     {"title":"Spinach Egg Stir-Fry","title_ko":"시금치 달걀 볶음","time":"10 min","kcal":"180kcal","difficulty":"Easy",
      "steps":["Wash spinach, pat dry","Sauté garlic in pan","Stir-fry spinach over high heat","Add eggs, soft scramble, season"],
      "steps_ko":["시금치를 씻어 물기를 제거한다","팬에 마늘을 볶는다","시금치를 강불에서 볶는다","달걀을 넣어 반숙으로 익히고 간한다"]},
     {"title":"Spinach Pesto Pasta","title_ko":"시금치 페스토 파스타","time":"20 min","kcal":"380kcal","difficulty":"Medium",
      "steps":["Blend spinach, almonds, garlic, olive oil","Cook pasta in salted water","Toss pasta with pesto","Top with cherry tomatoes and parmesan"],
      "steps_ko":["시금치, 아몬드, 마늘, 올리브오일로 페스토를 만든다","파스타를 소금물에 삶는다","팬에 페스토와 파스타를 섞는다","방울토마토와 파마산을 올린다"]},
     {"title":"Green Spinach Smoothie","title_ko":"시금치 스무디","time":"5 min","kcal":"130kcal","difficulty":"Easy",
      "steps":["Add spinach, banana, almond milk to blender","Add honey and lemon juice","Blend until smooth","Add ice and serve cold"],
      "steps_ko":["시금치, 바나나, 아몬드밀크를 블렌더에 넣는다","꿀과 레몬즙을 넣는다","곱게 갈아준다","얼음을 넣어 차갑게 마신다"]},
     {"title":"Spinach Cheese Quiche","title_ko":"시금치 치즈 키시","time":"40 min","kcal":"320kcal","difficulty":"Medium",
      "steps":["Press pastry into tin, prick with fork","Sauté spinach, squeeze moisture","Mix eggs, cream, cheese, spinach","Bake 180°C for 30 min"],
      "steps_ko":["파이지를 틀에 깔고 포크로 구멍을 낸다","시금치를 볶아 물기를 짠다","달걀, 생크림, 치즈, 시금치를 섞는다","180도에서 30분 굽는다"]},
   ]},
  {"id":"egg","icon":"🥚","name":"Egg","name_ko":"달걀","name_en":"egg",
   "short":"Nature's perfect whole food","short_ko":"완전식품의 대명사",
   "badge":"6g Protein","badge_ko":"단백질 6g","category":"Protein","category_ko":"단백질",
   "description":"The most complete protein in nature — all essential amino acids plus choline for brain health.",
   "description_ko":"달걀은 자연이 만든 가장 완벽한 단백질 공급원이에요. 필수아미노산을 모두 함유하고, 난황에는 뇌 건강에 필수인 콜린이 풍부해요.",
   "effects":["Muscle synthesis","Brain health","Eye health","Satiety","Energy supply"],
   "effects_ko":["근육 합성","뇌 건강","눈 건강","포만감","에너지 공급"],
   "nutrition":{"Calories":"155kcal","Protein":"13.0g","Fiber":"0g","Carbs":"1.1g","Fat":"11.0g","Choline":"294mg"},
   "recipes":[
     {"title":"Egg Frittata","title_ko":"달걀 프리타타","time":"25 min","kcal":"280kcal","difficulty":"Medium",
      "steps":["Beat 4 eggs with salt and pepper","Sauté vegetables in oven-safe pan","Pour eggs over, cook low until edges set","Finish in oven 180°C for 10 min"],
      "steps_ko":["달걀 4개를 풀고 소금, 후추로 간한다","오븐용 팬에 채소를 볶는다","달걀을 붓고 약불에서 가장자리가 굳을 때까지 익힌다","180도 오븐에서 10분 마무리한다"]},
     {"title":"Scrambled Egg Avocado Bowl","title_ko":"스크램블 에그 아보카도 볼","time":"10 min","kcal":"320kcal","difficulty":"Easy",
      "steps":["Beat 2 eggs with milk, salt, pepper","Stir slowly over low heat with butter","Halve avocado, remove pit","Spoon scrambled eggs over avocado"],
      "steps_ko":["달걀 2개에 우유, 소금, 후추를 넣어 푼다","버터 팬에서 약불로 천천히 젓는다","아보카도를 반으로 갈라 씨를 제거한다","아보카도 위에 스크램블 에그를 얹는다"]},
     {"title":"Soft-Boiled Ramen Egg","title_ko":"반숙 라멘 달걀","time":"15 min","kcal":"90kcal","difficulty":"Easy",
      "steps":["Boil eggs exactly 6.5 minutes","Transfer to ice bath immediately","Marinate in soy, mirin, water overnight","Slice and serve on ramen or rice"],
      "steps_ko":["달걀을 정확히 6.5분 삶는다","즉시 얼음물에 넣는다","간장, 미린, 물에 하룻밤 재운다","라멘이나 덮밥에 올려 낸다"]},
     {"title":"Egg Salad Sandwich","title_ko":"달걀 샐러드 샌드위치","time":"12 min","kcal":"340kcal","difficulty":"Easy",
      "steps":["Boil and peel eggs","Mix with mayo, mustard, salt, pepper","Layer on whole grain bread with lettuce","Top with tomato and cucumber"],
      "steps_ko":["달걀을 삶아 껍질을 벗긴다","마요네즈, 머스터드, 소금, 후추와 버무린다","통곡물빵에 양상추를 깔고 달걀 샐러드를 올린다","토마토와 오이 슬라이스를 올린다"]},
   ]},
  {"id":"oats","icon":"🌾","name":"Oats","name_ko":"귀리","name_en":"oats",
   "short":"Beta-glucan for lower cholesterol","short_ko":"베타글루칸·콜레스테롤 감소",
   "badge":"Heart Health","badge_ko":"심장 건강","category":"Whole Grain","category_ko":"통곡물",
   "description":"Rich in beta-glucan soluble fiber — clinically proven to lower cholesterol and prevent blood sugar spikes.",
   "description_ko":"베타글루칸이라는 수용성 식이섬유가 특히 풍부해요. 콜레스테롤을 낮추고 혈당 급등을 막는 데 효과적이에요.",
   "effects":["Lower cholesterol","Blood sugar control","Satiety","Heart health","Gut health"],
   "effects_ko":["콜레스테롤 감소","혈당 조절","포만감","심장 건강","장 건강"],
   "nutrition":{"Calories":"389kcal","Protein":"17.0g","Fiber":"10.6g","Carbs":"66.3g","Fat":"6.9g","Magnesium":"177mg"},
   "recipes":[
     {"title":"Overnight Oats","title_ko":"오버나이트 오츠","time":"5 min+8h","kcal":"320kcal","difficulty":"Easy",
      "steps":["Combine oats and almond milk","Add chia seeds, honey, vanilla","Refrigerate overnight","Top with fruit and nuts in the morning"],
      "steps_ko":["귀리와 아몬드밀크를 용기에 담는다","치아씨드, 꿀, 바닐라를 넣는다","냉장고에 하룻밤 둔다","아침에 과일과 견과류를 올린다"]},
     {"title":"Banana Oat Pancakes","title_ko":"바나나 귀리 팬케이크","time":"20 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Mash banana, mix with eggs and oats","Add cinnamon and baking powder","Cook both sides over low heat","Serve with maple syrup and fruit"],
      "steps_ko":["바나나를 으깨고 달걀과 귀리를 섞는다","시나몬과 베이킹파우더를 넣는다","팬에 약불로 양면을 굽는다","메이플시럽과 과일을 곁들인다"]},
     {"title":"Oat Granola Bars","title_ko":"귀리 그래놀라 바","time":"30 min+2h","kcal":"200kcal","difficulty":"Easy",
      "steps":["Mix oats, nuts, and seeds","Pour in melted honey and coconut oil","Spread flat and bake","Cool, chill 2 hours, slice"],
      "steps_ko":["귀리, 견과류, 씨앗을 섞는다","꿀과 코코넛오일을 녹여 붓는다","트레이에 납작하게 펴서 굽는다","식혀서 냉장고에 2시간 두고 잘라 완성한다"]},
     {"title":"Apple Cinnamon Baked Oats","title_ko":"사과 시나몬 베이크드 오츠","time":"30 min","kcal":"290kcal","difficulty":"Easy",
      "steps":["Mix oats, milk, egg, honey, baking powder, cinnamon","Fold in diced apple and walnuts","Pour into baking dish","Bake 180°C for 25 min"],
      "steps_ko":["귀리, 우유, 달걀, 꿀, 베이킹파우더, 시나몬을 섞는다","사과와 호두를 넣는다","베이킹 용기에 붓는다","180도에서 25분 굽는다"]},
   ]},
  {"id":"kimchi","icon":"🥬","name":"Kimchi","name_ko":"김치","name_en":"kimchi",
   "short":"Probiotic Korean fermented food","short_ko":"유산균·한국 대표 발효식품",
   "badge":"Probiotics","badge_ko":"프로바이오틱스","category":"Fermented","category_ko":"발효식품",
   "description":"UNESCO Intangible Cultural Heritage. Billions of beneficial bacteria for gut health, plus vitamins C and K.",
   "description_ko":"유네스코 무형문화유산에 등재된 한국의 대표 발효식품이에요. 젖산균이 풍부해 장 건강에 탁월하고 비타민 C, K도 풍부해요.",
   "effects":["Gut health","Immunity boost","Antioxidant","Digestion","Weight management"],
   "effects_ko":["장 건강","면역 강화","항산화","소화 촉진","체중 관리"],
   "nutrition":{"Calories":"15kcal","Protein":"1.1g","Fiber":"1.6g","Carbs":"2.4g","Fat":"0.5g","Probiotics":"Billions CFU"},
   "recipes":[
     {"title":"Kimchi Fried Rice","title_ko":"김치 볶음밥","time":"15 min","kcal":"380kcal","difficulty":"Easy",
      "steps":["Stir-fry kimchi in sesame oil","Add rice, stir-fry over high heat","Top with fried egg","Sprinkle seaweed and sesame"],
      "steps_ko":["팬에 참기름을 두르고 김치를 볶는다","밥을 넣고 강불에서 볶는다","달걀 프라이를 올린다","김가루와 참깨를 뿌려 완성한다"]},
     {"title":"Kimchi Tofu Jjigae","title_ko":"김치 두부 찌개","time":"25 min","kcal":"210kcal","difficulty":"Easy",
      "steps":["Stir-fry pork, then add kimchi","Make broth with water, gochugaru, soy sauce","Add tofu and simmer 10 min","Top with scallions and sesame"],
      "steps_ko":["돼지고기를 볶다가 김치를 넣는다","물, 고춧가루, 간장으로 육수를 만든다","두부를 넣고 10분 끓인다","파와 깨를 올려 완성한다"]},
     {"title":"Kimchi Pancakes","title_ko":"김치전","time":"15 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Finely chop kimchi, squeeze liquid","Mix flour, water, egg into batter","Stir kimchi into batter","Pan-fry in oil until golden"],
      "steps_ko":["김치를 잘게 썰어 물기를 짠다","밀가루, 물, 달걀로 반죽을 만든다","김치를 넣어 섞는다","팬에 기름을 두르고 노릇하게 부쳐낸다"]},
     {"title":"Kimchi Pasta","title_ko":"김치 파스타","time":"20 min","kcal":"420kcal","difficulty":"Medium",
      "steps":["Cook pasta in salted water","Stir-fry kimchi in butter","Add heavy cream for sauce","Toss with pasta and top with parmesan"],
      "steps_ko":["파스타를 소금물에 삶는다","버터로 김치를 볶는다","생크림을 넣어 소스를 만든다","파스타와 섞고 파마산을 올린다"]},
   ]},
  {"id":"broccoli","icon":"🥦","name":"Broccoli","name_ko":"브로콜리","name_en":"broccoli",
   "short":"King of anti-cancer vegetables","short_ko":"항암 채소의 왕",
   "badge":"Anti-Cancer","badge_ko":"항암","category":"Vegetables","category_ko":"채소",
   "description":"More vitamin C than oranges. Sulforaphane is a potent anti-cancer compound. Lightly steaming preserves nutrients best.",
   "description_ko":"비타민 C 함량이 오렌지보다 높고 설포라판이라는 항암 성분이 풍부해요. 살짝 데치거나 쪄서 먹는 게 영양 보존에 가장 좋아요.",
   "effects":["Anti-cancer","Immunity boost","Digestion","Bone health","Blood sugar control"],
   "effects_ko":["항암","면역력 강화","소화 개선","뼈 건강","혈당 조절"],
   "nutrition":{"Calories":"34kcal","Protein":"2.8g","Fiber":"2.6g","Carbs":"6.6g","Fat":"0.4g","Vitamin C":"89.2mg"},
   "recipes":[
     {"title":"Garlic Broccoli Stir-Fry","title_ko":"브로콜리 마늘 볶음","time":"10 min","kcal":"120kcal","difficulty":"Easy",
      "steps":["Cut into florets, blanch 30 sec","Brown garlic in pan","Stir-fry over high heat 2 min","Finish with oyster sauce and sesame oil"],
      "steps_ko":["브로콜리를 한 입 크기로 잘라 30초 데친다","팬에 마늘을 볶는다","강불에서 2분 볶는다","굴소스와 참기름으로 마무리한다"]},
     {"title":"Cream of Broccoli Soup","title_ko":"브로콜리 크림수프","time":"25 min","kcal":"210kcal","difficulty":"Medium",
      "steps":["Sauté onion and potato in olive oil","Add broccoli and broth, simmer 15 min","Blend smooth","Stir in heavy cream"],
      "steps_ko":["양파와 감자를 올리브오일에 볶는다","브로콜리와 채수를 넣고 15분 끓인다","핸드블렌더로 곱게 간다","생크림을 넣어 크리미하게 만든다"]},
     {"title":"Broccoli Cheese Omelette","title_ko":"브로콜리 치즈 오믈렛","time":"12 min","kcal":"290kcal","difficulty":"Easy",
      "steps":["Finely chop broccoli, blanch","Beat 3 eggs with salt and pepper","Pour into buttered pan, add broccoli and cheese","Fold in half, heat until cheese melts"],
      "steps_ko":["브로콜리를 잘게 썰어 데친다","달걀 3개를 풀고 소금, 후추로 간한다","버터 팬에 달걀을 붓고 브로콜리와 치즈를 올린다","반으로 접어 치즈가 녹을 때까지 가열한다"]},
     {"title":"Broccoli Quinoa Bowl","title_ko":"브로콜리 퀴노아 볼","time":"25 min","kcal":"320kcal","difficulty":"Easy",
      "steps":["Cook quinoa","Roast broccoli in olive oil 20 min","Make lemon tahini dressing","Top quinoa with broccoli, drizzle dressing"],
      "steps_ko":["퀴노아를 익힌다","브로콜리를 올리브오일로 20분 굽는다","레몬 타히니 드레싱을 만든다","퀴노아 위에 브로콜리를 올리고 드레싱을 뿌린다"]},
   ]},
  {"id":"almond","icon":"🌰","name":"Almond","name_ko":"아몬드","name_en":"almond",
   "short":"Vitamin E antioxidant nut","short_ko":"비타민E·항산화 견과류",
   "badge":"Antioxidant","badge_ko":"항산화","category":"Nuts","category_ko":"견과류",
   "description":"Rich in vitamin E — one of the most powerful fat-soluble antioxidants. Magnesium helps manage blood sugar and blood pressure.",
   "description_ko":"비타민 E가 풍부해 강력한 항산화 작용을 하고 피부 건강을 지켜줘요. 마그네슘이 혈당·혈압 관리에 도움이 돼요.",
   "effects":["Antioxidant","Skin care","Blood sugar control","Heart health","Bone strength"],
   "effects_ko":["항산화","피부 미용","혈당 조절","심장 건강","뼈 강화"],
   "nutrition":{"Calories":"579kcal","Protein":"21.2g","Fiber":"12.5g","Carbs":"21.6g","Fat":"49.9g","Vitamin E":"25.6mg"},
   "recipes":[
     {"title":"Almond Energy Balls","title_ko":"아몬드 에너지 볼","time":"15 min","kcal":"120kcal","difficulty":"Easy",
      "steps":["Process almonds, dates, oats in food processor","Add honey and cocoa; blend until holds","Roll into bite-sized balls","Coat in coconut flakes and chill"],
      "steps_ko":["아몬드, 대추야자, 귀리를 푸드프로세서에 넣는다","꿀과 코코아를 넣고 뭉쳐질 때까지 간다","한 입 크기로 동그랗게 만든다","코코넛 플레이크를 굴려 냉장고에 굳힌다"]},
     {"title":"Almond Butter Toast","title_ko":"아몬드 버터 토스트","time":"5 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Toast whole grain bread","Spread generously with almond butter","Top with banana slices","Drizzle honey, sprinkle chia seeds"],
      "steps_ko":["통곡물빵을 굽는다","아몬드버터를 듬뿍 바른다","바나나 슬라이스를 올린다","꿀을 드리즐하고 치아씨드를 뿌린다"]},
     {"title":"Almond Crusted Chicken","title_ko":"아몬드 크러스트 치킨","time":"30 min","kcal":"380kcal","difficulty":"Medium",
      "steps":["Grind almonds into fine crumb","Dip chicken in egg wash, coat in almond crumbs","Bake at 200°C for 20 min","Finish with lemon and herbs"],
      "steps_ko":["아몬드를 곱게 갈아 가루를 만든다","달걀물에 닭가슴살을 담갔다 아몬드 가루를 묻힌다","200도 오븐에서 20분 굽는다","레몬과 허브로 마무리한다"]},
     {"title":"Almond Granola","title_ko":"아몬드 그래놀라","time":"30 min","kcal":"380kcal","difficulty":"Easy",
      "steps":["Mix oats, sliced almonds, sunflower seeds","Toss with honey, olive oil, cinnamon","Bake at 160°C for 25 min","Cool and mix with raisins and cranberries"],
      "steps_ko":["귀리, 슬라이스 아몬드, 해바라기씨를 섞는다","꿀, 올리브오일, 시나몬으로 버무린다","160도에서 25분 굽는다","식혀서 건포도, 크랜베리와 섞는다"]},
   ]},
  {"id":"greek_yogurt","icon":"🥛","name":"Greek Yogurt","name_ko":"그릭요거트","name_en":"greek yogurt",
   "short":"Probiotic high-protein dairy","short_ko":"프로바이오틱스·고단백",
   "badge":"Gut Health","badge_ko":"장 건강","category":"Dairy","category_ko":"유제품",
   "description":"Higher protein than regular yogurt, with live cultures improving gut health. A cup provides 17–20g of protein.",
   "description_ko":"그릭요거트는 단백질 함량이 높고 유산균이 장 건강을 개선해줘요. 포만감이 오래 지속돼 다이어트식으로도 훌륭해요.",
   "effects":["Gut health","Immunity boost","Bone strength","Satiety","Muscle recovery"],
   "effects_ko":["장 건강","면역력 강화","뼈 강화","포만감","근육 회복"],
   "nutrition":{"Calories":"59kcal","Protein":"10.0g","Fiber":"0g","Carbs":"3.6g","Fat":"0.4g","Calcium":"111mg"},
   "recipes":[
     {"title":"Greek Yogurt Parfait","title_ko":"그릭요거트 파르페","time":"5 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Spoon Greek yogurt into cup","Add granola layer","Top with berries and banana","Drizzle honey, garnish with mint"],
      "steps_ko":["컵에 그릭요거트를 담는다","그래놀라를 올린다","베리류와 바나나를 올린다","꿀을 드리즐하고 민트로 장식한다"]},
     {"title":"Yogurt Chicken Marinade","title_ko":"요거트 닭고기 마리네이드","time":"25 min","kcal":"310kcal","difficulty":"Medium",
      "steps":["Mix yogurt with lemon, garlic, cumin, paprika","Marinate chicken 30+ min","Grill 6 min per side","Serve with herbs and lemon"],
      "steps_ko":["요거트에 레몬즙, 마늘, 큐민, 파프리카를 섞는다","닭가슴살을 30분 이상 재운다","그릴에서 양면 6분씩 굽는다","허브와 레몬을 곁들여 낸다"]},
     {"title":"Frozen Yogurt Bark","title_ko":"냉동 요거트 바크","time":"10 min+3h","kcal":"100kcal","difficulty":"Easy",
      "steps":["Spread Greek yogurt on lined baking sheet","Drizzle honey, add granola, berries, nuts","Freeze 3 hours until solid","Break into pieces and serve"],
      "steps_ko":["그릭요거트를 베이킹 시트에 편다","꿀을 뿌리고 그래놀라, 베리, 견과류를 올린다","3시간 냉동한다","손으로 쪼개서 낸다"]},
     {"title":"Yogurt Pancakes","title_ko":"요거트 팬케이크","time":"20 min","kcal":"260kcal","difficulty":"Easy",
      "steps":["Mix Greek yogurt, egg, oat flour","Add baking powder and honey","Pan-fry on low heat","Serve with fruit and maple syrup"],
      "steps_ko":["그릭요거트, 달걀, 귀리가루를 섞는다","베이킹파우더와 꿀을 넣는다","팬에 약불로 부쳐낸다","과일과 메이플시럽을 곁들인다"]},
   ]},
  {"id":"turmeric","icon":"🟠","name":"Turmeric","name_ko":"강황","name_en":"turmeric",
   "short":"Curcumin anti-inflammatory spice","short_ko":"커큐민·항염 슈퍼 향신료",
   "badge":"Anti-Inflammatory","badge_ko":"항염증","category":"Spices","category_ko":"향신료",
   "description":"Curcumin is one of the most studied natural anti-inflammatory compounds. Add black pepper to increase bioavailability by 2000%.",
   "description_ko":"커큐민은 가장 광범위하게 연구된 천연 항염증 성분 중 하나예요. 후추와 함께 먹으면 흡수율이 2000% 높아져요.",
   "effects":["Anti-inflammatory","Joint health","Brain function","Antioxidant","Digestion"],
   "effects_ko":["항염증","관절 건강","뇌 기능 향상","항산화","소화 개선"],
   "nutrition":{"Calories":"354kcal","Protein":"7.8g","Fiber":"21.1g","Carbs":"64.9g","Fat":"9.9g","Curcumin":"3–5%"},
   "recipes":[
     {"title":"Golden Milk","title_ko":"황금 우유","time":"8 min","kcal":"120kcal","difficulty":"Easy",
      "steps":["Add 1/2 tsp turmeric to milk","Add cinnamon, ginger, black pepper","Heat gently over medium","Sweeten with honey"],
      "steps_ko":["우유에 강황 1/2작은술을 넣는다","시나몬, 생강가루, 후추를 넣는다","중불에서 따뜻하게 데운다","꿀을 넣어 완성한다"]},
     {"title":"Turmeric Lentil Soup","title_ko":"강황 렌틸 수프","time":"30 min","kcal":"260kcal","difficulty":"Easy",
      "steps":["Sauté onion and garlic","Add lentils, broth, turmeric, cumin","Simmer 25 min","Stir in lemon juice and coconut milk"],
      "steps_ko":["양파와 마늘을 볶는다","렌틸콩, 채수, 강황, 큐민을 넣는다","25분 끓인다","레몬즙과 코코넛밀크를 넣어 마무리한다"]},
     {"title":"Turmeric Smoothie","title_ko":"강황 스무디","time":"5 min","kcal":"150kcal","difficulty":"Easy",
      "steps":["Blend banana, mango, 1/2 tsp turmeric","Add coconut milk, ginger, black pepper","Blend smooth","Dust with cinnamon"],
      "steps_ko":["바나나, 망고, 강황 1/2작은술을 넣는다","코코넛밀크, 생강, 후추를 넣는다","곱게 간다","시나몬을 뿌려 완성한다"]},
     {"title":"Turmeric Roasted Cauliflower","title_ko":"강황 구운 콜리플라워","time":"30 min","kcal":"130kcal","difficulty":"Easy",
      "steps":["Cut cauliflower into florets","Toss with olive oil, turmeric, cumin, salt","Roast 200°C for 25 min","Finish with lemon and cilantro"],
      "steps_ko":["콜리플라워를 꽃 부분으로 자른다","올리브오일, 강황, 큐민, 소금으로 버무린다","200도에서 25분 굽는다","레몬즙과 고수로 마무리한다"]},
   ]},
  {"id":"walnut","icon":"🫀","name":"Walnut","name_ko":"호두","name_en":"walnut",
   "short":"Omega-3 brain health nut","short_ko":"오메가-3·뇌 건강 견과류",
   "badge":"Brain Health","badge_ko":"뇌 건강","category":"Nuts","category_ko":"견과류",
   "description":"Rich in plant-based omega-3 ALA and polyphenols that reduce oxidative stress. Even looks like a brain — and it's great for yours.",
   "description_ko":"식물성 오메가-3 ALA와 산화 스트레스를 줄이는 폴리페놀이 풍부해요. 호두의 생김새가 뇌와 닮았고 실제로 뇌 건강에도 좋아요.",
   "effects":["Brain health","Heart protection","Antioxidant","Reduced inflammation","Better sleep"],
   "effects_ko":["뇌 건강","심장 보호","항산화","염증 억제","수면 개선"],
   "nutrition":{"Calories":"654kcal","Protein":"15.2g","Fiber":"6.7g","Carbs":"13.7g","Fat":"65.2g","Omega-3":"9.1g"},
   "recipes":[
     {"title":"Walnut Spinach Salad","title_ko":"호두 시금치 샐러드","time":"12 min","kcal":"240kcal","difficulty":"Easy",
      "steps":["Lightly toast walnuts in dry pan","Prepare spinach, apple, cranberries","Make balsamic dressing","Toss and top with walnuts"],
      "steps_ko":["호두를 팬에 살짝 볶는다","시금치, 사과, 크랜베리를 준비한다","발사믹 드레싱을 만든다","재료를 섞고 호두를 올린다"]},
     {"title":"Walnut Brownies","title_ko":"호두 브라우니","time":"35 min","kcal":"280kcal","difficulty":"Medium",
      "steps":["Melt dark chocolate and butter","Stir in eggs and sugar","Fold in flour, cocoa, salt, walnuts","Bake 180°C for 25 min"],
      "steps_ko":["다크초콜릿과 버터를 중탕으로 녹인다","달걀과 설탕을 넣어 섞는다","밀가루, 코코아, 소금, 호두를 섞는다","180도에서 25분 굽는다"]},
     {"title":"Walnut Banana Smoothie","title_ko":"호두 바나나 스무디","time":"5 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Blend banana, walnuts, almond milk","Add honey and cinnamon","Blend smooth","Top with walnuts"],
      "steps_ko":["바나나, 호두, 아몬드밀크를 블렌더에 넣는다","꿀과 시나몬을 넣는다","곱게 간다","호두를 올린다"]},
     {"title":"Walnut Crusted Salmon","title_ko":"호두 크러스트 연어","time":"25 min","kcal":"420kcal","difficulty":"Medium",
      "steps":["Chop walnuts, mix with Dijon and herbs","Spread on salmon fillet","Bake 200°C for 14–16 min","Serve with roasted vegetables"],
      "steps_ko":["호두를 잘게 썰어 디종 머스터드, 허브와 섞는다","연어 위에 골고루 펴 바른다","200도에서 14~16분 굽는다","구운 채소와 함께 낸다"]},
   ]},
  {"id":"chia","icon":"⚫","name":"Chia Seeds","name_ko":"치아씨드","name_en":"chia seeds",
   "short":"Omega-3 and fibre super seed","short_ko":"오메가-3·식이섬유 슈퍼씨앗",
   "badge":"Superfood","badge_ko":"슈퍼푸드","category":"Seeds","category_ko":"씨앗",
   "description":"Absorb up to 12x their weight in water forming a gel — promoting fullness. Highest plant-based source of calcium and omega-3 ALA.",
   "description_ko":"무게의 12배까지 물을 흡수해 젤 형태가 되어 포만감을 오래 유지시켜줘요. 식물성 칼슘과 오메가-3 ALA의 가장 좋은 공급원이에요.",
   "effects":["Satiety","Bone strength","Heart health","Blood sugar control","Digestion"],
   "effects_ko":["포만감","뼈 강화","심장 건강","혈당 조절","소화 개선"],
   "nutrition":{"Calories":"486kcal","Protein":"16.5g","Fiber":"34.4g","Carbs":"42.1g","Fat":"30.7g","Calcium":"631mg"},
   "recipes":[
     {"title":"Chia Seed Pudding","title_ko":"치아씨드 푸딩","time":"5 min+4h","kcal":"200kcal","difficulty":"Easy",
      "steps":["Pour 1 cup almond milk over 3 tbsp chia","Add honey and vanilla; stir well","Refrigerate at least 4 hours","Top with fruit, nuts, granola"],
      "steps_ko":["치아씨드 3큰술에 아몬드밀크 1컵을 붓는다","꿀과 바닐라를 넣고 잘 섞는다","냉장고에 최소 4시간 둔다","과일, 견과류, 그래놀라를 올린다"]},
     {"title":"Chia Jam","title_ko":"치아씨드 잼","time":"15 min","kcal":"40kcal","difficulty":"Easy",
      "steps":["Heat berries with honey and lemon","Simmer 10 min, stirring","Off heat, stir in chia seeds","Cool and refrigerate"],
      "steps_ko":["베리류, 꿀, 레몬즙을 냄비에서 끓인다","10분 저으며 졸인다","불을 끄고 치아씨드를 넣는다","식혀서 냉장 보관한다"]},
     {"title":"Chia Energy Bars","title_ko":"치아씨드 에너지 바","time":"15 min+2h","kcal":"180kcal","difficulty":"Easy",
      "steps":["Mix oats, chia, almond butter, honey","Stir in chocolate chips and dried fruit","Press flat and refrigerate 2 hours","Cut into bars"],
      "steps_ko":["귀리, 치아씨드, 아몬드버터, 꿀을 섞는다","초코칩과 건과일을 넣는다","납작하게 눌러 냉장고에 2시간 굳힌다","먹기 좋은 크기로 잘라낸다"]},
     {"title":"Chia Yogurt Bowl","title_ko":"치아씨드 요거트 볼","time":"5 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Stir 1 tbsp chia into Greek yogurt","Rest 10 min for chia to swell","Top with fruit and nuts","Drizzle honey"],
      "steps_ko":["그릭요거트에 치아씨드 1큰술을 넣는다","10분 두어 치아씨드가 불어나게 한다","과일과 견과류를 올린다","꿀을 드리즐하여 완성한다"]},
   ]},
  {"id":"mango","icon":"🥭","name":"Mango","name_ko":"망고","name_en":"mango",
   "short":"Tropical vitamin C and folate","short_ko":"열대 비타민C·엽산",
   "badge":"Vitamin C","badge_ko":"비타민C","category":"Fruit","category_ko":"과일",
   "description":"One cup provides nearly 70% of daily vitamin C. Mangiferin has potent anti-diabetic and anti-inflammatory properties.",
   "description_ko":"한 컵으로 하루 비타민 C 필요량의 70%를 채울 수 있어요. 망기페린이라는 독특한 항산화 성분이 강력한 항당뇨 효과를 가져요.",
   "effects":["Immunity boost","Skin health","Eye protection","Digestive enzymes","Anti-inflammatory"],
   "effects_ko":["면역 강화","피부 건강","눈 보호","소화 효소","항염증"],
   "nutrition":{"Calories":"60kcal","Protein":"0.8g","Fiber":"1.6g","Carbs":"15.0g","Fat":"0.4g","Vitamin C":"36.4mg"},
   "recipes":[
     {"title":"Mango Salsa","title_ko":"망고 살사","time":"10 min","kcal":"80kcal","difficulty":"Easy",
      "steps":["Dice ripe mango, red onion, jalapeño, cilantro","Add lime juice and pinch of salt","Mix gently","Serve with grilled fish or tacos"],
      "steps_ko":["잘 익은 망고, 적양파, 할라피뇨, 고수를 썬다","라임즙과 소금을 넣는다","가볍게 섞는다","구운 생선이나 타코와 함께 낸다"]},
     {"title":"Mango Lassi","title_ko":"망고 라씨","time":"5 min","kcal":"190kcal","difficulty":"Easy",
      "steps":["Blend ripe mango with yogurt","Add cardamom and honey","Blend until smooth","Serve over ice"],
      "steps_ko":["잘 익은 망고와 요거트를 블렌더에 넣는다","카다몬 한 꼬집과 꿀을 넣는다","곱게 간다","얼음 위에 서브한다"]},
     {"title":"Mango Avocado Salad","title_ko":"망고 아보카도 샐러드","time":"10 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Slice mango and avocado","Add red onion, cucumber, cilantro","Dress with lime, olive oil, chili flakes","Toss gently and serve"],
      "steps_ko":["망고와 아보카도를 슬라이스한다","적양파, 오이, 고수를 넣는다","라임즙, 올리브오일, 고추 플레이크로 드레싱한다","가볍게 버무려 낸다"]},
     {"title":"Mango Chicken Stir-Fry","title_ko":"망고 치킨 볶음","time":"20 min","kcal":"320kcal","difficulty":"Medium",
      "steps":["Stir-fry chicken with garlic and ginger","Add bell pepper and snap peas","Add diced mango and soy-lime sauce","Toss and serve over jasmine rice"],
      "steps_ko":["닭고기를 마늘, 생강과 볶는다","파프리카와 스냅피를 넣는다","망고와 간장-라임 소스를 넣는다","버무려서 재스민 라이스와 함께 낸다"]},
   ]},
  {"id":"sardine","icon":"🐟","name":"Sardine","name_ko":"정어리","name_en":"sardine",
   "short":"Omega-3 and calcium-rich small fish","short_ko":"오메가-3·칼슘 풍부한 작은 생선",
   "badge":"Sustainable","badge_ko":"지속가능","category":"Seafood","category_ko":"해산물",
   "description":"Among the most nutrient-dense foods. Rich in omega-3, vitamin D, and calcium from edible bones. Most sustainable seafood choice.",
   "description_ko":"영양소 밀도가 가장 높은 식품 중 하나예요. 오메가-3, 비타민 D, 먹을 수 있는 뼈에서 나오는 칼슘이 풍부해요.",
   "effects":["Brain health","Bone strength","Heart health","Vitamin D","Anti-inflammatory"],
   "effects_ko":["뇌 건강","뼈 강화","심장 건강","비타민D","항염증"],
   "nutrition":{"Calories":"208kcal","Protein":"24.6g","Fiber":"0g","Carbs":"0g","Fat":"11.5g","Calcium":"382mg"},
   "recipes":[
     {"title":"Sardine Toast","title_ko":"정어리 토스트","time":"8 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Toast sourdough bread","Mash sardines with lemon and Dijon","Spread over toast","Top with cucumber, red onion, capers"],
      "steps_ko":["사워도우 빵을 굽는다","정어리를 레몬즙과 디종 머스터드로 으깬다","빵에 펴 바른다","오이, 적양파, 케이퍼를 올린다"]},
     {"title":"Sardine Pasta","title_ko":"정어리 파스타","time":"20 min","kcal":"420kcal","difficulty":"Easy",
      "steps":["Cook pasta in salted water","Sauté garlic, chili flakes, sardines in olive oil","Flake sardines, add pasta water","Toss pasta, finish with lemon and parsley"],
      "steps_ko":["파스타를 소금물에 삶는다","올리브오일에 마늘, 고추, 정어리를 볶는다","정어리를 부수고 면수를 넣는다","파스타와 섞고 레몬, 파슬리로 마무리한다"]},
     {"title":"Sardine Salad","title_ko":"정어리 샐러드","time":"10 min","kcal":"240kcal","difficulty":"Easy",
      "steps":["Mix sardines with lemon and olive oil","Add cherry tomatoes, olives, red onion","Toss with mixed greens","Finish with fresh parsley"],
      "steps_ko":["정어리를 레몬즙과 올리브오일로 섞는다","방울토마토, 올리브, 적양파를 넣는다","혼합 채소와 버무린다","파슬리로 마무리한다"]},
     {"title":"Sardine Crostini","title_ko":"정어리 크로스티니","time":"12 min","kcal":"200kcal","difficulty":"Easy",
      "steps":["Slice baguette, brush with olive oil, toast","Spread with cream cheese","Top with sardine fillets","Garnish with dill and lemon zest"],
      "steps_ko":["바게트를 슬라이스하고 올리브오일을 발라 굽는다","크림치즈를 바른다","정어리 필레를 올린다","딜과 레몬 제스트로 장식한다"]},
   ]},
  {"id":"ginger","icon":"🫚","name":"Ginger","name_ko":"생강","name_en":"ginger",
   "short":"Anti-nausea and anti-inflammatory root","short_ko":"항구역질·항염 뿌리 식품",
   "badge":"Digestive Aid","badge_ko":"소화 촉진","category":"Spices","category_ko":"향신료",
   "description":"Gingerol is one of the most powerful anti-inflammatory compounds in nature. Clinically effective for nausea and digestive issues.",
   "description_ko":"진저롤은 자연에서 가장 강력한 항염증 성분 중 하나예요. 메스꺼움과 소화 장애에 임상적으로 효과적이에요.",
   "effects":["Nausea relief","Anti-inflammatory","Digestive aid","Immune support","Muscle recovery"],
   "effects_ko":["구역질 완화","항염증","소화 촉진","면역 강화","근육 회복"],
   "nutrition":{"Calories":"80kcal","Protein":"1.8g","Fiber":"2.0g","Carbs":"17.8g","Fat":"0.8g","Gingerol":"Abundant"},
   "recipes":[
     {"title":"Ginger Lemon Tea","title_ko":"생강 레몬 차","time":"8 min","kcal":"30kcal","difficulty":"Easy",
      "steps":["Slice fresh ginger thinly","Simmer in water 5 minutes","Squeeze in lemon juice","Sweeten with honey"],
      "steps_ko":["생강을 얇게 슬라이스한다","물에서 5분 끓인다","레몬즙을 넣는다","꿀로 달콤하게 마무리한다"]},
     {"title":"Ginger Carrot Soup","title_ko":"생강 당근 수프","time":"30 min","kcal":"150kcal","difficulty":"Easy",
      "steps":["Sauté onion and ginger in olive oil","Add carrots and broth, simmer 20 min","Blend smooth","Finish with coconut milk and lime"],
      "steps_ko":["양파와 생강을 올리브오일에 볶는다","당근과 채수를 넣고 20분 끓인다","핸드블렌더로 곱게 간다","코코넛밀크와 라임즙으로 마무리한다"]},
     {"title":"Mango Ginger Smoothie","title_ko":"망고 생강 스무디","time":"5 min","kcal":"180kcal","difficulty":"Easy",
      "steps":["Blend frozen mango, banana, fresh ginger","Add coconut milk and turmeric","Blend until smooth","Garnish with fresh mint"],
      "steps_ko":["냉동 망고, 바나나, 생강을 블렌더에 넣는다","코코넛밀크와 강황을 넣는다","곱게 간다","민트로 장식한다"]},
     {"title":"Ginger Stir-Fry Sauce","title_ko":"생강 볶음 소스","time":"5 min","kcal":"60kcal","difficulty":"Easy",
      "steps":["Grate fresh ginger finely","Mix with soy sauce, garlic, sesame oil, honey","Add rice vinegar","Use as stir-fry sauce or marinade"],
      "steps_ko":["생강을 곱게 간다","간장, 마늘, 참기름, 꿀과 섞는다","식초를 조금 넣는다","볶음 소스나 마리네이드로 활용한다"]},
   ]},
  {"id":"kefir","icon":"🥛","name":"Kefir","name_ko":"케피어","name_en":"kefir",
   "short":"50+ probiotic strains","short_ko":"50종 이상의 유산균",
   "badge":"Probiotic King","badge_ko":"프로바이오틱 챔피언","category":"Fermented","category_ko":"발효식품",
   "description":"Contains up to 50 different strains of beneficial bacteria — far more than regular yogurt. Studies show it can inhibit tumour growth.",
   "description_ko":"최대 50가지 종류의 유익한 균과 효모를 함유해요. 일반 요거트보다 훨씬 다양한 균이 있으며 종양 억제 효과도 연구되었어요.",
   "effects":["Gut health","Immunity boost","Bone strength","Reduced allergies","Anti-cancer"],
   "effects_ko":["장 건강","면역 강화","뼈 강화","알레르기 감소","항암"],
   "nutrition":{"Calories":"61kcal","Protein":"3.8g","Fiber":"0g","Carbs":"4.8g","Fat":"3.5g","Probiotics":"50+ strains"},
   "recipes":[
     {"title":"Kefir Smoothie","title_ko":"케피어 스무디","time":"5 min","kcal":"220kcal","difficulty":"Easy",
      "steps":["Add kefir, banana, frozen berries to blender","Add drizzle of honey","Blend smooth","Pour and serve immediately"],
      "steps_ko":["케피어, 바나나, 냉동 베리를 블렌더에 넣는다","꿀을 조금 넣는다","곱게 간다","즉시 서브한다"]},
     {"title":"Kefir Overnight Oats","title_ko":"케피어 오버나이트 오츠","time":"5 min+8h","kcal":"310kcal","difficulty":"Easy",
      "steps":["Mix oats with kefir instead of milk","Add chia seeds, honey, vanilla","Refrigerate overnight","Top with fruit and granola"],
      "steps_ko":["우유 대신 케피어로 귀리를 섞는다","치아씨드, 꿀, 바닐라를 넣는다","냉장고에 하룻밤 둔다","과일과 그래놀라를 올린다"]},
     {"title":"Kefir Marinated Chicken","title_ko":"케피어 마리네이드 치킨","time":"30 min+marinate","kcal":"290kcal","difficulty":"Medium",
      "steps":["Marinate chicken in kefir, garlic, lemon, herbs overnight","The acid tenderises the meat","Grill or bake 200°C until cooked","Serve with salad and pita"],
      "steps_ko":["닭고기를 케피어, 마늘, 레몬, 허브에 하룻밤 재운다","산성이 고기를 부드럽게 만든다","그릴 또는 200도에서 굽는다","샐러드와 피타와 함께 낸다"]},
     {"title":"Kefir Berry Popsicles","title_ko":"케피어 베리 아이스바","time":"10 min+4h","kcal":"80kcal","difficulty":"Easy",
      "steps":["Blend kefir with mixed berries and honey","Pour into popsicle molds","Freeze for at least 4 hours","Run under warm water to unmold"],
      "steps_ko":["케피어, 혼합 베리, 꿀을 블렌딩한다","아이스바 틀에 붓는다","4시간 이상 냉동한다","따뜻한 물에 잠깐 담가 틀을 뺀다"]},
   ]},
  {"id":"hemp_seeds","icon":"🌿","name":"Hemp Seeds","name_ko":"햄프씨드","name_en":"hemp seeds",
   "short":"Perfect omega-6 to omega-3 ratio","short_ko":"이상적인 오메가6:3 비율",
   "badge":"Complete Protein","badge_ko":"완전단백질","category":"Seeds","category_ko":"씨앗",
   "description":"A perfectly balanced omega-6 to omega-3 ratio of 3:1. One of few plant sources of complete protein, rich in GLA.",
   "description_ko":"오메가-6와 오메가-3의 비율이 3:1로 인간 건강에 이상적이에요. 완전단백질을 제공하는 몇 안 되는 식물성 식품이에요.",
   "effects":["Heart health","Brain health","Anti-inflammatory","Muscle recovery","Hormone balance"],
   "effects_ko":["심장 건강","뇌 건강","항염증","근육 회복","호르몬 균형"],
   "nutrition":{"Calories":"553kcal","Protein":"31.6g","Fiber":"4.0g","Carbs":"8.7g","Fat":"48.8g","Omega-3":"8.7g"},
   "recipes":[
     {"title":"Hemp Seed Power Bowl","title_ko":"햄프씨드 파워 볼","time":"10 min","kcal":"350kcal","difficulty":"Easy",
      "steps":["Base of quinoa or brown rice","Top with roasted veggies and avocado","Sprinkle 3 tbsp hemp seeds","Drizzle lemon tahini dressing"],
      "steps_ko":["퀴노아나 현미밥을 베이스로 깐다","구운 채소와 아보카도를 올린다","햄프씨드 3큰술을 뿌린다","레몬 타히니 드레싱을 드리즐한다"]},
     {"title":"Hemp Seed Smoothie","title_ko":"햄프씨드 스무디","time":"5 min","kcal":"320kcal","difficulty":"Easy",
      "steps":["Blend banana, spinach, almond milk","Add 3 tbsp hemp seeds and almond butter","Add honey, blend smooth","Pour and serve"],
      "steps_ko":["바나나, 시금치, 아몬드밀크를 블렌딩한다","햄프씨드 3큰술과 아몬드버터를 넣는다","꿀을 넣고 곱게 간다","잔에 따라 서브한다"]},
     {"title":"Hemp Energy Bites","title_ko":"햄프씨드 에너지 볼","time":"15 min","kcal":"130kcal","difficulty":"Easy",
      "steps":["Mix oats, hemp seeds, almond butter, honey","Add chocolate chips and shredded coconut","Roll into balls","Refrigerate 30 min to firm up"],
      "steps_ko":["귀리, 햄프씨드, 아몬드버터, 꿀을 섞는다","초코칩과 코코넛 채를 넣는다","동그랗게 빚는다","냉장고에 30분 굳힌다"]},
     {"title":"Hemp Seed Pesto","title_ko":"햄프씨드 페스토","time":"10 min","kcal":"140kcal","difficulty":"Easy",
      "steps":["Blend hemp seeds, basil, garlic, olive oil, lemon","Add parmesan and blend again","Season with salt","Toss with pasta or use as dip"],
      "steps_ko":["햄프씨드, 바질, 마늘, 올리브오일, 레몬을 갈아준다","파마산을 넣고 다시 간다","소금으로 간한다","파스타에 버무리거나 딥으로 활용한다"]},
   ]},
  {"id":"pomegranate","icon":"🍎","name":"Pomegranate","name_ko":"석류","name_en":"pomegranate",
   "short":"3x more antioxidants than red wine","short_ko":"레드와인의 3배 항산화력",
   "badge":"Antioxidant King","badge_ko":"항산화 챔피언","category":"Fruit","category_ko":"과일",
   "description":"Contains punicalagin and punicic acid found nowhere else. Studies show 3x more antioxidant activity than red wine or green tea.",
   "description_ko":"퓨니칼라긴과 퓨니식산은 석류에서만 발견되는 특별한 성분이에요. 연구에 따르면 레드와인이나 녹차보다 3배 더 높은 항산화 활성을 가져요.",
   "effects":["Antioxidant","Heart health","Anti-cancer","Reduced inflammation","Memory improvement"],
   "effects_ko":["항산화","심장 건강","항암","염증 억제","기억력 향상"],
   "nutrition":{"Calories":"83kcal","Protein":"1.7g","Fiber":"4.0g","Carbs":"18.7g","Fat":"1.2g","Vitamin C":"10.2mg"},
   "recipes":[
     {"title":"Pomegranate Salad","title_ko":"석류 샐러드","time":"10 min","kcal":"180kcal","difficulty":"Easy",
      "steps":["Combine mixed greens, pomegranate seeds, walnuts","Add crumbled feta cheese","Dress with pomegranate molasses, olive oil, lemon","Toss gently"],
      "steps_ko":["혼합 채소, 석류 씨앗, 호두를 담는다","페타 치즈를 부숴 넣는다","석류 시럽, 올리브오일, 레몬으로 드레싱한다","가볍게 버무린다"]},
     {"title":"Overnight Pomegranate Oats","title_ko":"석류 오버나이트 오츠","time":"5 min+8h","kcal":"280kcal","difficulty":"Easy",
      "steps":["Mix oats, almond milk, chia seeds, vanilla","Refrigerate overnight","Top with Greek yogurt and pomegranate seeds","Drizzle with honey"],
      "steps_ko":["귀리, 아몬드밀크, 치아씨드, 바닐라를 섞는다","냉장고에 하룻밤 둔다","그릭요거트와 석류 씨앗을 올린다","꿀을 드리즐한다"]},
     {"title":"Pomegranate Iced Tea","title_ko":"석류 아이스티","time":"10 min","kcal":"40kcal","difficulty":"Easy",
      "steps":["Brew green tea and let cool","Add pomegranate juice and lemon","Sweeten with honey","Serve over ice with mint"],
      "steps_ko":["녹차를 우려서 식힌다","석류즙과 레몬즙을 넣는다","꿀로 달콤하게 만든다","얼음과 민트를 넣어 낸다"]},
     {"title":"Pomegranate Glazed Salmon","title_ko":"석류 글레이즈 연어","time":"25 min","kcal":"340kcal","difficulty":"Medium",
      "steps":["Reduce pomegranate juice with honey and rosemary","Season salmon with salt and pepper","Sear in hot pan 3 min each side","Brush with glaze, finish 180°C 8 min"],
      "steps_ko":["석류즙, 꿀, 로즈마리로 글레이즈를 만든다","연어에 소금, 후추를 뿌린다","뜨거운 팬에서 양면 3분씩 굽는다","글레이즈를 바르고 180도에서 8분 마무리한다"]},
   ]},
  {"id":"tuna","icon":"🐟","name":"Tuna","name_ko":"참치","name_en":"tuna",
   "short":"Lean protein powerhouse","short_ko":"저지방 고단백 생선",
   "badge":"Low Fat","badge_ko":"저지방","category":"Seafood","category_ko":"해산물",
   "description":"One of the leanest high-protein foods. Rich in selenium, B12, and niacin. Great for muscle building on a budget.",
   "description_ko":"가장 단백질이 풍부하면서 지방이 적은 식품 중 하나예요. 셀레늄, B12, 나이아신이 풍부해요.",
   "effects":["Muscle synthesis","Heart health","Immunity","Brain health","Weight management"],
   "effects_ko":["근육 합성","심장 건강","면역력","뇌 건강","체중 관리"],
   "nutrition":{"Calories":"144kcal","Protein":"23.3g","Fiber":"0g","Carbs":"0g","Fat":"5.1g","Selenium":"36.5μg"},
   "recipes":[
     {"title":"Tuna Avocado Bowl","title_ko":"참치 아보카도 볼","time":"10 min","kcal":"350kcal","difficulty":"Easy",
      "steps":["Drain tuna and flake into bowl","Add diced avocado, cucumber, edamame","Season with soy sauce, sesame oil, sriracha","Serve over brown rice"],
      "steps_ko":["참치를 체에 걸러 볼에 담는다","아보카도, 오이, 에다마메를 썰어 넣는다","간장, 참기름, 스리라차로 간한다","현미밥 위에 올린다"]},
     {"title":"Tuna Melt","title_ko":"참치 멜트 토스트","time":"12 min","kcal":"380kcal","difficulty":"Easy",
      "steps":["Mix tuna with mayo, celery, red onion, lemon","Spread on bread, top with cheddar","Broil until cheese is melted","Serve with pickles and salad"],
      "steps_ko":["참치를 마요, 셀러리, 적양파, 레몬으로 섞는다","빵에 펴 바르고 체다치즈를 올린다","오븐에서 치즈가 녹을 때까지 굽는다","피클과 샐러드와 함께 낸다"]},
     {"title":"Nicoise Salad","title_ko":"니수아즈 샐러드","time":"20 min","kcal":"310kcal","difficulty":"Medium",
      "steps":["Boil eggs, green beans, and potatoes","Arrange with tuna, olives, tomatoes","Make French vinaigrette with Dijon","Drizzle over salad and season"],
      "steps_ko":["달걀, 그린빈, 감자를 각각 삶는다","참치, 올리브, 토마토와 함께 플래터에 담는다","디종으로 비네그레트를 만든다","드레싱을 뿌리고 간한다"]},
     {"title":"Tuna Pasta Salad","title_ko":"참치 파스타 샐러드","time":"20 min","kcal":"390kcal","difficulty":"Easy",
      "steps":["Cook pasta, rinse under cold water","Mix with tuna, corn, peas, red onion","Add mayo, lemon juice, salt, pepper","Chill and serve"],
      "steps_ko":["파스타를 삶아 찬물에 헹군다","참치, 옥수수, 완두콩, 적양파와 섞는다","마요, 레몬즙, 소금, 후추를 넣는다","냉장해서 낸다"]},
   ]},
  {"id":"edamame","icon":"🫛","name":"Edamame","name_ko":"에다마메","name_en":"edamame",
   "short":"Complete protein young soybeans","short_ko":"완전단백질 풋콩",
   "badge":"Plant Protein","badge_ko":"식물성단백질","category":"Legumes","category_ko":"콩류",
   "description":"Young soybeans with all essential amino acids. Rich in isoflavones supporting heart and bone health.",
   "description_ko":"필수아미노산을 모두 함유한 몇 안 되는 식물성 식품이에요. 심장과 뼈 건강에 좋은 이소플라본이 풍부해요.",
   "effects":["Complete protein","Bone health","Heart health","Blood sugar control","Antioxidant"],
   "effects_ko":["완전단백질","뼈 건강","심장 건강","혈당 조절","항산화"],
   "nutrition":{"Calories":"121kcal","Protein":"11.9g","Fiber":"5.2g","Carbs":"8.9g","Fat":"5.2g","Iron":"2.3mg"},
   "recipes":[
     {"title":"Salted Edamame","title_ko":"소금 에다마메","time":"8 min","kcal":"120kcal","difficulty":"Easy",
      "steps":["Boil edamame in salted water 4–5 min","Drain and toss with flaky sea salt","Optional: add sesame oil and chili flakes","Squeeze pods into mouth to eat"],
      "steps_ko":["에다마메를 소금물에 4~5분 삶는다","건져서 즉시 굵은 소금과 버무린다","참기름과 고추 플레이크를 넣어도 좋다","꼬투리를 눌러 콩을 빼 먹는다"]},
     {"title":"Edamame Hummus","title_ko":"에다마메 훔무스","time":"10 min","kcal":"160kcal","difficulty":"Easy",
      "steps":["Blend shelled edamame with garlic, lemon, tahini","Add olive oil and season with salt","Drizzle with olive oil and sesame seeds","Serve with pita or crudités"],
      "steps_ko":["껍질 깐 에다마메, 마늘, 레몬즙, 타히니를 간다","올리브오일을 넣고 소금으로 간한다","올리브오일과 참깨를 뿌린다","피타빵이나 채소 스틱과 함께 낸다"]},
     {"title":"Edamame Fried Rice","title_ko":"에다마메 볶음밥","time":"15 min","kcal":"340kcal","difficulty":"Easy",
      "steps":["Stir-fry garlic and ginger in sesame oil","Add leftover rice, stir-fry high heat","Add edamame, corn, soy sauce, eggs","Top with scallions and sesame"],
      "steps_ko":["참기름에 마늘, 생강을 볶는다","찬밥을 넣고 강불에서 볶는다","에다마메, 옥수수, 간장, 달걀을 넣는다","파와 참깨를 뿌린다"]},
     {"title":"Edamame Avocado Toast","title_ko":"에다마메 아보카도 토스트","time":"10 min","kcal":"280kcal","difficulty":"Easy",
      "steps":["Mash edamame and avocado with lemon","Season with salt, pepper, red pepper flakes","Spread on toasted sourdough","Top with sesame seeds and microgreens"],
      "steps_ko":["에다마메와 아보카도를 레몬즙과 함께 으깬다","소금, 후추, 고추 플레이크로 간한다","구운 사워도우에 펴 바른다","참깨와 새싹 채소를 올린다"]},
   ]},
]
def call_claude(prompt, system="You are a helpful nutrition assistant. Respond only in JSON when asked."):
    try:
        resp = requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1500,
                  "system":system,
                  "messages":[{"role":"user","content":prompt}]},
            timeout=30)
        data = resp.json()
        return "".join(b["text"] for b in data.get("content",[]) if b.get("type")=="text")
    except Exception as e:
        return f"Error: {e}"

def ai_add_ingredient(name):
    prompt = f"""Create a nutrition profile for: "{name}"
Return ONLY valid JSON, no markdown:
{{"id":"snake_case","icon":"emoji","name":"English name","name_ko":"한국어 이름","name_en":"english",
"short":"one line EN","short_ko":"한줄 KO","badge":"badge EN","badge_ko":"배지 KO",
"category":"category EN","category_ko":"카테고리 KO",
"description":"2-3 sentences EN","description_ko":"2-3문장 KO",
"effects":["e1","e2","e3","e4","e5"],"effects_ko":["효능1","효능2","효능3","효능4","효능5"],
"nutrition":{{"Calories":"Xkcal","Protein":"Xg","Fiber":"Xg","Carbs":"Xg","Fat":"Xg","key":"val"}},
"recipes":[
  {{"title":"Recipe EN","title_ko":"레시피 KO","time":"X min","kcal":"Xkcal","difficulty":"Easy",
   "steps":["s1","s2","s3","s4"],"steps_ko":["단1","단2","단3","단4"]}},
  {{"title":"Recipe 2 EN","title_ko":"레시피2 KO","time":"X min","kcal":"Xkcal","difficulty":"Easy",
   "steps":["s1","s2","s3","s4"],"steps_ko":["단1","단2","단3","단4"]}}
]}}"""
    raw = call_claude(prompt)
    raw = raw.replace("```json","").replace("```","").strip()
    try:
        return json.loads(raw)
    except:
        return None

def ai_health_score(meal_name, diary_note, photo_b64=None):
    content = [{"type":"text","text":f"""Analyze this meal for health score.
Meal: {meal_name}
Notes: {diary_note}
Return ONLY JSON: {{"score":75,"grade":"B+","feedback_en":"...","feedback_ko":"...","suggestions_en":"...","suggestions_ko":"..."}}"""}]
    if photo_b64:
        content.insert(0,{"type":"image","source":{"type":"base64","media_type":"image/jpeg","data":photo_b64}})
    try:
        resp = requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":600,
                  "messages":[{"role":"user","content":content}]},
            timeout=30)
        data = resp.json()
        raw = "".join(b["text"] for b in data.get("content",[]) if b.get("type")=="text")
        raw = raw.replace("```json","").replace("```","").strip()
        return json.loads(raw)
    except:
        return None

def do_search_ingr(q, all_ings):
    q = q.strip().lower()
    if not q: return []
    return [i for i in all_ings if
            q in i["name"].lower() or
            q in i.get("name_ko","").lower() or
            q in i["name_en"].lower() or
            q in i["short"].lower() or
            q in i.get("short_ko","").lower() or
            q in i["category"].lower() or
            q in i.get("category_ko","").lower() or
            any(q in e.lower() for e in i["effects"]) or
            any(q in e.lower() for e in i.get("effects_ko",[]))]

def do_search_recipe(q, all_ings):
    q = q.strip().lower()
    if not q: return []
    results = []
    for ing in all_ings:
        for rec in ing["recipes"]:
            if (q in rec["title"].lower() or
                q in rec.get("title_ko","").lower() or
                q in ing["name"].lower() or
                q in ing.get("name_ko","").lower()):
                results.append((ing, rec))
    return results

def render_ing_detail(ing):
    lang = st.session_state.lang
    effects = ing.get("effects_ko",[]) if lang=="ko" else ing["effects"]
    desc = ing.get("description_ko","") if lang=="ko" else ing["description"]
    eff_html = "".join(f'<span class="eff">{e}</span>' for e in effects)
    nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in ing["nutrition"].items())
    name_d = ing.get("name_ko",ing["name"]) if lang=="ko" else ing["name"]
    st.markdown(f"""
    <div class="detail-box">
        <div class="d-title">{ing['icon']} {name_d}</div>
        <div class="d-desc">{desc}</div>
        <div class="d-lbl">{t('key_benefits')}</div><div class="effects">{eff_html}</div>
        <div class="d-lbl">{t('nutrition')}</div><div class="nut-grid">{nut_html}</div>
    </div>""", unsafe_allow_html=True)

def render_recipe_card(ing, rec):
    lang = st.session_state.lang
    title = rec.get("title_ko",rec["title"]) if lang=="ko" else rec["title"]
    steps = rec.get("steps_ko",rec["steps"]) if lang=="ko" else rec["steps"]
    diff_label = t("difficulty", rec["difficulty"])
    dc = {"Easy":"#2C5F21","Medium":"#7A5C00","Hard":"#8B0000"}.get(rec["difficulty"],"#555")
    steps_html = "".join(f'<div class="r-step"><span class="r-num">{j+1}</span><span>{s}</span></div>' for j,s in enumerate(steps))
    img_url = RECIPE_IMAGES.get(rec["title"], RECIPE_IMAGES["default"])
    st.markdown(f"""
    <div class="recipe-card">
        <img src="{img_url}" style="width:100%;height:180px;object-fit:cover;border-radius:10px;margin-bottom:14px;" onerror="this.style.display='none'"/>
        <div class="r-title">{title}</div>
        <div class="r-meta">
            <span>⏱ {rec['time']}</span><span>🔥 {rec['kcal']}</span>
            <span>🌿 {ing.get('name_ko',ing['name']) if lang=='ko' else ing['name']}</span>
            <span style="color:{dc};font-weight:500;">● {diff_label}</span>
        </div>
        {steps_html}
    </div>""", unsafe_allow_html=True)
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,header,footer{visibility:hidden;}
.stApp{background:#F7F5F0;}
.nav{display:flex;align-items:center;justify-content:space-between;padding:14px 0 10px;border-bottom:1px solid #E2DDD4;margin-bottom:24px;}
.nav-logo{font-family:'DM Serif Display',serif;font-size:22px;color:#2C3A1E;display:flex;align-items:center;gap:8px;}
.nav-dot{width:9px;height:9px;border-radius:50%;background:#4A7C3F;display:inline-block;}
.nav-tag{font-size:11px;color:#6B7A60;font-style:italic;}
.hero-wrap{position:relative;border-radius:18px;overflow:hidden;margin-bottom:28px;min-height:300px;}
.hero-img{width:100%;height:320px;object-fit:cover;display:block;filter:brightness(0.52);}
.hero-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;width:90%;}
.hero-eye{color:#A8D5A2;font-size:11px;font-weight:500;letter-spacing:.15em;margin-bottom:8px;}
.hero-title{font-family:'DM Serif Display',serif;font-size:38px;color:#fff;line-height:1.2;margin-bottom:10px;}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.85);line-height:1.65;}
.stat-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.25);border-radius:99px;padding:6px 16px;color:#fff;font-size:13px;font-weight:500;margin:4px;}
.stat-num{font-family:'DM Serif Display',serif;font-size:20px;color:#A8D5A2;}
.sec-title{font-family:'DM Serif Display',serif;font-size:20px;color:#2C3A1E;margin-bottom:4px;}
.sec-sub{font-size:12px;color:#7A8A70;margin-bottom:16px;}
.ingr-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:18px 12px;text-align:center;}
.i-icon{font-size:30px;margin-bottom:7px;}
.i-name{font-weight:500;font-size:13px;color:#2C3A1E;margin-bottom:3px;}
.i-short{font-size:11px;color:#7A8A70;line-height:1.4;margin-bottom:6px;}
.i-badge{display:inline-block;font-size:10px;font-weight:500;padding:2px 8px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}
.search-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:16px;margin-bottom:10px;display:flex;align-items:center;gap:14px;}
.search-icon{font-size:30px;flex-shrink:0;}
.search-info{flex:1;}
.search-name{font-weight:500;font-size:15px;color:#2C3A1E;margin-bottom:2px;}
.search-short{font-size:12px;color:#7A8A70;margin-bottom:5px;}
.search-badges{display:flex;gap:5px;flex-wrap:wrap;}
.s-badge{font-size:10px;font-weight:500;padding:2px 8px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}
.detail-box{background:#F0F7EB;border:1.5px solid #C5DDB8;border-radius:14px;padding:20px;margin-bottom:12px;}
.d-title{font-family:'DM Serif Display',serif;font-size:18px;color:#2C3A1E;margin-bottom:5px;}
.d-desc{font-size:13px;color:#4A5A40;line-height:1.75;margin-bottom:12px;}
.d-lbl{font-size:10px;font-weight:500;letter-spacing:.07em;color:#7A8A70;margin-bottom:5px;}
.effects{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px;}
.eff{font-size:11px;padding:3px 9px;border-radius:99px;background:#fff;color:#4A5A40;border:1px solid #D8D3C8;}
.nut-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;}
.nut-item{background:#fff;border-radius:8px;padding:9px;text-align:center;border:1px solid #E2DDD4;}
.nut-val{font-size:14px;font-weight:500;color:#2C3A1E;}
.nut-lbl{font-size:10px;color:#7A8A70;margin-top:2px;}
.recipe-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:18px;margin-bottom:12px;}
.r-title{font-family:'DM Serif Display',serif;font-size:17px;color:#2C3A1E;margin-bottom:5px;}
.r-meta{display:flex;gap:10px;font-size:12px;color:#7A8A70;margin-bottom:12px;flex-wrap:wrap;}
.r-step{display:flex;gap:9px;padding:7px 0;border-top:1px solid #F0ECE4;font-size:13px;color:#4A5A40;line-height:1.6;align-items:flex-start;}
.r-step:first-child{border-top:none;}
.r-num{min-width:20px;height:20px;border-radius:50%;background:#4A7C3F;color:#fff;font-size:10px;font-weight:500;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}
.chart-box{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:20px;margin-bottom:22px;}
.upload-box{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:22px;margin-bottom:22px;}
.photo-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;overflow:hidden;margin-bottom:12px;}
.photo-img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;}
.photo-body{padding:12px 14px;}
.photo-user{font-size:13px;font-weight:500;color:#2C3A1E;margin-bottom:2px;}
.photo-recipe{font-size:12px;color:#4A7C3F;font-weight:500;margin-bottom:5px;}
.photo-note{font-size:12px;color:#5A6A50;line-height:1.6;}
.photo-time{font-size:11px;color:#9A9A90;margin-top:6px;}
.diary-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:16px;margin-bottom:10px;}
.divider{height:1px;background:#E2DDD4;margin:22px 0;}
.empty{text-align:center;padding:36px;background:#fff;border:1.5px dashed #D8D3C8;border-radius:14px;color:#7A8A70;font-size:13px;line-height:1.8;}
.stButton>button{background:#2C3A1E!important;color:#F0F7EB!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;padding:8px 16px!important;}
.stButton>button:hover{background:#4A7C3F!important;}
.stTextInput>div>div>input,.stTextArea textarea{border:1.5px solid #D8D3C8!important;border-radius:8px!important;background:#fff!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;color:#2C3A1E!important;}
.stTextInput>div>div>input:focus,.stTextArea textarea:focus{border-color:#4A7C3F!important;box-shadow:0 0 0 3px rgba(74,124,63,.12)!important;}
.stTextInput label,.stTextArea label,.stSelectbox label,.stFileUploader label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stFileUploader>div{border:1.5px dashed #C5DDB8!important;border-radius:8px!important;background:#F0F7EB!important;}
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;color:#5A6A50!important;padding:8px 16px!important;border-radius:8px!important;}
.stTabs [aria-selected="true"]{background:#EEF5E9!important;color:#2C3A1E!important;}
</style>
"""
def run_app():
    st.set_page_config(page_title="Nourish", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(CSS, unsafe_allow_html=True)

    # ── Session state ──
    defaults = {
        "lang":"en","detail_id":None,"search_results":[],
        "search_done":False,"active_goal":None,"recipe_search":"",
        "diary_entries":load_json(DIARY_FILE,[]),
        "community_posts":load_json(POSTS_FILE,[]),
        "custom_ingredients":load_json(INGREDIENTS_FILE,[]),
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    ALL_INGREDIENTS = INGREDIENTS + st.session_state.custom_ingredients

    # ── Nav + Language ──
    nc1, nc2 = st.columns([8,2])
    with nc1:
        tagline = APP_TAGLINE_KO if st.session_state.lang=="ko" else APP_TAGLINE_EN
        st.markdown(f'<div class="nav"><div class="nav-logo"><span class="nav-dot"></span>Nourish</div><div class="nav-tag">{tagline}</div></div>', unsafe_allow_html=True)
    with nc2:
        lang_choice = st.radio("lang", ["EN","한국어"], horizontal=True,
            index=0 if st.session_state.lang=="en" else 1, label_visibility="collapsed")
        if (lang_choice=="EN") != (st.session_state.lang=="en"):
            st.session_state.lang = "en" if lang_choice=="EN" else "ko"
            st.rerun()

    total_recipes = sum(len(i["recipes"]) for i in ALL_INGREDIENTS)
    total_ingr = len(ALL_INGREDIENTS)
    total_posts = len(st.session_state.community_posts)

    # ── Tabs ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([t("tab1"),t("tab2"),t("tab3"),t("tab4"),t("tab5")])

    # ════════════════════════════════════════════
    # TAB 1 — HOME
    # ════════════════════════════════════════════
    with tab1:
        if st.session_state.lang=="ko":
            hero_title = "자연이 주는 최고의<br>영양소를 탐험하세요"
            hero_sub = "신선한 식재료부터 맛있는 레시피까지 — 건강한 식탁의 모든 것"
        else:
            hero_title = "Discover the best<br>nutrition from nature"
            hero_sub = "From fresh ingredients to delicious recipes — everything for a healthier table"

        st.markdown(f"""
        <div class="hero-wrap">
            <img class="hero-img" src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1400&q=80"/>
            <div class="hero-text">
                <p class="hero-eye">🌿 NOURISH · WHOLESOME · HONEST</p>
                <h1 class="hero-title">{hero_title}</h1>
                <p class="hero-sub">{hero_sub}</p>
                <div style="margin-top:18px;">
                    <span class="stat-pill"><span class="stat-num">{total_ingr}</span>&nbsp;{t('home_stats_ingr')}</span>
                    <span class="stat-pill"><span class="stat-num">{total_recipes}</span>&nbsp;{t('home_stats_recipe')}</span>
                    <span class="stat-pill"><span class="stat-num">{total_posts}</span>&nbsp;{t('home_stats_users')}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Radar / Bar Chart ──
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown(f'<p class="sec-title">{t("goal_chart_title")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sec-sub">{t("goal_chart_sub")}</p>', unsafe_allow_html=True)
        health_goals = HEALTH_GOALS_KO if st.session_state.lang=="ko" else HEALTH_GOALS_EN
        goal_labels = list(health_goals.keys())
        gcols = st.columns(len(goal_labels))
        for i, goal in enumerate(goal_labels):
            with gcols[i]:
                if st.button(goal, key=f"hgoal_{i}", use_container_width=True):
                    st.session_state.active_goal = None if st.session_state.active_goal==goal else goal
                    st.rerun()

        COLORS = ["#4A7C3F","#E07B3F","#3F7CE0","#C03F7C","#7C3FC0","#3FC0B4","#C0A83F","#7C4A3F"]
        nutrient_dims = ["Protein","Fiber","Iron","Vit C","Omega-3","Antioxid.","Calcium"]
        ing_name_map = {i["id"]: (i.get("name_ko",i["name"]) if st.session_state.lang=="ko" else i["name"]) for i in ALL_INGREDIENTS}
        active = st.session_state.active_goal

        if active and active in health_goals:
            ing_ids = health_goals[active]
            fig = go.Figure()
            for idx, ing_id in enumerate(ing_ids):
                scores = NUTRIENT_SCORES.get(ing_id,[5]*7)
                color = COLORS[idx%len(COLORS)]
                r,g,b = int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
                fig.add_trace(go.Scatterpolar(
                    r=scores+[scores[0]], theta=nutrient_dims+[nutrient_dims[0]],
                    fill='toself', fillcolor=f"rgba({r},{g},{b},0.13)",
                    line=dict(color=color,width=2), name=ing_name_map.get(ing_id,ing_id),
                    hovertemplate=f"<b>{ing_name_map.get(ing_id,ing_id)}</b><br>%{{theta}}: %{{r}}/10<extra></extra>"))
            fig.update_layout(
                polar=dict(bgcolor="#F7F5F0",
                    radialaxis=dict(visible=True,range=[0,10],tickfont=dict(size=9),gridcolor="#E2DDD4"),
                    angularaxis=dict(tickfont=dict(size=11,color="#2C3A1E"),gridcolor="#E2DDD4")),
                paper_bgcolor="white",plot_bgcolor="white",
                font=dict(family="DM Sans, sans-serif",color="#2C3A1E"),
                legend=dict(orientation="h",yanchor="bottom",y=-0.3,xanchor="center",x=0.5,font=dict(size=11)),
                margin=dict(t=20,b=90,l=60,r=60),height=420)
        else:
            overall = {k:round(sum(v)/len(v),1) for k,v in NUTRIENT_SCORES.items()}
            sorted_items = sorted(overall.items(),key=lambda x:x[1],reverse=True)[:16]
            labels = [ing_name_map.get(k,k) for k,_ in sorted_items]
            values = [v for _,v in sorted_items]
            fig = go.Figure(go.Bar(x=values,y=labels,orientation='h',
                marker=dict(color=[COLORS[i%len(COLORS)] for i in range(len(labels))],line=dict(width=0)),
                hovertemplate="<b>%{y}</b><br>Score: %{x}/10<extra></extra>",
                text=[f"{v}" for v in values],textposition='outside',textfont=dict(size=10)))
            fig.update_layout(
                xaxis=dict(range=[0,11],tickfont=dict(size=10),gridcolor="#E2DDD4"),
                yaxis=dict(tickfont=dict(size=11,color="#2C3A1E"),autorange="reversed"),
                paper_bgcolor="white",plot_bgcolor="white",
                font=dict(family="DM Sans, sans-serif"),
                margin=dict(t=10,b=30,l=10,r=50),height=430)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<p style="font-size:11px;color:#9A9A90;text-align:center;margin-top:-4px;">Source: USDA FoodData Central · Scores 0–10 based on nutrient density per 100g</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Add Ingredient ──
        st.markdown(f'<p class="sec-title">✨ {t("ai_add_title")}</p>', unsafe_allow_html=True)
        aic1, aic2 = st.columns([4,1])
        with aic1:
            ai_name = st.text_input("ai_name", placeholder="e.g. spirulina / 스피루리나", label_visibility="collapsed", key="ai_ingr_input")
        with aic2:
            if st.button(t("ai_add_btn"), use_container_width=True, key="ai_add_go"):
                if ai_name.strip():
                    with st.spinner("🤖 Generating..." if st.session_state.lang=="en" else "🤖 AI가 생성 중..."):
                        new_ing = ai_add_ingredient(ai_name.strip())
                    if new_ing:
                        st.session_state.custom_ingredients.append(new_ing)
                        save_json(INGREDIENTS_FILE, st.session_state.custom_ingredients)
                        st.success(f"✅ Added: {new_ing.get('name_ko',new_ing['name']) if st.session_state.lang=='ko' else new_ing['name']}")
                        st.rerun()
                    else:
                        st.error("Failed. Try again." if st.session_state.lang=="en" else "생성 실패. 다시 시도해주세요.")

    # ════════════════════════════════════════════
    # TAB 2 — INGREDIENTS
    # ════════════════════════════════════════════
    with tab2:
        st.markdown(f'<p class="sec-title">{t("all_ingr")}</p>', unsafe_allow_html=True)
        si1, si2 = st.columns([5,1])
        with si1:
            search_ingr = st.text_input("ingr_s", placeholder=t("search_placeholder"), label_visibility="collapsed", key="ingr_search_box")
        with si2:
            ingr_search_btn = st.button(t("search_btn"), use_container_width=True, key="ingr_search_btn")

        if ingr_search_btn:
            st.session_state.search_results = do_search_ingr(search_ingr, ALL_INGREDIENTS)
            st.session_state.search_done = True
            st.session_state.detail_id = None

        if st.session_state.search_done:
            results = st.session_state.search_results
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            if not results:
                st.warning(f"{t('no_result')} '{search_ingr}'")
            else:
                st.markdown(f'<p class="sec-sub">🔍 {len(results)} result(s)</p>', unsafe_allow_html=True)
                for ing in results:
                    lang = st.session_state.lang
                    name_d = ing.get("name_ko",ing["name"]) if lang=="ko" else ing["name"]
                    short_d = ing.get("short_ko",ing["short"]) if lang=="ko" else ing["short"]
                    badge_d = ing.get("badge_ko",ing["badge"]) if lang=="ko" else ing["badge"]
                    cat_d = ing.get("category_ko",ing["category"]) if lang=="ko" else ing["category"]
                    rc1, rc2 = st.columns([7,1])
                    with rc1:
                        st.markdown(f"""<div class="search-card">
                            <span class="search-icon">{ing['icon']}</span>
                            <div class="search-info">
                                <div class="search-name">{name_d}</div>
                                <div class="search-short">{short_d}</div>
                                <div class="search-badges"><span class="s-badge">{badge_d}</span><span class="s-badge">{cat_d}</span></div>
                            </div></div>""", unsafe_allow_html=True)
                    with rc2:
                        btn_label = "정보" if lang=="ko" else "Info"
                        if st.button(btn_label, key=f"si_{ing['id']}", use_container_width=True):
                            st.session_state.detail_id = None if st.session_state.detail_id==ing["id"] else ing["id"]
                            st.rerun()
                    if st.session_state.detail_id == ing["id"]:
                        render_ing_detail(ing)
                        ing_name_d = ing.get("name_ko",ing["name"]) if st.session_state.lang=="ko" else ing["name"]
                        st.markdown(f'<p style="font-size:13px;font-weight:500;color:#2C3A1E;margin:10px 0 8px;">📋 {t("recipes_for")} {ing_name_d}</p>', unsafe_allow_html=True)
                        for rec in ing["recipes"]:
                            render_recipe_card(ing, rec)
            cc = st.columns([5,1])[1]
            with cc:
                if st.button(t("close_search"), use_container_width=True, key="close_ingr_search"):
                    st.session_state.search_done=False; st.session_state.search_results=[]; st.session_state.detail_id=None; st.rerun()
        else:
            # Featured cards
            st.markdown(f'<p class="sec-sub">{t("featured_sub")}</p>', unsafe_allow_html=True)
            feat_ings = [i for i in ALL_INGREDIENTS if i["id"] in FEATURED]
            cols4 = st.columns(4)
            for idx, ing in enumerate(feat_ings):
                lang = st.session_state.lang
                name_d = ing.get("name_ko",ing["name"]) if lang=="ko" else ing["name"]
                short_d = ing.get("short_ko",ing["short"]) if lang=="ko" else ing["short"]
                badge_d = ing.get("badge_ko",ing["badge"]) if lang=="ko" else ing["badge"]
                with cols4[idx%4]:
                    st.markdown(f"""<div class="ingr-card">
                        <div class="i-icon">{ing['icon']}</div>
                        <div class="i-name">{name_d}</div>
                        <div class="i-short">{short_d}</div>
                        <span class="i-badge">{badge_d}</span></div>""", unsafe_allow_html=True)
                    if st.button(name_d, key=f"feat_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id==ing["id"] else ing["id"]
                        st.rerun()

            if st.session_state.detail_id:
                d = next((i for i in feat_ings if i["id"]==st.session_state.detail_id), None)
                if d:
                    render_ing_detail(d)
                    dname = d.get("name_ko",d["name"]) if st.session_state.lang=="ko" else d["name"]
                    st.markdown(f'<p style="font-size:13px;font-weight:500;color:#2C3A1E;margin:10px 0 8px;">📋 {t("recipes_for")} {dname}</p>', unsafe_allow_html=True)
                    for rec in d["recipes"]:
                        render_recipe_card(d, rec)
                    if st.columns([5,1])[1].button(t("close_search"), use_container_width=True, key="close_feat"):
                        st.session_state.detail_id=None; st.rerun()

            # All non-featured ingredients
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            non_feat = [i for i in ALL_INGREDIENTS if i["id"] not in FEATURED]
            nf_cols = st.columns(4)
            for idx, ing in enumerate(non_feat):
                lang = st.session_state.lang
                name_d = ing.get("name_ko",ing["name"]) if lang=="ko" else ing["name"]
                badge_d = ing.get("badge_ko",ing["badge"]) if lang=="ko" else ing["badge"]
                with nf_cols[idx%4]:
                    st.markdown(f"""<div class="ingr-card">
                        <div class="i-icon">{ing['icon']}</div>
                        <div class="i-name">{name_d}</div>
                        <span class="i-badge">{badge_d}</span></div>""", unsafe_allow_html=True)
                    if st.button(name_d, key=f"nf_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id==ing["id"] else ing["id"]
                        st.rerun()
            # Show detail for non-featured
            if st.session_state.detail_id:
                d2 = next((i for i in non_feat if i["id"]==st.session_state.detail_id), None)
                if d2:
                    render_ing_detail(d2)
                    dname2 = d2.get("name_ko",d2["name"]) if st.session_state.lang=="ko" else d2["name"]
                    st.markdown(f'<p style="font-size:13px;font-weight:500;color:#2C3A1E;margin:10px 0 8px;">📋 {t("recipes_for")} {dname2}</p>', unsafe_allow_html=True)
                    for rec in d2["recipes"]:
                        render_recipe_card(d2, rec)
                    if st.columns([5,1])[1].button(t("close_search"), use_container_width=True, key="close_nf"):
                        st.session_state.detail_id=None; st.rerun()

    # ════════════════════════════════════════════
    # TAB 3 — RECIPES
    # ════════════════════════════════════════════
    with tab3:
        st.markdown(f'<p class="sec-title">{t("recipe_title")}</p>', unsafe_allow_html=True)
        rs1, rs2 = st.columns([5,1])
        with rs1:
            recipe_q = st.text_input("rq", placeholder=t("recipe_search_ph"), label_visibility="collapsed", key="recipe_search_input")
        with rs2:
            if st.button(t("search_btn"), key="r_search_btn", use_container_width=True):
                st.session_state.recipe_search = recipe_q.strip()

        if st.session_state.recipe_search:
            r_results = do_search_recipe(st.session_state.recipe_search, ALL_INGREDIENTS)
            st.markdown(f'<p class="sec-sub">🔍 {len(r_results)} recipe(s)</p>', unsafe_allow_html=True)
            if not r_results:
                st.warning(f"No recipes found for '{st.session_state.recipe_search}'")
            for ing, rec in r_results:
                render_recipe_card(ing, rec)
            if st.columns([5,1])[1].button(t("close_search"), key="close_rsearch"):
                st.session_state.recipe_search=""; st.rerun()
        else:
            all_labels = []
            for ing in ALL_INGREDIENTS:
                for rec in ing["recipes"]:
                    lang = st.session_state.lang
                    label = f"{ing['icon']} {rec.get('title_ko',rec['title']) if lang=='ko' else rec['title']} ({ing.get('name_ko',ing['name']) if lang=='ko' else ing['name']})"
                    all_labels.append((label, ing, rec))
            all_labels_sorted = sorted(all_labels, key=lambda x: x[0])
            sel = st.selectbox(t("select_recipe"),
                options=[t("select_recipe")]+[l for l,_,_ in all_labels_sorted],
                label_visibility="collapsed")
            if sel != t("select_recipe"):
                for label, ing, rec in all_labels_sorted:
                    if label == sel:
                        render_recipe_card(ing, rec)
                        break
            else:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown(f'<p class="sec-sub">{"Showing first 12 recipes — use search or dropdown for more" if st.session_state.lang=="en" else "처음 12개 레시피 — 검색이나 드롭다운으로 더 보기"}</p>', unsafe_allow_html=True)
                rcols = st.columns(2)
                count = 0
                for ing in ALL_INGREDIENTS:
                    for rec in ing["recipes"]:
                        if count >= 12: break
                        with rcols[count%2]:
                            render_recipe_card(ing, rec)
                        count += 1
                    if count >= 12: break

    # ════════════════════════════════════════════
    # TAB 4 — FOOD SHARE
    # ════════════════════════════════════════════
    with tab4:
        st.markdown(f'<p class="sec-title">{t("share_title")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sec-sub">{t("share_sub")}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="upload-box"><div style="font-family:DM Serif Display,serif;font-size:18px;color:#2C3A1E;margin-bottom:4px;">{t("upload_title")}</div><div style="font-size:12px;color:#7A8A70;margin-bottom:16px;">{t("upload_sub")}</div>', unsafe_allow_html=True)
        uf1, uf2 = st.columns(2)
        with uf1:
            nickname = st.text_input(t("nickname"), placeholder="HealthyChef 👩‍🍳", key="share_nick")
        with uf2:
            recipe_name_share = st.text_input(t("recipe_name"), placeholder="Quinoa Bowl", key="share_rname", value=st.session_state.get("pending_recipe",""))
        note_share = st.text_area(t("note"), placeholder="😋", height=80, key="share_note_ta")
        photo_file = st.file_uploader("📸", type=["jpg","jpeg","png"], key="share_photo", label_visibility="collapsed")
        if st.button(t("share_btn"), use_container_width=True, key="share_submit"):
            if not nickname: st.warning(t("share_warn_nick"))
            elif not recipe_name_share: st.warning(t("share_warn_recipe"))
            elif not photo_file: st.warning(t("share_warn_photo"))
            else:
                img_b64 = base64.b64encode(photo_file.read()).decode()
                ext = photo_file.name.split(".")[-1].lower()
                mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
                new_post = {"nickname":nickname,"recipe":recipe_name_share,"note":note_share,
                            "img_b64":img_b64,"mime":mime,"time":datetime.now().strftime("%Y.%m.%d %H:%M"),"likes":0}
                st.session_state.community_posts.insert(0, new_post)
                save_json(POSTS_FILE, st.session_state.community_posts)
                st.session_state["pending_recipe"]=""
                st.success(f"🎉 {t('share_success')}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if not st.session_state.community_posts:
            st.markdown('<div class="empty">🍽<br><br>' + ("Be the first to share!" if st.session_state.lang=="en" else "첫 번째 요리 사진을 올려보세요!") + '</div>', unsafe_allow_html=True)
        else:
            pcols = st.columns(3)
            for idx, post in enumerate(st.session_state.community_posts):
                with pcols[idx%3]:
                    st.markdown(f"""<div class="photo-card">
                        <img class="photo-img" src="data:{post['mime']};base64,{post['img_b64']}" alt="{post['recipe']}"/>
                        <div class="photo-body">
                            <div class="photo-user">👤 {post['nickname']}</div>
                            <div class="photo-recipe">🌿 {post['recipe']}</div>
                            <div class="photo-note">{post.get('note','')}</div>
                            <div class="photo-time">{post['time']}</div>
                        </div></div>""", unsafe_allow_html=True)
                    bc1,bc2,bc3 = st.columns(3)
                    with bc1:
                        if st.button(f"❤️ {post['likes']}", key=f"like4_{idx}", use_container_width=True):
                            st.session_state.community_posts[idx]["likes"]+=1
                            save_json(POSTS_FILE, st.session_state.community_posts); st.rerun()
                    with bc2:
                        if st.button(t("copy_link"), key=f"copy4_{idx}", use_container_width=True):
                            share_text = f"🌿 {post['recipe']} #Nourish #HealthyEating"
                            st.toast(f"✅ {share_text}")
                    with bc3:
                        if st.button("🗑️", key=f"del4_{idx}", use_container_width=True):
                            st.session_state.community_posts.pop(idx)
                            save_json(POSTS_FILE, st.session_state.community_posts); st.rerun()
                    if st.button(t("insta_share"), key=f"insta4_{idx}", use_container_width=True):
                        st.info(f"📋 Copy for Instagram:\n\n🌿 **{post['recipe']}** — made with love!\n#Nourish #HealthyEating #HomeCooking #FoodPhotography")

    # ════════════════════════════════════════════
    # TAB 5 — MY DIARY
    # ════════════════════════════════════════════
    with tab5:
        st.markdown(f'<p class="sec-title">{t("diary_title")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sec-sub">{t("diary_sub")}</p>', unsafe_allow_html=True)

        with st.expander("➕ " + ("New Entry" if st.session_state.lang=="en" else "새 일기 작성"), expanded=True):
            dc1, dc2 = st.columns(2)
            with dc1:
                d_date = st.date_input(t("diary_date"), key="d_date")
                d_meal = st.text_input(t("diary_meal"), placeholder="e.g. Quinoa Bowl / 퀴노아 볼", key="d_meal")
            with dc2:
                d_mood = st.select_slider(t("diary_mood"), options=["😖","😕","😐","😊","😋"], value="😊", key="d_mood")
                d_photo = st.file_uploader("📸 " + ("Photo (optional)" if st.session_state.lang=="en" else "사진 (선택)"), type=["jpg","jpeg","png"], key="d_photo")
            d_note = st.text_area(t("diary_note"), height=90, key="d_note",
                placeholder="How did it go?" if st.session_state.lang=="en" else "오늘의 요리 이야기를 적어보세요...")

            col_save, col_ai = st.columns(2)
            with col_save:
                if st.button(t("diary_submit"), use_container_width=True, key="diary_save"):
                    if d_meal.strip():
                        entry = {"date":str(d_date),"meal":d_meal,"note":d_note,"mood":d_mood}
                        if d_photo:
                            entry["img_b64"] = base64.b64encode(d_photo.read()).decode()
                            entry["mime"] = "image/jpeg" if d_photo.name.lower().endswith(("jpg","jpeg")) else "image/png"
                        st.session_state.diary_entries.insert(0, entry)
                        save_json(DIARY_FILE, st.session_state.diary_entries)
                        st.success("✅ Saved!" if st.session_state.lang=="en" else "✅ 저장됐어요!")
                        st.rerun()
                    else:
                        st.warning("Enter a meal name." if st.session_state.lang=="en" else "요리 이름을 입력해주세요.")
            with col_ai:
                if st.button(t("health_score_btn"), use_container_width=True, key="diary_ai"):
                    if d_meal.strip():
                        with st.spinner("🤖 Analysing..." if st.session_state.lang=="en" else "🤖 분석 중..."):
                            photo_b64 = None
                            if d_photo:
                                d_photo.seek(0)
                                photo_b64 = base64.b64encode(d_photo.read()).decode()
                            result = ai_health_score(d_meal, d_note, photo_b64)
                        if result:
                            score = result.get("score",0)
                            grade = result.get("grade","?")
                            fb = result.get("feedback_ko","") if st.session_state.lang=="ko" else result.get("feedback_en","")
                            sug = result.get("suggestions_ko","") if st.session_state.lang=="ko" else result.get("suggestions_en","")
                            color = "#4A7C3F" if score>=75 else "#E07B3F" if score>=50 else "#C03F3F"
                            st.markdown(f"""
                            <div style="text-align:center;padding:20px;background:#F0F7EB;border-radius:14px;border:1.5px solid #C5DDB8;">
                                <div style="width:72px;height:72px;border-radius:50%;background:{color};display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#fff;margin:0 auto 8px;font-family:'DM Serif Display',serif;">{grade}</div>
                                <p style="font-size:26px;font-weight:700;color:{color};margin:0;">{score}<span style="font-size:13px;color:#7A8A70;">/100</span></p>
                                <p style="font-size:13px;color:#4A5A40;margin:8px 0 4px;">{fb}</p>
                                <p style="font-size:12px;color:#7A8A70;">💡 {sug}</p>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.error("AI analysis failed." if st.session_state.lang=="en" else "AI 분석에 실패했어요.")
                    else:
                        st.warning("Enter a meal name first." if st.session_state.lang=="en" else "요리 이름을 먼저 입력해주세요.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if not st.session_state.diary_entries:
            st.markdown('<div class="empty">📔<br><br>' + ("No diary entries yet!" if st.session_state.lang=="en" else "아직 일기가 없어요. 첫 번째 이야기를 써보세요!") + '</div>', unsafe_allow_html=True)
        else:
            for i, entry in enumerate(st.session_state.diary_entries):
                ec1, ec2 = st.columns([1,7])
                with ec1:
                    st.markdown(f'<div style="font-size:34px;text-align:center;padding-top:8px;">{entry.get("mood","😊")}</div>', unsafe_allow_html=True)
                with ec2:
                    st.markdown(f"""<div class="diary-card">
                        <div style="font-size:12px;color:#7A8A70;margin-bottom:3px;">{entry['date']}</div>
                        <div style="font-size:15px;font-weight:500;color:#2C3A1E;margin-bottom:5px;">🌿 {entry['meal']}</div>
                        <div style="font-size:13px;color:#4A5A40;line-height:1.65;">{entry.get('note','')}</div>
                    </div>""", unsafe_allow_html=True)
                    if "img_b64" in entry:
                        st.image(f"data:{entry.get('mime','image/jpeg')};base64,{entry['img_b64']}", width=180)
                    if st.button("🗑️", key=f"del_diary_{i}"):
                        st.session_state.diary_entries.pop(i)
                        save_json(DIARY_FILE, st.session_state.diary_entries); st.rerun()

    lang = st.session_state.lang
    footer_tag = APP_TAGLINE_KO if lang=="ko" else APP_TAGLINE_EN
    st.markdown(f'<div style="margin-top:48px;padding:14px 0;border-top:1px solid #E2DDD4;text-align:center;font-size:11px;color:#7A8A70;">Nourish · {footer_tag} · SKKU Art Project</div>', unsafe_allow_html=True)

run_app()
