import streamlit as st
import base64
import json
import os
from datetime import datetime
from pathlib import Path

APP_NAME    = "Nourish"
APP_TAGLINE = "wholesome ingredients, honest recipes"

# ── Persistent storage path ───────────────────────────────────────────────
DATA_DIR   = Path("nourish_data")
POSTS_FILE = DATA_DIR / "community_posts.json"
DATA_DIR.mkdir(exist_ok=True)

def load_posts():
    if POSTS_FILE.exists():
        try:
            return json.loads(POSTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_posts(posts):
    POSTS_FILE.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")

st.set_page_config(page_title=APP_NAME, page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,header,footer{visibility:hidden;}
.stApp{background:#F7F5F0;}

.nav{display:flex;align-items:center;justify-content:space-between;padding:16px 0 12px;border-bottom:1px solid #E2DDD4;margin-bottom:32px;}
.nav-logo{font-family:'DM Serif Display',serif;font-size:22px;color:#2C3A1E;display:flex;align-items:center;gap:8px;}
.nav-dot{width:9px;height:9px;border-radius:50%;background:#4A7C3F;display:inline-block;}
.nav-tag{font-size:11px;color:#6B7A60;font-style:italic;}

.hero{background:#EEF0E8;border-radius:14px;padding:40px 36px;margin-bottom:36px;border:1px solid #DDE0D4;}
.hero *{color:#2C3A1E!important;}
.hero .hero-eye{color:#4A7C3F!important;font-size:11px;font-weight:500;letter-spacing:.1em;}
.hero .hero-sub{color:#5A6A50!important;font-size:14px;line-height:1.65;}
.hero-title{font-family:'DM Serif Display',serif;font-size:34px;line-height:1.25;margin-bottom:8px;}

.sec-title{font-family:'DM Serif Display',serif;font-size:20px;color:#2C3A1E;margin-bottom:4px;}
.sec-sub{font-size:12px;color:#7A8A70;margin-bottom:18px;}

.ingr-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:22px 16px;text-align:center;}
.ingr-card.sel{border-color:#2C3A1E;background:#F0F7EB;}
.i-icon{font-size:32px;margin-bottom:10px;}
.i-name{font-weight:500;font-size:15px;color:#2C3A1E;margin-bottom:4px;}
.i-short{font-size:12px;color:#7A8A70;line-height:1.4;margin-bottom:8px;}
.i-badge{display:inline-block;font-size:10px;font-weight:500;padding:3px 10px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}

.search-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:20px;margin-bottom:12px;display:flex;align-items:center;gap:16px;}
.search-icon{font-size:36px;flex-shrink:0;}
.search-info{flex:1;}
.search-name{font-weight:500;font-size:16px;color:#2C3A1E;margin-bottom:3px;}
.search-short{font-size:12px;color:#7A8A70;margin-bottom:6px;}
.search-badges{display:flex;gap:6px;flex-wrap:wrap;}
.s-badge{font-size:10px;font-weight:500;padding:2px 9px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}

.detail-box{background:#F0F7EB;border:1.5px solid #C5DDB8;border-radius:14px;padding:24px;margin-bottom:16px;}
.d-title{font-family:'DM Serif Display',serif;font-size:20px;color:#2C3A1E;margin-bottom:6px;}
.d-desc{font-size:13px;color:#4A5A40;line-height:1.75;margin-bottom:14px;}
.d-lbl{font-size:10px;font-weight:500;letter-spacing:.07em;color:#7A8A70;margin-bottom:6px;}
.effects{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;}
.eff{font-size:11px;padding:3px 10px;border-radius:99px;background:#fff;color:#4A5A40;border:1px solid #D8D3C8;}
.nut-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.nut-item{background:#fff;border-radius:8px;padding:10px;text-align:center;border:1px solid #E2DDD4;}
.nut-val{font-size:15px;font-weight:500;color:#2C3A1E;}
.nut-lbl{font-size:10px;color:#7A8A70;margin-top:2px;}

.recipe-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:22px;margin-bottom:14px;}
.r-title{font-family:'DM Serif Display',serif;font-size:18px;color:#2C3A1E;margin-bottom:6px;}
.r-meta{display:flex;gap:14px;font-size:12px;color:#7A8A70;margin-bottom:14px;}
.r-step{display:flex;gap:10px;padding:8px 0;border-top:1px solid #F0ECE4;font-size:13px;color:#4A5A40;line-height:1.6;align-items:flex-start;}
.r-step:first-child{border-top:none;}
.r-num{min-width:20px;height:20px;border-radius:50%;background:#4A7C3F;color:#fff;font-size:10px;font-weight:500;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}

.upload-box{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:28px;margin-bottom:28px;}
.upload-title{font-family:'DM Serif Display',serif;font-size:18px;color:#2C3A1E;margin-bottom:4px;}
.upload-sub{font-size:12px;color:#7A8A70;margin-bottom:20px;}
.photo-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;overflow:hidden;margin-bottom:16px;}
.photo-img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;}
.photo-body{padding:14px 16px;}
.photo-user{font-size:13px;font-weight:500;color:#2C3A1E;margin-bottom:3px;}
.photo-recipe{font-size:12px;color:#4A7C3F;font-weight:500;margin-bottom:6px;}
.photo-note{font-size:12px;color:#5A6A50;line-height:1.6;}
.photo-time{font-size:11px;color:#9A9A90;margin-top:8px;}
.no-posts{text-align:center;padding:60px 20px;background:#fff;border:1.5px dashed #D8D3C8;border-radius:14px;}
.no-posts-icon{font-size:40px;margin-bottom:12px;}
.no-posts-text{font-size:14px;color:#7A8A70;line-height:1.6;}

.divider{height:1px;background:#E2DDD4;margin:28px 0;}
.sel-chip{display:inline-flex;align-items:center;gap:4px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;border-radius:99px;padding:4px 12px;font-size:12px;font-weight:500;margin:3px;}
.empty{text-align:center;padding:48px;background:#fff;border:1.5px dashed #D8D3C8;border-radius:14px;color:#7A8A70;font-size:13px;line-height:1.8;}

.stButton>button{background:#2C3A1E!important;color:#F0F7EB!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;padding:8px 16px!important;}
.stButton>button:hover{background:#4A7C3F!important;}
.stTextInput>div>div>input,.stTextArea textarea{border:1.5px solid #D8D3C8!important;border-radius:8px!important;background:#fff!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;color:#2C3A1E!important;}
.stTextInput>div>div>input:focus,.stTextArea textarea:focus{border-color:#4A7C3F!important;box-shadow:0 0 0 3px rgba(74,124,63,.12)!important;}
.stTextInput label,.stTextArea label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stFileUploader label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stFileUploader>div{border:1.5px dashed #C5DDB8!important;border-radius:8px!important;background:#F0F7EB!important;}
.stTabs [data-baseweb="tab-list"]{gap:8px;}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;color:#5A6A50!important;padding:8px 20px!important;border-radius:8px!important;}
.stTabs [aria-selected="true"]{background:#EEF5E9!important;color:#2C3A1E!important;}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# DATA — 5 recipes per ingredient
# ════════════════════════════════════════════════════════════════════
FEATURED = ["quinoa","avocado","salmon","tofu","blueberry","lentil"]

INGREDIENTS = [
    {"id":"quinoa","icon":"🌾","name":"Quinoa","name_en":"quinoa","short":"Complete protein super seed","badge":"Gluten-Free","category":"Whole Grain",
     "description":"Quinoa, native to the Andean mountains of South America, is the only grain that contains all 9 essential amino acids — making it a complete protein. It's naturally gluten-free, ideal for those with wheat allergies.",
     "effects":["Blood sugar control","Muscle recovery","Improved digestion","Satiety","Energy boost"],
     "nutrition":{"Calories":"120kcal","Protein":"4.4g","Fiber":"2.8g","Carbs":"21.3g","Fat":"1.9g","Iron":"1.5mg"},
     "recipes":[
         {"title":"Quinoa Salad Bowl","time":"20 min","kcal":"310kcal","difficulty":"Easy","steps":["Cook 1 cup quinoa in 2 cups water for 15 min, then rest 5 min","Slice cucumber, cherry tomatoes, and red onion","Make a dressing with lemon juice, olive oil, salt, and pepper","Toss quinoa with vegetables and dressing to finish"]},
         {"title":"Quinoa Shrimp Fried Rice","time":"25 min","kcal":"380kcal","difficulty":"Medium","steps":["Cook quinoa ahead and let it cool","Sauté sesame oil, garlic, and shrimp in a pan","Add quinoa and egg, stir-fry over high heat","Season with soy sauce and oyster sauce, top with scallions and sesame"]},
         {"title":"Quinoa Greek Yogurt Breakfast Bowl","time":"10 min","kcal":"270kcal","difficulty":"Easy","steps":["Take pre-cooked quinoa from the fridge","Mix 1:1 with Greek yogurt","Stir in honey and cinnamon","Top with blueberries, sliced almonds, and mint"]},
         {"title":"Quinoa Vegetable Soup","time":"30 min","kcal":"220kcal","difficulty":"Easy","steps":["Sauté onion, carrot, and celery in olive oil","Add 4 cups vegetable broth and quinoa","Simmer on low for 20 minutes","Finish with salt, pepper, and parsley"]},
         {"title":"Quinoa Stuffed Peppers","time":"40 min","kcal":"350kcal","difficulty":"Medium","steps":["Cut tops off peppers and remove seeds","Mix cooked quinoa, black beans, corn, and tomato sauce for filling","Fill peppers with mixture and top with cheese","Bake at 200°C (390°F) for 25 minutes"]},
     ]},
    {"id":"avocado","icon":"🥑","name":"Avocado","name_en":"avocado","short":"Healthy monounsaturated fats","badge":"Vitamin E","category":"Healthy Fats",
     "description":"Known as 'butter of the forest,' avocado boasts a creamy texture and incredible nutrition. It's rich in heart-healthy monounsaturated fatty acids and contains twice the potassium of a banana.",
     "effects":["Heart health","Skin care","Blood pressure control","Nutrient absorption","Anti-inflammatory"],
     "nutrition":{"Calories":"160kcal","Protein":"2.0g","Fiber":"6.7g","Carbs":"8.5g","Fat":"14.7g","Potassium":"485mg"},
     "recipes":[
         {"title":"Avocado Toast","time":"10 min","kcal":"280kcal","difficulty":"Easy","steps":["Toast whole grain bread until golden","Mash avocado with lemon juice, salt, and pepper","Spread generously on toast","Top with a poached egg and chia seeds"]},
         {"title":"Avocado Mentaiko Rice Bowl","time":"15 min","kcal":"420kcal","difficulty":"Easy","steps":["Mix warm rice with sesame oil and soy sauce","Slice avocado and prepare mentaiko (pollock roe)","Top rice with avocado, mentaiko, and egg yolk","Sprinkle seaweed flakes and sesame, then mix to eat"]},
         {"title":"Guacamole","time":"8 min","kcal":"150kcal","difficulty":"Easy","steps":["Mash 2 ripe avocados with a fork","Finely chop tomato, red onion, and cilantro","Add lime juice, salt, and cumin","Serve with tortilla chips"]},
         {"title":"Avocado Chocolate Mousse","time":"15 min","kcal":"240kcal","difficulty":"Easy","steps":["Blend ripe avocado, cocoa powder, and honey","Add a splash of almond milk for creaminess","Add a drop of vanilla extract","Pour into cups and top with raspberries and mint"]},
         {"title":"Avocado Caesar Dressing Pasta","time":"20 min","kcal":"460kcal","difficulty":"Medium","steps":["Make a creamy dressing with avocado, lemon juice, garlic, olive oil, and parmesan","Cook pasta in salted water","Toss warm pasta with the dressing","Top with arugula, cherry tomatoes, and croutons"]},
     ]},
    {"id":"salmon","icon":"🐟","name":"Salmon","name_en":"salmon","short":"High omega-3 fatty fish","badge":"20g Protein","category":"Protein",
     "description":"Salmon is one of the best sources of omega-3 fatty acids. Rich in EPA and DHA, it excels at supporting brain health, cardiovascular health, and reducing inflammation.",
     "effects":["Brain health","Cardiovascular protection","Reduced inflammation","Immunity","Bone strength"],
     "nutrition":{"Calories":"208kcal","Protein":"20.0g","Fiber":"0g","Carbs":"0g","Fat":"13.0g","Omega-3":"2.3g"},
     "recipes":[
         {"title":"Salmon Poke Bowl","time":"15 min","kcal":"450kcal","difficulty":"Easy","steps":["Place brown rice in a bowl","Cube salmon and marinate in soy sauce, sesame oil, and ginger for 5 min","Prepare edamame, cucumber, carrot, and avocado","Arrange over rice and drizzle with sriracha mayo"]},
         {"title":"Herb-Baked Salmon","time":"22 min","kcal":"390kcal","difficulty":"Medium","steps":["Coat salmon with olive oil, garlic, lemon juice, and dill","Bake at 200°C (390°F) for 12 minutes","Roast asparagus alongside","Finish with lemon and parsley"]},
         {"title":"Salmon Avocado Tartare","time":"15 min","kcal":"320kcal","difficulty":"Medium","steps":["Finely dice fresh salmon","Cut avocado into small cubes","Season with soy sauce, sesame oil, lemon juice, and wasabi","Serve on crackers or cucumber slices"]},
         {"title":"Salmon Cream Pasta","time":"25 min","kcal":"520kcal","difficulty":"Medium","steps":["Cook pasta in salted water","Pan-sear salmon in butter, then break into flakes","Add heavy cream, parmesan, and lemon juice for sauce","Add pasta and mix, finish with dill and capers"]},
         {"title":"Salmon Miso Soup","time":"20 min","kcal":"210kcal","difficulty":"Easy","steps":["Make a kombu dashi broth","Dissolve 2 tbsp miso paste","Cut salmon into bite-sized pieces and add","Add tofu, daikon, and scallions, simmer 5 min"]},
     ]},
    {"id":"tofu","icon":"🫘","name":"Tofu","name_en":"tofu","short":"Plant-based complete protein","badge":"Low Calorie","category":"Plant Protein",
     "description":"Tofu is the go-to plant protein made from ground soybeans. Low in calories yet rich in protein — perfect for weight management — and high in calcium for bone health.",
     "effects":["Weight management","Bone strength","Muscle maintenance","Lower cholesterol","Hormone balance"],
     "nutrition":{"Calories":"76kcal","Protein":"8.0g","Fiber":"0.3g","Carbs":"1.9g","Fat":"4.8g","Calcium":"350mg"},
     "recipes":[
         {"title":"Soft Tofu Miso Soup","time":"20 min","kcal":"180kcal","difficulty":"Easy","steps":["Simmer anchovy and kombu broth for 10 minutes","Dissolve 2 tbsp miso, add zucchini and mushrooms","Tear in soft tofu and simmer 5 min","Add green chili and scallions, then turn off heat"]},
         {"title":"Tofu Steak","time":"15 min","kcal":"220kcal","difficulty":"Easy","steps":["Slice tofu 2cm thick and pat dry","Make a sauce with soy sauce, honey, garlic, and sesame oil","Pan-fry both sides 3 min each until golden","Pour sauce over and cook 1 min, top with sesame and scallions"]},
         {"title":"Mapo Tofu","time":"20 min","kcal":"280kcal","difficulty":"Medium","steps":["Stir-fry ground pork in a pan","Add doubanjiang, minced garlic, and ginger","Add tofu and season with broth and soy sauce","Thicken with cornstarch slurry, finish with scallions and Sichuan pepper"]},
         {"title":"Turmeric Tofu Scramble","time":"12 min","kcal":"200kcal","difficulty":"Easy","steps":["Crumble tofu and squeeze out moisture","Sauté olive oil and garlic in a pan","Add tofu, turmeric, cumin, and salt; stir-fry","Fold in spinach and cherry tomatoes to finish"]},
         {"title":"Tofu Caprese Salad","time":"10 min","kcal":"160kcal","difficulty":"Easy","steps":["Slice tofu 1cm thick","Slice tomatoes to the same thickness","Alternate tofu, tomato, and basil layers","Drizzle with olive oil, balsamic, salt, and pepper"]},
     ]},
    {"id":"blueberry","icon":"🫐","name":"Blueberry","name_en":"blueberry","short":"Antioxidant superfood","badge":"Vitamin C","category":"Berries",
     "description":"Blueberries are packed with anthocyanin, a powerful antioxidant pigment. They're especially effective for brain health and memory improvement, and neutralise free radicals to slow aging.",
     "effects":["Antioxidant","Brain health","Anti-aging","Blood sugar control","Eye protection"],
     "nutrition":{"Calories":"57kcal","Protein":"0.7g","Fiber":"2.4g","Carbs":"14.5g","Fat":"0.3g","Vitamin C":"9.7mg"},
     "recipes":[
         {"title":"Blueberry Smoothie Bowl","time":"8 min","kcal":"260kcal","difficulty":"Easy","steps":["Blend frozen blueberries and banana","Add Greek yogurt and blend until thick","Top with granola and chia seeds","Drizzle with honey"]},
         {"title":"Blueberry Cheesecake Mousse","time":"20 min","kcal":"290kcal","difficulty":"Medium","steps":["Whip cream cheese with honey and vanilla","Fold in whipped cream gently","Cook blueberries with lemon juice and sugar into a sauce","Spoon mousse into cups and top with sauce"]},
         {"title":"Blueberry Banana Pancakes","time":"20 min","kcal":"310kcal","difficulty":"Easy","steps":["Mash banana and mix with eggs and oat flour","Fold blueberries into batter","Cook both sides over low heat","Top with maple syrup and fresh blueberries"]},
         {"title":"Blueberry Chia Jam","time":"15 min","kcal":"40kcal","difficulty":"Easy","steps":["Combine blueberries, honey, and lemon juice in a saucepan; bring to a boil","Stir and simmer 10 minutes","Remove from heat and stir in chia seeds","Cool and store in a glass jar in the fridge"]},
         {"title":"Blueberry Yogurt Ice Bars","time":"10 min + 4h freeze","kcal":"90kcal","difficulty":"Easy","steps":["Mix Greek yogurt, honey, and vanilla","Mash blueberries and swirl into yogurt","Pour into ice bar molds and insert sticks","Freeze for at least 4 hours"]},
     ]},
    {"id":"lentil","icon":"🌱","name":"Lentils","name_en":"lentils","short":"Fiber and iron powerhouse","badge":"Vegan","category":"Legumes",
     "description":"One of the world's oldest cultivated crops, lentils are especially rich in protein and iron. Their high fibre content improves gut health and prevents blood sugar spikes.",
     "effects":["Gut health","Blood sugar control","Anaemia prevention","Satiety","Prenatal health"],
     "nutrition":{"Calories":"116kcal","Protein":"9.0g","Fiber":"7.9g","Carbs":"20.1g","Fat":"0.4g","Iron":"3.3mg"},
     "recipes":[
         {"title":"Lentil Soup","time":"35 min","kcal":"290kcal","difficulty":"Easy","steps":["Sauté onion, garlic, and carrot in olive oil","Add lentils, vegetable broth, cumin, and paprika","Simmer on low for 25 minutes","Partially blend with a hand blender; finish with lemon juice"]},
         {"title":"Lentil Curry","time":"30 min","kcal":"350kcal","difficulty":"Medium","steps":["Fry curry paste to release aroma","Add coconut milk and lentils","Simmer on low for 20 minutes","Stir in spinach for 2 min, then serve with rice"]},
         {"title":"Lentil Tacos","time":"25 min","kcal":"320kcal","difficulty":"Easy","steps":["Season lentils with cumin, paprika, and garlic; stir-fry","Warm tortillas","Prepare avocado, tomato, and lettuce","Layer lentils and veggies on tortillas with salsa"]},
         {"title":"Lentil Meatballs","time":"35 min","kcal":"280kcal","difficulty":"Medium","steps":["Combine cooked lentils, oats, garlic, and parsley","Season with salt, pepper, and cumin","Roll into balls and bake at 200°C (390°F) for 20 min","Serve with tomato sauce over pasta or rice"]},
         {"title":"Lentil Stuffed Squash","time":"45 min","kcal":"310kcal","difficulty":"Medium","steps":["Halve small squash and scoop out seeds","Mix lentils, tomato, paprika, and herbs for filling","Fill squash and top with cheese","Bake at 180°C (350°F) for 30 minutes"]},
     ]},
    # ── Search-only ingredients ─────────────────────────────────────────────
    {"id":"spinach","icon":"🥬","name":"Spinach","name_en":"spinach","short":"Green powerhouse of iron and folate","badge":"Low Calorie","category":"Vegetables",
     "description":"Spinach is rich in iron, folate, vitamins K and A, yet extremely low in calories. Lutein protects eye health, and magnesium aids sleep.",
     "effects":["Anaemia prevention","Eye health","Bone strength","Improved digestion","Skin care"],
     "nutrition":{"Calories":"23kcal","Protein":"2.9g","Fiber":"2.2g","Carbs":"3.6g","Fat":"0.4g","Iron":"2.7mg"},
     "recipes":[
         {"title":"Spinach & Egg Stir-Fry","time":"10 min","kcal":"180kcal","difficulty":"Easy","steps":["Wash spinach and pat dry","Sauté garlic in a pan","Stir-fry spinach over high heat","Add eggs, cook to a soft scramble, and season"]},
         {"title":"Spinach Pesto Pasta","time":"20 min","kcal":"380kcal","difficulty":"Medium","steps":["Blend spinach, almonds, garlic, and olive oil into pesto","Cook pasta in salted water","Toss pasta with pesto in the pan","Top with cherry tomatoes and parmesan"]},
         {"title":"Green Spinach Smoothie","time":"5 min","kcal":"130kcal","difficulty":"Easy","steps":["Add a handful of spinach, banana, and almond milk to blender","Add honey and lemon juice","Blend until smooth","Add ice and serve cold"]},
         {"title":"Spinach & Cheese Quiche","time":"40 min","kcal":"320kcal","difficulty":"Medium","steps":["Press pastry into tin and prick with a fork","Sauté spinach and squeeze out moisture","Mix eggs, cream, cheese, and spinach for filling","Pour into pastry and bake at 180°C (350°F) for 30 min"]},
         {"title":"Spinach Miso Soup","time":"15 min","kcal":"80kcal","difficulty":"Easy","steps":["Make anchovy broth","Dissolve miso paste","Add spinach and simmer 2 minutes","Add tofu and scallions to finish"]},
     ]},
    {"id":"sweetpotato","icon":"🍠","name":"Sweet Potato","name_en":"sweet potato","short":"Rich in beta-carotene and fibre","badge":"Vitamin A","category":"Vegetables",
     "description":"Sweet potatoes are loaded with beta-carotene, supporting immunity and eye health. Their glycaemic index is lower than regular potatoes, making them a healthier carb source.",
     "effects":["Immunity boost","Eye protection","Gut health","Blood pressure control","Energy supply"],
     "nutrition":{"Calories":"86kcal","Protein":"1.6g","Fiber":"3.0g","Carbs":"20.1g","Fat":"0.1g","Vitamin A":"961μg"},
     "recipes":[
         {"title":"Sweet Potato Latte","time":"10 min","kcal":"180kcal","difficulty":"Easy","steps":["Steam and mash sweet potato","Stir into warm milk","Add honey and cinnamon","Blend with a hand blender to finish"]},
         {"title":"Sweet Potato Gratin","time":"35 min","kcal":"290kcal","difficulty":"Medium","steps":["Thinly slice sweet potato","Make a cream sauce with heavy cream, garlic, salt, and pepper","Layer sweet potato in a dish and pour cream sauce over","Bake at 180°C (350°F) for 25 min, add cheese, bake 10 min more"]},
         {"title":"Sweet Potato Salad","time":"20 min","kcal":"230kcal","difficulty":"Easy","steps":["Boil sweet potato and cut into bite-sized pieces","Make a dressing with mayo, honey, and lemon juice","Add raisins and almonds","Gently toss sweet potato with dressing"]},
         {"title":"Sweet Potato Curry","time":"30 min","kcal":"310kcal","difficulty":"Easy","steps":["Cube sweet potato","Sauté onion and garlic in olive oil","Add curry powder, coconut milk, and sweet potato","Simmer 20 min and serve with rice"]},
         {"title":"Roasted Sweet Potato Tacos","time":"35 min","kcal":"340kcal","difficulty":"Medium","steps":["Cut sweet potato into wedges; season with olive oil, cumin, and paprika","Roast at 200°C (390°F) for 25 min","Place roasted wedges on tortillas","Add avocado, salsa, and cilantro to finish"]},
     ]},
    {"id":"egg","icon":"🥚","name":"Egg","name_en":"egg","short":"Nature's perfect whole food","badge":"6g Protein","category":"Protein",
     "description":"Eggs are nature's most complete protein source, containing all essential amino acids. The yolk is packed with choline, essential for brain health.",
     "effects":["Muscle synthesis","Brain health","Eye health","Satiety","Energy supply"],
     "nutrition":{"Calories":"155kcal","Protein":"13.0g","Fiber":"0g","Carbs":"1.1g","Fat":"11.0g","Choline":"294mg"},
     "recipes":[
         {"title":"Scrambled Egg Avocado Bowl","time":"10 min","kcal":"320kcal","difficulty":"Easy","steps":["Beat 2 eggs with milk, salt, and pepper","Stir slowly over low heat with butter","Halve an avocado and remove the pit","Spoon scrambled eggs over the avocado"]},
         {"title":"Eggs in Hell","time":"20 min","kcal":"240kcal","difficulty":"Medium","steps":["Sauté olive oil and garlic in a pan","Add tomato sauce and simmer 5 minutes","Create wells in the sauce and crack eggs in","Cover and heat until eggs are set"]},
         {"title":"Egg Frittata","time":"25 min","kcal":"280kcal","difficulty":"Medium","steps":["Beat 4 eggs with salt and pepper","Sauté vegetables in an oven-safe pan","Pour eggs over and cook on low until edges set","Finish in the oven at 180°C (350°F) for 10 min"]},
         {"title":"Egg Gimbap","time":"30 min","kcal":"380kcal","difficulty":"Medium","steps":["Make a thin egg omelette and roll it up","Prepare carrot, spinach, and pickled radish","Season rice with sesame oil and salt","Spread rice on seaweed, add fillings, roll and slice"]},
         {"title":"Egg Salad Sandwich","time":"12 min","kcal":"340kcal","difficulty":"Easy","steps":["Boil eggs and peel","Mix with mayo, mustard, salt, and pepper","Line whole grain bread with lettuce and add egg salad","Top with tomato and cucumber slices, close with bread"]},
     ]},
    {"id":"broccoli","icon":"🥦","name":"Broccoli","name_en":"broccoli","short":"King of anti-cancer vegetables","badge":"Anti-Cancer","category":"Vegetables",
     "description":"Broccoli has more vitamin C than oranges and is rich in sulforaphane, a potent anti-cancer compound. Lightly steaming is best for preserving nutrients.",
     "effects":["Anti-cancer","Immunity boost","Improved digestion","Bone health","Blood sugar control"],
     "nutrition":{"Calories":"34kcal","Protein":"2.8g","Fiber":"2.6g","Carbs":"6.6g","Fat":"0.4g","Vitamin C":"89.2mg"},
     "recipes":[
         {"title":"Garlic Broccoli Stir-Fry","time":"10 min","kcal":"120kcal","difficulty":"Easy","steps":["Cut broccoli into florets and blanch for 30 seconds","Brown garlic in a pan","Stir-fry broccoli over high heat for 2 min","Finish with oyster sauce and sesame oil"]},
         {"title":"Cream of Broccoli Soup","time":"25 min","kcal":"210kcal","difficulty":"Medium","steps":["Sauté onion and potato in olive oil","Add broccoli and vegetable broth; simmer 15 min","Blend smooth with a hand blender","Stir in heavy cream for creaminess"]},
         {"title":"Broccoli Cheese Omelette","time":"12 min","kcal":"290kcal","difficulty":"Easy","steps":["Finely chop broccoli and blanch","Beat 3 eggs with salt and pepper","Pour eggs into a buttered pan; add broccoli and cheese","Fold in half and heat until cheese melts"]},
         {"title":"Broccoli Sesame Dressing Salad","time":"15 min","kcal":"150kcal","difficulty":"Easy","steps":["Cut broccoli into florets and lightly blanch","Make a dressing with sesame, soy sauce, vinegar, sugar, and sesame oil","Toss blanched broccoli with dressing","Finish with sesame seeds"]},
         {"title":"Broccoli Quinoa Bowl","time":"25 min","kcal":"320kcal","difficulty":"Easy","steps":["Cook quinoa","Roast broccoli in olive oil in the oven for 20 min","Make a lemon tahini dressing","Top quinoa with broccoli and drizzle with dressing"]},
     ]},
    {"id":"oats","icon":"🌿","name":"Oats","name_en":"oats","short":"Beta-glucan for lower cholesterol","badge":"Heart Health","category":"Whole Grain",
     "description":"Oats are especially rich in beta-glucan, a soluble dietary fibre. They're effective at lowering cholesterol and preventing blood sugar spikes.",
     "effects":["Lower cholesterol","Blood sugar control","Satiety","Heart health","Gut health"],
     "nutrition":{"Calories":"389kcal","Protein":"17.0g","Fiber":"10.6g","Carbs":"66.3g","Fat":"6.9g","Magnesium":"177mg"},
     "recipes":[
         {"title":"Overnight Oats","time":"5 min + 8h chill","kcal":"320kcal","difficulty":"Easy","steps":["Combine oats and almond milk in a container","Add chia seeds, honey, and vanilla","Refrigerate overnight","Top with fruit and nuts in the morning"]},
         {"title":"Banana Oat Pancakes","time":"20 min","kcal":"280kcal","difficulty":"Easy","steps":["Mash banana and mix with eggs and oats","Add cinnamon and baking powder","Cook both sides over low heat","Serve with maple syrup and fruit"]},
         {"title":"Oat Energy Cookies","time":"25 min","kcal":"150kcal","difficulty":"Easy","steps":["Mix oats, banana, and peanut butter","Stir in chocolate chips and raisins","Shape into rounds on a baking tray","Bake at 180°C (350°F) for 12 minutes"]},
         {"title":"Oat Risotto","time":"30 min","kcal":"340kcal","difficulty":"Medium","steps":["Sauté onion and garlic in butter","Add oats and stir-fry 1 min more","Gradually add vegetable broth, stirring for 20 min","Finish with parmesan and butter for creaminess"]},
         {"title":"Oat Granola Bars","time":"30 min + 2h chill","kcal":"200kcal","difficulty":"Easy","steps":["Mix oats, nuts, and seeds","Pour in melted honey and coconut oil","Spread flat and bake","Cool, chill 2 hours, then slice into bars"]},
     ]},
    {"id":"kimchi","icon":"🥬","name":"Kimchi","name_en":"kimchi","short":"Probiotic Korean fermented food","badge":"Probiotics","category":"Fermented",
     "description":"Kimchi is a UNESCO Intangible Cultural Heritage and Korea's iconic fermented food. Rich in lactic acid bacteria for gut health, plus vitamins C and K.",
     "effects":["Gut health","Immunity boost","Antioxidant","Improved digestion","Weight management"],
     "nutrition":{"Calories":"15kcal","Protein":"1.1g","Fiber":"1.6g","Carbs":"2.4g","Fat":"0.5g","Probiotics":"Hundreds of millions CFU"},
     "recipes":[
         {"title":"Kimchi Fried Rice","time":"15 min","kcal":"380kcal","difficulty":"Easy","steps":["Stir-fry kimchi in sesame oil","Add rice and stir-fry over high heat","Top with a fried egg","Sprinkle seaweed flakes and sesame to finish"]},
         {"title":"Kimchi Tofu Jjigae","time":"25 min","kcal":"210kcal","difficulty":"Easy","steps":["Stir-fry pork, then add kimchi","Make a broth with water, gochugaru, and soy sauce","Add tofu and simmer 10 min","Top with scallions and sesame to finish"]},
         {"title":"Kimchi Pasta","time":"20 min","kcal":"420kcal","difficulty":"Medium","steps":["Cook pasta in salted water","Stir-fry kimchi in butter","Add heavy cream to make a sauce","Toss with pasta and top with parmesan"]},
         {"title":"Kimchi Pancakes","time":"15 min","kcal":"280kcal","difficulty":"Easy","steps":["Finely chop kimchi and squeeze out liquid","Mix flour, water, and egg into batter","Stir kimchi into batter","Pan-fry in oil until golden on both sides"]},
         {"title":"Kimchi Risotto","time":"30 min","kcal":"390kcal","difficulty":"Medium","steps":["Sauté onion in butter, then add kimchi","Add rice and stir-fry 1 min","Gradually add broth, stirring for 18 min","Finish with sesame oil and parmesan"]},
     ]},
    {"id":"garlic","icon":"🧄","name":"Garlic","name_en":"garlic","short":"Allicin — natural antibiotic effect","badge":"Immunity Boost","category":"Spices",
     "description":"Garlic's allicin has antibacterial and antiviral properties and improves cardiovascular health. Eating it raw provides the highest potency.",
     "effects":["Immunity boost","Antibacterial & antiviral","Cardiovascular health","Blood pressure control","Anti-cancer"],
     "nutrition":{"Calories":"149kcal","Protein":"6.4g","Fiber":"2.1g","Carbs":"33.1g","Fat":"0.5g","Allicin":"Abundant"},
     "recipes":[
         {"title":"Garlic Olive Oil Pasta (Aglio e Olio)","time":"20 min","kcal":"380kcal","difficulty":"Easy","steps":["Cook pasta in salted water","Heat olive oil and sauté garlic in a pan","Add pasta and pasta water and toss","Finish with chili flakes, parmesan, and parsley"]},
         {"title":"Black Garlic Honey Dressing Salad","time":"10 min","kcal":"160kcal","difficulty":"Easy","steps":["Mash 3 cloves of black garlic","Mix with honey, balsamic, olive oil, and salt","Prepare salad greens","Drizzle with dressing to finish"]},
         {"title":"Garlic Butter Shrimp","time":"15 min","kcal":"250kcal","difficulty":"Easy","steps":["Clean and devein shrimp","Melt butter in a pan and sauté garlic","Add shrimp and cook until pink","Finish with lemon juice and parsley"]},
         {"title":"Roasted Garlic Potato Soup","time":"30 min","kcal":"220kcal","difficulty":"Easy","steps":["Roast a whole head of garlic in the oven and squeeze out cloves","Simmer potato and onion in broth","Add roasted garlic and blend smooth","Finish with heavy cream, salt, and pepper"]},
         {"title":"Garlic Soy Braised Chicken","time":"40 min","kcal":"450kcal","difficulty":"Medium","steps":["Cut chicken into bite-sized pieces","Make a sauce with soy sauce, garlic, sugar, and gochugaru","Toss chicken in sauce and stir-fry","Add potato and carrot with water and braise 20 min"]},
     ]},
    {"id":"banana","icon":"🍌","name":"Banana","name_en":"banana","short":"Potassium for instant energy","badge":"Post-Workout Snack","category":"Fruit",
     "description":"Bananas are rich in potassium to prevent muscle cramps, and their fast-digesting carbohydrates provide immediate energy.",
     "effects":["Energy boost","Muscle cramp prevention","Mood lift","Improved digestion","Blood pressure control"],
     "nutrition":{"Calories":"89kcal","Protein":"1.1g","Fiber":"2.6g","Carbs":"23.0g","Fat":"0.3g","Potassium":"358mg"},
     "recipes":[
         {"title":"Banana Ice Cream","time":"5 min + 3h freeze","kcal":"100kcal","difficulty":"Easy","steps":["Slice bananas and freeze","Blend frozen bananas until creamy","Add peanut butter and cocoa","Scoop into a bowl and top with nuts"]},
         {"title":"2-Ingredient Banana Pancakes","time":"15 min","kcal":"180kcal","difficulty":"Easy","steps":["Mash 1 banana","Mix in 2 eggs until combined","Cook one tablespoon at a time over low heat","Serve with maple syrup and fruit"]},
         {"title":"Banana Bread","time":"60 min","kcal":"220kcal","difficulty":"Medium","steps":["Mash 3 very ripe bananas","Stir in eggs, honey, and olive oil","Mix in whole wheat flour, baking soda, and cinnamon","Bake at 180°C (350°F) for 45 minutes"]},
         {"title":"Banana Oatmeal","time":"10 min","kcal":"290kcal","difficulty":"Easy","steps":["Cook oats in milk for 5 minutes","Slice banana and place on top","Add honey, cinnamon, and nuts","Enjoy warm straight away"]},
         {"title":"Banana Peanut Butter Smoothie","time":"5 min","kcal":"310kcal","difficulty":"Easy","steps":["Add banana, almond milk, and peanut butter to blender","Add honey and cocoa powder","Blend smooth","Pour into a glass and top with banana slices"]},
     ]},
    {"id":"chickpea","icon":"🟡","name":"Chickpea","name_en":"chickpea","short":"Protein and fibre-rich legume","badge":"Vegan","category":"Legumes",
     "description":"Chickpeas are high in protein and dietary fibre with a low glycaemic index, making them great for blood sugar management.",
     "effects":["Blood sugar control","Improved digestion","Muscle synthesis","Satiety","Energy metabolism"],
     "nutrition":{"Calories":"164kcal","Protein":"8.9g","Fiber":"7.6g","Carbs":"27.4g","Fat":"2.6g","Iron":"2.9mg"},
     "recipes":[
         {"title":"Hummus","time":"10 min","kcal":"180kcal","difficulty":"Easy","steps":["Add cooked chickpeas, tahini, and garlic to a blender","Add lemon juice, olive oil, and salt; blend smooth","Adjust consistency with water","Top with paprika powder and olive oil"]},
         {"title":"Roasted Chickpea Salad","time":"30 min","kcal":"310kcal","difficulty":"Easy","steps":["Season chickpeas with olive oil, cumin, and paprika","Roast at 200°C (390°F) for 25 minutes","Prepare arugula, cherry tomatoes, and cucumber","Toss vegetables with chickpeas and lemon dressing"]},
         {"title":"Chickpea Curry","time":"30 min","kcal":"340kcal","difficulty":"Easy","steps":["Sauté onion, garlic, and tomato","Add curry powder and coconut milk","Add chickpeas and simmer 15 minutes","Serve with rice or naan"]},
         {"title":"Chickpea Avocado Salad","time":"12 min","kcal":"280kcal","difficulty":"Easy","steps":["Rinse chickpeas and drain","Dice avocado","Add cucumber, cherry tomatoes, and parsley","Toss with lemon juice, olive oil, and salt"]},
         {"title":"Chickpea Pancakes (Besan)","time":"20 min","kcal":"200kcal","difficulty":"Medium","steps":["Mix chickpea flour, water, and salt into batter","Add diced onion, cilantro, and cumin","Pan-fry thin pancakes","Serve with yogurt sauce"]},
     ]},
    {"id":"almond","icon":"🌰","name":"Almond","name_en":"almond","short":"Vitamin E antioxidant nut","badge":"Antioxidant","category":"Nuts",
     "description":"Almonds are rich in vitamin E for powerful antioxidant protection and skin health. Magnesium helps manage blood sugar and blood pressure.",
     "effects":["Antioxidant","Skin care","Blood sugar control","Heart health","Bone strength"],
     "nutrition":{"Calories":"579kcal","Protein":"21.2g","Fiber":"12.5g","Carbs":"21.6g","Fat":"49.9g","Vitamin E":"25.6mg"},
     "recipes":[
         {"title":"Almond Energy Balls","time":"15 min","kcal":"120kcal","difficulty":"Easy","steps":["Process almonds, dates, and oats in a food processor","Add honey and cocoa; blend until it holds together","Roll into bite-sized balls","Coat in coconut flakes and chill"]},
         {"title":"Almond Granola","time":"30 min","kcal":"380kcal","difficulty":"Easy","steps":["Mix oats, sliced almonds, and sunflower seeds","Toss with honey, olive oil, and cinnamon","Bake at 160°C (320°F) for 25 minutes","Cool and mix with raisins and cranberries"]},
         {"title":"Almond Butter Toast","time":"5 min","kcal":"280kcal","difficulty":"Easy","steps":["Toast whole grain bread","Spread generously with almond butter","Top with banana slices","Drizzle honey and sprinkle chia seeds"]},
         {"title":"Homemade Almond Milk","time":"10 min + 4h soak","kcal":"30kcal","difficulty":"Easy","steps":["Soak almonds in water for at least 4 hours","Blend soaked almonds with 4 cups water","Strain through a cheesecloth","Add salt and vanilla to finish"]},
         {"title":"Almond-Crusted Chicken","time":"30 min","kcal":"380kcal","difficulty":"Medium","steps":["Grind almonds into a fine crumb","Dip chicken breast in egg wash, then coat in almond crumbs","Bake at 200°C (390°F) for 20 minutes","Finish with lemon and herbs"]},
     ]},
    {"id":"greek_yogurt","icon":"🥛","name":"Greek Yogurt","name_en":"greek yogurt","short":"Probiotic high-protein dairy","badge":"Gut Health","category":"Dairy",
     "description":"Greek yogurt is high in protein and its live cultures improve gut health. Long-lasting satiety makes it an excellent diet food.",
     "effects":["Gut health","Immunity boost","Bone strength","Satiety","Muscle recovery"],
     "nutrition":{"Calories":"59kcal","Protein":"10.0g","Fiber":"0g","Carbs":"3.6g","Fat":"0.4g","Calcium":"111mg"},
     "recipes":[
         {"title":"Greek Yogurt Parfait","time":"5 min","kcal":"280kcal","difficulty":"Easy","steps":["Spoon Greek yogurt into a cup","Add a layer of granola","Top with blueberries, strawberries, and banana","Drizzle honey and garnish with mint"]},
         {"title":"Greek Yogurt Chicken Marinade","time":"25 min","kcal":"310kcal","difficulty":"Medium","steps":["Mix yogurt with lemon juice, garlic, cumin, and paprika","Marinate chicken breast for at least 30 minutes","Grill 6 minutes per side","Serve with herbs and lemon"]},
         {"title":"Greek Yogurt Dip","time":"8 min","kcal":"80kcal","difficulty":"Easy","steps":["Stir olive oil into Greek yogurt","Mix in minced garlic, dill, and lemon juice","Season with salt and pepper","Serve with veggie sticks or pita chips"]},
         {"title":"Greek Yogurt Pancakes","time":"20 min","kcal":"260kcal","difficulty":"Easy","steps":["Mix Greek yogurt, egg, and oat flour","Add baking powder and honey","Pan-fry on low heat","Serve with fruit and maple syrup"]},
         {"title":"Greek Yogurt Ice Cream","time":"10 min + 6h freeze","kcal":"120kcal","difficulty":"Easy","steps":["Mix Greek yogurt, honey, and vanilla","Fold in your choice of fruit","Transfer to an airtight container and freeze","Stir every 30 minutes for a smooth texture"]},
     ]},
    {"id":"turmeric","icon":"🟠","name":"Turmeric","name_en":"turmeric","short":"Curcumin anti-inflammatory super spice","badge":"Anti-Inflammatory","category":"Spices",
     "description":"Turmeric contains curcumin, a powerful anti-inflammatory and antioxidant compound. It supports joint health and has been shown to enhance brain function.",
     "effects":["Anti-inflammatory","Joint health","Brain function boost","Antioxidant","Improved digestion"],
     "nutrition":{"Calories":"354kcal","Protein":"7.8g","Fiber":"21.1g","Carbs":"64.9g","Fat":"9.9g","Curcumin":"3–5%"},
     "recipes":[
         {"title":"Golden Milk","time":"8 min","kcal":"120kcal","difficulty":"Easy","steps":["Add 1/2 tsp turmeric to milk","Add cinnamon, ginger powder, and black pepper","Heat gently over medium heat","Sweeten with honey to finish"]},
         {"title":"Turmeric Tofu Scramble","time":"12 min","kcal":"200kcal","difficulty":"Easy","steps":["Crumble tofu and squeeze out moisture","Sauté olive oil and garlic in a pan","Add tofu, turmeric, cumin, and salt; stir-fry","Fold in spinach and cherry tomatoes to finish"]},
         {"title":"Turmeric Fried Rice","time":"15 min","kcal":"340kcal","difficulty":"Easy","steps":["Heat olive oil in a pan and sauté garlic","Add leftover rice and sprinkle 1 tsp turmeric","Add egg and stir-fry","Finish with soy sauce, sesame oil, and scallions"]},
         {"title":"Turmeric Lentil Soup","time":"30 min","kcal":"260kcal","difficulty":"Easy","steps":["Sauté onion and garlic","Add lentils, vegetable broth, turmeric, and cumin","Simmer for 25 minutes","Stir in lemon juice and coconut milk to finish"]},
         {"title":"Turmeric Smoothie","time":"5 min","kcal":"150kcal","difficulty":"Easy","steps":["Add banana, mango, and 1/2 tsp turmeric to blender","Add coconut milk, ginger, and black pepper","Blend smooth","Pour into a glass and dust with cinnamon"]},
     ]},
    {"id":"walnut","icon":"🫀","name":"Walnut","name_en":"walnut","short":"Omega-3 brain health nut","badge":"Brain Health","category":"Nuts",
     "description":"Walnuts are rich in plant-based omega-3 fatty acids, and their polyphenols reduce oxidative stress. About 7 walnuts a day is ideal.",
     "effects":["Brain health","Heart protection","Antioxidant","Reduced inflammation","Better sleep"],
     "nutrition":{"Calories":"654kcal","Protein":"15.2g","Fiber":"6.7g","Carbs":"13.7g","Fat":"65.2g","Omega-3":"9.1g"},
     "recipes":[
         {"title":"Walnut Banana Smoothie","time":"5 min","kcal":"280kcal","difficulty":"Easy","steps":["Add banana, walnuts, and almond milk to blender","Add honey and cinnamon","Blend smooth","Pour into a glass and top with walnuts"]},
         {"title":"Walnut Spinach Salad","time":"12 min","kcal":"240kcal","difficulty":"Easy","steps":["Lightly toast walnuts in a dry pan","Prepare spinach, apple, and cranberries","Make a balsamic dressing","Toss ingredients and top with walnuts"]},
         {"title":"Walnut Brownies","time":"35 min","kcal":"280kcal","difficulty":"Medium","steps":["Melt dark chocolate and butter in a double boiler","Stir in eggs and sugar","Fold in flour, cocoa, salt, and walnuts","Bake at 180°C (350°F) for 25 minutes"]},
         {"title":"Walnut Oat Cookies","time":"25 min","kcal":"160kcal","difficulty":"Easy","steps":["Mix oats, whole wheat flour, sugar, and butter","Stir in eggs and vanilla","Fold in walnuts and raisins","Bake at 180°C (350°F) for 12 minutes"]},
         {"title":"Walnut Miso Dressing","time":"8 min","kcal":"90kcal","difficulty":"Easy","steps":["Finely chop walnuts","Mix miso, honey, vinegar, and sesame oil","Stir in chopped walnuts","Serve with salad greens or lettuce wraps"]},
     ]},
    {"id":"chia","icon":"⚫","name":"Chia Seeds","name_en":"chia seeds","short":"Omega-3 and fibre super seed","badge":"Superfood","category":"Seeds",
     "description":"Chia seeds absorb water to form a gel, keeping you fuller for longer. Rich in omega-3, calcium, and phosphorus for bone and heart health.",
     "effects":["Satiety","Bone strength","Heart health","Blood sugar control","Improved digestion"],
     "nutrition":{"Calories":"486kcal","Protein":"16.5g","Fiber":"34.4g","Carbs":"42.1g","Fat":"30.7g","Calcium":"631mg"},
     "recipes":[
         {"title":"Chia Seed Pudding","time":"5 min + 4h chill","kcal":"200kcal","difficulty":"Easy","steps":["Pour 1 cup almond milk over 3 tbsp chia seeds","Add honey and vanilla; stir well","Refrigerate for at least 4 hours","Top with fruit, nuts, and granola"]},
         {"title":"Chia Lemonade","time":"10 min","kcal":"80kcal","difficulty":"Easy","steps":["Soak chia seeds in water for 5 minutes","Add lemon juice and honey","Add mint leaves","Serve over ice"]},
         {"title":"Chia Jam","time":"15 min","kcal":"40kcal","difficulty":"Easy","steps":["Heat strawberries or blueberries in a saucepan","Add honey and lemon juice; simmer 10 min","Remove from heat and stir in chia seeds","Cool and refrigerate"]},
         {"title":"Chia Energy Bars","time":"15 min + 2h chill","kcal":"180kcal","difficulty":"Easy","steps":["Mix oats, chia seeds, almond butter, and honey","Stir in chocolate chips and dried fruit","Press flat and refrigerate for 2 hours","Cut into bars"]},
         {"title":"Chia Seed Yogurt Bowl","time":"5 min","kcal":"220kcal","difficulty":"Easy","steps":["Stir 1 tbsp chia seeds into Greek yogurt","Rest for 10 minutes to let chia seeds swell","Top with fruit and nuts","Drizzle honey to finish"]},
     ]},
]

# ── Session state ─────────────────────────────────────────────────────────
for k, v in [("selected", set()), ("detail_id", None), ("search_results", []), ("search_done", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

if "community_posts" not in st.session_state:
    st.session_state.community_posts = load_posts()

def toggle(ingr_id):
    if ingr_id in st.session_state.selected:
        st.session_state.selected.discard(ingr_id)
    else:
        st.session_state.selected.add(ingr_id)

def do_search(q):
    q = q.strip().lower()
    if not q: return []
    return [i for i in INGREDIENTS if q in i["name"].lower() or q in i["name_en"].lower() or q in i["short"].lower() or q in i["category"].lower()]

# ── Navigation ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav">
    <div class="nav-logo"><span class="nav-dot"></span>{APP_NAME}</div>
    <div class="nav-tag">{APP_TAGLINE}</div>
</div>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌿 Ingredients & Recipes", "📸 Food Photo Share"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — Ingredient Explorer
# ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="hero">
        <p class="hero-eye" style="color:#4A7C3F!important;">🌿 GOOD FOOD STARTS HERE</p>
        <h1 class="hero-title" style="color:#2C3A1E!important;">Explore today's<br>ingredients</h1>
        <p class="hero-sub" style="color:#5A6A50!important;">22 ingredients in our library — browse the 6 featured picks,<br>or type a name in the search bar to find what you need</p>
    </div>""", unsafe_allow_html=True)

    sc1, sc2 = st.columns([5, 1])
    with sc1:
        search_q = st.text_input("Search ingredients", placeholder="e.g. spinach, broccoli, nuts, fermented ...", label_visibility="visible", key="search_box")
    with sc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_btn = st.button("Search 🔍", use_container_width=True, key="search_btn")

    if search_btn:
        st.session_state.search_results = do_search(search_q)
        st.session_state.search_done = True
        st.session_state.detail_id = None

    if st.session_state.search_done:
        results = st.session_state.search_results
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if not results:
            st.warning(f"No ingredients found for '{search_q}'.")
        else:
            st.markdown(f'<p class="sec-sub">🔍 {len(results)} result(s) found</p>', unsafe_allow_html=True)
            for ing in results:
                is_sel = ing["id"] in st.session_state.selected
                rc1, rc2, rc3 = st.columns([6, 1, 1])
                with rc1:
                    badges = f'<span class="s-badge">{ing["badge"]}</span><span class="s-badge">{ing["category"]}</span>'
                    st.markdown(f"""
                    <div class="search-card">
                        <span class="search-icon">{ing['icon']}</span>
                        <div class="search-info">
                            <div class="search-name">{ing['name']}</div>
                            <div class="search-short">{ing['short']}</div>
                            <div class="search-badges">{badges}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with rc2:
                    if st.button("Deselect" if is_sel else "Select", key=f"sr_sel_{ing['id']}", use_container_width=True):
                        toggle(ing["id"]); st.rerun()
                with rc3:
                    if st.button("Info", key=f"sr_info_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                        st.rerun()
                if st.session_state.detail_id == ing["id"]:
                    eff_html = "".join(f'<span class="eff">{e}</span>' for e in ing["effects"])
                    nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in ing["nutrition"].items())
                    st.markdown(f"""
                    <div class="detail-box">
                        <div class="d-title">{ing['icon']} {ing['name']}</div>
                        <div class="d-desc">{ing['description']}</div>
                        <div class="d-lbl">KEY BENEFITS</div><div class="effects">{eff_html}</div>
                        <div class="d-lbl">NUTRITION (per 100g)</div><div class="nut-grid">{nut_html}</div>
                    </div>""", unsafe_allow_html=True)
        cc = st.columns([4,1])[1]
        with cc:
            if st.button("Close Search ✕", use_container_width=True):
                st.session_state.search_done = False; st.session_state.search_results = []; st.session_state.detail_id = None; st.rerun()

    if not st.session_state.search_done:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">Today\'s Featured Ingredients</p>', unsafe_allow_html=True)
        st.markdown('<p class="sec-sub">Click a card to view detailed information</p>', unsafe_allow_html=True)

        featured_ings = [i for i in INGREDIENTS if i["id"] in FEATURED]
        cols = st.columns(3)
        for idx, ing in enumerate(featured_ings):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="ingr-card">
                    <div class="i-icon">{ing['icon']}</div>
                    <div class="i-name">{ing['name']}</div>
                    <div class="i-short">{ing['short']}</div>
                    <span class="i-badge">{ing['badge']}</span>
                </div>""", unsafe_allow_html=True)
                if st.button(ing["name"], key=f"f_card_{ing['id']}", use_container_width=True):
                    st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                    st.rerun()

        if st.session_state.detail_id:
            d = next((i for i in featured_ings if i["id"] == st.session_state.detail_id), None)
            if d:
                eff_html = "".join(f'<span class="eff">{e}</span>' for e in d["effects"])
                nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in d["nutrition"].items())
                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="detail-box">
                    <div class="d-title">{d['icon']} {d['name']}</div>
                    <div class="d-desc">{d['description']}</div>
                    <div class="d-lbl">KEY BENEFITS</div><div class="effects">{eff_html}</div>
                    <div class="d-lbl">NUTRITION (per 100g)</div><div class="nut-grid">{nut_html}</div>
                </div>""", unsafe_allow_html=True)
                cc = st.columns([5,1])[1]
                with cc:
                    if st.button("Close ✕", use_container_width=True, key="close_detail"):
                        st.session_state.detail_id = None; st.rerun()

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#fff;border:1.5px dashed #C5DDB8;border-radius:12px;padding:18px 24px;text-align:center;">
            <p style="font-size:13px;color:#4A5A40;margin:0;">
                🔍 Search all <strong style="color:#2C3A1E;">22 ingredients</strong> using the search bar above<br>
                <span style="font-size:12px;color:#7A8A70;">Spinach · Sweet Potato · Egg · Oats · Kimchi · Turmeric · Garlic · Banana · Walnut · Chia Seeds · Broccoli · Chickpea · Almond · Greek Yogurt ···</span>
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">Recipes</p>', unsafe_allow_html=True)

        all_ings = INGREDIENTS
        recipe_names = []
        for ing in all_ings:
            for rec in ing["recipes"]:
                recipe_names.append(f"{ing['icon']} {rec['title']} ({ing['name']})")

        selected_recipe = st.selectbox(
            "Recipe search",
            options=["— Select a recipe —"] + recipe_names,
            label_visibility="collapsed",
        )

        if selected_recipe != "— Select a recipe —":
            for ing in all_ings:
                for rec in ing["recipes"]:
                    label = f"{ing['icon']} {rec['title']} ({ing['name']})"
                    if label == selected_recipe:
                        dc = {"Easy":"#2C5F21","Medium":"#7A5C00","Hard":"#8B0000"}.get(rec["difficulty"],"#555")
                        steps_html = "".join(
                            f'<div class="r-step"><span class="r-num">{j+1}</span><span>{s}</span></div>'
                            for j, s in enumerate(rec["steps"])
                        )
                        st.markdown(f"""
                        <div class="recipe-card">
                            <div class="r-title">{rec['title']}</div>
                            <div class="r-meta">
                                <span>⏱ {rec['time']}</span>
                                <span>🔥 {rec['kcal']}</span>
                                <span>🌿 {ing['name']}</span>
                                <span style="color:{dc};font-weight:500;">● {rec['difficulty']}</span>
                            </div>
                            {steps_html}
                        </div>""", unsafe_allow_html=True)
                        sc = st.columns([4,1])[1]
                        with sc:
                            if st.button("📸 Share Photo", key=f"share_{ing['id']}_{rec['title']}", use_container_width=True):
                                st.session_state["pending_recipe"] = rec["title"]
                                st.info(f"📸 Head to the Food Photo Share tab to upload a photo of **{rec['title']}**!")
        else:
            st.markdown('<div class="empty">🍽<br><br>Select a recipe from the dropdown above</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 2 — Food Photo Share
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="sec-title">📸 Food Photo Share</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Share photos of your homemade dishes with the community</p>', unsafe_allow_html=True)

    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">Upload Your Dish</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-sub">Add a photo and a few details</div>', unsafe_allow_html=True)

    uf1, uf2 = st.columns(2)
    with uf1:
        nickname = st.text_input("Nickname", placeholder="e.g. HealthyChef 👩‍🍳")
    with uf2:
        recipe_name = st.text_input("Recipe Name", placeholder="e.g. Quinoa Salad Bowl", value=st.session_state.get("pending_recipe",""))
    note = st.text_area("A note", placeholder="Share your review or a personal tip 😋", height=90)
    photo_file = st.file_uploader("Upload Photo", type=["jpg","jpeg","png"])

    if st.button("🌿 Share", use_container_width=True):
        if not nickname:
            st.warning("Please enter a nickname.")
        elif not recipe_name:
            st.warning("Please enter a recipe name.")
        elif not photo_file:
            st.warning("Please upload a photo.")
        else:
            img_b64 = base64.b64encode(photo_file.read()).decode()
            ext  = photo_file.name.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            new_post = {
                "nickname": nickname, "recipe": recipe_name,
                "note": note, "img_b64": img_b64, "mime": mime,
                "time": datetime.now().strftime("%Y.%m.%d %H:%M"),
                "likes": 0,
            }
            st.session_state.community_posts.insert(0, new_post)
            save_posts(st.session_state.community_posts)
            st.session_state["pending_recipe"] = ""
            st.success(f"🎉 Your photo of '{recipe_name}' has been shared!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.community_posts:
        st.markdown("""
        <div class="no-posts">
            <div class="no-posts-icon">🍽</div>
            <div class="no-posts-text">No photos shared yet<br>Be the first to share your dish!</div>
        </div>""", unsafe_allow_html=True)
    else:
        total = len(st.session_state.community_posts)
        st.markdown(f'<p style="font-size:13px;color:#7A8A70;margin-bottom:20px;"><strong style="color:#2C3A1E;">{total}</strong> dish photo(s) shared</p>', unsafe_allow_html=True)
        pcols = st.columns(3)
        for idx, post in enumerate(st.session_state.community_posts):
            with pcols[idx % 3]:
                st.markdown(f"""
                <div class="photo-card">
                    <img class="photo-img" src="data:{post['mime']};base64,{post['img_b64']}" alt="{post['recipe']}"/>
                    <div class="photo-body">
                        <div class="photo-user">👤 {post['nickname']}</div>
                        <div class="photo-recipe">🌿 {post['recipe']}</div>
                        <div class="photo-note">{post['note'] if post['note'] else ''}</div>
                        <div class="photo-time">{post['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
                lc, dc2 = st.columns(2)
                with lc:
                    if st.button(f"❤️  {post['likes']}", key=f"like_{idx}", use_container_width=True):
                        st.session_state.community_posts[idx]["likes"] += 1
                        save_posts(st.session_state.community_posts)
                        st.rerun()
                with dc2:
                    if st.button("Delete", key=f"del_{idx}", use_container_width=True):
                        st.session_state.community_posts.pop(idx)
                        save_posts(st.session_state.community_posts)
                        st.rerun()

st.markdown(f"""
<div style="margin-top:56px;padding:18px 0;border-top:1px solid #E2DDD4;text-align:center;font-size:11px;color:#7A8A70;">
    {APP_NAME} · {APP_TAGLINE} · SKKU Art Project
</div>""", unsafe_allow_html=True)
