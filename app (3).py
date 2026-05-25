import streamlit as st
import base64
from datetime import datetime

APP_NAME    = "Nourish"
APP_TAGLINE = "wholesome ingredients, honest recipes"

st.set_page_config(page_title=APP_NAME, page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,header,footer{visibility:hidden;}
.stApp{background:#F7F5F0;}

/* 네비 */
.nav{display:flex;align-items:center;justify-content:space-between;padding:16px 0 12px;border-bottom:1px solid #E2DDD4;margin-bottom:32px;}
.nav-logo{font-family:'DM Serif Display',serif;font-size:22px;color:#2C3A1E;display:flex;align-items:center;gap:8px;}
.nav-dot{width:9px;height:9px;border-radius:50%;background:#4A7C3F;display:inline-block;}
.nav-tag{font-size:11px;color:#6B7A60;font-style:italic;}

/* 히어로 */
.hero{background:#EEF0E8;border-radius:14px;padding:40px 36px;margin-bottom:36px;border:1px solid #DDE0D4;}
.hero-eye{font-size:11px;font-weight:500;letter-spacing:.1em;color:#4A7C3F;margin-bottom:8px;}
.hero-title{font-family:'DM Serif Display',serif;font-size:34px;color:#2C3A1E;line-height:1.25;margin-bottom:8px;}
.hero-sub{font-size:14px;color:#5A6A50;line-height:1.65;}

/* 섹션 */
.sec-title{font-family:'DM Serif Display',serif;font-size:20px;color:#2C3A1E;margin-bottom:4px;}
.sec-sub{font-size:12px;color:#7A8A70;margin-bottom:18px;}

/* 식재료 카드 — 넉넉한 여백 */
.ingr-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:22px 16px;text-align:center;}
.ingr-card.sel{border-color:#2C3A1E;background:#F0F7EB;}
.i-icon{font-size:32px;margin-bottom:10px;}
.i-name{font-weight:500;font-size:15px;color:#2C3A1E;margin-bottom:4px;}
.i-short{font-size:12px;color:#7A8A70;line-height:1.4;margin-bottom:8px;}
.i-badge{display:inline-block;font-size:10px;font-weight:500;padding:3px 10px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}

/* 검색 결과 카드 */
.search-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:20px;margin-bottom:12px;display:flex;align-items:center;gap:16px;}
.search-icon{font-size:36px;flex-shrink:0;}
.search-info{flex:1;}
.search-name{font-weight:500;font-size:16px;color:#2C3A1E;margin-bottom:3px;}
.search-short{font-size:12px;color:#7A8A70;margin-bottom:6px;}
.search-badges{display:flex;gap:6px;flex-wrap:wrap;}
.s-badge{font-size:10px;font-weight:500;padding:2px 9px;border-radius:99px;background:#EEF5E9;color:#2C5F21;border:1px solid #C5DDB8;}

/* 상세 설명 */
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

/* 레시피 카드 */
.recipe-card{background:#fff;border:1.5px solid #E2DDD4;border-radius:14px;padding:22px;margin-bottom:14px;}
.r-title{font-family:'DM Serif Display',serif;font-size:18px;color:#2C3A1E;margin-bottom:6px;}
.r-meta{display:flex;gap:14px;font-size:12px;color:#7A8A70;margin-bottom:14px;}
.r-step{display:flex;gap:10px;padding:8px 0;border-top:1px solid #F0ECE4;font-size:13px;color:#4A5A40;line-height:1.6;align-items:flex-start;}
.r-step:first-child{border-top:none;}
.r-num{min-width:20px;height:20px;border-radius:50%;background:#4A7C3F;color:#fff;font-size:10px;font-weight:500;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}

/* 커뮤니티 */
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

/* 버튼 */
.stButton>button{background:#2C3A1E!important;color:#F0F7EB!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;padding:8px 16px!important;}
.stButton>button:hover{background:#4A7C3F!important;}

/* 인풋 */
.stTextInput>div>div>input,.stTextArea textarea{border:1.5px solid #D8D3C8!important;border-radius:8px!important;background:#fff!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;color:#2C3A1E!important;}
.stTextInput>div>div>input:focus,.stTextArea textarea:focus{border-color:#4A7C3F!important;box-shadow:0 0 0 3px rgba(74,124,63,.12)!important;}
.stTextInput label,.stTextArea label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stFileUploader label{color:#2C3A1E!important;font-size:13px!important;font-weight:500!important;}
.stFileUploader>div{border:1.5px dashed #C5DDB8!important;border-radius:8px!important;background:#F0F7EB!important;}

/* 탭 */
.stTabs [data-baseweb="tab-list"]{gap:8px;}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:500!important;color:#5A6A50!important;padding:8px 20px!important;border-radius:8px!important;}
.stTabs [aria-selected="true"]{background:#EEF5E9!important;color:#2C3A1E!important;}

/* 경고/성공 */
.stAlert p{color:#2C3A1E!important;}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# 데이터
# ════════════════════════════════════════════════════════════════════
FEATURED = ["quinoa","avocado","salmon","tofu","blueberry","lentil"]  # 메인 6개

INGREDIENTS = [
    {"id":"quinoa","icon":"🌾","name":"퀴노아","name_en":"quinoa","short":"완전단백질 슈퍼씨앗","badge":"글루텐프리","category":"통곡물",
     "description":"퀴노아는 남미 안데스 산맥 원산지의 슈퍼푸드로, 곡물 중 유일하게 9가지 필수아미노산을 모두 함유한 완전단백질 식품이에요. 글루텐이 없어 밀 알레르기가 있는 분들도 안심하고 먹을 수 있고, 식이섬유가 풍부해 포만감이 오래 지속돼요.",
     "effects":["혈당 조절","근육 회복","소화 개선","포만감","에너지 공급"],
     "nutrition":{"칼로리":"120kcal","단백질":"4.4g","식이섬유":"2.8g","탄수화물":"21.3g","지방":"1.9g","철분":"1.5mg"},
     "recipes":[
         {"title":"퀴노아 샐러드 볼","time":"20분","kcal":"310kcal","difficulty":"쉬움","steps":["퀴노아 1컵을 물 2컵에 15분 끓인 뒤 5분 뜸 들인다","오이·방울토마토·적양파를 먹기 좋게 썬다","레몬즙·올리브오일·소금·후추로 드레싱을 만든다","퀴노아에 채소와 드레싱을 섞어 완성한다"]},
         {"title":"퀴노아 새우 볶음밥","time":"25분","kcal":"380kcal","difficulty":"보통","steps":["퀴노아를 미리 지어 식혀둔다","팬에 참기름을 두르고 마늘·새우를 볶는다","퀴노아와 달걀을 넣고 강불에서 볶는다","간장·굴소스로 간하고 파·깨를 뿌린다"]},
     ]},
    {"id":"avocado","icon":"🥑","name":"아보카도","name_en":"avocado","short":"건강한 단일불포화지방","badge":"비타민E","category":"건강지방",
     "description":"아보카도는 '숲속의 버터'라 불릴 만큼 크리미한 식감과 풍부한 영양을 자랑해요. 심장 건강에 좋은 단일불포화지방산이 풍부하고, 칼륨 함량이 바나나의 2배예요. 비타민 E·K·엽산이 가득해 피부 미용과 혈관 건강에도 탁월해요.",
     "effects":["심장 건강","피부 미용","혈압 조절","영양소 흡수 향상","항염증"],
     "nutrition":{"칼로리":"160kcal","단백질":"2.0g","식이섬유":"6.7g","탄수화물":"8.5g","지방":"14.7g","칼륨":"485mg"},
     "recipes":[
         {"title":"아보카도 토스트","time":"10분","kcal":"280kcal","difficulty":"쉬움","steps":["통곡물빵을 노릇하게 굽는다","아보카도를 으깨 레몬즙·소금·후추를 넣는다","빵에 듬뿍 바른다","반숙 달걀과 치아씨드를 올린다"]},
         {"title":"아보카도 명란 비빔밥","time":"15분","kcal":"420kcal","difficulty":"쉬움","steps":["따뜻한 밥에 참기름·간장을 섞는다","아보카도를 슬라이스하고 명란을 준비한다","밥 위에 아보카도·명란·달걀노른자를 올린다","김가루·깨를 뿌리고 비벼 먹는다"]},
     ]},
    {"id":"salmon","icon":"🐟","name":"연어","name_en":"salmon","short":"오메가-3 고함량 생선","badge":"단백질 20g","category":"단백질",
     "description":"연어는 오메가-3 지방산의 가장 좋은 공급원 중 하나예요. EPA와 DHA가 풍부해 뇌 건강·심혈관 건강·염증 억제에 탁월해요. 고품질 단백질과 비타민 D·B12도 풍부해 면역력 강화와 뼈 건강에도 도움이 돼요.",
     "effects":["뇌 건강","심혈관 보호","염증 억제","면역력","뼈 강화"],
     "nutrition":{"칼로리":"208kcal","단백질":"20.0g","식이섬유":"0g","탄수화물":"0g","지방":"13.0g","오메가3":"2.3g"},
     "recipes":[
         {"title":"연어 포케 볼","time":"15분","kcal":"450kcal","difficulty":"쉬움","steps":["현미밥을 볼에 담는다","연어를 큐브로 썰어 간장·참기름·생강즙에 5분 재운다","에다마메·오이·당근·아보카도를 준비한다","밥 위에 올리고 스리라차 마요를 뿌린다"]},
         {"title":"허브 오븐 구이 연어","time":"22분","kcal":"390kcal","difficulty":"보통","steps":["연어에 올리브오일·마늘·레몬즙·딜을 바른다","200도 오븐에서 12분 굽는다","아스파라거스를 함께 굽는다","레몬·파슬리로 마무리한다"]},
     ]},
    {"id":"tofu","icon":"🫘","name":"두부","name_en":"tofu","short":"식물성 완전단백질","badge":"저칼로리","category":"식물성단백질",
     "description":"두부는 콩을 갈아 만든 식물성 단백질의 대표 식품이에요. 칼로리가 낮으면서도 단백질이 풍부해 다이어트식으로 완벽하고, 칼슘 함량이 높아 뼈 건강에도 좋아요. 이소플라본이 풍부해 항암 효과도 기대할 수 있어요.",
     "effects":["다이어트","뼈 강화","근육 유지","콜레스테롤 감소","호르몬 균형"],
     "nutrition":{"칼로리":"76kcal","단백질":"8.0g","식이섬유":"0.3g","탄수화물":"1.9g","지방":"4.8g","칼슘":"350mg"},
     "recipes":[
         {"title":"순두부 된장국","time":"20분","kcal":"180kcal","difficulty":"쉬움","steps":["멸치·다시마 육수를 10분 끓인다","된장 2큰술을 풀고 애호박·버섯을 넣는다","순두부를 뜯어 넣고 5분 끓인다","청양고추·파를 넣고 불을 끈다"]},
         {"title":"두부 스테이크","time":"15분","kcal":"220kcal","difficulty":"쉬움","steps":["두부를 2cm로 썰어 물기를 제거한다","간장·꿀·마늘·참기름으로 소스를 만든다","팬에 양면 3분씩 노릇하게 굽는다","소스 붓고 1분 조리고 깨·파를 얹는다"]},
     ]},
    {"id":"blueberry","icon":"🫐","name":"블루베리","name_en":"blueberry","short":"항산화 슈퍼푸드","badge":"비타민C","category":"베리류",
     "description":"블루베리는 안토시아닌이라는 강력한 항산화 색소로 가득 차 있어요. 뇌 건강과 기억력 개선에 효과적이고, 활성산소를 제거해 노화를 늦춰줘요. 냉동 블루베리도 신선한 것 못지않게 영양이 유지돼요.",
     "effects":["항산화","뇌 건강","노화 방지","혈당 조절","시력 보호"],
     "nutrition":{"칼로리":"57kcal","단백질":"0.7g","식이섬유":"2.4g","탄수화물":"14.5g","지방":"0.3g","비타민C":"9.7mg"},
     "recipes":[
         {"title":"블루베리 스무디 볼","time":"8분","kcal":"260kcal","difficulty":"쉬움","steps":["냉동 블루베리·바나나를 블렌딩한다","그릭요거트를 넣고 걸쭉하게 만든다","그래놀라·치아씨드를 올린다","꿀을 드리즐한다"]},
         {"title":"블루베리 치즈케이크 무스","time":"20분","kcal":"290kcal","difficulty":"보통","steps":["크림치즈를 풀고 꿀·바닐라를 섞는다","생크림을 휘핑해 가볍게 섞는다","블루베리를 레몬즙·설탕으로 소스로 끓인다","컵에 무스를 담고 소스를 올린다"]},
     ]},
    {"id":"lentil","icon":"🌱","name":"렌틸콩","name_en":"lentils","short":"식이섬유·철분의 보고","badge":"채식","category":"콩류",
     "description":"렌틸콩은 세계에서 가장 오래된 재배 작물 중 하나로, 단백질과 철분이 특히 풍부해요. 식이섬유 함량이 매우 높아 장 건강을 개선하고 혈당 급등을 막아줘요. 채식주의자들의 훌륭한 단백질 공급원이에요.",
     "effects":["장 건강","혈당 조절","빈혈 예방","포만감","임산부 건강"],
     "nutrition":{"칼로리":"116kcal","단백질":"9.0g","식이섬유":"7.9g","탄수화물":"20.1g","지방":"0.4g","철분":"3.3mg"},
     "recipes":[
         {"title":"렌틸 수프","time":"35분","kcal":"290kcal","difficulty":"쉬움","steps":["양파·마늘·당근을 올리브오일에 볶는다","렌틸콩·채수·큐민·파프리카를 넣는다","약불에서 25분 끓인다","핸드블렌더로 반쯤 갈고 레몬즙으로 마무리한다"]},
         {"title":"렌틸 커리","time":"30분","kcal":"350kcal","difficulty":"보통","steps":["커리 페이스트를 볶아 향을 낸다","코코넛밀크·렌틸콩을 넣는다","약불에서 20분 졸인다","시금치를 넣고 2분 가열한 뒤 밥과 낸다"]},
     ]},
    # 검색으로만 나오는 식재료 16개
    {"id":"spinach","icon":"🥬","name":"시금치","name_en":"spinach","short":"철분·엽산의 녹색 보고","badge":"저칼로리","category":"채소",
     "description":"시금치는 '슈퍼 채소'라 불릴 만큼 다양한 영양소가 압축된 식품이에요. 철분·엽산·비타민 K·A가 풍부하고 칼로리는 매우 낮아요. 루테인이 눈 건강을 지켜주고, 마그네슘이 수면에 도움을 줘요.",
     "effects":["빈혈 예방","눈 건강","뼈 강화","소화 개선","피부 미용"],
     "nutrition":{"칼로리":"23kcal","단백질":"2.9g","식이섬유":"2.2g","탄수화물":"3.6g","지방":"0.4g","철분":"2.7mg"},
     "recipes":[
         {"title":"시금치 달걀 볶음","time":"10분","kcal":"180kcal","difficulty":"쉬움","steps":["시금치를 씻어 물기를 제거한다","팬에 마늘을 볶는다","시금치를 강불에서 볶는다","달걀 넣어 반숙으로 익히고 간한다"]},
         {"title":"시금치 페스토 파스타","time":"20분","kcal":"380kcal","difficulty":"보통","steps":["시금치·아몬드·마늘·올리브오일로 페스토를 만든다","파스타를 소금물에 삶는다","팬에 페스토와 파스타를 섞는다","방울토마토와 파마산을 올린다"]},
     ]},
    {"id":"sweetpotato","icon":"🍠","name":"고구마","name_en":"sweet potato","short":"베타카로틴·식이섬유 풍부","badge":"비타민A","category":"채소",
     "description":"고구마는 달콤한 맛과 함께 뛰어난 영양 프로필을 자랑해요. 베타카로틴이 풍부해 면역력과 시력 보호에 도움을 줘요. 혈당 지수가 흰 감자보다 낮아 더 건강한 탄수화물 공급원이에요.",
     "effects":["면역력 강화","시력 보호","장 건강","혈압 조절","에너지 공급"],
     "nutrition":{"칼로리":"86kcal","단백질":"1.6g","식이섬유":"3.0g","탄수화물":"20.1g","지방":"0.1g","비타민A":"961μg"},
     "recipes":[
         {"title":"고구마 라떼","time":"10분","kcal":"180kcal","difficulty":"쉬움","steps":["고구마를 쪄서 으깬다","따뜻한 우유 200ml에 으깬 고구마를 넣는다","꿀·시나몬을 넣는다","핸드블렌더로 갈아 완성한다"]},
         {"title":"고구마 그라탱","time":"35분","kcal":"290kcal","difficulty":"보통","steps":["고구마를 얇게 슬라이스한다","생크림·마늘·소금·후추로 크림소스를 만든다","용기에 고구마를 쌓고 크림소스를 붓는다","180도에서 25분 굽고 치즈를 올려 10분 더 굽는다"]},
     ]},
    {"id":"chickpea","icon":"🟡","name":"병아리콩","name_en":"chickpea","short":"단백질·식이섬유 풍부한 콩","badge":"채식","category":"콩류",
     "description":"병아리콩은 중동·지중해 요리의 핵심 식재료로 전 세계적으로 인기가 높아요. 단백질과 식이섬유가 풍부하고 혈당 지수가 낮아 당뇨 관리에도 좋아요.",
     "effects":["혈당 조절","소화 개선","근육 합성","포만감","에너지 대사"],
     "nutrition":{"칼로리":"164kcal","단백질":"8.9g","식이섬유":"7.6g","탄수화물":"27.4g","지방":"2.6g","철분":"2.9mg"},
     "recipes":[
         {"title":"훔무스","time":"10분","kcal":"180kcal","difficulty":"쉬움","steps":["삶은 병아리콩·타히니·마늘을 블렌더에 넣는다","레몬즙·올리브오일·소금을 넣고 곱게 간다","물로 농도를 조절한다","파프리카 파우더·올리브오일을 올린다"]},
         {"title":"구운 병아리콩 샐러드","time":"30분","kcal":"310kcal","difficulty":"쉬움","steps":["병아리콩에 올리브오일·큐민·파프리카로 양념한다","200도 오븐에서 25분 굽는다","루꼴라·방울토마토·오이를 준비한다","채소에 병아리콩을 올리고 레몬 드레싱을 뿌린다"]},
     ]},
    {"id":"almond","icon":"🌰","name":"아몬드","name_en":"almond","short":"비타민E·건강지방 견과류","badge":"항산화","category":"견과류",
     "description":"아몬드는 영양가가 가장 높은 견과류 중 하나예요. 비타민 E가 풍부해 강력한 항산화 작용을 하고 피부 건강을 지켜줘요. 마그네슘이 혈당·혈압 관리에 도움이 돼요.",
     "effects":["항산화","피부 미용","혈당 조절","심장 건강","뼈 강화"],
     "nutrition":{"칼로리":"579kcal","단백질":"21.2g","식이섬유":"12.5g","탄수화물":"21.6g","지방":"49.9g","비타민E":"25.6mg"},
     "recipes":[
         {"title":"아몬드 에너지 볼","time":"15분","kcal":"120kcal","difficulty":"쉬움","steps":["아몬드·대추야자·귀리를 푸드프로세서에 넣는다","꿀·코코아를 넣고 뭉쳐질 때까지 간다","한 입 크기로 동그랗게 만든다","코코넛 플레이크를 굴려 냉장고에 30분 굳힌다"]},
         {"title":"아몬드 그래놀라","time":"30분","kcal":"380kcal","difficulty":"쉬움","steps":["귀리·슬라이스 아몬드·해바라기씨를 섞는다","꿀·올리브오일·시나몬을 넣어 버무린다","160도 오븐에서 25분 굽는다","식혀서 건포도·크랜베리와 섞는다"]},
     ]},
    {"id":"egg","icon":"🥚","name":"달걀","name_en":"egg","short":"완전식품의 대명사","badge":"단백질 6g","category":"단백질",
     "description":"달걀은 자연이 만든 가장 완벽한 단백질 공급원이에요. 필수아미노산을 모두 함유하고, 난황에는 뇌 건강에 필수인 콜린이 풍부해요. 루테인·제아잔틴이 눈 건강을 지켜줘요.",
     "effects":["근육 합성","뇌 건강","눈 건강","포만감","에너지 공급"],
     "nutrition":{"칼로리":"155kcal","단백질":"13.0g","식이섬유":"0g","탄수화물":"1.1g","지방":"11.0g","콜린":"294mg"},
     "recipes":[
         {"title":"스크램블 에그 아보카도 볼","time":"10분","kcal":"320kcal","difficulty":"쉬움","steps":["달걀 2개에 우유·소금·후추를 넣어 푼다","버터 팬에서 약불로 천천히 젓는다","아보카도를 반으로 갈라 씨를 제거한다","아보카도 위에 스크램블 에그를 얹는다"]},
         {"title":"에그 인 헬","time":"20분","kcal":"240kcal","difficulty":"보통","steps":["팬에 올리브오일·마늘을 볶는다","토마토 소스를 넣고 5분 끓인다","소스에 홈을 만들어 달걀을 깨 넣는다","뚜껑을 덮고 달걀이 익을 때까지 가열한다"]},
     ]},
    {"id":"greek_yogurt","icon":"🥛","name":"그릭요거트","name_en":"greek yogurt","short":"프로바이오틱스·고단백","badge":"장 건강","category":"유제품",
     "description":"그릭요거트는 일반 요거트보다 훨씬 진하고 단백질 함량이 높아요. 유산균이 장내 유익균을 늘려 소화 건강을 개선하고 면역력을 높여줘요.",
     "effects":["장 건강","면역력 강화","뼈 강화","포만감","근육 회복"],
     "nutrition":{"칼로리":"59kcal","단백질":"10.0g","식이섬유":"0g","탄수화물":"3.6g","지방":"0.4g","칼슘":"111mg"},
     "recipes":[
         {"title":"그릭요거트 파르페","time":"5분","kcal":"280kcal","difficulty":"쉬움","steps":["컵에 그릭요거트를 담는다","그래놀라를 올린다","블루베리·딸기·바나나를 올린다","꿀을 드리즐하고 민트로 장식한다"]},
         {"title":"그릭요거트 치킨 마리네이드","time":"25분","kcal":"310kcal","difficulty":"보통","steps":["요거트에 레몬즙·마늘·큐민·파프리카를 섞는다","닭가슴살을 30분 이상 재운다","그릴에서 양면 6분씩 굽는다","허브와 레몬을 곁들여 서브한다"]},
     ]},
    {"id":"broccoli","icon":"🥦","name":"브로콜리","name_en":"broccoli","short":"항암·비타민C 채소의 왕","badge":"항암","category":"채소",
     "description":"브로콜리는 십자화과 채소 중 가장 영양이 풍부해요. 비타민 C 함량이 오렌지보다 높고 설포라판이라는 항암 성분이 풍부해요. 살짝 데치거나 쪄서 먹는 게 영양 보존에 가장 좋아요.",
     "effects":["항암","면역력 강화","소화 개선","뼈 건강","혈당 조절"],
     "nutrition":{"칼로리":"34kcal","단백질":"2.8g","식이섬유":"2.6g","탄수화물":"6.6g","지방":"0.4g","비타민C":"89.2mg"},
     "recipes":[
         {"title":"브로콜리 마늘 볶음","time":"10분","kcal":"120kcal","difficulty":"쉬움","steps":["브로콜리를 한 입 크기로 잘라 30초 데친다","팬에 마늘을 노릇하게 볶는다","브로콜리를 강불에서 2분 볶는다","굴소스·참기름으로 마무리한다"]},
         {"title":"브로콜리 크림수프","time":"25분","kcal":"210kcal","difficulty":"보통","steps":["양파·감자를 올리브오일에 볶는다","브로콜리·채수를 넣고 15분 끓인다","핸드블렌더로 곱게 간다","생크림을 넣어 크리미하게 만든다"]},
     ]},
    {"id":"oats","icon":"🌿","name":"귀리","name_en":"oats","short":"베타글루칸·콜레스테롤 감소","badge":"심장 건강","category":"통곡물",
     "description":"귀리는 '가장 건강한 곡물' 중 하나로, 베타글루칸이라는 수용성 식이섬유가 특히 풍부해요. 콜레스테롤을 낮추고 혈당 급등을 막는 데 효과적이에요.",
     "effects":["콜레스테롤 감소","혈당 조절","포만감","심장 건강","장 건강"],
     "nutrition":{"칼로리":"389kcal","단백질":"17.0g","식이섬유":"10.6g","탄수화물":"66.3g","지방":"6.9g","마그네슘":"177mg"},
     "recipes":[
         {"title":"오버나이트 오츠","time":"5분+냉장8h","kcal":"320kcal","difficulty":"쉬움","steps":["귀리·아몬드밀크를 용기에 담는다","치아씨드·꿀·바닐라를 넣는다","냉장고에 하룻밤 둔다","아침에 과일·견과류를 올린다"]},
         {"title":"바나나 귀리 팬케이크","time":"20분","kcal":"280kcal","difficulty":"쉬움","steps":["바나나를 으깨고 달걀·귀리를 섞는다","시나몬·베이킹파우더를 넣는다","팬에 약불로 양면을 굽는다","메이플시럽과 과일을 곁들인다"]},
     ]},
    {"id":"kimchi","icon":"🥬","name":"김치","name_en":"kimchi","short":"유산균·한국 대표 발효식품","badge":"프로바이오틱스","category":"발효식품",
     "description":"김치는 유네스코 무형문화유산에 등재된 한국의 대표 발효식품이에요. 젖산균이 풍부해 장 건강에 탁월하고, 면역력을 높여줘요. 비타민 C·K와 식이섬유도 풍부해요.",
     "effects":["장 건강","면역 강화","항산화","소화 촉진","체중 관리"],
     "nutrition":{"칼로리":"15kcal","단백질":"1.1g","식이섬유":"1.6g","탄수화물":"2.4g","지방":"0.5g","유산균":"수억 CFU"},
     "recipes":[
         {"title":"김치 볶음밥","time":"15분","kcal":"380kcal","difficulty":"쉬움","steps":["팬에 참기름을 두르고 김치를 볶는다","밥을 넣고 강불에서 볶는다","달걀 프라이를 올린다","김가루·참깨를 뿌려 완성한다"]},
         {"title":"김치 두부 찌개","time":"25분","kcal":"210kcal","difficulty":"쉬움","steps":["돼지고기를 볶다가 김치를 넣는다","물·고춧가루·간장으로 육수를 만든다","두부를 넣고 10분 끓인다","파·깨를 올려 완성한다"]},
     ]},
    {"id":"turmeric","icon":"🟠","name":"강황","name_en":"turmeric","short":"커큐민·항염 슈퍼 향신료","badge":"항염증","category":"향신료",
     "description":"강황은 카레의 노란색을 내는 향신료로, 커큐민이라는 강력한 항염증·항산화 성분을 함유해요. 관절 건강에 도움이 되고 뇌 기능을 향상시키는 효과도 있어요.",
     "effects":["항염증","관절 건강","뇌 기능 향상","항산화","소화 개선"],
     "nutrition":{"칼로리":"354kcal","단백질":"7.8g","식이섬유":"21.1g","탄수화물":"64.9g","지방":"9.9g","커큐민":"3~5%"},
     "recipes":[
         {"title":"황금 우유 (골든 밀크)","time":"8분","kcal":"120kcal","difficulty":"쉬움","steps":["우유 200ml에 강황 1/2작은술을 넣는다","시나몬·생강가루·후추 한 꼬집을 추가한다","중불에서 따뜻하게 데운다","꿀 1작은술을 넣어 완성한다"]},
         {"title":"강황 두부 스크램블","time":"12분","kcal":"200kcal","difficulty":"쉬움","steps":["두부를 손으로 부숴 물기를 제거한다","팬에 올리브오일·마늘을 볶는다","두부·강황·큐민·소금을 넣고 볶는다","시금치·방울토마토를 넣어 마무리한다"]},
     ]},
    {"id":"banana","icon":"🍌","name":"바나나","name_en":"banana","short":"칼륨·에너지 즉시 보충","badge":"운동 후 간식","category":"과일",
     "description":"바나나는 운동 전후 가장 좋은 스낵이에요. 칼륨이 풍부해 근육 경련을 예방하고, 빠르게 소화되는 탄수화물이 즉각적인 에너지를 공급해줘요. 트립토판이 기분을 좋게 해줘요.",
     "effects":["에너지 보충","근육 경련 예방","기분 개선","소화 개선","혈압 조절"],
     "nutrition":{"칼로리":"89kcal","단백질":"1.1g","식이섬유":"2.6g","탄수화물":"23.0g","지방":"0.3g","칼륨":"358mg"},
     "recipes":[
         {"title":"바나나 아이스크림","time":"5분+냉동3h","kcal":"100kcal","difficulty":"쉬움","steps":["바나나를 슬라이스해 냉동한다","냉동 바나나를 블렌더에 넣고 크리미하게 간다","땅콩버터·코코아 파우더를 넣는다","그릇에 담고 견과류를 올린다"]},
         {"title":"바나나 팬케이크 (2재료)","time":"15분","kcal":"180kcal","difficulty":"쉬움","steps":["바나나 1개를 으깬다","달걀 2개를 넣어 잘 섞는다","팬에 한 큰술씩 올려 약불로 굽는다","메이플시럽·과일을 곁들인다"]},
     ]},
    {"id":"garlic","icon":"🧄","name":"마늘","name_en":"garlic","short":"알리신·천연 항생 효과","badge":"면역 강화","category":"향신료",
     "description":"마늘은 '천연 항생제'로 불릴 만큼 강력한 기능성 식품이에요. 알리신이 항균·항바이러스 효과를 발휘하고, 심혈관 건강을 개선해줘요. 날것으로 먹을 때 효능이 가장 높아요.",
     "effects":["면역 강화","항균·항바이러스","심혈관 건강","혈압 조절","항암"],
     "nutrition":{"칼로리":"149kcal","단백질":"6.4g","식이섬유":"2.1g","탄수화물":"33.1g","지방":"0.5g","알리신":"풍부"},
     "recipes":[
         {"title":"마늘 올리브오일 파스타","time":"20분","kcal":"380kcal","difficulty":"쉬움","steps":["파스타를 소금물에 삶는다","팬에 올리브오일을 두르고 마늘을 볶는다","파스타·면수를 넣어 섞는다","페퍼론치노·파마산·파슬리로 마무리한다"]},
         {"title":"흑마늘 꿀 드레싱 샐러드","time":"10분","kcal":"160kcal","difficulty":"쉬움","steps":["흑마늘 3알을 으깬다","꿀·발사믹·올리브오일·소금을 섞는다","샐러드 채소를 준비한다","드레싱을 뿌려 완성한다"]},
     ]},
    {"id":"chia","icon":"⚫","name":"치아씨드","name_en":"chia seeds","short":"오메가-3·식이섬유 슈퍼씨앗","badge":"슈퍼푸드","category":"씨앗",
     "description":"치아씨드는 작은 씨앗이지만 영양 밀도가 매우 높아요. 물을 흡수하면 젤 형태가 되어 포만감을 오래 유지시켜줘요. 오메가-3·칼슘·인이 풍부해 뼈 건강과 심장 건강에 좋아요.",
     "effects":["포만감","뼈 강화","심장 건강","혈당 조절","소화 개선"],
     "nutrition":{"칼로리":"486kcal","단백질":"16.5g","식이섬유":"34.4g","탄수화물":"42.1g","지방":"30.7g","칼슘":"631mg"},
     "recipes":[
         {"title":"치아씨드 푸딩","time":"5분+냉장4h","kcal":"200kcal","difficulty":"쉬움","steps":["치아씨드 3큰술에 아몬드밀크 1컵을 붓는다","꿀·바닐라를 넣고 잘 섞는다","냉장고에 최소 4시간 둔다","과일·견과류·그래놀라를 올린다"]},
         {"title":"치아씨드 레몬에이드","time":"10분","kcal":"80kcal","difficulty":"쉬움","steps":["물 500ml에 치아씨드를 5분 불린다","레몬즙·꿀을 넣는다","민트 잎을 넣는다","얼음 넣어 차갑게 마신다"]},
     ]},
    {"id":"walnut","icon":"🫀","name":"호두","name_en":"walnut","short":"오메가-3·뇌 건강 견과류","badge":"뇌 건강","category":"견과류",
     "description":"호두는 뇌 건강에 가장 좋은 견과류예요. 식물성 오메가-3 지방산이 풍부하고 폴리페놀이 산화 스트레스를 줄여줘요. 하루 7알 정도가 적당해요.",
     "effects":["뇌 건강","심장 보호","항산화","염증 억제","수면 개선"],
     "nutrition":{"칼로리":"654kcal","단백질":"15.2g","식이섬유":"6.7g","탄수화물":"13.7g","지방":"65.2g","오메가3":"9.1g"},
     "recipes":[
         {"title":"호두 바나나 스무디","time":"5분","kcal":"280kcal","difficulty":"쉬움","steps":["바나나·호두·아몬드밀크를 블렌더에 넣는다","꿀·시나몬을 넣는다","곱게 갈아준다","컵에 담고 호두를 올린다"]},
         {"title":"호두 시금치 샐러드","time":"12분","kcal":"240kcal","difficulty":"쉬움","steps":["호두를 팬에 살짝 볶는다","시금치·사과·크랜베리를 준비한다","발사믹 드레싱을 만든다","재료를 섞고 호두를 올린다"]},
     ]},
]

# ── 세션 상태 ─────────────────────────────────────────────────────────
for k, v in [("selected", set()), ("detail_id", None), ("search_results", []), ("search_done", False), ("community_posts", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

def toggle(ingr_id):
    if ingr_id in st.session_state.selected:
        st.session_state.selected.discard(ingr_id)
    else:
        st.session_state.selected.add(ingr_id)

def do_search(q):
    q = q.strip().lower()
    if not q:
        return []
    return [i for i in INGREDIENTS if q in i["name"] or q in i["name_en"].lower() or q in i["short"].lower() or q in i["category"].lower()]

# ── 네비게이션 ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav">
    <div class="nav-logo"><span class="nav-dot"></span>{APP_NAME}</div>
    <div class="nav-tag">{APP_TAGLINE}</div>
</div>""", unsafe_allow_html=True)

# ── 탭 ────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🌿 식재료 탐색", "🍽 레시피", "📸 음식 사진 공유"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — 식재료 탐색
# ════════════════════════════════════════════════════════════════════
with tab1:

    # 히어로
    st.markdown(f"""
    <div class="hero">
        <p class="hero-eye">🌿 GOOD FOOD STARTS HERE</p>
        <h1 class="hero-title">오늘의 식재료를<br>탐색해보세요</h1>
        <p class="hero-sub">22가지 식재료 수록 — 아래 추천 6가지를 살펴보거나,<br>검색창에 이름을 입력해 원하는 식재료를 찾아보세요</p>
    </div>""", unsafe_allow_html=True)

    # ── 검색창 ───────────────────────────────────────────────────────
    sc1, sc2 = st.columns([5, 1])
    with sc1:
        search_q = st.text_input(
            "식재료 검색",
            placeholder="예: 시금치, broccoli, 견과류, 발효식품 ...",
            label_visibility="visible",
            key="search_box"
        )
    with sc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_btn = st.button("검색 🔍", use_container_width=True, key="search_btn")

    if search_btn:
        results = do_search(search_q)
        st.session_state.search_results = results
        st.session_state.search_done = True
        st.session_state.detail_id = None

    # ── 검색 결과 ────────────────────────────────────────────────────
    if st.session_state.search_done:
        results = st.session_state.search_results
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if not results:
            st.warning(f"'{search_q}'에 해당하는 식재료를 찾지 못했어요. 다른 이름으로 검색해보세요.")
        else:
            st.markdown(f'<p class="sec-sub">🔍 검색 결과 {len(results)}개</p>', unsafe_allow_html=True)
            for ing in results:
                is_sel = ing["id"] in st.session_state.selected
                rc1, rc2, rc3 = st.columns([6, 1, 1])
                with rc1:
                    badges = f'<span class="s-badge">{ing["badge"]}</span><span class="s-badge">{ing["category"]}</span>'
                    st.markdown(f"""
                    <div class="search-card">
                        <span class="search-icon">{ing['icon']}</span>
                        <div class="search-info">
                            <div class="search-name">{ing['name']} <span style="font-size:13px;color:#7A8A70;">({ing['name_en']})</span></div>
                            <div class="search-short">{ing['short']}</div>
                            <div class="search-badges">{badges}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with rc2:
                    if st.button("해제" if is_sel else "선택", key=f"sr_sel_{ing['id']}", use_container_width=True):
                        toggle(ing["id"]); st.rerun()
                with rc3:
                    if st.button("정보", key=f"sr_info_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                        st.rerun()

                # 상세 설명
                if st.session_state.detail_id == ing["id"]:
                    eff_html = "".join(f'<span class="eff">{e}</span>' for e in ing["effects"])
                    nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in ing["nutrition"].items())
                    st.markdown(f"""
                    <div class="detail-box">
                        <div class="d-title">{ing['icon']} {ing['name']}</div>
                        <div class="d-desc">{ing['description']}</div>
                        <div class="d-lbl">주요 효능</div>
                        <div class="effects">{eff_html}</div>
                        <div class="d-lbl">영양 성분 (100g 기준)</div>
                        <div class="nut-grid">{nut_html}</div>
                    </div>""", unsafe_allow_html=True)

        close_c = st.columns([4, 1])[1]
        with close_c:
            if st.button("검색 닫기 ✕", use_container_width=True):
                st.session_state.search_done = False
                st.session_state.search_results = []
                st.session_state.detail_id = None
                st.rerun()

    # ── 추천 식재료 6개 (검색 결과 없을 때만 표시) ────────────────────
    if not st.session_state.search_done:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">오늘의 추천 식재료</p>', unsafe_allow_html=True)
        st.markdown('<p class="sec-sub">선택 버튼을 누르면 레시피 탭에서 레시피를 확인할 수 있어요 · 정보 버튼으로 상세 영양 정보 확인</p>', unsafe_allow_html=True)

        featured_ings = [i for i in INGREDIENTS if i["id"] in FEATURED]

        # 3열 × 2행
        cols = st.columns(3)
        for idx, ing in enumerate(featured_ings):
            is_sel = ing["id"] in st.session_state.selected
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="ingr-card {'sel' if is_sel else ''}">
                    <div class="i-icon">{ing['icon']}</div>
                    <div class="i-name">{'✓ ' if is_sel else ''}{ing['name']}</div>
                    <div class="i-short">{ing['short']}</div>
                    <span class="i-badge">{ing['badge']}</span>
                </div>""", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("해제" if is_sel else "선택", key=f"f_sel_{ing['id']}", use_container_width=True):
                        toggle(ing["id"]); st.rerun()
                with b2:
                    if st.button("정보", key=f"f_info_{ing['id']}", use_container_width=True):
                        st.session_state.detail_id = None if st.session_state.detail_id == ing["id"] else ing["id"]
                        st.rerun()

                # 상세 설명
                if st.session_state.detail_id == ing["id"]:
                    eff_html = "".join(f'<span class="eff">{e}</span>' for e in ing["effects"])
                    nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in ing["nutrition"].items())
                    # 3열 안에서 detail은 아래 full-width로 빼줌
                    st.session_state["_pending_detail"] = ing
        
        # 상세 설명 full-width 출력
        if st.session_state.detail_id and not st.session_state.search_done:
            d = next((i for i in featured_ings if i["id"] == st.session_state.detail_id), None)
            if d:
                eff_html = "".join(f'<span class="eff">{e}</span>' for e in d["effects"])
                nut_html = "".join(f'<div class="nut-item"><div class="nut-val">{v}</div><div class="nut-lbl">{k}</div></div>' for k,v in d["nutrition"].items())
                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="detail-box">
                    <div class="d-title">{d['icon']} {d['name']} <span style="font-size:14px;color:#7A8A70;">({d['name_en']})</span></div>
                    <div class="d-desc">{d['description']}</div>
                    <div class="d-lbl">주요 효능</div>
                    <div class="effects">{eff_html}</div>
                    <div class="d-lbl">영양 성분 (100g 기준)</div>
                    <div class="nut-grid">{nut_html}</div>
                </div>""", unsafe_allow_html=True)
                close_c = st.columns([5, 1])[1]
                with close_c:
                    if st.button("닫기 ✕", use_container_width=True, key="close_detail"):
                        st.session_state.detail_id = None; st.rerun()

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#fff;border:1.5px dashed #C5DDB8;border-radius:12px;padding:20px 24px;text-align:center;">
            <p style="font-size:13px;color:#4A5A40;margin:0;">
                🔍 <strong style="color:#2C3A1E;">22가지 식재료</strong> 전체를 탐색하려면 위 검색창에 이름을 입력해보세요<br>
                <span style="font-size:12px;color:#7A8A70;">시금치 · 고구마 · 달걀 · 귀리 · 김치 · 강황 · 마늘 · 바나나 · 호두 · 치아씨드 · 브로콜리 · 병아리콩 · 아몬드 · 그릭요거트 · 귀리 ···</span>
            </p>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 2 — 레시피
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="sec-title">레시피</p>', unsafe_allow_html=True)

    if not st.session_state.selected:
        st.markdown('<div class="empty">🥗<br><br>식재료 탐색 탭에서 재료를 선택하면<br>여기에 레시피가 나타나요</div>', unsafe_allow_html=True)
    else:
        sel_names = [i["name"] for i in INGREDIENTS if i["id"] in st.session_state.selected]
        chips = "".join(f'<span class="sel-chip">🌿 {n}</span>' for n in sel_names)
        st.markdown(f'<div style="margin-bottom:18px;">{chips}</div>', unsafe_allow_html=True)

        cc = st.columns([5, 1])[1]
        with cc:
            if st.button("선택 초기화", use_container_width=True):
                st.session_state.selected.clear(); st.rerun()

        for ing in INGREDIENTS:
            if ing["id"] not in st.session_state.selected: continue
            for rec in ing["recipes"]:
                dc = {"쉬움":"#2C5F21","보통":"#7A5C00","어려움":"#8B0000"}.get(rec["difficulty"],"#555")
                steps_html = "".join(f'<div class="r-step"><span class="r-num">{j+1}</span><span>{s}</span></div>' for j,s in enumerate(rec["steps"]))
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
                    if st.button("📸 사진 공유", key=f"go_share_{ing['id']}_{rec['title']}", use_container_width=True):
                        st.session_state["pending_recipe"] = rec["title"]
                        st.info(f"📸 음식 사진 공유 탭에서 **{rec['title']}** 사진을 올려보세요!")

# ════════════════════════════════════════════════════════════════════
# TAB 3 — 음식 사진 공유
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="sec-title">📸 음식 사진 공유</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">직접 만든 요리 사진을 올리고 서로 공유해요</p>', unsafe_allow_html=True)

    # ── 업로드 폼 ─────────────────────────────────────────────────────
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">내 요리 올리기</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-sub">사진과 간단한 정보를 입력해주세요</div>', unsafe_allow_html=True)

    uf1, uf2 = st.columns(2)
    with uf1:
        nickname = st.text_input("닉네임", placeholder="예: 건강요리사 👩‍🍳")
    with uf2:
        recipe_name = st.text_input("레시피 이름", placeholder="예: 퀴노아 샐러드 볼",
                                     value=st.session_state.get("pending_recipe",""))
    note = st.text_area("한마디", placeholder="맛 후기나 나만의 팁을 남겨보세요 😋", height=90)
    photo_file = st.file_uploader("사진 업로드", type=["jpg","jpeg","png"])

    if st.button("🌿 공유하기", use_container_width=True):
        if not nickname:
            st.warning("닉네임을 입력해주세요.")
        elif not recipe_name:
            st.warning("레시피 이름을 입력해주세요.")
        elif not photo_file:
            st.warning("사진을 업로드해주세요.")
        else:
            img_b64 = base64.b64encode(photo_file.read()).decode()
            ext  = photo_file.name.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            st.session_state.community_posts.insert(0, {
                "nickname": nickname, "recipe": recipe_name,
                "note": note, "img_b64": img_b64, "mime": mime,
                "time": datetime.now().strftime("%Y.%m.%d %H:%M"),
                "likes": 0,
            })
            st.session_state["pending_recipe"] = ""
            st.success(f"🎉 '{recipe_name}' 사진이 공유됐어요!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── 피드 ─────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.community_posts:
        st.markdown("""
        <div class="no-posts">
            <div class="no-posts-icon">🍽</div>
            <div class="no-posts-text">
                아직 공유된 사진이 없어요<br>
                첫 번째 요리 사진을 올려보세요!
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        total = len(st.session_state.community_posts)
        st.markdown(f'<p style="font-size:13px;color:#7A8A70;margin-bottom:20px;">총 <strong style="color:#2C3A1E;">{total}개</strong>의 요리 사진</p>', unsafe_allow_html=True)

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
                        st.session_state.community_posts[idx]["likes"] += 1; st.rerun()
                with dc2:
                    if st.button("삭제", key=f"del_{idx}", use_container_width=True):
                        st.session_state.community_posts.pop(idx); st.rerun()

# ── 푸터 ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:56px;padding:18px 0;border-top:1px solid #E2DDD4;text-align:center;font-size:11px;color:#7A8A70;">
    {APP_NAME} · {APP_TAGLINE} · SKKU Art Project
</div>""", unsafe_allow_html=True)
