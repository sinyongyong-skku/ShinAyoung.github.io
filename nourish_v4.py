import streamlit as st
import json
from pathlib import Path

APP_NAME = "Nourish"

# ── Language ──────────────────────────────────────────────────────
T = {
    "en": {
        "tab1": "🌿 Home", "tab2": "🥦 Ingredients", "tab3": "🍳 Recipes",
        "hero_title": "Discover the best<br>nutrition from nature",
        "hero_sub": "Fresh ingredients · Honest recipes · Healthy living",
        "stats_ingr": "Ingredients", "stats_recipe": "Recipes",
        "featured_title": "Featured Ingredients",
        "featured_sub": "Click an ingredient to see recipes",
        "search_placeholder": "Search ingredients (EN / 한국어)...",
        "search_btn": "Search 🔍", "close_btn": "Close ✕",
        "no_result": "No results for",
        "key_benefits": "KEY BENEFITS", "nutrition": "NUTRITION (per 100g)",
        "recipes_for": "Recipes with",
        "recipe_title": "All Recipes",
        "recipe_search_ph": "Search recipe or ingredient...",
        "select_recipe": "— Select a recipe —",
        "difficulty": {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"},
        "lang_btn": "🇰🇷 한국어로 보기",
    },
    "ko": {
        "tab1": "🌿 홈", "tab2": "🥦 식재료", "tab3": "🍳 레시피",
        "hero_title": "자연이 주는 최고의<br>영양소를 탐험하세요",
        "hero_sub": "신선한 식재료 · 정직한 레시피 · 건강한 생활",
        "stats_ingr": "가지 식재료", "stats_recipe": "개 레시피",
        "featured_title": "대표 식재료",
        "featured_sub": "식재료를 클릭하면 레시피가 나와요",
        "search_placeholder": "식재료 검색 (한국어 / EN)...",
        "search_btn": "검색 🔍", "close_btn": "닫기 ✕",
        "no_result": "검색 결과 없음:",
        "key_benefits": "주요 효능", "nutrition": "영양 성분 (100g 기준)",
        "recipes_for": "관련 레시피",
        "recipe_title": "전체 레시피",
        "recipe_search_ph": "레시피 또는 식재료 검색...",
        "select_recipe": "— 레시피를 선택해주세요 —",
        "difficulty": {"Easy": "쉬움", "Medium": "보통", "Hard": "어려움"},
        "lang_btn": "🇺🇸 View in English",
    },
}

def t(key, sub=None):
    lang = st.session_state.get("lang", "ko")
    base = T[lang].get(key, T["en"].get(key, key))
    if sub and isinstance(base, dict):
        return base.get(sub, sub)
    return base

# ══════════════════════════════════════════════════════════════════
# INGREDIENT DATA
# ══════════════════════════════════════════════════════════════════
FEATURED = ["quinoa", "salmon", "tofu", "blueberry", "spinach", "kimchi"]

INGREDIENTS = [
    # ── 슈퍼푸드 ──────────────────────────────────────────────────
    {"id":"quinoa","icon":"🌾","name":"Quinoa","name_ko":"퀴노아",
     "short":"Complete protein super seed","short_ko":"완전단백질 슈퍼씨앗",
     "badge":"Gluten-Free","badge_ko":"글루텐프리","category":"Whole Grain","category_ko":"통곡물",
     "description":"Quinoa contains all 9 essential amino acids. Naturally gluten-free and packed with iron and magnesium.",
     "description_ko":"퀴노아는 9가지 필수아미노산을 모두 함유한 완전단백질 식품이에요. 글루텐이 없어 밀 알레르기가 있는 분들도 안심하고 먹을 수 있어요.",
     "effects":["Blood sugar control","Muscle recovery","Digestion","Satiety","Energy"],
     "effects_ko":["혈당 조절","근육 회복","소화 개선","포만감","에너지 공급"],
     "nutrition":{"Calories":"120kcal","Protein":"4.4g","Fiber":"2.8g","Carbs":"21.3g","Fat":"1.9g","Iron":"1.5mg"},
     "recipes":[
         {"title":"Quinoa Salad Bowl","title_ko":"퀴노아 샐러드 볼","time":"20 min","kcal":"310kcal","difficulty":"Easy",
          "steps":["Cook 1 cup quinoa in 2 cups water for 15 min","Dice cucumber, cherry tomatoes, red onion","Make dressing: lemon juice, olive oil, salt, pepper","Toss everything together and serve"],
          "steps_ko":["퀴노아 1컵을 물 2컵에 15분 끓인 뒤 식힌다","오이, 방울토마토, 적양파를 썬다","드레싱: 레몬즙, 올리브오일, 소금, 후추","모두 섞어 완성한다"]},
         {"title":"Quinoa Breakfast Bowl","title_ko":"퀴노아 아침 볼","time":"10 min","kcal":"270kcal","difficulty":"Easy",
          "steps":["Mix cooked quinoa 1:1 with Greek yogurt","Stir in honey and cinnamon","Top with blueberries and sliced almonds","Garnish with mint leaves"],
          "steps_ko":["익힌 퀴노아와 그릭요거트를 1:1로 섞는다","꿀과 시나몬을 넣어 섞는다","블루베리와 아몬드를 올린다","민트잎으로 마무리한다"]},
         {"title":"Quinoa Vegetable Soup","title_ko":"퀴노아 채소 수프","time":"30 min","kcal":"220kcal","difficulty":"Easy",
          "steps":["Sauté onion, carrot, celery in olive oil","Add 4 cups vegetable broth and quinoa","Simmer on low heat for 20 minutes","Season with salt, pepper, and fresh parsley"],
          "steps_ko":["양파, 당근, 셀러리를 올리브오일에 볶는다","채수 4컵과 퀴노아를 넣는다","약불에서 20분 끓인다","소금, 후추, 파슬리로 마무리한다"]},
     ]},
    {"id":"salmon","icon":"🐟","name":"Salmon","name_ko":"연어",
     "short":"High omega-3 fatty fish","short_ko":"오메가-3 고함량 생선",
     "badge":"20g Protein","badge_ko":"단백질 20g","category":"Seafood","category_ko":"해산물",
     "description":"One of the best omega-3 sources. Rich in EPA and DHA for brain, heart, and inflammation reduction.",
     "description_ko":"오메가-3 지방산의 가장 좋은 공급원 중 하나예요. EPA와 DHA가 풍부해 뇌 건강, 심혈관 건강, 염증 억제에 탁월해요.",
     "effects":["Brain health","Heart protection","Reduces inflammation","Immunity","Bone strength"],
     "effects_ko":["뇌 건강","심혈관 보호","염증 억제","면역력","뼈 강화"],
     "nutrition":{"Calories":"208kcal","Protein":"20.0g","Fiber":"0g","Carbs":"0g","Fat":"13.0g","Omega-3":"2.3g"},
     "recipes":[
         {"title":"Salmon Poke Bowl","title_ko":"연어 포케 볼","time":"15 min","kcal":"450kcal","difficulty":"Easy",
          "steps":["Place brown rice in bowl","Marinate salmon cubes in soy sauce, sesame oil, ginger for 5 min","Arrange edamame, cucumber, avocado alongside","Drizzle with sriracha mayo"],
          "steps_ko":["현미밥을 볼에 담는다","연어를 간장, 참기름, 생강즙에 5분 재운다","에다마메, 오이, 아보카도를 준비한다","스리라차 마요를 뿌린다"]},
         {"title":"Miso Glazed Salmon","title_ko":"미소 연어 구이","time":"20 min","kcal":"350kcal","difficulty":"Easy",
          "steps":["Mix miso paste, mirin, soy sauce, honey for glaze","Coat salmon fillets and marinate 15 min","Pan-fry or broil 4 min each side","Serve with steamed rice and sesame greens"],
          "steps_ko":["미소, 미린, 간장, 꿀로 글레이즈를 만든다","연어에 바르고 15분 재운다","팬에서 양면 4분씩 굽는다","따뜻한 밥과 함께 낸다"]},
         {"title":"Herb-Baked Salmon","title_ko":"허브 오븐 구이 연어","time":"22 min","kcal":"390kcal","difficulty":"Medium",
          "steps":["Coat salmon with olive oil, minced garlic, lemon juice, and fresh dill","Season with salt and pepper","Bake at 200°C for 12–14 minutes","Serve with roasted asparagus and lemon wedge"],
          "steps_ko":["연어에 올리브오일, 마늘, 레몬즙, 딜을 바른다","소금과 후추로 간한다","200도에서 12~14분 굽는다","아스파라거스와 레몬을 곁들여 낸다"]},
     ]},
    {"id":"tofu","icon":"🫘","name":"Tofu","name_ko":"두부",
     "short":"Plant-based complete protein","short_ko":"식물성 완전단백질",
     "badge":"Low Calorie","badge_ko":"저칼로리","category":"Plant Protein","category_ko":"식물성단백질",
     "description":"Low calorie yet rich in protein and calcium. Perfect for weight management and bone health.",
     "description_ko":"칼로리가 낮으면서도 단백질이 풍부해 다이어트식으로 완벽하고 칼슘도 높아 뼈 건강에도 좋아요.",
     "effects":["Weight management","Bone strength","Muscle maintenance","Lower cholesterol","Hormone balance"],
     "effects_ko":["다이어트","뼈 강화","근육 유지","콜레스테롤 감소","호르몬 균형"],
     "nutrition":{"Calories":"76kcal","Protein":"8.0g","Fiber":"0.3g","Carbs":"1.9g","Fat":"4.8g","Calcium":"350mg"},
     "recipes":[
         {"title":"Sundubu Jjigae (Soft Tofu Stew)","title_ko":"순두부찌개","time":"20 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Make anchovy-kelp broth and bring to boil","Dissolve 2 tbsp gochugaru paste in broth","Add zucchini, mushrooms, and soft tofu gently","Crack an egg in, add scallions and serve boiling hot"],
          "steps_ko":["멸치·다시마 육수를 낸다","고춧가루 2큰술을 풀고 애호박, 버섯을 넣는다","순두부를 뜯어 넣고 5분 끓인다","달걀을 넣고 청양고추, 파를 올려 완성한다"]},
         {"title":"Tofu Steak","title_ko":"두부 스테이크","time":"15 min","kcal":"220kcal","difficulty":"Easy",
          "steps":["Slice firm tofu 2cm thick, pat completely dry","Make glaze: soy sauce, honey, garlic, sesame oil","Pan-fry both sides 3–4 min until deep golden","Pour glaze over, cook 1 min, garnish with sesame and scallions"],
          "steps_ko":["두부를 2cm로 썰어 물기를 완전히 제거한다","소스: 간장, 꿀, 마늘, 참기름","팬에 양면 3~4분씩 노릇하게 굽는다","소스를 붓고 1분 조리고 깨, 파를 얹는다"]},
         {"title":"Mapo Tofu","title_ko":"마파두부","time":"20 min","kcal":"280kcal","difficulty":"Medium",
          "steps":["Stir-fry ground pork until cooked","Add doubanjiang paste, minced garlic and ginger","Add tofu cubes, broth, and soy sauce; simmer 5 min","Thicken with cornstarch slurry, finish with scallions and Sichuan pepper"],
          "steps_ko":["돼지고기 다짐육을 볶는다","두반장, 마늘, 생강을 넣는다","두부, 육수, 간장을 넣고 5분 끓인다","전분물로 걸쭉하게 만들고 파, 산초로 마무리한다"]},
     ]},
    {"id":"blueberry","icon":"🫐","name":"Blueberry","name_ko":"블루베리",
     "short":"Antioxidant superfood","short_ko":"항산화 슈퍼푸드",
     "badge":"Vitamin C","badge_ko":"비타민C","category":"Berries","category_ko":"베리류",
     "description":"Packed with anthocyanin antioxidants for brain health and anti-aging. Among the highest antioxidant foods known.",
     "description_ko":"안토시아닌이라는 강력한 항산화 색소로 가득 차 있어요. 뇌 건강과 기억력 개선에 효과적이고 활성산소를 제거해 노화를 늦춰줘요.",
     "effects":["Antioxidant","Brain health","Anti-aging","Blood sugar control","Eye protection"],
     "effects_ko":["항산화","뇌 건강","노화 방지","혈당 조절","시력 보호"],
     "nutrition":{"Calories":"57kcal","Protein":"0.7g","Fiber":"2.4g","Carbs":"14.5g","Fat":"0.3g","Vitamin C":"9.7mg"},
     "recipes":[
         {"title":"Blueberry Smoothie Bowl","title_ko":"블루베리 스무디 볼","time":"8 min","kcal":"260kcal","difficulty":"Easy",
          "steps":["Blend frozen blueberries and banana until thick","Add a spoonful of Greek yogurt and blend briefly","Pour into bowl, top with granola and chia seeds","Drizzle honey and add fresh blueberries"],
          "steps_ko":["냉동 블루베리와 바나나를 걸쭉하게 블렌딩한다","그릭요거트를 넣고 짧게 섞는다","그래놀라와 치아씨드를 올린다","꿀을 드리즐하고 생블루베리를 올린다"]},
         {"title":"Blueberry Chia Jam","title_ko":"블루베리 치아씨드 잼","time":"15 min","kcal":"40kcal","difficulty":"Easy",
          "steps":["Combine blueberries, honey, lemon juice in saucepan","Bring to boil then simmer stirring for 10 min","Remove from heat, stir in 2 tbsp chia seeds","Cool and store in glass jar in fridge up to 2 weeks"],
          "steps_ko":["블루베리, 꿀, 레몬즙을 냄비에서 끓인다","10분 저으며 졸인다","불을 끄고 치아씨드 2큰술을 넣는다","식혀서 유리병에 냉장 보관한다"]},
         {"title":"Blueberry Banana Pancakes","title_ko":"블루베리 바나나 팬케이크","time":"20 min","kcal":"310kcal","difficulty":"Easy",
          "steps":["Mash banana, mix with 2 eggs and 1/2 cup oat flour","Fold in blueberries gently","Cook tablespoon-sized portions over low heat, flip when bubbles form","Serve with maple syrup and extra blueberries"],
          "steps_ko":["바나나를 으깨고 달걀 2개, 귀리가루 1/2컵을 섞는다","블루베리를 반죽에 살살 넣는다","약불에서 양면을 굽는다","메이플시럽과 블루베리를 올린다"]},
     ]},
    {"id":"spinach","icon":"🥬","name":"Spinach","name_ko":"시금치",
     "short":"Iron and folate powerhouse","short_ko":"철분·엽산의 녹색 보고",
     "badge":"Low Calorie","badge_ko":"저칼로리","category":"Vegetables","category_ko":"채소",
     "description":"Rich in iron, folate, vitamins K and A. Lutein protects eye health. Only 23 kcal per 100g.",
     "description_ko":"철분, 엽산, 비타민 K, A가 풍부하고 칼로리는 매우 낮아요. 루테인이 눈 건강을 지켜주고 마그네슘이 수면에 도움을 줘요.",
     "effects":["Anaemia prevention","Eye health","Bone strength","Digestion","Skin care"],
     "effects_ko":["빈혈 예방","눈 건강","뼈 강화","소화 개선","피부 미용"],
     "nutrition":{"Calories":"23kcal","Protein":"2.9g","Fiber":"2.2g","Carbs":"3.6g","Fat":"0.4g","Iron":"2.7mg"},
     "recipes":[
         {"title":"Spinach Doenjang Soup","title_ko":"시금치 된장국","time":"15 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Make anchovy broth and bring to boil","Dissolve 2 tbsp doenjang (Korean miso) in broth","Add tofu cubes and washed spinach","Simmer 3 min, add scallions and serve hot"],
          "steps_ko":["멸치 육수를 낸다","된장 2큰술을 풀어준다","두부와 씻은 시금치를 넣는다","3분 끓이고 파를 올려 완성한다"]},
         {"title":"Spinach Pesto Pasta","title_ko":"시금치 페스토 파스타","time":"20 min","kcal":"380kcal","difficulty":"Medium",
          "steps":["Blend spinach, almonds, garlic, olive oil, parmesan into pesto","Cook pasta in well-salted water until al dente","Reserve 1/2 cup pasta water, drain pasta","Toss pasta with pesto, loosen with pasta water as needed"],
          "steps_ko":["시금치, 아몬드, 마늘, 올리브오일, 파마산으로 페스토를 만든다","파스타를 소금물에 삶는다","파스타와 페스토를 팬에서 섞는다","방울토마토와 파마산을 올린다"]},
         {"title":"Spinach Egg Stir-Fry","title_ko":"시금치 달걀 볶음","time":"10 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Wash spinach thoroughly and shake dry","Sauté minced garlic in sesame oil until fragrant","Add spinach and stir-fry over high heat 2 min","Push to side, scramble 2 eggs, combine and season"],
          "steps_ko":["시금치를 씻어 물기를 제거한다","팬에 참기름을 두르고 마늘을 볶는다","시금치를 강불에서 2분 볶는다","달걀을 넣어 반숙으로 익히고 간한다"]},
     ]},
    {"id":"kimchi","icon":"🥬","name":"Kimchi","name_ko":"김치",
     "short":"Korea's probiotic superfood","short_ko":"한국의 유산균 발효식품",
     "badge":"Probiotics","badge_ko":"프로바이오틱스","category":"Fermented","category_ko":"발효식품",
     "description":"UNESCO Intangible Cultural Heritage. Billions of beneficial bacteria for gut health, plus vitamins C and K.",
     "description_ko":"유네스코 무형문화유산. 젖산균이 풍부해 장 건강에 탁월하고 비타민 C, K도 풍부해요.",
     "effects":["Gut health","Immunity boost","Antioxidant","Digestion","Weight management"],
     "effects_ko":["장 건강","면역 강화","항산화","소화 촉진","체중 관리"],
     "nutrition":{"Calories":"15kcal","Protein":"1.1g","Fiber":"1.6g","Carbs":"2.4g","Fat":"0.5g","Probiotics":"Billions CFU"},
     "recipes":[
         {"title":"Kimchi Fried Rice","title_ko":"김치 볶음밥","time":"15 min","kcal":"380kcal","difficulty":"Easy",
          "steps":["Stir-fry well-fermented kimchi in sesame oil until slightly caramelised","Add cold cooked rice, pressing and breaking clumps","Stir-fry over high heat until rice is slightly crispy","Top with a fried egg and sprinkle seaweed flakes and sesame"],
          "steps_ko":["잘 익은 김치를 참기름에 볶는다","찬밥을 넣고 강불에서 볶는다","달걀 프라이를 올린다","김가루와 참깨를 뿌려 완성한다"]},
         {"title":"Kimchi Jjigae","title_ko":"김치찌개","time":"25 min","kcal":"210kcal","difficulty":"Easy",
          "steps":["Stir-fry pork belly pieces until slightly browned","Add aged kimchi and stir-fry together 2 min","Add water, gochugaru, soy sauce and bring to boil","Add tofu, simmer 15 min, finish with scallions"],
          "steps_ko":["돼지고기를 볶다가 김치를 넣는다","물, 고춧가루, 간장을 넣고 끓인다","두부를 넣고 15분 끓인다","파를 올려 완성한다"]},
         {"title":"Kimchi Pancakes","title_ko":"김치전","time":"15 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Finely chop kimchi and squeeze out excess liquid","Mix with flour, water, egg, and a pinch of sugar into thick batter","Heat oil in pan over medium-high, pour batter to form pancakes","Fry until golden and crispy on both sides, serve with dipping sauce"],
          "steps_ko":["김치를 잘게 썰어 물기를 꼭 짠다","밀가루, 물, 달걀로 반죽을 만든다","팬에 기름을 두르고 중강불에서 굽는다","양면을 노릇하게 부쳐 초간장과 함께 낸다"]},
     ]},

    # ── 한국 식재료 ────────────────────────────────────────────────
    {"id":"sweet_potato","icon":"🍠","name":"Sweet Potato","name_ko":"고구마",
     "short":"Beta-carotene energy root","short_ko":"베타카로틴·에너지 뿌리채소",
     "badge":"Vitamin A","badge_ko":"비타민A","category":"Root Vegetable","category_ko":"구황작물",
     "description":"Rich in beta-carotene, dietary fibre, and vitamin C. Lower glycaemic index than white potato, making it a healthier carb choice.",
     "description_ko":"베타카로틴, 식이섬유, 비타민 C가 풍부해요. 흰 감자보다 혈당 지수가 낮아 더 건강한 탄수화물 공급원이에요.",
     "effects":["Immunity boost","Eye protection","Gut health","Blood pressure control","Energy supply"],
     "effects_ko":["면역 강화","시력 보호","장 건강","혈압 조절","에너지 공급"],
     "nutrition":{"Calories":"86kcal","Protein":"1.6g","Fiber":"3.0g","Carbs":"20.1g","Fat":"0.1g","Vitamin A":"961μg"},
     "recipes":[
         {"title":"Baked Sweet Potato","title_ko":"군고구마","time":"40 min","kcal":"130kcal","difficulty":"Easy",
          "steps":["Wash sweet potatoes thoroughly","Wrap in aluminium foil","Bake at 200°C for 35–40 minutes until fork-tender","Slice open and serve with butter or as-is"],
          "steps_ko":["고구마를 깨끗이 씻는다","호일로 감싼다","200도에서 35~40분 굽는다","칼집을 넣고 버터를 곁들여 낸다"]},
         {"title":"Sweet Potato Latte","title_ko":"고구마 라떼","time":"10 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Steam or boil sweet potato until soft, then mash","Stir mashed sweet potato into warm milk (ratio 1:3)","Add honey and cinnamon to taste","Blend with hand blender for smooth texture"],
          "steps_ko":["고구마를 쪄서 으깬다","따뜻한 우유에 으깬 고구마를 넣는다","꿀과 시나몬을 넣는다","핸드블렌더로 갈아 완성한다"]},
         {"title":"Sweet Potato & Black Bean Bowl","title_ko":"고구마 블랙빈 볼","time":"30 min","kcal":"370kcal","difficulty":"Easy",
          "steps":["Cube sweet potato, toss with cumin and smoked paprika, roast 200°C 25 min","Warm black beans with garlic and lime juice","Serve over brown rice","Top with avocado, pickled onion, and cilantro"],
          "steps_ko":["고구마를 깍둑썰어 큐민, 파프리카로 양념해 25분 굽는다","블랙빈을 마늘과 라임즙으로 데운다","현미밥 위에 올린다","아보카도, 피클드 양파, 고수를 올린다"]},
     ]},
    {"id":"potato","icon":"🥔","name":"Potato","name_ko":"감자",
     "short":"Versatile staple crop","short_ko":"활용도 높은 구황작물",
     "badge":"Potassium","badge_ko":"칼륨","category":"Root Vegetable","category_ko":"구황작물",
     "description":"Rich in potassium, vitamin C, and resistant starch when cooled. One of the world's most important staple foods.",
     "description_ko":"칼륨, 비타민 C, 냉각 후 생기는 저항성 전분이 풍부해요. 세계에서 가장 중요한 주식 중 하나예요.",
     "effects":["Blood pressure control","Energy supply","Gut health","Immunity","Satiety"],
     "effects_ko":["혈압 조절","에너지 공급","장 건강","면역력","포만감"],
     "nutrition":{"Calories":"77kcal","Protein":"2.0g","Fiber":"2.2g","Carbs":"17.5g","Fat":"0.1g","Potassium":"421mg"},
     "recipes":[
         {"title":"Gamja Jorim (Braised Potatoes)","title_ko":"감자조림","time":"25 min","kcal":"210kcal","difficulty":"Easy",
          "steps":["Peel and cube potatoes (3cm pieces), soak in water 5 min","Stir-fry in sesame oil until lightly golden","Add soy sauce, sugar, corn syrup, water; bring to boil","Reduce heat, simmer 12–15 min until sauce is glossy and thick"],
          "steps_ko":["감자를 깍둑썰어 5분 물에 담근다","팬에 참기름을 두르고 살짝 볶는다","간장, 설탕, 물엿, 물을 넣고 끓인다","약불에서 12~15분 졸여 완성한다"]},
         {"title":"Korean Potato Soup","title_ko":"감자국","time":"20 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Make anchovy broth","Add thinly sliced potatoes and simmer 10 min","Season with doenjang or salt","Add scallions, dried seaweed, and serve"],
          "steps_ko":["멸치 육수를 낸다","감자를 얇게 썰어 넣고 10분 끓인다","된장이나 소금으로 간한다","파, 미역을 넣어 마무리한다"]},
         {"title":"Potato Pancakes","title_ko":"감자전","time":"20 min","kcal":"240kcal","difficulty":"Easy",
          "steps":["Grate raw potatoes, squeeze out as much moisture as possible","Mix with a pinch of salt and beaten egg","Fry spoonfuls in oil over medium heat until golden on both sides","Serve hot with soy dipping sauce"],
          "steps_ko":["감자를 강판에 갈아 물기를 꼭 짠다","소금 한 꼬집과 달걀을 넣어 섞는다","팬에 기름을 두르고 중불에서 굽는다","초간장과 함께 낸다"]},
     ]},
    {"id":"taro","icon":"🫚","name":"Taro","name_ko":"토란",
     "short":"Korean autumn root vegetable","short_ko":"가을철 한국 구황작물",
     "badge":"Fiber Rich","badge_ko":"식이섬유","category":"Root Vegetable","category_ko":"구황작물",
     "description":"A traditional Korean autumn vegetable rich in dietary fibre and potassium. Contains galactans that support immunity.",
     "description_ko":"칼륨과 식이섬유가 풍부한 가을철 전통 구황작물이에요. 갈락탄 성분이 면역력 강화에 도움을 줘요.",
     "effects":["Gut health","Blood pressure control","Immunity","Satiety","Bone health"],
     "effects_ko":["장 건강","혈압 조절","면역력","포만감","뼈 건강"],
     "nutrition":{"Calories":"112kcal","Protein":"1.5g","Fiber":"4.3g","Carbs":"26.5g","Fat":"0.2g","Potassium":"591mg"},
     "recipes":[
         {"title":"Toran Guk (Taro Soup)","title_ko":"토란국","time":"35 min","kcal":"150kcal","difficulty":"Medium",
          "steps":["Peel taro wearing gloves; rinse to reduce itch-causing oxalate","Blanch taro in salted water 5 min, drain","Make beef bone or anchovy broth","Add taro and simmer 20 min; season with doenjang, salt, scallions"],
          "steps_ko":["토란의 껍질을 벗기고 끓는 물에 5분 데친다","멸치 혹은 사골 육수를 낸다","토란을 넣고 20분 끓인다","된장, 소금, 파로 간하여 완성한다"]},
         {"title":"Taro Rice","title_ko":"토란밥","time":"40 min","kcal":"290kcal","difficulty":"Easy",
          "steps":["Peel and cut taro into bite-sized pieces, blanch 3 min","Add taro to rice cooker with rinsed rice","Add water as usual and cook","Serve with doenjang jjigae and season with sesame oil and soy sauce"],
          "steps_ko":["토란 껍질을 벗기고 끓는 물에 3분 데친다","씻은 쌀에 토란을 넣는다","물을 넣고 밥을 짓는다","된장찌개와 함께 참기름, 간장으로 간하여 먹는다"]},
     ]},
    {"id":"bellflower_root","icon":"🌿","name":"Bellflower Root","name_ko":"도라지",
     "short":"Korean medicinal root vegetable","short_ko":"한국 전통 약용 뿌리채소",
     "badge":"Saponin","badge_ko":"사포닌","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A traditional Korean medicinal root rich in saponins that support respiratory health. Often used in namul side dishes.",
     "description_ko":"사포닌이 풍부해 기관지와 면역력 강화에 도움을 줘요. 나물 반찬으로 즐겨 먹는 전통 식재료예요.",
     "effects":["Respiratory health","Immunity boost","Anti-inflammatory","Gut health","Antioxidant"],
     "effects_ko":["기관지 건강","면역 강화","항염증","장 건강","항산화"],
     "nutrition":{"Calories":"78kcal","Protein":"1.8g","Fiber":"3.1g","Carbs":"17.8g","Fat":"0.2g","Saponin":"Abundant"},
     "recipes":[
         {"title":"Doraji Namul","title_ko":"도라지나물","time":"20 min","kcal":"90kcal","difficulty":"Easy",
          "steps":["Slice bellflower root thinly, rub with salt, rinse and squeeze dry","Blanch in boiling water 1 min, rinse under cold water","Season with sesame oil, garlic, salt, and sesame seeds","Stir-fry briefly in pan and serve as banchan"],
          "steps_ko":["도라지를 가늘게 찢어 소금에 주물러 쓴맛을 제거한다","끓는 물에 1분 데쳐 찬물에 헹군다","참기름, 마늘, 소금, 깨로 무친다","팬에서 살짝 볶아 반찬으로 낸다"]},
         {"title":"Doraji Bibimbap Topping","title_ko":"도라지 비빔밥 나물","time":"15 min","kcal":"70kcal","difficulty":"Easy",
          "steps":["Prepare doraji namul as above","Use as one of the colourful toppings for bibimbap","Pairs well with spinach, bean sprouts, carrots, and a fried egg","Add gochujang and sesame oil to complete the bibimbap"],
          "steps_ko":["도라지나물을 위와 같이 준비한다","비빔밥의 고명 중 하나로 올린다","시금치, 콩나물, 당근, 달걀 프라이와 곁들인다","고추장, 참기름과 함께 비벼 먹는다"]},
     ]},
    {"id":"kongnamul","icon":"🌱","name":"Bean Sprouts","name_ko":"콩나물",
     "short":"Korean staple sprout vegetable","short_ko":"한국 대표 콩나물",
     "badge":"Vitamin C","badge_ko":"비타민C","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A staple of Korean cuisine, rich in vitamin C and asparagine. Often used in soups, bibimbap, and as a side dish.",
     "description_ko":"한국 요리의 기본 재료로, 비타민 C와 아스파라긴산이 풍부해요. 국, 비빔밥, 반찬으로 즐겨 먹어요.",
     "effects":["Immunity boost","Hangover relief","Digestion","Detox","Low calorie"],
     "effects_ko":["면역 강화","숙취 해소","소화 개선","해독","저칼로리"],
     "nutrition":{"Calories":"30kcal","Protein":"3.2g","Fiber":"1.8g","Carbs":"4.1g","Fat":"0.3g","Vitamin C":"12.8mg"},
     "recipes":[
         {"title":"Kongnamul Guk (Bean Sprout Soup)","title_ko":"콩나물국","time":"15 min","kcal":"60kcal","difficulty":"Easy",
          "steps":["Rinse bean sprouts thoroughly","Add to water with dried anchovies, bring to boil with lid on","Do not lift lid for first 5 min (prevents fishy smell)","Season with salt, garlic, scallions, and a drop of sesame oil"],
          "steps_ko":["콩나물을 깨끗이 씻는다","물에 멸치와 함께 넣고 뚜껑을 닫고 끓인다","처음 5분은 뚜껑을 열면 안 된다","소금, 마늘, 파, 참기름으로 간하여 완성한다"]},
         {"title":"Kongnamul Muchim","title_ko":"콩나물무침","time":"10 min","kcal":"50kcal","difficulty":"Easy",
          "steps":["Blanch bean sprouts in boiling salted water for 2 min","Drain and cool under cold water, squeeze gently","Season with sesame oil, garlic, salt, gochugaru, sesame seeds","Toss well and serve as banchan"],
          "steps_ko":["콩나물을 소금물에 2분 데친다","찬물에 헹궈 살짝 짠다","참기름, 마늘, 소금, 고춧가루, 깨로 무친다","골고루 버무려 반찬으로 낸다"]},
     ]},
    {"id":"perilla","icon":"🌿","name":"Perilla Leaf","name_ko":"깻잎",
     "short":"Aromatic Korean herb leaf","short_ko":"향긋한 한국 허브잎",
     "badge":"Antioxidant","badge_ko":"항산화","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A beloved Korean aromatic herb rich in rosmarinic acid, calcium, and iron. Distinctive flavour essential to Korean cuisine.",
     "description_ko":"로즈마린산, 칼슘, 철분이 풍부한 한국의 대표 향채예요. 한국 음식의 독특한 향미를 내는 필수 식재료예요.",
     "effects":["Anti-inflammatory","Bone health","Antioxidant","Antimicrobial","Skin health"],
     "effects_ko":["항염증","뼈 건강","항산화","항균","피부 건강"],
     "nutrition":{"Calories":"37kcal","Protein":"3.9g","Fiber":"3.3g","Carbs":"6.3g","Fat":"0.6g","Calcium":"211mg"},
     "recipes":[
         {"title":"Kkaennip Jangajji (Pickled Perilla)","title_ko":"깻잎 장아찌","time":"15 min+2 days","kcal":"45kcal","difficulty":"Easy",
          "steps":["Layer perilla leaves in a container","Make brine: soy sauce, vinegar, sugar, water, garlic, chili","Pour brine over leaves and press down","Refrigerate 2 days before eating; keeps for 2 weeks"],
          "steps_ko":["깻잎을 용기에 차곡차곡 쌓는다","간장, 식초, 설탕, 물, 마늘, 고추로 양념장을 만든다","양념장을 붓고 눌러준다","냉장고에 이틀 후부터 먹는다"]},
         {"title":"Perilla Leaf Wraps","title_ko":"깻잎 쌈","time":"5 min","kcal":"30kcal","difficulty":"Easy",
          "steps":["Wash fresh perilla leaves and pat dry","Use as wraps for grilled meat, rice, or sashimi","Add a smear of ssamjang (Korean chilli paste)","Top with garlic slice and green chili for full flavour"],
          "steps_ko":["깻잎을 씻어 물기를 뺀다","고기, 밥, 회를 싸서 먹는다","쌈장을 조금 얹는다","마늘, 청양고추와 함께 먹으면 더 맛있다"]},
     ]},
    {"id":"garlic","icon":"🧄","name":"Garlic","name_ko":"마늘",
     "short":"Allicin — natural antibiotic","short_ko":"알리신·천연 항생 효과",
     "badge":"Immunity Boost","badge_ko":"면역 강화","category":"Spices","category_ko":"향신료",
     "description":"Garlic's allicin compound has powerful antibacterial and antiviral properties. A cornerstone of Korean and global cooking.",
     "description_ko":"알리신 성분이 강력한 항균·항바이러스 효과를 내요. 한국 요리에서 빠질 수 없는 핵심 식재료예요.",
     "effects":["Immunity boost","Antibacterial","Cardiovascular health","Blood pressure control","Anti-cancer"],
     "effects_ko":["면역 강화","항균·항바이러스","심혈관 건강","혈압 조절","항암"],
     "nutrition":{"Calories":"149kcal","Protein":"6.4g","Fiber":"2.1g","Carbs":"33.1g","Fat":"0.5g","Allicin":"Abundant"},
     "recipes":[
         {"title":"Garlic Butter Shrimp","title_ko":"마늘 버터 새우","time":"15 min","kcal":"250kcal","difficulty":"Easy",
          "steps":["Clean and devein fresh shrimp","Melt butter in pan over medium heat, add sliced garlic","Add shrimp and cook until pink, about 2 min per side","Finish with lemon juice, parsley, and chili flakes"],
          "steps_ko":["새우를 손질한다","팬에 버터를 녹이고 마늘을 볶는다","새우를 넣어 분홍빛이 될 때까지 굽는다","레몬즙과 파슬리를 뿌려 완성한다"]},
         {"title":"Garlic Olive Oil Pasta","title_ko":"마늘 올리브오일 파스타","time":"20 min","kcal":"380kcal","difficulty":"Easy",
          "steps":["Cook pasta in heavily salted water until al dente","Heat generous olive oil, gently fry thinly sliced garlic until golden","Add chili flakes, then pasta with a splash of pasta water","Toss vigorously, finish with parsley and parmesan"],
          "steps_ko":["파스타를 소금물에 삶는다","올리브오일에 얇게 썬 마늘을 황금빛이 될 때까지 볶는다","고추 플레이크, 파스타, 면수를 넣어 섞는다","파슬리와 파마산으로 마무리한다"]},
         {"title":"Korean Black Garlic Honey Glaze","title_ko":"흑마늘 꿀 소스","time":"10 min","kcal":"90kcal","difficulty":"Easy",
          "steps":["Mash 5 cloves of black garlic into paste","Mix with honey, soy sauce, rice vinegar, and sesame oil","Use as glaze for roasted chicken or pork ribs","Also works as a salad dressing when thinned with water"],
          "steps_ko":["흑마늘 5알을 페이스트로 으깬다","꿀, 간장, 쌀식초, 참기름과 섞는다","닭고기나 돼지갈비 글레이즈로 활용한다","물로 희석하면 샐러드 드레싱으로도 좋다"]},
     ]},
    {"id":"ginger","icon":"🫚","name":"Ginger","name_ko":"생강",
     "short":"Anti-nausea and warming root","short_ko":"항구역·몸을 따뜻하게 하는 뿌리",
     "badge":"Digestive Aid","badge_ko":"소화 촉진","category":"Spices","category_ko":"향신료",
     "description":"Gingerol is one of the most powerful anti-inflammatory compounds in nature. Used in Korean cuisine and traditional medicine for centuries.",
     "description_ko":"진저롤은 자연에서 가장 강력한 항염증 성분 중 하나예요. 한국 요리와 한의학에서 오랫동안 활용해온 식재료예요.",
     "effects":["Nausea relief","Anti-inflammatory","Digestive aid","Immune support","Warming effect"],
     "effects_ko":["구역질 완화","항염증","소화 촉진","면역 강화","몸을 따뜻하게"],
     "nutrition":{"Calories":"80kcal","Protein":"1.8g","Fiber":"2.0g","Carbs":"17.8g","Fat":"0.8g","Gingerol":"Abundant"},
     "recipes":[
         {"title":"Ginger Tea (Saenggang Cha)","title_ko":"생강차","time":"10 min","kcal":"40kcal","difficulty":"Easy",
          "steps":["Peel and thinly slice 30g fresh ginger","Simmer in 2 cups water for 8 minutes","Strain into mug, add honey and a slice of lemon","Drink warm — especially good for colds and digestion"],
          "steps_ko":["생강 30g을 얇게 슬라이스한다","물 2컵에 8분 끓인다","체에 걸러 꿀과 레몬을 넣는다","따뜻하게 마신다 — 감기와 소화에 좋다"]},
         {"title":"Ginger Carrot Soup","title_ko":"생강 당근 수프","time":"30 min","kcal":"150kcal","difficulty":"Easy",
          "steps":["Sauté onion and fresh ginger in olive oil until soft","Add diced carrots and vegetable broth, simmer 20 min","Blend completely smooth with hand blender","Finish with coconut milk, lime juice, and salt"],
          "steps_ko":["양파와 생강을 올리브오일에 볶는다","당근과 채수를 넣고 20분 끓인다","핸드블렌더로 곱게 간다","코코넛밀크와 라임즙으로 마무리한다"]},
     ]},
    {"id":"doenjang","icon":"🫙","name":"Doenjang","name_ko":"된장",
     "short":"Korean fermented soybean paste","short_ko":"한국 전통 발효 콩 페이스트",
     "badge":"Probiotic","badge_ko":"프로바이오틱","category":"Fermented","category_ko":"발효식품",
     "description":"Korea's traditional fermented soybean paste, aged for months to years. Rich in probiotics, plant protein, and unique umami flavour.",
     "description_ko":"수개월에서 수년간 발효시킨 한국 전통 된장이에요. 프로바이오틱스, 식물성 단백질, 독특한 감칠맛이 풍부해요.",
     "effects":["Gut health","Anti-cancer","Immunity boost","Bone health","Antioxidant"],
     "effects_ko":["장 건강","항암","면역 강화","뼈 건강","항산화"],
     "nutrition":{"Calories":"182kcal","Protein":"12.5g","Fiber":"5.4g","Carbs":"23.2g","Fat":"6.0g","Probiotics":"Rich"},
     "recipes":[
         {"title":"Doenjang Jjigae","title_ko":"된장찌개","time":"20 min","kcal":"160kcal","difficulty":"Easy",
          "steps":["Make anchovy-kelp broth and bring to boil","Dissolve 3 tbsp doenjang in the broth","Add tofu, zucchini, mushrooms, and onion","Simmer 10 min, add scallions and serve boiling hot"],
          "steps_ko":["멸치·다시마 육수를 낸다","된장 3큰술을 풀어준다","두부, 애호박, 버섯, 양파를 넣는다","10분 끓이고 파를 올려 완성한다"]},
         {"title":"Ssamjang Dip","title_ko":"쌈장","time":"5 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Mix 3 tbsp doenjang with 1 tbsp gochujang","Add minced garlic, sesame oil, sesame seeds, and a little sugar","Optionally add finely diced onion or green onion","Use as dip for ssam wraps, raw vegetables, or meat"],
          "steps_ko":["된장 3큰술과 고추장 1큰술을 섞는다","다진 마늘, 참기름, 깨, 설탕을 넣는다","양파나 파를 잘게 썰어 넣어도 좋다","쌈, 채소, 고기 찍어 먹는 소스로 활용한다"]},
     ]},
    {"id":"seaweed","icon":"🌊","name":"Seaweed (Miyeok)","name_ko":"미역",
     "short":"Korean sea vegetable rich in iodine","short_ko":"요오드 풍부한 한국 해조류",
     "badge":"Iodine","badge_ko":"요오드","category":"Sea Vegetable","category_ko":"해조류",
     "description":"A staple of Korean postpartum recovery soup. Rich in iodine, calcium, and fucoidan — a compound with anti-cancer properties.",
     "description_ko":"한국 산후조리의 필수 식재료예요. 요오드, 칼슘, 항암 효과가 있는 푸코이단이 풍부해요.",
     "effects":["Thyroid health","Bone strength","Anti-cancer","Postpartum recovery","Weight management"],
     "effects_ko":["갑상선 건강","뼈 강화","항암","산후 회복","체중 관리"],
     "nutrition":{"Calories":"45kcal","Protein":"3.0g","Fiber":"3.4g","Carbs":"9.1g","Fat":"0.6g","Iodine":"1600μg"},
     "recipes":[
         {"title":"Miyeok Guk (Seaweed Soup)","title_ko":"미역국","time":"25 min","kcal":"100kcal","difficulty":"Easy",
          "steps":["Soak dried miyeok 10 min, squeeze and cut into pieces","Stir-fry miyeok in sesame oil with a little garlic","Add water or beef broth (4 cups) and bring to boil","Season with soup soy sauce and salt; simmer 15 min"],
          "steps_ko":["건미역을 10분 불려 물기를 짜고 자른다","참기름과 마늘로 미역을 볶는다","물이나 소고기 육수 4컵을 넣고 끓인다","국간장, 소금으로 간하여 15분 끓인다"]},
         {"title":"Miyeok Muchim","title_ko":"미역무침","time":"10 min","kcal":"50kcal","difficulty":"Easy",
          "steps":["Soak dried miyeok, blanch briefly, rinse cold","Season with sesame oil, soy sauce, vinegar, sugar, garlic","Toss well and add sesame seeds","Serve as refreshing banchan"],
          "steps_ko":["미역을 불려 살짝 데쳐 찬물에 헹군다","참기름, 간장, 식초, 설탕, 마늘로 무친다","깨를 뿌린다","시원한 반찬으로 낸다"]},
     ]},
    {"id":"egg","icon":"🥚","name":"Egg","name_ko":"달걀",
     "short":"Nature's perfect whole food","short_ko":"완전식품의 대명사",
     "badge":"Complete Protein","badge_ko":"완전단백질","category":"Protein","category_ko":"단백질",
     "description":"The most complete protein in nature — all essential amino acids plus choline for brain health. Essential in Korean home cooking.",
     "description_ko":"자연이 만든 가장 완벽한 단백질 공급원이에요. 필수아미노산을 모두 함유하고 뇌 건강에 필수인 콜린이 풍부해요.",
     "effects":["Muscle synthesis","Brain health","Eye health","Satiety","Energy supply"],
     "effects_ko":["근육 합성","뇌 건강","눈 건강","포만감","에너지 공급"],
     "nutrition":{"Calories":"155kcal","Protein":"13.0g","Fiber":"0g","Carbs":"1.1g","Fat":"11.0g","Choline":"294mg"},
     "recipes":[
         {"title":"Gyeran Jjim (Steamed Egg)","title_ko":"계란찜","time":"15 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Beat 3 eggs with 200ml anchovy broth or water","Season with soup soy sauce and salt","Pour into earthenware pot or heatproof bowl","Steam covered over medium heat 8–10 min until softly set"],
          "steps_ko":["달걀 3개를 멸치 육수 200ml와 풀어준다","국간장, 소금으로 간한다","뚝배기나 내열 그릇에 붓는다","중불에서 8~10분 쪄서 완성한다"]},
         {"title":"Egg Fried Rice","title_ko":"달걀 볶음밥","time":"10 min","kcal":"350kcal","difficulty":"Easy",
          "steps":["Heat sesame oil in wok over high heat","Add cold leftover rice and break up clumps","Push rice to side, scramble 2 eggs in the space","Combine, season with soy sauce, salt, top with scallions"],
          "steps_ko":["팬에 참기름을 두르고 강불에 달군다","찬밥을 넣고 덩어리를 풀어준다","옆으로 밀고 달걀 2개를 스크램블한다","합쳐서 간장, 소금으로 간하고 파를 올린다"]},
         {"title":"Avocado Scrambled Eggs","title_ko":"아보카도 스크램블 에그","time":"10 min","kcal":"320kcal","difficulty":"Easy",
          "steps":["Beat 2 eggs with a splash of milk, salt, and pepper","Slowly stir over low heat with butter until softly set","Halve an avocado and remove the stone","Spoon creamy scrambled eggs over avocado halves"],
          "steps_ko":["달걀 2개를 우유, 소금, 후추와 풀어준다","버터 팬에서 약불로 천천히 저으며 익힌다","아보카도를 반으로 갈라 씨를 제거한다","아보카도 위에 스크램블 에그를 얹는다"]},
     ]},
    {"id":"broccoli","icon":"🥦","name":"Broccoli","name_ko":"브로콜리",
     "short":"King of anti-cancer vegetables","short_ko":"항암 채소의 왕",
     "badge":"Anti-Cancer","badge_ko":"항암","category":"Vegetables","category_ko":"채소",
     "description":"More vitamin C than oranges. Sulforaphane is a potent anti-cancer compound. Best lightly steamed.",
     "description_ko":"비타민 C 함량이 오렌지보다 높고 설포라판이라는 항암 성분이 풍부해요. 살짝 데쳐 먹는 게 영양 보존에 가장 좋아요.",
     "effects":["Anti-cancer","Immunity boost","Digestion","Bone health","Blood sugar control"],
     "effects_ko":["항암","면역력 강화","소화 개선","뼈 건강","혈당 조절"],
     "nutrition":{"Calories":"34kcal","Protein":"2.8g","Fiber":"2.6g","Carbs":"6.6g","Fat":"0.4g","Vitamin C":"89.2mg"},
     "recipes":[
         {"title":"Garlic Broccoli Stir-Fry","title_ko":"브로콜리 마늘 볶음","time":"10 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Cut broccoli into florets, blanch in salted water 30 sec","Heat oil in pan, add minced garlic and fry until golden","Add blanched broccoli and stir-fry over high heat 2 min","Finish with oyster sauce, sesame oil, and sesame seeds"],
          "steps_ko":["브로콜리를 한 입 크기로 잘라 30초 데친다","팬에 기름을 두르고 마늘을 황금빛이 될 때까지 볶는다","강불에서 2분 볶는다","굴소스와 참기름으로 마무리한다"]},
         {"title":"Cream of Broccoli Soup","title_ko":"브로콜리 크림수프","time":"25 min","kcal":"210kcal","difficulty":"Medium",
          "steps":["Sauté onion and potato in olive oil until soft","Add broccoli florets and vegetable broth, simmer 15 min","Blend completely smooth with hand blender","Stir in heavy cream, season with salt, white pepper, and nutmeg"],
          "steps_ko":["양파와 감자를 올리브오일에 볶는다","브로콜리와 채수를 넣고 15분 끓인다","핸드블렌더로 곱게 간다","생크림을 넣어 크리미하게 만든다"]},
     ]},
    {"id":"avocado","icon":"🥑","name":"Avocado","name_ko":"아보카도",
     "short":"Healthy monounsaturated fats","short_ko":"건강한 단일불포화지방",
     "badge":"Vitamin E","badge_ko":"비타민E","category":"Healthy Fats","category_ko":"건강지방",
     "description":"Rich in heart-healthy monounsaturated fats and potassium. Contains twice the potassium of a banana.",
     "description_ko":"심장 건강에 좋은 단일불포화지방산이 풍부하고 칼륨 함량이 바나나의 2배예요.",
     "effects":["Heart health","Skin care","Blood pressure","Nutrient absorption","Anti-inflammatory"],
     "effects_ko":["심장 건강","피부 미용","혈압 조절","영양소 흡수","항염증"],
     "nutrition":{"Calories":"160kcal","Protein":"2.0g","Fiber":"6.7g","Carbs":"8.5g","Fat":"14.7g","Potassium":"485mg"},
     "recipes":[
         {"title":"Avocado Toast","title_ko":"아보카도 토스트","time":"10 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Toast whole grain bread until golden and crispy","Mash ripe avocado with lemon juice, salt, and black pepper","Spread generously on toast","Top with a poached egg, chili flakes, and chia seeds"],
          "steps_ko":["통곡물빵을 굽는다","아보카도를 레몬즙, 소금, 후추와 으깬다","빵에 듬뿍 바른다","반숙 달걀과 치아씨드를 올린다"]},
         {"title":"Guacamole","title_ko":"과카몰리","time":"8 min","kcal":"150kcal","difficulty":"Easy",
          "steps":["Mash 2 very ripe avocados with a fork, leaving some texture","Finely dice tomato, red onion, and cilantro and fold in","Add fresh lime juice, salt, cumin, and jalapeño","Serve immediately with tortilla chips or vegetable sticks"],
          "steps_ko":["잘 익은 아보카도 2개를 으깬다","토마토, 적양파, 고수를 잘게 썬다","라임즙, 소금, 큐민을 넣는다","토르티야 칩과 함께 바로 낸다"]},
     ]},
    {"id":"lentil","icon":"🌱","name":"Lentils","name_ko":"렌틸콩",
     "short":"Fiber and iron powerhouse","short_ko":"식이섬유·철분의 보고",
     "badge":"Vegan","badge_ko":"채식","category":"Legumes","category_ko":"콩류",
     "description":"One of the world's oldest crops. High in protein, iron, and fibre. Improves gut health and prevents blood sugar spikes.",
     "description_ko":"세계에서 가장 오래된 재배 작물 중 하나로, 단백질과 철분이 특히 풍부해요. 장 건강을 개선하고 혈당 급등을 막아줘요.",
     "effects":["Gut health","Blood sugar control","Anaemia prevention","Satiety","Prenatal health"],
     "effects_ko":["장 건강","혈당 조절","빈혈 예방","포만감","임산부 건강"],
     "nutrition":{"Calories":"116kcal","Protein":"9.0g","Fiber":"7.9g","Carbs":"20.1g","Fat":"0.4g","Iron":"3.3mg"},
     "recipes":[
         {"title":"Lentil Soup","title_ko":"렌틸 수프","time":"35 min","kcal":"290kcal","difficulty":"Easy",
          "steps":["Sauté diced onion, garlic, and carrot in olive oil until soft","Add red lentils, vegetable broth, cumin, paprika, and turmeric","Simmer on low heat for 25 minutes until lentils are soft","Partially blend with hand blender, finish with lemon juice"],
          "steps_ko":["양파, 마늘, 당근을 올리브오일에 볶는다","렌틸콩, 채수, 큐민, 파프리카를 넣는다","약불에서 25분 끓인다","핸드블렌더로 반쯤 갈고 레몬즙으로 마무리한다"]},
         {"title":"Lentil Curry","title_ko":"렌틸 커리","time":"30 min","kcal":"350kcal","difficulty":"Medium",
          "steps":["Fry curry paste in oil until fragrant","Add coconut milk and red lentils, stir well","Simmer on low heat for 20 minutes","Stir in a large handful of spinach, serve with steamed rice"],
          "steps_ko":["커리 페이스트를 볶아 향을 낸다","코코넛밀크와 렌틸콩을 넣는다","약불에서 20분 졸인다","시금치를 넣고 밥과 함께 낸다"]},
     ]},
    {"id":"oats","icon":"🌾","name":"Oats","name_ko":"귀리",
     "short":"Beta-glucan for lower cholesterol","short_ko":"베타글루칸·콜레스테롤 감소",
     "badge":"Heart Health","badge_ko":"심장 건강","category":"Whole Grain","category_ko":"통곡물",
     "description":"Rich in beta-glucan soluble fibre — clinically proven to lower LDL cholesterol and prevent blood sugar spikes.",
     "description_ko":"베타글루칸이라는 수용성 식이섬유가 특히 풍부해요. 콜레스테롤을 낮추고 혈당 급등을 막는 데 임상적으로 효과가 입증됐어요.",
     "effects":["Lower cholesterol","Blood sugar control","Satiety","Heart health","Gut health"],
     "effects_ko":["콜레스테롤 감소","혈당 조절","포만감","심장 건강","장 건강"],
     "nutrition":{"Calories":"389kcal","Protein":"17.0g","Fiber":"10.6g","Carbs":"66.3g","Fat":"6.9g","Magnesium":"177mg"},
     "recipes":[
         {"title":"Overnight Oats","title_ko":"오버나이트 오츠","time":"5 min + 8h","kcal":"320kcal","difficulty":"Easy",
          "steps":["Combine 1/2 cup rolled oats with 1 cup almond milk in a jar","Add 1 tbsp chia seeds, a drizzle of honey, and vanilla extract","Stir well, seal, and refrigerate overnight","In the morning top with fresh fruit, nuts, and granola"],
          "steps_ko":["귀리 1/2컵과 아몬드밀크 1컵을 용기에 담는다","치아씨드, 꿀, 바닐라를 넣고 잘 섞는다","뚜껑을 닫고 냉장고에 하룻밤 둔다","아침에 과일과 견과류를 올린다"]},
         {"title":"Banana Oat Pancakes","title_ko":"바나나 귀리 팬케이크","time":"20 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Mash 1 ripe banana and mix with 2 eggs and 1/2 cup rolled oats","Add cinnamon and baking powder, mix well","Cook tablespoon-sized portions over low heat, flip after 2–3 min","Serve with maple syrup, sliced banana, and berries"],
          "steps_ko":["바나나 1개를 으깨고 달걀 2개, 귀리 1/2컵을 섞는다","시나몬과 베이킹파우더를 넣는다","약불에서 양면을 굽는다","메이플시럽과 과일을 곁들인다"]},
     ]},
    {"id":"walnut","icon":"🫀","name":"Walnut","name_ko":"호두",
     "short":"Omega-3 brain health nut","short_ko":"오메가-3·뇌 건강 견과류",
     "badge":"Brain Health","badge_ko":"뇌 건강","category":"Nuts","category_ko":"견과류",
     "description":"Rich in plant-based omega-3 ALA and polyphenols. Even looks like a brain — and it's great for yours.",
     "description_ko":"식물성 오메가-3 ALA와 폴리페놀이 풍부해요. 호두의 생김새가 뇌와 닮았고 실제로 뇌 건강에도 좋아요.",
     "effects":["Brain health","Heart protection","Antioxidant","Reduced inflammation","Better sleep"],
     "effects_ko":["뇌 건강","심장 보호","항산화","염증 억제","수면 개선"],
     "nutrition":{"Calories":"654kcal","Protein":"15.2g","Fiber":"6.7g","Carbs":"13.7g","Fat":"65.2g","Omega-3":"9.1g"},
     "recipes":[
         {"title":"Walnut Porridge","title_ko":"호두죽","time":"25 min","kcal":"280kcal","difficulty":"Medium",
          "steps":["Soak walnuts 30 min, blend with 1 cup water until smooth","Wash glutinous rice and blend coarsely","Combine walnut milk and rice in pot, cook stirring constantly","Season with salt and honey when thick and creamy"],
          "steps_ko":["호두를 30분 불려 물 1컵과 함께 곱게 간다","찹쌀을 씻어 대충 갈아준다","호두즙과 찹쌀을 냄비에 넣고 저으며 끓인다","걸쭉해지면 소금과 꿀로 간한다"]},
         {"title":"Walnut Spinach Salad","title_ko":"호두 시금치 샐러드","time":"12 min","kcal":"240kcal","difficulty":"Easy",
          "steps":["Lightly toast walnuts in a dry pan until fragrant","Combine baby spinach, sliced apple, and dried cranberries","Make balsamic dressing: olive oil, balsamic vinegar, honey, Dijon","Toss salad with dressing and top with walnuts"],
          "steps_ko":["팬에서 호두를 살짝 볶는다","시금치, 사과, 크랜베리를 준비한다","발사믹 드레싱을 만든다","재료를 섞고 호두를 올린다"]},
     ]},
    {"id":"greek_yogurt","icon":"🥛","name":"Greek Yogurt","name_ko":"그릭요거트",
     "short":"Probiotic high-protein dairy","short_ko":"프로바이오틱스·고단백",
     "badge":"Gut Health","badge_ko":"장 건강","category":"Dairy","category_ko":"유제품",
     "description":"Higher protein than regular yogurt with live cultures improving gut health. A cup provides 17–20g of protein.",
     "description_ko":"단백질 함량이 높고 유산균이 장 건강을 개선해줘요. 한 컵으로 17~20g의 단백질을 섭취할 수 있어요.",
     "effects":["Gut health","Immunity boost","Bone strength","Satiety","Muscle recovery"],
     "effects_ko":["장 건강","면역력 강화","뼈 강화","포만감","근육 회복"],
     "nutrition":{"Calories":"59kcal","Protein":"10.0g","Fiber":"0g","Carbs":"3.6g","Fat":"0.4g","Calcium":"111mg"},
     "recipes":[
         {"title":"Greek Yogurt Parfait","title_ko":"그릭요거트 파르페","time":"5 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Layer Greek yogurt generously in a glass or bowl","Add a layer of crunchy granola","Top with fresh berries, sliced banana, and kiwi","Finish with a drizzle of honey and mint leaves"],
          "steps_ko":["컵에 그릭요거트를 듬뿍 담는다","그래놀라를 올린다","베리류, 바나나, 키위를 올린다","꿀을 드리즐하고 민트로 장식한다"]},
         {"title":"Yogurt Chicken Marinade","title_ko":"요거트 닭고기 마리네이드","time":"25 min + marinate","kcal":"310kcal","difficulty":"Medium",
          "steps":["Mix Greek yogurt with lemon juice, garlic, cumin, and smoked paprika","Score chicken breasts and coat thoroughly in marinade","Marinate at least 30 min, ideally overnight in fridge","Grill or bake at 200°C until cooked through, serve with herbs"],
          "steps_ko":["요거트에 레몬즙, 마늘, 큐민, 파프리카를 섞는다","닭가슴살에 칼집을 넣고 마리네이드를 입힌다","30분 이상, 가능하면 하룻밤 재운다","그릴에서 양면 6분씩 굽는다"]},
     ]},
    {"id":"turmeric","icon":"🟠","name":"Turmeric","name_ko":"강황",
     "short":"Curcumin anti-inflammatory spice","short_ko":"커큐민·항염 슈퍼 향신료",
     "badge":"Anti-Inflammatory","badge_ko":"항염증","category":"Spices","category_ko":"향신료",
     "description":"Curcumin is one of the most studied anti-inflammatory compounds. Add black pepper to boost absorption by 2000%.",
     "description_ko":"커큐민은 가장 광범위하게 연구된 천연 항염증 성분 중 하나예요. 후추와 함께 먹으면 흡수율이 2000% 높아져요.",
     "effects":["Anti-inflammatory","Joint health","Brain function","Antioxidant","Digestion"],
     "effects_ko":["항염증","관절 건강","뇌 기능 향상","항산화","소화 개선"],
     "nutrition":{"Calories":"354kcal","Protein":"7.8g","Fiber":"21.1g","Carbs":"64.9g","Fat":"9.9g","Curcumin":"3–5%"},
     "recipes":[
         {"title":"Golden Milk","title_ko":"황금 우유","time":"8 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Warm 250ml milk in a small saucepan over medium heat","Add 1/2 tsp turmeric, 1/4 tsp cinnamon, pinch of ginger and black pepper","Whisk until well combined and gently steaming","Sweeten with honey and enjoy warm"],
          "steps_ko":["우유 250ml를 중불에서 데운다","강황 1/2작은술, 시나몬, 생강, 후추를 넣는다","거품기로 잘 섞는다","꿀을 넣어 따뜻하게 마신다"]},
         {"title":"Turmeric Tofu Scramble","title_ko":"강황 두부 스크램블","time":"12 min","kcal":"200kcal","difficulty":"Easy",
          "steps":["Press firm tofu dry and crumble with hands","Sauté olive oil and garlic in pan until fragrant","Add tofu, turmeric, cumin, salt — stir-fry 5 min","Fold in spinach and cherry tomatoes until wilted"],
          "steps_ko":["두부를 손으로 부숴 물기를 제거한다","올리브오일과 마늘을 볶는다","두부, 강황, 큐민, 소금을 넣고 볶는다","시금치와 방울토마토를 넣어 마무리한다"]},
     ]},
    {"id":"chia","icon":"⚫","name":"Chia Seeds","name_ko":"치아씨드",
     "short":"Omega-3 and fibre super seed","short_ko":"오메가-3·식이섬유 슈퍼씨앗",
     "badge":"Superfood","badge_ko":"슈퍼푸드","category":"Seeds","category_ko":"씨앗",
     "description":"Absorb 12x their weight in water, forming a gel that promotes fullness. Highest plant-based source of calcium.",
     "description_ko":"무게의 12배까지 물을 흡수해 젤 형태가 되어 포만감을 오래 유지시켜줘요. 식물성 칼슘의 가장 좋은 공급원이에요.",
     "effects":["Satiety","Bone strength","Heart health","Blood sugar control","Digestion"],
     "effects_ko":["포만감","뼈 강화","심장 건강","혈당 조절","소화 개선"],
     "nutrition":{"Calories":"486kcal","Protein":"16.5g","Fiber":"34.4g","Carbs":"42.1g","Fat":"30.7g","Calcium":"631mg"},
     "recipes":[
         {"title":"Chia Seed Pudding","title_ko":"치아씨드 푸딩","time":"5 min + 4h","kcal":"200kcal","difficulty":"Easy",
          "steps":["Combine 3 tbsp chia seeds with 1 cup almond milk in a jar","Add honey and vanilla extract, stir vigorously","Stir again after 5 min to prevent clumping","Refrigerate at least 4 hours, top with mango and granola"],
          "steps_ko":["치아씨드 3큰술에 아몬드밀크 1컵을 붓는다","꿀과 바닐라를 넣고 잘 섞는다","5분 후 다시 한 번 저어준다","4시간 냉장 후 과일과 그래놀라를 올린다"]},
         {"title":"Chia Berry Jam","title_ko":"치아씨드 베리잼","time":"15 min","kcal":"40kcal","difficulty":"Easy",
          "steps":["Heat mixed berries with honey and lemon juice in saucepan","Mash berries and simmer stirring for 10 min","Remove from heat and stir in 2 tbsp chia seeds","Cool and store in glass jar in fridge"],
          "steps_ko":["베리류, 꿀, 레몬즙을 냄비에서 끓인다","베리를 으깨며 10분 졸인다","불을 끄고 치아씨드를 넣는다","식혀서 냉장 보관한다"]},
     ]},
    {"id":"sardine","icon":"🐟","name":"Sardine","name_ko":"정어리",
     "short":"Omega-3 and calcium-rich small fish","short_ko":"오메가-3·칼슘 풍부한 작은 생선",
     "badge":"Sustainable","badge_ko":"지속가능","category":"Seafood","category_ko":"해산물",
     "description":"One of the most nutrient-dense and sustainable seafood choices. Rich in omega-3, vitamin D, and calcium from edible bones.",
     "description_ko":"영양소 밀도가 가장 높고 지속 가능한 해산물이에요. 오메가-3, 비타민 D, 먹을 수 있는 뼈의 칼슘이 풍부해요.",
     "effects":["Brain health","Bone strength","Heart health","Vitamin D","Anti-inflammatory"],
     "effects_ko":["뇌 건강","뼈 강화","심장 건강","비타민D","항염증"],
     "nutrition":{"Calories":"208kcal","Protein":"24.6g","Fiber":"0g","Carbs":"0g","Fat":"11.5g","Calcium":"382mg"},
     "recipes":[
         {"title":"Sardine Toast","title_ko":"정어리 토스트","time":"8 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Toast sourdough bread until golden","Drain sardines and mash with lemon juice and Dijon mustard","Spread generously over toast","Top with thinly sliced cucumber, red onion, and capers"],
          "steps_ko":["사워도우 빵을 굽는다","정어리를 레몬즙과 디종 머스터드로 으깬다","빵에 펴 바른다","오이, 적양파, 케이퍼를 올린다"]},
         {"title":"Sardine Pasta","title_ko":"정어리 파스타","time":"20 min","kcal":"420kcal","difficulty":"Easy",
          "steps":["Cook spaghetti in well-salted water","Sauté garlic and chili flakes in generous olive oil","Add sardines and break into flakes with wooden spoon","Toss pasta with sardine oil, pasta water, lemon and parsley"],
          "steps_ko":["파스타를 소금물에 삶는다","올리브오일에 마늘과 고추를 볶는다","정어리를 넣어 부순다","파스타, 면수, 레몬, 파슬리와 섞는다"]},
     ]},
    {"id":"mango","icon":"🥭","name":"Mango","name_ko":"망고",
     "short":"Tropical vitamin C powerhouse","short_ko":"열대 비타민C 파워",
     "badge":"Vitamin C","badge_ko":"비타민C","category":"Fruit","category_ko":"과일",
     "description":"One cup provides nearly 70% of daily vitamin C needs. Mangiferin has unique anti-diabetic properties.",
     "description_ko":"한 컵으로 하루 비타민 C 필요량의 70%를 채울 수 있어요. 망기페린이라는 독특한 항당뇨 성분이 있어요.",
     "effects":["Immunity boost","Skin health","Eye protection","Digestive enzymes","Anti-inflammatory"],
     "effects_ko":["면역 강화","피부 건강","눈 보호","소화 효소","항염증"],
     "nutrition":{"Calories":"60kcal","Protein":"0.8g","Fiber":"1.6g","Carbs":"15.0g","Fat":"0.4g","Vitamin C":"36.4mg"},
     "recipes":[
         {"title":"Mango Salsa","title_ko":"망고 살사","time":"10 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Dice ripe mango, red onion, jalapeño, and fresh cilantro","Combine in bowl","Add fresh lime juice and a pinch of salt","Serve with grilled fish, tacos, or tortilla chips"],
          "steps_ko":["망고, 적양파, 할라피뇨, 고수를 썬다","볼에 담는다","라임즙과 소금을 넣는다","구운 생선이나 타코와 함께 낸다"]},
         {"title":"Mango Lassi","title_ko":"망고 라씨","time":"5 min","kcal":"190kcal","difficulty":"Easy",
          "steps":["Blend 1 ripe mango (cubed) with 200ml plain yogurt","Add a pinch of cardamom and honey to taste","Blend until completely smooth","Serve over ice — optionally top with saffron or rose petals"],
          "steps_ko":["망고와 요거트 200ml를 블렌더에 넣는다","카다몬 한 꼬집과 꿀을 넣는다","곱게 간다","얼음 위에 서브한다"]},
     ]},
    {"id":"almond","icon":"🌰","name":"Almond","name_ko":"아몬드",
     "short":"Vitamin E antioxidant nut","short_ko":"비타민E·항산화 견과류",
     "badge":"Antioxidant","badge_ko":"항산화","category":"Nuts","category_ko":"견과류",
     "description":"Rich in vitamin E for powerful antioxidant protection. Magnesium helps manage blood sugar and blood pressure.",
     "description_ko":"비타민 E가 풍부해 강력한 항산화 작용을 하고 피부 건강을 지켜줘요. 마그네슘이 혈당·혈압 관리에 도움이 돼요.",
     "effects":["Antioxidant","Skin care","Blood sugar control","Heart health","Bone strength"],
     "effects_ko":["항산화","피부 미용","혈당 조절","심장 건강","뼈 강화"],
     "nutrition":{"Calories":"579kcal","Protein":"21.2g","Fiber":"12.5g","Carbs":"21.6g","Fat":"49.9g","Vitamin E":"25.6mg"},
     "recipes":[
         {"title":"Almond Energy Balls","title_ko":"아몬드 에너지 볼","time":"15 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Process almonds, dates, and rolled oats in food processor","Add cocoa powder and honey; blend until mixture holds together","Roll into walnut-sized balls with damp hands","Coat in shredded coconut and refrigerate 30 min to firm up"],
          "steps_ko":["아몬드, 대추야자, 귀리를 푸드프로세서에 넣는다","코코아와 꿀을 넣고 뭉쳐질 때까지 간다","동그랗게 빚는다","코코넛 플레이크를 굴려 냉장고에 굳힌다"]},
         {"title":"Almond Butter Toast","title_ko":"아몬드 버터 토스트","time":"5 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Toast whole grain bread until golden","Spread a thick layer of almond butter","Top with banana slices","Drizzle with honey and sprinkle chia seeds and cinnamon"],
          "steps_ko":["통곡물빵을 굽는다","아몬드버터를 듬뿍 바른다","바나나 슬라이스를 올린다","꿀, 치아씨드, 시나몬을 뿌린다"]},
     ]},

    # ── 추가 한국 식재료 ───────────────────────────────────────────
    {"id":"zucchini","icon":"🥒","name":"Zucchini (Hobak)","name_ko":"애호박",
     "short":"Korean summer squash","short_ko":"한국 대표 여름 채소",
     "badge":"Low Calorie","badge_ko":"저칼로리","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A staple in Korean cooking, zucchini is low in calories and rich in vitamin C and potassium. Used in jjigae, namul, and jeon.",
     "description_ko":"한국 요리의 기본 채소로 칼로리가 낮고 비타민 C와 칼륨이 풍부해요. 찌개, 나물, 전에 두루 쓰여요.",
     "effects":["Low calorie","Digestion","Hydration","Eye health","Immunity"],
     "effects_ko":["저칼로리","소화 개선","수분 보충","눈 건강","면역력"],
     "nutrition":{"Calories":"17kcal","Protein":"1.2g","Fiber":"1.1g","Carbs":"3.1g","Fat":"0.3g","Vitamin C":"17.9mg"},
     "recipes":[
         {"title":"Hobak Namul","title_ko":"애호박나물","time":"10 min","kcal":"60kcal","difficulty":"Easy",
          "steps":["Slice zucchini into thin half-moons","Salt lightly and squeeze out moisture after 5 min","Stir-fry with sesame oil, garlic, and salt","Finish with sesame seeds and scallions"],
          "steps_ko":["애호박을 반달 모양으로 얇게 썬다","소금에 절여 물기를 짠다","참기름, 마늘, 소금으로 볶는다","깨와 파로 마무리한다"]},
         {"title":"Hobak Jeon","title_ko":"애호박전","time":"15 min","kcal":"160kcal","difficulty":"Easy",
          "steps":["Slice zucchini 0.5cm thick rounds","Season with salt, coat in flour then egg wash","Pan-fry in oil over medium heat until golden on both sides","Serve hot with soy dipping sauce"],
          "steps_ko":["애호박을 0.5cm 두께로 썬다","소금으로 간하고 밀가루, 달걀물을 입힌다","중불에서 양면을 노릇하게 굽는다","초간장과 함께 낸다"]},
     ]},
    {"id":"napa_cabbage","icon":"🥬","name":"Napa Cabbage","name_ko":"배추",
     "short":"Korean kimchi base vegetable","short_ko":"김치의 주재료",
     "badge":"Vitamin K","badge_ko":"비타민K","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"The foundation of kimchi and baechu-guk. Rich in vitamin K, C, and folate. Low in calories and high in fibre.",
     "description_ko":"김치의 핵심 재료예요. 비타민 K, C, 엽산이 풍부하고 칼로리가 낮으면서 식이섬유가 높아요.",
     "effects":["Gut health","Immunity","Bone health","Detox","Low calorie"],
     "effects_ko":["장 건강","면역력","뼈 건강","해독","저칼로리"],
     "nutrition":{"Calories":"16kcal","Protein":"1.2g","Fiber":"1.7g","Carbs":"3.2g","Fat":"0.2g","Vitamin K":"59μg"},
     "recipes":[
         {"title":"Baechu Doenjang Guk","title_ko":"배추 된장국","time":"15 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Tear napa cabbage into pieces","Make anchovy broth and bring to boil","Dissolve doenjang in broth","Add cabbage, tofu, and scallions; simmer 8 min"],
          "steps_ko":["배추를 먹기 좋게 뜯는다","멸치 육수를 낸다","된장을 풀어준다","배추, 두부, 파를 넣고 8분 끓인다"]},
         {"title":"Baechu Kimchi","title_ko":"배추김치","time":"2h + ferment","kcal":"15kcal","difficulty":"Hard",
          "steps":["Quarter cabbage and salt generously, rest 2 hours","Rinse and squeeze dry thoroughly","Mix gochugaru, garlic, ginger, fish sauce, scallions, radish for paste","Coat every leaf with paste, pack into jar, ferment at room temp 1–2 days"],
          "steps_ko":["배추를 절여 2시간 둔다","씻어 물기를 꼭 짠다","고춧가루, 마늘, 생강, 젓갈, 파, 무로 양념을 만든다","잎 사이사이에 양념을 넣고 항아리에 담아 1~2일 발효시킨다"]},
     ]},
    {"id":"radish","icon":"🫚","name":"Radish (Mu)","name_ko":"무",
     "short":"Korean digestive root vegetable","short_ko":"소화 돕는 한국 뿌리채소",
     "badge":"Digestive Aid","badge_ko":"소화 촉진","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"Korean radish is crisp and mildly spicy, containing digestive enzymes. Used in soups, kimchi, and pickles.",
     "description_ko":"아밀라아제 등 소화 효소가 풍부한 한국의 대표 뿌리채소예요. 국, 김치, 깍두기에 두루 활용돼요.",
     "effects":["Digestion","Anti-inflammatory","Detox","Immunity","Low calorie"],
     "effects_ko":["소화 촉진","항염증","해독","면역력","저칼로리"],
     "nutrition":{"Calories":"18kcal","Protein":"0.6g","Fiber":"1.6g","Carbs":"4.1g","Fat":"0.1g","Vitamin C":"22mg"},
     "recipes":[
         {"title":"Mu Doenjang Guk","title_ko":"무 된장국","time":"15 min","kcal":"70kcal","difficulty":"Easy",
          "steps":["Peel and cube radish into 2cm pieces","Add to anchovy broth and simmer 10 min","Dissolve doenjang and add tofu","Finish with scallions and serve hot"],
          "steps_ko":["무를 2cm 크기로 깍둑썬다","멸치 육수에 넣고 10분 끓인다","된장을 풀고 두부를 넣는다","파를 올려 완성한다"]},
         {"title":"Kkakdugi (Radish Kimchi)","title_ko":"깍두기","time":"30 min + ferment","kcal":"20kcal","difficulty":"Medium",
          "steps":["Cube radish into 2cm pieces, salt and rest 20 min","Mix gochugaru, garlic, ginger, fish sauce, sugar","Combine radish with paste and mix well","Pack in jar, ferment 1 day at room temp then refrigerate"],
          "steps_ko":["무를 2cm로 깍둑썰어 소금에 20분 절인다","고춧가루, 마늘, 생강, 젓갈, 설탕을 섞는다","무에 양념을 버무린다","항아리에 담아 하루 실온 발효 후 냉장 보관한다"]},
     ]},
    {"id":"mushroom","icon":"🍄","name":"Shiitake Mushroom","name_ko":"표고버섯",
     "short":"Immune-boosting umami mushroom","short_ko":"면역력을 높이는 감칠맛 버섯",
     "badge":"Lentinan","badge_ko":"렌티난","category":"Mushroom","category_ko":"버섯",
     "description":"Rich in lentinan, a beta-glucan that enhances immune function and has anti-cancer properties. Provides deep umami flavour.",
     "description_ko":"면역 기능을 강화하고 항암 효과가 있는 베타글루칸인 렌티난이 풍부해요. 깊은 감칠맛이 특징이에요.",
     "effects":["Immunity boost","Anti-cancer","Cholesterol reduction","Gut health","Bone health"],
     "effects_ko":["면역 강화","항암","콜레스테롤 감소","장 건강","뼈 건강"],
     "nutrition":{"Calories":"34kcal","Protein":"2.2g","Fiber":"2.5g","Carbs":"6.8g","Fat":"0.5g","Vitamin D":"18IU"},
     "recipes":[
         {"title":"Pyogo Namul","title_ko":"표고버섯나물","time":"12 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Soak dried shiitake 30 min, slice thinly","Stir-fry with sesame oil, soy sauce, garlic","Season with salt and sesame seeds","Serve as banchan or bibimbap topping"],
          "steps_ko":["건표고버섯을 30분 불려 얇게 썬다","참기름, 간장, 마늘로 볶는다","소금과 깨로 간한다","반찬이나 비빔밥 나물로 낸다"]},
         {"title":"Mushroom Doenjang Soup","title_ko":"버섯 된장국","time":"15 min","kcal":"90kcal","difficulty":"Easy",
          "steps":["Slice shiitake and oyster mushrooms","Make anchovy broth","Dissolve doenjang, add mushrooms and tofu","Simmer 8 min, finish with scallions"],
          "steps_ko":["표고버섯과 느타리버섯을 썬다","멸치 육수를 낸다","된장을 풀고 버섯과 두부를 넣는다","8분 끓이고 파를 올린다"]},
     ]},
    {"id":"oyster_mushroom","icon":"🍄","name":"Oyster Mushroom","name_ko":"느타리버섯",
     "short":"Meaty low-calorie mushroom","short_ko":"쫄깃한 저칼로리 버섯",
     "badge":"Protein","badge_ko":"단백질","category":"Mushroom","category_ko":"버섯",
     "description":"Oyster mushrooms are meaty in texture and high in protein relative to calories. Rich in B vitamins and ergothioneine antioxidant.",
     "description_ko":"쫄깃한 식감과 높은 단백질 함량이 특징이에요. B 비타민과 항산화 성분인 에르고티오닌이 풍부해요.",
     "effects":["Immunity","Cholesterol reduction","Antioxidant","Low calorie","Brain health"],
     "effects_ko":["면역력","콜레스테롤 감소","항산화","저칼로리","뇌 건강"],
     "nutrition":{"Calories":"33kcal","Protein":"3.3g","Fiber":"2.3g","Carbs":"6.1g","Fat":"0.4g","Niacin":"4.9mg"},
     "recipes":[
         {"title":"Oyster Mushroom Stir-Fry","title_ko":"느타리버섯 볶음","time":"10 min","kcal":"90kcal","difficulty":"Easy",
          "steps":["Tear oyster mushrooms into strips","Stir-fry with butter and garlic over high heat","Season with soy sauce, pepper, and sesame oil","Top with scallions and sesame seeds"],
          "steps_ko":["느타리버섯을 손으로 뜯는다","버터와 마늘로 강불에서 볶는다","간장, 후추, 참기름으로 간한다","파와 깨를 뿌린다"]},
         {"title":"Mushroom Jeon","title_ko":"버섯전","time":"15 min","kcal":"140kcal","difficulty":"Easy",
          "steps":["Flatten oyster mushrooms gently","Season with salt, coat in flour then egg","Pan-fry in oil until golden on both sides","Serve with soy dipping sauce"],
          "steps_ko":["느타리버섯을 납작하게 편다","소금으로 간하고 밀가루, 달걀물을 입힌다","팬에서 양면을 노릇하게 굽는다","초간장과 함께 낸다"]},
     ]},
    {"id":"enoki","icon":"🍄","name":"Enoki Mushroom","name_ko":"팽이버섯",
     "short":"Delicate immune-supporting mushroom","short_ko":"가냘픈 면역 강화 버섯",
     "badge":"Low Calorie","badge_ko":"저칼로리","category":"Mushroom","category_ko":"버섯",
     "description":"Enoki mushrooms contain flammulin, a protein shown to inhibit tumour growth. Crisp texture and mild flavour make them versatile.",
     "description_ko":"종양 억제 효과가 있는 플라뮬린 단백질이 함유되어 있어요. 아삭한 식감과 순한 맛으로 다양한 요리에 활용돼요.",
     "effects":["Anti-cancer","Immunity","Low calorie","Gut health","Antioxidant"],
     "effects_ko":["항암","면역력","저칼로리","장 건강","항산화"],
     "nutrition":{"Calories":"37kcal","Protein":"2.7g","Fiber":"2.7g","Carbs":"7.6g","Fat":"0.3g","Flammulin":"Abundant"},
     "recipes":[
         {"title":"Enoki Butter Soy Stir-Fry","title_ko":"팽이버섯 버터구이","time":"8 min","kcal":"80kcal","difficulty":"Easy",
          "steps":["Trim root ends of enoki, separate clusters","Melt butter in pan over medium heat","Add enoki and stir-fry 3 min","Splash soy sauce, add scallions and serve"],
          "steps_ko":["팽이버섯 밑동을 자르고 분리한다","팬에 버터를 녹인다","팽이버섯을 3분 볶는다","간장을 뿌리고 파를 올려 낸다"]},
         {"title":"Enoki Soup","title_ko":"팽이버섯국","time":"10 min","kcal":"40kcal","difficulty":"Easy",
          "steps":["Make anchovy broth","Add enoki mushrooms and bring to gentle boil","Season with soup soy sauce and salt","Add egg drop style and garnish with scallions"],
          "steps_ko":["멸치 육수를 낸다","팽이버섯을 넣고 끓인다","국간장과 소금으로 간한다","달걀을 풀어 넣고 파를 올린다"]},
     ]},
    {"id":"gosari","icon":"🌿","name":"Bracken Fern","name_ko":"고사리",
     "short":"Traditional Korean mountain vegetable","short_ko":"한국 전통 산나물",
     "badge":"Iron Rich","badge_ko":"철분 풍부","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A beloved Korean mountain vegetable with an earthy, chewy texture. Rich in iron, fibre, and vitamins. Must be thoroughly cooked.",
     "description_ko":"구수하고 쫄깃한 식감으로 사랑받는 한국 전통 산나물이에요. 철분, 식이섬유, 비타민이 풍부해요. 반드시 충분히 익혀야 해요.",
     "effects":["Iron supplement","Bone health","Satiety","Digestion","Energy"],
     "effects_ko":["철분 보충","뼈 건강","포만감","소화 개선","에너지"],
     "nutrition":{"Calories":"34kcal","Protein":"4.6g","Fiber":"3.5g","Carbs":"5.8g","Fat":"0.4g","Iron":"1.7mg"},
     "recipes":[
         {"title":"Gosari Namul","title_ko":"고사리나물","time":"20 min","kcal":"90kcal","difficulty":"Medium",
          "steps":["Soak dried gosari overnight, boil 30 min until tender","Cut into 5cm pieces","Stir-fry with sesame oil, garlic, soy sauce, and a little water","Season with salt and sesame seeds"],
          "steps_ko":["건고사리를 하룻밤 불려 30분 삶는다","5cm 길이로 자른다","참기름, 마늘, 간장, 물을 넣어 볶는다","소금과 깨로 마무리한다"]},
         {"title":"Gosari Bibimbap","title_ko":"고사리 비빔밥","time":"30 min","kcal":"420kcal","difficulty":"Medium",
          "steps":["Prepare gosari namul as above","Cook spinach, bean sprout, and carrot namul separately","Place all vegetables over steamed rice in a bowl","Top with fried egg, add gochujang and sesame oil, mix well"],
          "steps_ko":["고사리나물을 위와 같이 준비한다","시금치, 콩나물, 당근 나물을 각각 무친다","따뜻한 밥 위에 나물을 색깔 맞춰 올린다","달걀 프라이를 올리고 고추장, 참기름을 넣어 비빈다"]},
     ]},
    {"id":"crown_daisy","icon":"🌿","name":"Crown Daisy","name_ko":"쑥갓",
     "short":"Aromatic Korean green herb","short_ko":"향긋한 한국 쑥 향채",
     "badge":"Antioxidant","badge_ko":"항산화","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"A distinctive aromatic green used in Korean hot pots and soups. Rich in beta-carotene, iron, and calcium with a unique herbal aroma.",
     "description_ko":"한국 전골과 국에 없어선 안 될 향채예요. 베타카로틴, 철분, 칼슘이 풍부하고 독특한 허브 향이 특징이에요.",
     "effects":["Eye health","Bone health","Antioxidant","Digestive aid","Calming"],
     "effects_ko":["눈 건강","뼈 건강","항산화","소화 촉진","심신 안정"],
     "nutrition":{"Calories":"22kcal","Protein":"2.1g","Fiber":"1.8g","Carbs":"3.9g","Fat":"0.4g","Beta-carotene":"2.1mg"},
     "recipes":[
         {"title":"Ssukgat Namul","title_ko":"쑥갓나물","time":"10 min","kcal":"50kcal","difficulty":"Easy",
          "steps":["Blanch crown daisy in boiling salted water 30 sec","Rinse in cold water and squeeze gently dry","Season with sesame oil, garlic, salt, and sesame seeds","Serve as refreshing banchan"],
          "steps_ko":["쑥갓을 소금 끓는 물에 30초 데친다","찬물에 헹궈 물기를 짠다","참기름, 마늘, 소금, 깨로 무친다","시원한 반찬으로 낸다"]},
         {"title":"Jeongol Topping","title_ko":"전골 고명","time":"5 min","kcal":"20kcal","difficulty":"Easy",
          "steps":["Wash crown daisy and trim stems","Add at the very end of cooking any Korean hot pot","The heat wilts the greens gently — do not overcook","The aroma elevates the entire dish"],
          "steps_ko":["쑥갓을 씻어 준비한다","전골이나 찌개 마지막에 올린다","살짝만 익혀 향을 살린다","향이 요리 전체를 살려준다"]},
     ]},
    {"id":"mugwort","icon":"🌿","name":"Mugwort","name_ko":"쑥",
     "short":"Korean spring medicinal herb","short_ko":"한국 봄철 약용 허브",
     "badge":"Iron Rich","badge_ko":"철분 풍부","category":"Korean Herb","category_ko":"한국 약초",
     "description":"A cornerstone of Korean traditional medicine and spring cuisine. Rich in iron, vitamins A and C, and artemisinin with anti-inflammatory effects.",
     "description_ko":"한국 전통 의학과 봄 음식의 핵심 재료예요. 철분, 비타민 A·C, 항염증 효과의 아르테미시닌이 풍부해요.",
     "effects":["Iron supplement","Anti-inflammatory","Warming effect","Digestive aid","Hormone balance"],
     "effects_ko":["철분 보충","항염증","몸을 따뜻하게","소화 촉진","호르몬 균형"],
     "nutrition":{"Calories":"36kcal","Protein":"3.8g","Fiber":"3.4g","Carbs":"5.5g","Fat":"0.8g","Iron":"2.9mg"},
     "recipes":[
         {"title":"Ssuk Tteok (Mugwort Rice Cake)","title_ko":"쑥떡","time":"40 min","kcal":"180kcal","difficulty":"Hard",
          "steps":["Blanch fresh mugwort briefly, squeeze very dry, chop finely","Mix with glutinous rice flour, water, and salt into dough","Fill with sweet red bean paste (or sesame)","Steam in steamer for 20 min until cooked through"],
          "steps_ko":["쑥을 살짝 데쳐 물기를 꼭 짜고 잘게 다진다","찹쌀가루, 물, 소금으로 반죽한다","팥이나 깨소 앙금을 넣어 모양을 빚는다","찜기에 20분 쪄서 완성한다"]},
         {"title":"Ssuk Doenjang Soup","title_ko":"쑥 된장국","time":"15 min","kcal":"90kcal","difficulty":"Easy",
          "steps":["Wash fresh mugwort and roughly chop","Make anchovy broth","Dissolve doenjang, add clams or tofu","Add mugwort at the end, simmer 2 min only"],
          "steps_ko":["쑥을 씻어 대충 자른다","멸치 육수를 낸다","된장을 풀고 조개나 두부를 넣는다","마지막에 쑥을 넣고 2분만 끓인다"]},
     ]},
    {"id":"black_sesame","icon":"🫙","name":"Black Sesame","name_ko":"흑임자(검은깨)",
     "short":"Korean black sesame — hair and bone health","short_ko":"모발·뼈 건강에 좋은 흑임자",
     "badge":"Calcium","badge_ko":"칼슘","category":"Seeds","category_ko":"씨앗",
     "description":"A treasured ingredient in Korean cuisine and medicine. Rich in calcium, iron, and antioxidant anthocyanins for hair and bone health.",
     "description_ko":"한국 음식과 한의학에서 귀하게 쓰이는 재료예요. 칼슘, 철분, 안토시아닌이 풍부해 모발과 뼈 건강에 특히 좋아요.",
     "effects":["Hair health","Bone strength","Antioxidant","Brain health","Iron supplement"],
     "effects_ko":["모발 건강","뼈 강화","항산화","뇌 건강","철분 보충"],
     "nutrition":{"Calories":"573kcal","Protein":"17.7g","Fiber":"11.8g","Carbs":"23.4g","Fat":"49.7g","Calcium":"975mg"},
     "recipes":[
         {"title":"Heukimja Juk (Black Sesame Porridge)","title_ko":"흑임자죽","time":"30 min","kcal":"280kcal","difficulty":"Medium",
          "steps":["Toast black sesame seeds, blend with water until smooth","Wash glutinous rice and soak 30 min","Blend soaked rice coarsely with water","Cook sesame milk and rice together, stirring constantly; season with salt and honey"],
          "steps_ko":["흑임자를 볶아 물과 함께 곱게 간다","찹쌀을 씻어 30분 불린다","불린 쌀을 물과 함께 대충 간다","흑임자즙과 쌀을 함께 넣고 저으며 끓이다 소금, 꿀로 간한다"]},
         {"title":"Black Sesame Latte","title_ko":"흑임자 라떼","time":"8 min","kcal":"200kcal","difficulty":"Easy",
          "steps":["Blend 2 tbsp toasted black sesame with 1 cup warm milk","Add honey and a pinch of salt","Blend until silky smooth","Pour into cup — beautiful dark colour"],
          "steps_ko":["볶은 흑임자 2큰술과 따뜻한 우유 1컵을 갈아준다","꿀과 소금 한 꼬집을 넣는다","곱게 블렌딩한다","컵에 따른다 — 아름다운 검은 색상"]},
     ]},
    {"id":"red_bean","icon":"🫘","name":"Red Bean (Adzuki)","name_ko":"팥",
     "short":"Korean traditional bean rich in polyphenols","short_ko":"폴리페놀 풍부한 한국 전통 콩",
     "badge":"Antioxidant","badge_ko":"항산화","category":"Legumes","category_ko":"콩류",
     "description":"Adzuki beans are a cornerstone of Korean sweets and porridge. High in protein, fibre, and polyphenols with diuretic properties.",
     "description_ko":"한국 전통 음식의 핵심 재료예요. 단백질, 식이섬유, 폴리페놀이 풍부하고 이뇨 작용도 있어요.",
     "effects":["Antioxidant","Edema relief","Blood sugar control","Gut health","Iron supplement"],
     "effects_ko":["항산화","부종 완화","혈당 조절","장 건강","철분 보충"],
     "nutrition":{"Calories":"329kcal","Protein":"19.9g","Fiber":"12.7g","Carbs":"62.9g","Fat":"0.5g","Iron":"5.0mg"},
     "recipes":[
         {"title":"Patjuk (Red Bean Porridge)","title_ko":"팥죽","time":"90 min","kcal":"310kcal","difficulty":"Medium",
          "steps":["Boil red beans until very tender (about 1 hour), drain first water","Add fresh water and simmer until beans fall apart","Strain to make smooth red bean broth","Cook with glutinous rice flour dumplings (saealssim), season with salt and sugar"],
          "steps_ko":["팥을 1시간 삶아 첫물은 버린다","새 물에 팥이 퍼질 때까지 끓인다","팥을 걸러 팥물을 만든다","새알심을 넣고 소금, 설탕으로 간하여 완성한다"]},
         {"title":"Red Bean Shaved Ice","title_ko":"팥빙수","time":"15 min","kcal":"280kcal","difficulty":"Easy",
          "steps":["Cook sweetened red bean paste (or use store-bought)","Shave ice finely or use crushed ice","Top with red beans, rice cakes (tteok), and condensed milk","Add mochi, corn flakes, or fruit as desired"],
          "steps_ko":["달콤한 팥을 준비한다","얼음을 곱게 간다","팥, 떡, 연유를 올린다","모찌, 콘플레이크, 과일을 추가한다"]},
     ]},
    {"id":"perilla_seed","icon":"🫙","name":"Perilla Seed Oil","name_ko":"들기름",
     "short":"Korean omega-3 rich seed oil","short_ko":"한국의 오메가-3 식용유",
     "badge":"Omega-3","badge_ko":"오메가-3","category":"Korean Ingredient","category_ko":"한국 식재료",
     "description":"Cold-pressed from perilla seeds, this nutty oil has the highest omega-3 content of any culinary oil. A staple of Korean cooking.",
     "description_ko":"들깨를 냉압착한 기름으로 식용유 중 오메가-3 함량이 가장 높아요. 한국 요리의 필수 재료예요.",
     "effects":["Brain health","Heart health","Anti-inflammatory","Skin health","Omega-3 supplement"],
     "effects_ko":["뇌 건강","심장 건강","항염증","피부 건강","오메가-3 보충"],
     "nutrition":{"Calories":"884kcal","Protein":"0g","Fiber":"0g","Carbs":"0g","Fat":"100g","Omega-3":"62%"},
     "recipes":[
         {"title":"Perilla Oil Doenjang Bibimbap","title_ko":"들기름 된장 비빔밥","time":"15 min","kcal":"420kcal","difficulty":"Easy",
          "steps":["Cook rice and place in bowl","Add namul vegetables of choice","Mix 1 tbsp doenjang with 1 tsp perilla oil and a little gochujang","Top with fried egg and drizzle perilla oil; mix everything together"],
          "steps_ko":["밥을 지어 그릇에 담는다","나물을 올린다","된장 1큰술, 들기름 1작은술, 고추장을 섞어 소스를 만든다","달걀 프라이를 올리고 들기름을 뿌려 비빈다"]},
         {"title":"Perilla Oil Seaweed Soup","title_ko":"들기름 미역국","time":"20 min","kcal":"100kcal","difficulty":"Easy",
          "steps":["Soak dried miyeok, squeeze and cut into pieces","Stir-fry miyeok in perilla oil with garlic (key step for flavour)","Add water or beef broth and bring to boil","Season with soup soy sauce and salt; simmer 12 min"],
          "steps_ko":["건미역을 불려 자른다","들기름과 마늘로 미역을 볶는다 (풍미의 핵심)","물이나 육수를 넣고 끓인다","국간장, 소금으로 간하여 12분 끓인다"]},
     ]},
    {"id":"yukgaejang_greens","icon":"🌿","name":"Water Parsley","name_ko":"미나리",
     "short":"Korean aromatic water herb","short_ko":"향긋한 한국 수생 허브",
     "badge":"Detox","badge_ko":"해독","category":"Korean Herb","category_ko":"한국 약초",
     "description":"Water parsley (minari) is a beloved Korean herb with a fresh, slightly peppery flavour. Rich in vitamins and minerals with detoxifying properties.",
     "description_ko":"한국 요리에서 사랑받는 허브로 신선하고 살짝 매운 향이 특징이에요. 비타민과 미네랄이 풍부하고 해독 효과가 있어요.",
     "effects":["Detox","Liver health","Antioxidant","Blood pressure control","Anti-inflammatory"],
     "effects_ko":["해독","간 건강","항산화","혈압 조절","항염증"],
     "nutrition":{"Calories":"27kcal","Protein":"2.1g","Fiber":"1.6g","Carbs":"4.9g","Fat":"0.3g","Vitamin C":"28mg"},
     "recipes":[
         {"title":"Minari Namul","title_ko":"미나리나물","time":"10 min","kcal":"55kcal","difficulty":"Easy",
          "steps":["Blanch minari in boiling salted water 30 sec","Rinse cold, squeeze dry, and cut 4cm lengths","Season with sesame oil, salt, garlic, and sesame seeds","Serve as cooling banchan"],
          "steps_ko":["미나리를 소금물에 30초 데친다","찬물에 헹궈 물기를 짜고 4cm로 자른다","참기름, 소금, 마늘, 깨로 무친다","시원한 반찬으로 낸다"]},
         {"title":"Haemul Pajeon with Minari","title_ko":"미나리 해물파전","time":"20 min","kcal":"290kcal","difficulty":"Medium",
          "steps":["Mix flour, water, egg into thin batter","Add sliced scallion, minari, and mixed seafood","Pour into oiled pan and spread evenly","Fry on medium-high until golden, flip and press"],
          "steps_ko":["밀가루, 물, 달걀로 반죽을 만든다","파, 미나리, 해물을 넣는다","기름 두른 팬에 얇게 펴 굽는다","중강불에서 노릇하게 굽고 뒤집는다"]},
     ]},
    {"id":"pumpkin","icon":"🎃","name":"Korean Pumpkin (Hobak)","name_ko":"늙은 호박(단호박)",
     "short":"Sweet Korean pumpkin rich in beta-carotene","short_ko":"베타카로틴 풍부한 단호박",
     "badge":"Vitamin A","badge_ko":"비타민A","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"Korean pumpkin (dan hobak) is sweeter and denser than regular pumpkin. Rich in beta-carotene, vitamin C, and potassium.",
     "description_ko":"단호박은 일반 호박보다 달고 쫀쫀해요. 베타카로틴, 비타민 C, 칼륨이 풍부해요.",
     "effects":["Eye health","Immunity","Blood pressure","Antioxidant","Satiety"],
     "effects_ko":["눈 건강","면역력","혈압 조절","항산화","포만감"],
     "nutrition":{"Calories":"45kcal","Protein":"1.4g","Fiber":"1.5g","Carbs":"11.7g","Fat":"0.1g","Beta-carotene":"1.6mg"},
     "recipes":[
         {"title":"Danhobakmukum (Braised Pumpkin)","title_ko":"단호박찜","time":"25 min","kcal":"130kcal","difficulty":"Easy",
          "steps":["Cut dan hobak into wedges, remove seeds","Steam 15 min until fork-tender","Optionally glaze with honey and butter in pan","Sprinkle with black sesame seeds and serve"],
          "steps_ko":["단호박을 8등분하여 씨를 제거한다","찜기에 15분 쪄서 부드럽게 만든다","꿀, 버터로 팬에서 글레이즈해도 좋다","흑임자를 뿌려 낸다"]},
         {"title":"Pumpkin Porridge","title_ko":"호박죽","time":"30 min","kcal":"190kcal","difficulty":"Easy",
          "steps":["Steam or boil pumpkin until very soft, blend smooth","Mix in glutinous rice flour with water to make paste","Cook pumpkin puree with rice flour paste, stirring constantly","Add sweet rice dumplings, season with salt and sugar"],
          "steps_ko":["단호박을 삶아 곱게 간다","찹쌀가루를 물로 개어준다","호박 퓨레에 찹쌀가루 물을 넣고 저으며 끓인다","새알심을 넣고 소금, 설탕으로 간한다"]},
     ]},
    {"id":"lotus_root","icon":"🪷","name":"Lotus Root","name_ko":"연근",
     "short":"Crunchy Korean root with iron and vitamin C","short_ko":"아삭한 철분·비타민C 뿌리채소",
     "badge":"Iron","badge_ko":"철분","category":"Korean Vegetable","category_ko":"한국 채소",
     "description":"Lotus root has a distinctive crunchy texture and beautiful cross-section. Rich in vitamin C, iron, and mucin that protects the stomach.",
     "description_ko":"독특한 아삭함과 아름다운 단면이 특징이에요. 비타민 C, 철분, 위를 보호하는 뮤신이 풍부해요.",
     "effects":["Iron supplement","Stomach protection","Immunity","Antioxidant","Digestion"],
     "effects_ko":["철분 보충","위 보호","면역력","항산화","소화 개선"],
     "nutrition":{"Calories":"74kcal","Protein":"2.6g","Fiber":"3.1g","Carbs":"17.2g","Fat":"0.1g","Vitamin C":"44mg"},
     "recipes":[
         {"title":"Yeongeun Jorim (Braised Lotus Root)","title_ko":"연근조림","time":"25 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Peel lotus root, slice 0.5cm thick, soak in vinegar water 5 min","Blanch briefly, then stir-fry in oil","Add soy sauce, sugar, corn syrup, and water; braise 15 min","Finish with sesame oil and sesame seeds"],
          "steps_ko":["연근을 0.5cm로 썰어 식초물에 5분 담근다","살짝 데쳐 팬에서 볶는다","간장, 설탕, 물엿, 물을 넣고 15분 조린다","참기름과 깨로 마무리한다"]},
         {"title":"Lotus Root Chips","title_ko":"연근칩","time":"30 min","kcal":"140kcal","difficulty":"Easy",
          "steps":["Slice lotus root paper-thin with mandoline","Soak in vinegar water, pat completely dry","Toss with olive oil and salt","Bake at 180°C for 20–25 min until crispy"],
          "steps_ko":["연근을 최대한 얇게 슬라이스한다","식초물에 담근 뒤 완전히 말린다","올리브오일과 소금으로 버무린다","180도에서 20~25분 바삭하게 굽는다"]},
     ]},
    {"id":"gochujang","icon":"🌶️","name":"Gochujang","name_ko":"고추장",
     "short":"Fermented Korean chili paste","short_ko":"발효 한국 고추장",
     "badge":"Capsaicin","badge_ko":"캡사이신","category":"Fermented","category_ko":"발효식품",
     "description":"Korea's iconic fermented chili paste combining heat, sweetness, and umami. Capsaicin boosts metabolism and has anti-inflammatory effects.",
     "description_ko":"매운맛, 단맛, 감칠맛이 어우러진 한국의 대표 발효 양념이에요. 캡사이신이 신진대사를 높이고 항염증 효과를 내요.",
     "effects":["Metabolism boost","Anti-inflammatory","Antioxidant","Gut health","Pain relief"],
     "effects_ko":["신진대사 촉진","항염증","항산화","장 건강","진통 효과"],
     "nutrition":{"Calories":"176kcal","Protein":"5.8g","Fiber":"5.2g","Carbs":"35.1g","Fat":"2.1g","Capsaicin":"Present"},
     "recipes":[
         {"title":"Bibimbap Sauce","title_ko":"비빔밥 고추장 소스","time":"5 min","kcal":"60kcal","difficulty":"Easy",
          "steps":["Mix 2 tbsp gochujang with 1 tbsp sesame oil","Add 1 tsp sugar, 1 tsp garlic, 1 tsp sesame seeds","Add a splash of water to loosen","Adjust heat and sweetness to taste"],
          "steps_ko":["고추장 2큰술에 참기름 1큰술을 섞는다","설탕 1작은술, 마늘 1작은술, 깨를 넣는다","물을 조금 넣어 농도를 조절한다","맛을 보며 간을 맞춘다"]},
         {"title":"Dakgalbi (Spicy Stir-Fried Chicken)","title_ko":"닭갈비","time":"30 min","kcal":"380kcal","difficulty":"Medium",
          "steps":["Make sauce: gochujang, soy sauce, sesame oil, garlic, ginger, sugar","Marinate chicken pieces 30 min","Stir-fry with cabbage, sweet potato, scallions over high heat","Cook until chicken is done and sauce is thick and glossy"],
          "steps_ko":["고추장, 간장, 참기름, 마늘, 생강, 설탕으로 양념을 만든다","닭고기를 30분 재운다","양배추, 고구마, 파와 함께 강불에서 볶는다","닭이 익고 소스가 걸쭉해질 때까지 볶는다"]},
     ]},
    {"id":"anchovy","icon":"🐟","name":"Dried Anchovy","name_ko":"멸치",
     "short":"Korean broth staple packed with calcium","short_ko":"칼슘 풍부한 한국 국물 재료",
     "badge":"Calcium","badge_ko":"칼슘","category":"Seafood","category_ko":"해산물",
     "description":"Dried anchovies are the backbone of Korean broth making. Exceptionally rich in calcium, omega-3, and vitamin D.",
     "description_ko":"한국 육수의 핵심 재료예요. 칼슘, 오메가-3, 비타민 D가 매우 풍부해요.",
     "effects":["Bone strength","Brain health","Heart health","Omega-3","Immunity"],
     "effects_ko":["뼈 강화","뇌 건강","심장 건강","오메가-3","면역력"],
     "nutrition":{"Calories":"310kcal","Protein":"55.0g","Fiber":"0g","Carbs":"0.7g","Fat":"9.6g","Calcium":"1,905mg"},
     "recipes":[
         {"title":"Myeolchi Bokkeum (Stir-Fried Anchovies)","title_ko":"멸치볶음","time":"12 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Dry-toast small anchovies in pan until lightly crispy","Add a splash of oil, soy sauce, sugar, corn syrup, garlic","Stir-fry 3–4 min until glossy and caramelised","Finish with sesame oil and sesame seeds"],
          "steps_ko":["잔멸치를 기름 없이 볶아 바삭하게 만든다","기름, 간장, 설탕, 물엿, 마늘을 넣는다","3~4분 볶아 윤기나게 한다","참기름과 깨로 마무리한다"]},
         {"title":"Korean Anchovy Broth","title_ko":"멸치 육수","time":"15 min","kcal":"20kcal","difficulty":"Easy",
          "steps":["Remove innards from large dried anchovies (reduces bitterness)","Add anchovies and kelp to cold water","Bring to boil, remove kelp, simmer 10 min","Strain and use as base for soups and jjigae"],
          "steps_ko":["큰 멸치의 내장을 제거한다 (쓴맛 감소)","멸치와 다시마를 찬물에 넣는다","끓으면 다시마를 건지고 10분 끓인다","체에 걸러 국, 찌개 육수로 활용한다"]},
     ]},

    # ── 글로벌 슈퍼푸드 추가 ────────────────────────────────────────
    {"id":"banana","icon":"🍌","name":"Banana","name_ko":"바나나",
     "short":"Instant energy and potassium","short_ko":"즉각적인 에너지와 칼륨",
     "badge":"Post-Workout","badge_ko":"운동 후 간식","category":"Fruit","category_ko":"과일",
     "description":"Fast-digesting carbohydrates for instant energy. Rich in potassium to prevent muscle cramps and vitamin B6 for mood.",
     "description_ko":"빠르게 소화되는 탄수화물이 즉각적인 에너지를 제공해요. 근육 경련을 예방하는 칼륨과 기분을 개선하는 비타민 B6이 풍부해요.",
     "effects":["Energy boost","Muscle cramp prevention","Mood lift","Digestion","Blood pressure control"],
     "effects_ko":["에너지 보충","근육 경련 예방","기분 개선","소화 개선","혈압 조절"],
     "nutrition":{"Calories":"89kcal","Protein":"1.1g","Fiber":"2.6g","Carbs":"23.0g","Fat":"0.3g","Potassium":"358mg"},
     "recipes":[
         {"title":"2-Ingredient Banana Pancakes","title_ko":"바나나 팬케이크 (2가지 재료)","time":"15 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Mash 1 very ripe banana until smooth","Beat in 2 eggs and stir together","Cook tablespoon-sized portions in lightly oiled pan over low heat","Flip when edges look set; serve with maple syrup and fruit"],
          "steps_ko":["잘 익은 바나나 1개를 곱게 으깬다","달걀 2개를 넣어 섞는다","약불에서 한 큰술씩 부어 굽는다","메이플시럽과 과일을 곁들인다"]},
         {"title":"Banana Peanut Butter Smoothie","title_ko":"바나나 땅콩버터 스무디","time":"5 min","kcal":"310kcal","difficulty":"Easy",
          "steps":["Add 1 frozen banana, 1 tbsp peanut butter, 1 cup almond milk to blender","Add a drizzle of honey and pinch of cinnamon","Blend until completely smooth","Pour into glass and enjoy immediately"],
          "steps_ko":["냉동 바나나, 땅콩버터 1큰술, 아몬드밀크 1컵을 블렌더에 넣는다","꿀과 시나몬을 넣는다","곱게 간다","바로 마신다"]},
     ]},
    {"id":"kiwi","icon":"🥝","name":"Kiwi","name_ko":"키위",
     "short":"More vitamin C than an orange","short_ko":"오렌지보다 비타민C가 많은 과일",
     "badge":"Vitamin C King","badge_ko":"비타민C 챔피언","category":"Fruit","category_ko":"과일",
     "description":"Kiwi contains nearly double the vitamin C of an orange by weight. Studies show eating 2 kiwis before bed improves sleep quality.",
     "description_ko":"무게 대비 비타민 C 함량이 오렌지의 약 2배예요. 자기 전에 키위 2개를 먹으면 수면의 질이 향상된다는 연구가 있어요.",
     "effects":["Immunity boost","Better sleep","Digestive enzymes","Blood clotting","Skin health"],
     "effects_ko":["면역 강화","수면 개선","소화 효소","혈액 응고","피부 건강"],
     "nutrition":{"Calories":"61kcal","Protein":"1.1g","Fiber":"3.0g","Carbs":"14.7g","Fat":"0.5g","Vitamin C":"92.7mg"},
     "recipes":[
         {"title":"Kiwi Green Smoothie","title_ko":"키위 그린 스무디","time":"5 min","kcal":"160kcal","difficulty":"Easy",
          "steps":["Peel and halve 2 kiwis","Add with 1 banana, handful spinach to blender","Add coconut water and lime juice","Blend until smooth and bright green"],
          "steps_ko":["키위 2개를 껍질을 벗겨 반으로 자른다","바나나 1개, 시금치 한 줌과 함께 블렌더에 넣는다","코코넛워터와 라임즙을 넣는다","곱게 갈아준다"]},
         {"title":"Kiwi Fruit Salad","title_ko":"키위 과일 샐러드","time":"10 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Slice kiwi, strawberries, mango, and pineapple","Combine in bowl","Add fresh lime juice and a pinch of chili powder","Garnish with fresh mint"],
          "steps_ko":["키위, 딸기, 망고, 파인애플을 썬다","볼에 담는다","라임즙과 고춧가루 한 꼬집을 넣는다","민트로 장식한다"]},
     ]},
    {"id":"chickpea","icon":"🟡","name":"Chickpea","name_ko":"병아리콩",
     "short":"Protein and fibre-rich legume","short_ko":"단백질·식이섬유 풍부한 콩",
     "badge":"Vegan Protein","badge_ko":"식물성단백질","category":"Legumes","category_ko":"콩류",
     "description":"Chickpeas are high in protein and dietary fibre with a low glycaemic index. The base of hummus and a global staple.",
     "description_ko":"단백질과 식이섬유가 풍부하고 혈당 지수가 낮아요. 훔무스의 기본 재료이자 전 세계적인 주식이에요.",
     "effects":["Blood sugar control","Digestion","Muscle synthesis","Satiety","Energy metabolism"],
     "effects_ko":["혈당 조절","소화 개선","근육 합성","포만감","에너지 대사"],
     "nutrition":{"Calories":"164kcal","Protein":"8.9g","Fiber":"7.6g","Carbs":"27.4g","Fat":"2.6g","Iron":"2.9mg"},
     "recipes":[
         {"title":"Hummus","title_ko":"훔무스","time":"10 min","kcal":"180kcal","difficulty":"Easy",
          "steps":["Blend cooked chickpeas, tahini, garlic, lemon juice, olive oil until smooth","Add ice water 1 tbsp at a time for ultra-creamy texture","Season with salt and cumin","Top with olive oil, paprika, and fresh parsley"],
          "steps_ko":["삶은 병아리콩, 타히니, 마늘, 레몬즙, 올리브오일을 곱게 간다","얼음물을 1큰술씩 넣어 크리미하게 만든다","소금과 큐민으로 간한다","올리브오일, 파프리카, 파슬리를 올린다"]},
         {"title":"Roasted Chickpea Salad","title_ko":"구운 병아리콩 샐러드","time":"30 min","kcal":"310kcal","difficulty":"Easy",
          "steps":["Toss drained chickpeas with olive oil, cumin, smoked paprika, salt","Roast at 200°C for 25 min until crispy","Combine with arugula, cherry tomatoes, cucumber","Dress with lemon juice, olive oil, and season to taste"],
          "steps_ko":["병아리콩에 올리브오일, 큐민, 파프리카, 소금을 버무린다","200도에서 25분 바삭하게 굽는다","루꼴라, 방울토마토, 오이와 섞는다","레몬 드레싱으로 마무리한다"]},
     ]},
    {"id":"edamame","icon":"🫛","name":"Edamame","name_ko":"에다마메",
     "short":"Complete protein young soybeans","short_ko":"완전단백질 풋콩",
     "badge":"Plant Protein","badge_ko":"식물성단백질","category":"Legumes","category_ko":"콩류",
     "description":"Young soybeans with all essential amino acids. Rich in isoflavones supporting heart and bone health.",
     "description_ko":"필수아미노산을 모두 함유한 몇 안 되는 식물성 식품이에요. 심장과 뼈 건강에 좋은 이소플라본이 풍부해요.",
     "effects":["Complete protein","Bone health","Heart health","Blood sugar control","Antioxidant"],
     "effects_ko":["완전단백질","뼈 건강","심장 건강","혈당 조절","항산화"],
     "nutrition":{"Calories":"121kcal","Protein":"11.9g","Fiber":"5.2g","Carbs":"8.9g","Fat":"5.2g","Iron":"2.3mg"},
     "recipes":[
         {"title":"Salted Edamame","title_ko":"소금 에다마메","time":"8 min","kcal":"120kcal","difficulty":"Easy",
          "steps":["Boil edamame pods in heavily salted water 4–5 min","Drain and immediately toss with flaky sea salt","Optional: add sesame oil and chili flakes","Eat by squeezing pods directly into mouth"],
          "steps_ko":["에다마메를 소금물에 4~5분 삶는다","건져서 굵은 소금과 버무린다","참기름과 고추 플레이크를 넣어도 좋다","꼬투리를 눌러 콩을 빼 먹는다"]},
         {"title":"Edamame Hummus","title_ko":"에다마메 훔무스","time":"10 min","kcal":"160kcal","difficulty":"Easy",
          "steps":["Blend shelled edamame with garlic, lemon juice, tahini, olive oil","Add water to reach smooth creamy consistency","Season with salt and white pepper","Drizzle olive oil and sprinkle sesame seeds to serve"],
          "steps_ko":["껍질 깐 에다마메, 마늘, 레몬즙, 타히니, 올리브오일을 간다","물을 넣어 크리미한 농도로 만든다","소금과 흰 후추로 간한다","올리브오일과 참깨를 뿌려 낸다"]},
     ]},
]

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def do_search(q, items):
    q = q.strip().lower()
    if not q: return []
    return [i for i in items if
            q in i["name"].lower() or
            q in i.get("name_ko","").lower() or
            q in i.get("name_en","").lower() or
            q in i["short"].lower() or
            q in i.get("short_ko","").lower() or
            q in i["category"].lower() or
            q in i.get("category_ko","").lower() or
            any(q in e.lower() for e in i["effects"]) or
            any(q in e.lower() for e in i.get("effects_ko",[]))]

def do_search_recipe(q, items):
    q = q.strip().lower()
    if not q: return []
    out = []
    for ing in items:
        for rec in ing["recipes"]:
            if (q in rec["title"].lower() or
                q in rec.get("title_ko","").lower() or
                q in ing["name"].lower() or
                q in ing.get("name_ko","").lower()):
                out.append((ing, rec))
    return out

def render_detail(ing):
    lang = st.session_state.lang
    effects = ing.get("effects_ko", ing["effects"]) if lang=="ko" else ing["effects"]
    desc = ing.get("description_ko", ing["description"]) if lang=="ko" else ing["description"]
    name_d = ing.get("name_ko", ing["name"]) if lang=="ko" else ing["name"]
    eff_html = "".join(f'<span class="eff">{e}</span>' for e in effects)
    nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in ing["nutrition"].items())
    st.markdown(f"""<div class="detail-box">
        <div class="d-title">{ing['icon']} {name_d}</div>
        <div class="d-desc">{desc}</div>
        <div class="d-lbl">{t('key_benefits')}</div><div class="effects">{eff_html}</div>
        <div class="d-lbl">{t('nutrition')}</div><div class="nut-grid">{nut_html}</div>
    </div>""", unsafe_allow_html=True)

def render_recipe(ing, rec):
    lang = st.session_state.lang
    title = rec.get("title_ko", rec["title"]) if lang=="ko" else rec["title"]
    steps = rec.get("steps_ko", rec["steps"]) if lang=="ko" else rec["steps"]
    ing_name = ing.get("name_ko", ing["name"]) if lang=="ko" else ing["name"]
    diff = t("difficulty", rec["difficulty"])
    dc = {"Easy":"#2C5F21","Medium":"#7A5C00","Hard":"#8B0000"}.get(rec["difficulty"],"#555")
    steps_html = "".join(f'<div class="r-step"><span class="r-num">{j+1}</span><span>{s}</span></div>' for j,s in enumerate(steps))
    st.markdown(f"""<div class="recipe-card">
        <div class="r-title">{title}</div>
        <div class="r-meta">
            <span>⏱ {rec['time']}</span><span>🔥 {rec['kcal']}</span>
            <span>🌿 {ing_name}</span>
            <span style="color:{dc};font-weight:500;">● {diff}</span>
        </div>{steps_html}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════════════════
st.set_page_config(page_title="Nourish", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,header,footer{visibility:hidden;}
.stApp{background:#F7F5F0;}
.nav{display:flex;align-items:center;justify-content:space-between;padding:14px 0 10px;border-bottom:1px solid #E2DDD4;margin-bottom:24px;}
.nav-logo{font-family:'DM Serif Display',serif;font-size:22px;color:#2C3A1E;display:flex;align-items:center;gap:8px;}
.nav-dot{width:9px;height:9px;border-radius:50%;background:#4A7C3F;display:inline-block;}
.nav-tag{font-size:11px;color:#6B7A60;font-style:italic;}
.hero-wrap{position:relative;border-radius:18px;overflow:hidden;margin-bottom:28px;}
.hero-img{width:100%;height:320px;object-fit:cover;display:block;filter:brightness(0.52);}
.hero-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;width:90%;}
.hero-eye{color:#A8D5A2;font-size:11px;font-weight:500;letter-spacing:.15em;margin-bottom:8px;}
.hero-title{font-family:'DM Serif Display',serif;font-size:38px;color:#fff;line-height:1.2;margin-bottom:10px;}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.85);line-height:1.65;}
.stat-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.25);border-radius:99px;padding:6px 16px;color:#fff;font-size:13px;font-weight:500;margin:4px;}
.stat-num{font-family:'DM Serif Display',serif;font-size:20px;color:#A8D5A2;}
.sec-title{font-family:'DM Serif Display',serif;font-size:20px;color:#2C3A1E;margin-bottom:4px;}
.sec-sub{font-size:12px;color:#7A8A70;margin-bottom:16px;}
.ingr-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:20px 14px;text-align:center;}
.i-icon{font-size:36px;margin-bottom:8px;}
.i-name{font-weight:500;font-size:14px;color:#2C3A1E;margin-bottom:3px;}
.i-short{font-size:11px;color:#7A8A70;line-height:1.4;margin-bottom:7px;}
.i-badge{display:inline-block;font-size:10px;font-weight:500;padding:2px 9px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}
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
.d-lbl{font-size:10px;font-weight:500;letter-spacing:.07em;color:#7A8A70;margin-bottom:5px;margin-top:10px;}
.effects{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:4px;}
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
.divider{height:1px;background:#E2DDD4;margin:22px 0;}
.empty{text-align:center;padding:36px;background:#fff;border:1.5px dashed #D8D3C8;border-radius:14px;color:#7A8A70;font-size:13px;line-height:1.8;}
.lang-box{background:#fff;border:1.5px solid #E2DDD4;border-radius:10px;padding:6px 14px;display:inline-flex;align-items:center;gap:8px;cursor:pointer;}
.stButton>button{background:#2C3A1E!important;color:#F0F7EB!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;padding:8px 16px!important;}
.stButton>button:hover{background:#4A7C3F!important;}
.stTextInput>div>div>input{border:1.5px solid #D8D3C8!important;border-radius:8px!important;background:#fff!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;color:#2C3A1E!important;}
.stTextInput>div>div>input:focus{border-color:#4A7C3F!important;box-shadow:0 0 0 3px rgba(74,124,63,.12)!important;}
.stTextInput label,.stSelectbox label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;color:#5A6A50!important;padding:8px 16px!important;border-radius:8px!important;}
.stTabs [aria-selected="true"]{background:#EEF5E9!important;color:#2C3A1E!important;}
</style>""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────
for k, v in [("lang","ko"),("detail_id",None),("s_results",[]),("s_done",False),("r_search","")]:
    if k not in st.session_state:
        st.session_state[k] = v

total_recipes = sum(len(i["recipes"]) for i in INGREDIENTS)
total_ingr = len(INGREDIENTS)

# ── Nav ────────────────────────────────────────────────────────────
nc1, nc2 = st.columns([8, 2])
with nc1:
    tagline = "건강한 식재료, 정직한 레시피" if st.session_state.lang=="ko" else "wholesome ingredients, honest recipes"
    st.markdown(f'<div class="nav"><div class="nav-logo"><span class="nav-dot"></span>Nourish</div><div class="nav-tag">{tagline}</div></div>', unsafe_allow_html=True)
with nc2:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    if st.session_state.lang == "ko":
        if st.button("🇺🇸 English", use_container_width=True, key="lang_toggle"):
            st.session_state.lang = "en"; st.rerun()
    else:
        if st.button("🇰🇷 한국어", use_container_width=True, key="lang_toggle"):
            st.session_state.lang = "ko"; st.rerun()

# ── Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([t("tab1"), t("tab2"), t("tab3")])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════
with tab1:
    hero_title = t("hero_title")
    hero_sub   = t("hero_sub")
    stats_ingr = t("stats_ingr")
    stats_rec  = t("stats_recipe")

    st.markdown(f"""
    <div class="hero-wrap">
        <img class="hero-img"
             src="https://images.unsplash.com/photo-1601758124510-52d02ddb7cbd?w=1400&q=80"
             onerror="this.src='https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1400&q=80'"/>
        <div class="hero-text">
            <p class="hero-eye">🌿 NOURISH · WHOLESOME · HONEST</p>
            <h1 class="hero-title">{hero_title}</h1>
            <p class="hero-sub">{hero_sub}</p>
            <div style="margin-top:18px;">
                <span class="stat-pill"><span class="stat-num">{total_ingr}</span>&nbsp;{stats_ingr}</span>
                <span class="stat-pill"><span class="stat-num">{total_recipes}</span>&nbsp;{stats_rec}</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — INGREDIENTS
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f'<p class="sec-title">{t("featured_title")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sec-sub">{t("featured_sub")}</p>', unsafe_allow_html=True)

    # 6 featured cards
    feat_ings = [i for i in INGREDIENTS if i["id"] in FEATURED]
    cols = st.columns(3)
    for idx, ing in enumerate(feat_ings):
        lang = st.session_state.lang
        name_d  = ing.get("name_ko", ing["name"]) if lang=="ko" else ing["name"]
        short_d = ing.get("short_ko", ing["short"]) if lang=="ko" else ing["short"]
        badge_d = ing.get("badge_ko", ing["badge"]) if lang=="ko" else ing["badge"]
        with cols[idx % 3]:
            st.markdown(f"""<div class="ingr-card">
                <div class="i-icon">{ing['icon']}</div>
                <div class="i-name">{name_d}</div>
                <div class="i-short">{short_d}</div>
                <span class="i-badge">{badge_d}</span>
            </div>""", unsafe_allow_html=True)
            if st.button(name_d, key=f"feat_{ing['id']}", use_container_width=True):
                st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                st.rerun()

    # Detail + recipes for featured
    if st.session_state.detail_id and st.session_state.detail_id in FEATURED:
        d = next((i for i in feat_ings if i["id"] == st.session_state.detail_id), None)
        if d:
            render_detail(d)
            dname = d.get("name_ko", d["name"]) if st.session_state.lang=="ko" else d["name"]
            st.markdown(f'<p style="font-size:13px;font-weight:500;color:#2C3A1E;margin:10px 0 8px;">📋 {t("recipes_for")} {dname}</p>', unsafe_allow_html=True)
            for rec in d["recipes"]:
                render_recipe(d, rec)
            if st.columns([5,1])[1].button(t("close_btn"), key="close_feat", use_container_width=True):
                st.session_state.detail_id = None; st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Search section
    si1, si2 = st.columns([5, 1])
    with si1:
        sq = st.text_input("ingr_sq", placeholder=t("search_placeholder"),
                           label_visibility="collapsed", key="ingr_search_box")
    with si2:
        if st.button(t("search_btn"), use_container_width=True, key="ingr_s_btn"):
            st.session_state.s_results = do_search(sq, INGREDIENTS)
            st.session_state.s_done = True
            st.session_state.detail_id = None

    if st.session_state.s_done:
        results = st.session_state.s_results
        if not results:
            st.warning(f"{t('no_result')} '{sq}'")
        else:
            st.markdown(f'<p class="sec-sub">🔍 {len(results)} result(s)</p>', unsafe_allow_html=True)
            for ing in results:
                lang = st.session_state.lang
                name_d  = ing.get("name_ko", ing["name"]) if lang=="ko" else ing["name"]
                short_d = ing.get("short_ko", ing["short"]) if lang=="ko" else ing["short"]
                badge_d = ing.get("badge_ko", ing["badge"]) if lang=="ko" else ing["badge"]
                cat_d   = ing.get("category_ko", ing["category"]) if lang=="ko" else ing["category"]
                rc1, rc2 = st.columns([7, 1])
                with rc1:
                    st.markdown(f"""<div class="search-card">
                        <span class="search-icon">{ing['icon']}</span>
                        <div class="search-info">
                            <div class="search-name">{name_d}</div>
                            <div class="search-short">{short_d}</div>
                            <div class="search-badges">
                                <span class="s-badge">{badge_d}</span>
                                <span class="s-badge">{cat_d}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with rc2:
                    btn_lbl = "정보" if st.session_state.lang=="ko" else "Info"
                    if st.button(btn_lbl, key=f"si_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                        st.rerun()
                if st.session_state.detail_id == ing["id"]:
                    render_detail(ing)
                    ing_name_d = ing.get("name_ko", ing["name"]) if st.session_state.lang=="ko" else ing["name"]
                    st.markdown(f'<p style="font-size:13px;font-weight:500;color:#2C3A1E;margin:10px 0 8px;">📋 {t("recipes_for")} {ing_name_d}</p>', unsafe_allow_html=True)
                    for rec in ing["recipes"]:
                        render_recipe(ing, rec)
        if st.columns([5,1])[1].button(t("close_btn"), key="close_s", use_container_width=True):
            st.session_state.s_done = False
            st.session_state.s_results = []
            st.session_state.detail_id = None
            st.rerun()

# ══════════════════════════════════════════════════════════════════
# TAB 3 — RECIPES
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f'<p class="sec-title">{t("recipe_title")}</p>', unsafe_allow_html=True)

    rs1, rs2 = st.columns([5, 1])
    with rs1:
        rq = st.text_input("rq", placeholder=t("recipe_search_ph"),
                           label_visibility="collapsed", key="r_search_box")
    with rs2:
        if st.button(t("search_btn"), key="r_s_btn", use_container_width=True):
            st.session_state.r_search = rq.strip()

    if st.session_state.r_search:
        r_results = do_search_recipe(st.session_state.r_search, INGREDIENTS)
        st.markdown(f'<p class="sec-sub">🔍 {len(r_results)} recipe(s)</p>', unsafe_allow_html=True)
        if not r_results:
            st.warning(f"No recipes found for '{st.session_state.r_search}'")
        for ing, rec in r_results:
            render_recipe(ing, rec)
        if st.columns([5,1])[1].button(t("close_btn"), key="close_r", use_container_width=True):
            st.session_state.r_search = ""; st.rerun()
    else:
        # Dropdown
        lang = st.session_state.lang
        all_labels = []
        for ing in INGREDIENTS:
            for rec in ing["recipes"]:
                title_d   = rec.get("title_ko", rec["title"]) if lang=="ko" else rec["title"]
                ing_name_d = ing.get("name_ko", ing["name"]) if lang=="ko" else ing["name"]
                label = f"{ing['icon']} {title_d} ({ing_name_d})"
                all_labels.append((label, ing, rec))
        all_labels.sort(key=lambda x: x[0])

        sel = st.selectbox(t("select_recipe"),
                           options=[t("select_recipe")] + [l for l,_,_ in all_labels],
                           label_visibility="collapsed")
        if sel != t("select_recipe"):
            for label, ing, rec in all_labels:
                if label == sel:
                    render_recipe(ing, rec)
                    break
        else:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f'<p class="sec-sub">{"First 12 recipes — search or use dropdown for more" if lang=="en" else "처음 12개 레시피 — 검색이나 드롭다운으로 더 보기"}</p>', unsafe_allow_html=True)
            rcols = st.columns(2)
            count = 0
            for ing in INGREDIENTS:
                for rec in ing["recipes"]:
                    if count >= 12: break
                    with rcols[count % 2]:
                        render_recipe(ing, rec)
                    count += 1
                if count >= 12: break

footer_tag = "건강한 식재료, 정직한 레시피" if st.session_state.lang=="ko" else "wholesome ingredients, honest recipes"
st.markdown(f'<div style="margin-top:48px;padding:14px 0;border-top:1px solid #E2DDD4;text-align:center;font-size:11px;color:#7A8A70;">Nourish · {footer_tag} · SKKU Art Project</div>', unsafe_allow_html=True)
# This will be replaced - just checking append works
