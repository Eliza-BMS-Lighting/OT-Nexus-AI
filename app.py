# -*- coding: utf-8 -*-
import streamlit as st
import openai
import os
import pandas as pd

# 1. 網頁基本設定 (專業臨床與教學督導風格)
st.set_page_config(
    page_title="OT-Nexus AI: 青少年與成人情緒調節團體企畫助理",
    page_icon="🧠",
    layout="wide"
)

# 2. 本機參考資料夾設定
REFERENCE_FOLDER = "clinical_references"
os.makedirs(REFERENCE_FOLDER, exist_ok=True)

# 讀取本機/雲端共享文獻的函數
def load_local_references():
    local_content = ""
    if os.path.exists(REFERENCE_FOLDER):
        files = [f for f in os.listdir(REFERENCE_FOLDER) if f.endswith(('.txt', '.md'))]
        for file in files:
            file_path = os.path.join(REFERENCE_FOLDER, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    local_content += f"\n\n=== 雲端共享文獻：{file} ===\n"
                    local_content += f.read()
            except Exception as e:
                pass
    return local_content

# 3. 專業臨床學術理論架構對照表
OT_THEORIES = [
    {"理論架構": "人類職能模式 (MOHO)", "職能介入應用": "探索職能動機(意志)、習慣、社會角色、生活節奏與環境支持"},
    {"理論架構": "PEO／PEOP 模式", "職能介入應用": "分析個人能力(P)、環境條件(E)與活動要求(O)是否適配並進行調適"},
    {"理論架構": "加拿大職能表現與投入模式 (CMOP-E)", "職能介入應用": "從自我照顧、生產力與休閒中選擇有意義的調節與投入活動"},
    {"理論架構": "感覺統合理論／感覺調節", "臨床指標項目": "依過度喚醒(Hyper-arousal)或低度喚醒(Hypo-arousal)選擇本體覺、觸覺等感官活動"},
    {"理論架構": "認知行為取向 (CBT)", "臨床指標項目": "連結情境、自動化想法、情緒、生理反應與適應性行為選擇"},
    {"理論架構": "辯證行為治療技巧 (DBT)", "臨床指標項目": "正念覺察、痛苦耐受(Distress Tolerance)、情緒調節與人際效能訓練"},
    {"理論架構": "復元模式 (Recovery Model)", "臨床指標項目": "強調希望感、主動選擇、提升自我效能及有意義的生活職能參與"},
    {"理論架構": "社會情緒學習 (SEL)", "臨床指標項目": "培養自我覺察、自我管理、社會覺察及人際關係建立能力"},
    {"理論架構": "活躍老化與生命回顧", "臨床指標項目": "維繫自主權、重塑生命故事、建立具期待感的生活節奏與角色認同"}
]

# 核心 10 大職能介入方案資料庫 (完全比照上傳之 text 內容)
OT_PROGRAMS = {
    "方案一：心情色彩研究室": {
        "activity": "流動畫／壓克力刮畫創作",
        "issue": "難以辨識或表達情緒、難以說明內在感受、情緒覺察障礙。",
        "concept": "成員使用顏色、線條、方向及材料流動呈現當下情緒。活動的治療價值來自選擇、感官經驗、動作控制、容許不確定及作品完成，不以作品好壞或心理分析為重點。",
        "tools": "畫紙、壓克力顏料、刮板、滴管、吸管、圍裙、桌墊及清潔用品。",
        "steps": (
            "1. 選擇代表目前情緒的 2～3 種顏色。\n"
            "2. 觀察顏料的濃淡、流速及混合變化。\n"
            "3. 使用滴、刮、吹或轉動畫紙完成創作並為作品命名。\n"
            "4. 分享創作過程中舒服、最困難或意外的部分。\n"
            "5. 連結自己平時面對情緒變化的調節方法。"
        ),
        "mechanism": "• 感官與動作調節。\n• 非語言情緒表達。\n• 接受無法完全控制的結果。\n• 經驗選擇與完成感。",
        "grading": (
            "• 簡易：限制三種顏色，提供步驟示範。\n"
            "• 進階：設定兩種不同情緒，呈現其轉變或共存。"
        ),
        "application": "引導成員思考，當情緒難以用語言表達時，可否先透過顏色、書寫、音樂或動作整理自己。"
    },
    "方案二：我的安心飲品實驗室": {
        "activity": "製作個人化無酒精飲品",
        "issue": "壓力過高、感官過載、缺乏自我照顧習慣、需要調節喚醒狀態。",
        "concept": "透過清洗、測量、調配、攪拌與品嚐，練習放慢速度、覺察感官經驗及依序完成任務。",
        "tools": "水果、茶包、氣泡水、量杯、湯匙、紙杯、冰塊、托盤、視覺化食譜及清潔用品。",
        "steps": (
            "1. 觀察不同材料的顏色、香氣與味道。\n"
            "2. 選擇自己希望的飲品感受（如清爽、溫暖或提振）並依比例調配。\n"
            "3. 緩慢品嚐前三口，辨識味覺與身體反應並為其命名。\n"
            "4. 設計適合自己的下課、下班或睡前轉換儀式。"
        ),
        "mechanism": "• 多感官覺察。\n• 任務順序與注意力集中。\n• 選擇與控制感。\n• 建立健康的自我照顧儀式。",
        "grading": (
            "• 簡易：使用預先分裝材料及圖片食譜。\n"
            "• 進階：自行設計比例，並考量預算、營養及適用情境。"
        ),
        "application": "須事前確認過敏、吞嚥及飲食限制；輔助成員建立健康的自我照顧轉換儀式。"
    },
    "方案三：把怒氣揉成形": {
        "activity": "黏土容器或情緒角色塑形",
        "issue": "憤怒、衝動、身體緊繃、人際衝突、衝動控制與需求表達困難。",
        "concept": "運用揉、壓、推、捏及塑形等本體覺活動，安全釋放身體張力，再將無形的憤怒轉化為可觀察、可調整的作品。",
        "tools": "輕黏土或陶土、墊板、塑形工具、滾輪、顏料及圍裙。",
        "steps": (
            "1. 以黏土呈現「怒氣出現時的形狀」。\n"
            "2. 使用揉、壓或推等動作調整身體張力。\n"
            "3. 將原有造形改造成容器、角色或保護物並加入代表「暫停」或「保護」的元素。\n"
            "4. 分享改造過程中的選擇與困難，連結生活中的安全暫停及需求表達。"
        ),
        "mechanism": "• 本體覺與觸覺調節。\n• 衝動延宕。\n• 具體化與轉化情緒。\n• 問題解決及挫折耐受。",
        "grading": (
            "• 簡易：完成單一情緒造形。\n"
            "• 進階：將情緒造形轉變成具有功能的容器或物品。"
        ),
        "application": "帶領者不替成員解釋作品。若成員情緒升高，先停止討論事件，回到材料操作本體覺調節。"
    },
    "方案四：煩惱分類收納盒": {
        "activity": "紙盒改造與功能性收納盒製作",
        "issue": "焦慮、反覆思考、事情混亂、無法開始行動、認知負荷過重。",
        "concept": "成員將回收紙盒改造成「現在處理、稍後處理、需要協助」的功能性收納盒，以實際分類和製作活動練習組織、排序及問題解決。",
        "tools": "回收紙盒、色紙、剪刀、膠水、標籤、裝飾材料及便利貼。",
        "steps": (
            "1. 選擇紙盒並規劃用途。\n"
            "2. 測量、裁切及黏貼外觀，將收納盒分成三個區域。\n"
            "3. 使用便利貼寫下近期擔心或待辦事項。\n"
            "4. 將事項分類放入不同區域，從「現在處理」中選擇一項最小行動。"
        ),
        "mechanism": "• 外化反覆思考。\n• 組織與分類。\n• 降低認知負荷。\n• 將焦慮轉化為可執行行動。"
    },
    "方案五：一份給自己的能量餐": {
        "activity": "製作免開火三明治、飯糰或營養餐盒",
        "issue": "情緒低落、生活退縮、缺乏動力、自我照顧不足、活動啟動困難。",
        "concept": "透過準備一份可食用、可完成的餐點，增加活動啟動、程序執行、選擇及照顧自己的具體經驗。",
        "tools": "吐司或米飯、蔬果、蛋白質食材、餐盒、餐具、手套、圖像食譜及清潔用品。",
        "steps": (
            "1. 從有限選項中選擇主食與配料。\n"
            "2. 依步驟清洗、分裝、組合，完成餐點擺盤並命名。\n"
            "3. 品嚐並記錄活動前後的精神與成就感。\n"
            "4. 規劃一項本週可完成的簡易自我照顧任務。"
        ),
        "mechanism": "• 行為啟動 (Behavioral Activation)。\n• 感官刺激與程序完成感。\n• 建立日常自我照顧與健康管理。"
    },
    "方案六：我的身分拼貼誌": {
        "activity": "製作個人迷你刊物（zine）或摺頁書",
        "issue": "自我認同模糊、自我概念模糊、過度依賴外部或他人評價。",
        "concept": "成員透過剪貼、書寫與編排，完成一本呈現角色、興趣、能力、重要關係及未來探索方向的個人小誌。",
        "tools": "A3或A4紙、雜誌、照片、圖卡、剪刀、膠水、色筆、印章及貼紙。",
        "steps": (
            "1. 將紙張摺成迷你刊物，各頁分別呈現：角色、興趣、完成的事、重要他人與未來探索。\n"
            "2. 設計封面與名稱，選擇願意分享的一頁分享。\n"
            "3. 規劃一項新的興趣或角色探索活動。"
        ),
        "mechanism": "• 建立多元自我概念。\n• 整理生命經驗。\n• 增加自主選擇與勝任感。"
    },
    "方案七：價值市集": {
        "activity": "模擬市集競標與生活資源配置遊戲",
        "issue": "價值澄清困難、生涯選擇、家庭期待與決策衝突。",
        "concept": "成員運用有限代幣競標健康、自由、穩定、成就、家庭、友誼等生活價值，從實際取捨中覺察個人優先順序。",
        "tools": "價值商品卡、代幣、競標牌、購物袋、記錄表及情境卡。",
        "steps": (
            "1. 每人獲得相同代幣，預先規劃與競標價值商品。\n"
            "2. 檢視最後取得與放棄的價值。\n"
            "3. 比較目前生活時間與所選價值是否一致，並設定一項本週實踐價值之行動。"
        ),
        "mechanism": "• 練習選擇與承擔代價。\n• 增加價值清晰度。\n• face 選擇中的遺憾與不確定。"
    },
    "方案八：我的真實生活攝影展": {
        "activity": "生活攝影與四格照片故事製作",
        "issue": "社群比較、外表焦慮、自我否定、過度關注他人生活。",
        "concept": "成員拍攝自己真實生活中具有意義、努力、支持或恢復感的片段，製作一組不以完美形象為目的的生活照片故事。",
        "tools": "手機或相機、照片印表機或數位簡報工具、卡紙、標題卡及貼紙。",
        "steps": (
            "1. 選擇「我的日常力量」主題。\n"
            "2. 拍攝並選取四格照片（完成的小事、支持者、恢復地方、想投入的活動）。\n"
            "3. 撰寫真實說明，分享願公開的部分並規劃增加真實生活參與。"
        ),
        "mechanism": "• 注意力轉向真實生活。\n• 辨識優勢與有意義職能。\n• 重建完整自我敘事。"
    },
    "方案九：一週生活便當盒": {
        "activity": "利用分格盒設計一週職能平衡配置",
        "issue": "過勞與角色失衡、角色衝突、缺乏休閒及恢復活動。",
        "concept": "將一週可用的時間與精力視為容量有限的便當盒，使用不同顏色的活動卡安排自我照顧、工作、休閒、社交及休息。",
        "tools": "分格盒、不同顏色活動卡、角色卡、時間籌碼及一週行程表。",
        "steps": (
            "1. 為不同職能領域設定顏色，使用籌碼呈現目前一週。\n"
            "2. 觀察過滿、空白或擠壓的區塊。\n"
            "3. 重新配置理想可行的一週，選擇改善計畫並放入真實行事曆。"
        ),
        "mechanism": "• 視覺化角色負荷。\n• 提升時間與精力覺察。\n• 練習設定界線與活動取捨。"
    },
    "方案十：人際任務桌遊": {
        "activity": "合作式情境桌遊",
        "issue": "不敢拒絕、不會求助、人際界線混淆、人際衝突。",
        "concept": "成員透過抽取情境、角色與限制卡，在遊戲規則下完成拒絕、協商、求助及表達需求等任務。",
        "tools": "遊戲地圖、骰子、棋子、情境卡、任務卡、限制卡、句型卡及代幣。",
        "steps": (
            "1. 輪流抽取人際情境卡，依任務要求選擇接受、拒絕、協商或求助。\n"
            "2. 隊友提供替代回應並抽取限制卡練習，共同完成人際任務。"
        ),
        "mechanism": "• 在安全環境中預演人際反應。\n• 增加回應彈性。\n• 建立同儕支持及問題解決經驗。"
    }
}

# 3. 網頁視覺與側邊欄設計 (專業黑/藍色調，凸顯醫學與督導定位)
st.title("🧠 OT-Nexus AI 職能治療數位督導系統")
st.subheader("【青少年與成人情緒調節團體與活動設計】")
st.write("本系統作為 **職能治療學系學生** 進行情緒調節活動分析、臨床推理 (Clinical Reasoning) 與團體企畫書設計的**學習鷹架**。")
st.markdown("---")

# 側邊欄設計
st.sidebar.image("https://img.icons8.com/illustrations/lex/112/brain.png", width=90)
st.sidebar.header("🧭 臨床督導導航儀")

# 【甲方案】安全讀取 OpenAI API 金鑰
api_key = ""
api_key_configured = False

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
    api_key_configured = True
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")
    api_key_configured = True

# 載入相容 OpenAI 1.0.0+ 之最新 SDK Client
client = None
if api_key_configured:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        pass

# ==========================================
# 🌟 【方案 B】雲端實時文獻拖曳上傳器 (Web Uploader)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("📤 雲端擴充：上傳臨床新指引")
uploaded_files = st.sidebar.file_uploader(
    "請拖曳或上傳 .txt / .md 臨床指引文件：", 
    type=["txt", "md"], 
    accept_multiple_files=True,
    help="任何治療師或學生在此處上傳新文獻後，系統後台會即時讀取並將其融入第二步的 AI 督導決策大腦中！"
)

# 讀取上傳檔案的文字內容
cloud_reference_text = ""
if uploaded_files:
    st.sidebar.success(f"📈 成功導入 {len(uploaded_files)} 個雲端自訂文獻！")
    for uploaded_file in uploaded_files:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            cloud_reference_text += f"\n\n=== 雲端即時文獻：{uploaded_file.name} ===\n{file_content}"
            st.sidebar.text(f"📄 {uploaded_file.name} (已學會)")
        except Exception as e:
            st.sidebar.error(f"解析 {uploaded_file.name} 失敗：{str(e)}")
else:
    st.sidebar.info("💡 提示：您可直接拖入「生氣冷靜指引.txt」，AI 會即時將其學會並融入對話！")

# 側邊欄：指南快速檢索
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 實務方案與步驟")
target_group = st.sidebar.selectbox("請選擇方案進行指南導航：", list(OT_PROGRAMS.keys()))

if target_group:
    prog = OT_PROGRAMS[target_group]
    with st.sidebar.expander(f"🔍 查看 {target_group} 詳情"):
        st.markdown(f"**🎯 核心媒介活動：**\n`{prog['activity']}`")
        st.markdown(f"**📌 適用主要議題：**\n{prog['issue']}")
        st.markdown(f"**💡 活動概念設計：**\n{prog['concept']}")
        st.markdown(f"**🛠️ 設備與材料：**\n{prog['tools']}")
        st.markdown(f"**👣 標準實施步驟：**\n{prog['steps']}")
        st.markdown(f"**💓 情緒調節機制：**\n{prog['mechanism']}")

# 側邊欄顯示理論架構 (MOHO, PEO, CMOP-E...)
with st.sidebar.expander("📚 臨床理論架構與介入對照表"):
    df_theories = pd.DataFrame(OT_THEORIES)
    st.dataframe(df_theories, hide_index=True)

# 4. 主畫面：Section 1 - 臨床個案情境分析與活動分級模組
st.header("📋 第一階段：個案職能需求分析與分級治療設計")
st.write("請治療師或實習生依據評估與觀察，輸入個案身心訊號與情境。系統將依據職能治療核心原理，即時生成客製化的活動分析報告與 SOAP 記錄草稿：")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 👥 1. 服務對象特性 (Target Population)")
    user_age = st.selectbox("• 目標年齡群組：", ["青少年 (Adolescents)", "成人 (Adults)", "銀髮族 (The Elderly)"])
    member_count = st.text_input("• 團體人數：", "8 人")
    diagnosis_char = st.text_input("• 診斷或功能特性：", "輕度憂鬱與社交焦慮個案")
    cognitive_comm = st.text_input("• 認知與溝通能力：", "具備基本語言理解，但難以口語清晰表達情緒感受")
    motor_sensory = st.text_input("• 動作與感覺特性：", "感覺調節障礙、對高分貝聲音敏感")
    experiences = st.text_input("• 興趣與生活經驗：", "喜歡手作與手繪創作、有使用社群媒體習慣")

    st.markdown("### 🏢 2. 場域與限制條件 (Contextual Venue)")
    venue_type = st.text_input("• 介入場域：", "精神科日間病房 (Day Hospital)")
    group_type = st.selectbox("• 介入型式：", ["團體方案 (Group)", "個別活動 (Individual)"])
    available_time = st.text_input("• 可用時間：", "60 分鐘")
    budget_tools = st.text_input("• 可用設備及預算限制：", "低預算、現場有手作回收紙盒、色紙與基本文具")

with col2:
    st.markdown("### 🎯 3. 主要臨床議題與職能問題 (Core Issues)")
    case_event = st.text_input("• 主要情緒與觸發情境：", "當工作任務堆積或訊息未獲回覆時產生焦慮")
    physical_arousal = st.text_input("• 常見身體反應訊號：", "心跳變快、手握緊、呼吸急促且焦慮 7 分")
    impacted_occupation = st.text_input("• 受到影響的生活職能：", "工作表現下降、作息規律性失調、睡眠品質差")
    target_ability = st.text_input("• 預計改善之能力：", "時間組織與排序能力、情緒覺察與降低認知負荷")
    safety_concern = st.text_input("• 需注意的安全或健康狀況：", "避免使用美工刀等利器，維持情緒安全氛圍")

    st.markdown("### 🧪 4. 期待產出方案與理論媒介 (Expected Output)")
    target_program = st.selectbox("• 預選媒合活動方案：", list(OT_PROGRAMS.keys()))
    theory_link = st.selectbox("• 預計連結之職能治療理論 (OT Theory)：", [t["理論架構"] for t in OT_THEORIES])
    activity_level = st.selectbox("• 方案設計難度分級需求：", ["簡易", "中等", "進階"])

if st.button("🚀 生成標準化職能活動企畫與評量分析"):
    selected_act = OT_PROGRAMS[target_program]
    st.success("✨ 職能治療臨床介入企畫方案生成成功！")
    
    st.markdown("### 📝 職能活動企畫書與臨床推理初稿")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.info(f"**🎯 推薦核心方案：{target_program} — {selected_act['activity']}**")
        st.markdown(f"**• 主要議題：** {selected_act['issue']}")
        st.markdown(f"**• 概念原理：** {selected_act['concept']}")
        st.markdown(f"**• 標準實施步驟：**\n{selected_act['steps']}")
        st.markdown(f"**• 理論學理連結：** 連結【{theory_link}】以「生活中的職能參與」為介入核心媒介，分析個案【{case_event}】時的調節反應。")
    with col_b:
        st.warning("**📝 臨床電子病歷 SOAP 紀錄草稿 (SOAP Note Draft)**")
        soap_box = f"""
【S (Subjective) 主觀敘述】：
個案主訴「{case_event}」，面臨狀況時自覺心率加快。

【O (Objective) 客觀觀察】：
個案於團體中呈現「{physical_arousal}」生理反應，自覺目前壓力強度為 {arousal_intensity if 'arousal_intensity' in locals() else 7} 分。

【A (Assessment) 臨床評估】：
個案因職能角色負荷與焦慮反覆思考，干擾其「{impacted_occupation}」之職能投入。本次介入連結「{theory_link}」架構，提供「{target_program}」作為調節媒介。

【P (Plan) 介入計畫】：
預計引導個案進行「{selected_act['activity']}」。藉由活動中的非語言表達、選擇與完成經驗，提升個案的「{target_ability}」。後續將評估其能否將策略遷移至日常生活中。
"""
        st.code(soap_box, language="markdown")

st.markdown("---")

# 5. 主畫面：Section 2 - 臨床數位督導與個案研討 AI 對話模組
st.header("💬 第二階段：臨床專家督導與個案決策 AI 對話")
st.write("本對話模組為 **「數位臨床督導系統」**。系統已內建【臨床智慧模擬與實證推理引擎】。")

# 初始化對話歷史
if "clinical_messages" not in st.session_state:
    st.session_state.clinical_messages = []

# 顯示歷史訊息
for msg in st.session_state.clinical_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 臨床智慧模擬與事實推理引擎 (Mock Supervisor Engine)
def generate_clinical_mock_response(query):
    query_lower = query.lower()
    
    if any(k in query_lower for k in ["色彩", "流動畫", "畫畫", "研究室", "表達", "心情色彩"]):
        res = """**【臨床實務督導與分析反饋】**

針對您所諮詢的「方案一：心情色彩研究室」情境，以下為結合臨床職能治療學理的督導分析：

1. **職能治療介入原理**：
   - 本方案採用「流動畫創作」作為治療媒介。活動的核心價值來自於色彩的非語言表達、選擇的主控權，以及顏料流動的感官經驗與本體控制。
   - 請特別叮嚀實習學生：**活動的治療價值是「過程與自主權」，切勿在現場對個案的作品進行心理象徵或美醜分析**，以免引發個案的焦慮與防衛心。

2. **臨床 Use of Self 與步驟引導**：
   - 治療師此時扮演「支持與共同調節者」。當個案不知道怎麼下筆或害怕失敗時，引導其「限制使用3種顏色，提供示範」，並在過程中給予高支持、低評價的溫暖語音引導。
"""
    elif any(k in query_lower for k in ["飲品", "安心飲品", "過載", "充電站"]):
        res = """**【臨床實務督導與分析反饋】**

針對您所諮詢的「方案二：我的安心飲品實驗室」情境：

1. **感官調節與健康管理原理**：
   - 飲品調配是一項高度結構化且整合多重感官（視覺、嗅覺、味覺與本體覺）的職能活動。個案在測量、清洗、攪拌、品嚐的依序過程中，可有效移轉焦慮與反覆反芻的認知負荷。
2. **Use of Self 溝通技巧**：
   - 引導個案在品嚐前三口時進行「緩慢且專注的正念呼吸」，辨識液體在口中的感官回饋，建立「自我照顧轉換儀式」融入其日常。
   - **注意事項**：事前必須確認其吞嚥安全、過敏史與代謝疾病禁忌。
"""
    elif any(k in query_lower for k in ["怒氣", "揉", "黏土", "憤怒", "衝動"]):
        res = """**【臨床實務督導與分析反饋】**

針對您所諮詢的「方案三：把怒氣揉成形」個案情境：

1. **本體覺與觸覺調節機制**：
   - 黏土阻力活動提供極佳的本體覺刺激，能安全釋放因憤怒或人際衝突帶來的肌肉緊繃與交感神經高喚醒。
2. **Use of Self 與界線**：
   - 治療師在此方案扮演「安全邊界守護者」。引導個案將怒氣塑形，再轉化為具有保護性或實用功能的容器（問題解決與挫折耐受）。
   - 若個案在對話中情緒再度失調，請實習生暫停事件探討，直接引導其回到本體覺黏土操作，協助其降溫。
"""
    else:
        res = f"""**【臨床實務督導與分析反饋】**

針對您輸入的諮詢情境「{query}」，AI 督導結合《青少年與成人情緒調節團體介入方案》給予以下臨床分析：

1. **理論與媒介媒合建議**：
   - 對照 **MOHO (人類職能模式)**，評估此情绪是否干擾了個案的日常習慣與角色扮演？
   - 建議根據個案的核心職能痛點媒合方案：
     - 若為焦慮、反覆反芻與拖延，推薦使用「方案四：煩惱分類收納盒」；
     - 若為情緒低落、高生活退縮與缺乏動力，推薦使用「方案五：一份給自己的能量餐」進行行為啟動；
     - 若為自我否定或社群比較，推薦使用「方案八：我的真實生活攝影展」將注意力拉回真實生活。

2. **安全原則與專家覆核**：
   - 任何生成的活動企畫初稿，皆必須由授課教師或臨床督導進行人工 facts-check 與覆核方可落地。若有自傷或傷人意圖，請立刻暫停介入引導，開啟醫療轉介程序。
"""
    return res

# 接收臨床問題輸入
if user_input := st.chat_input("請描述您想與督導討論的團體方案設計、活動分級或理論連結問題..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.clinical_messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        if api_key_configured:
            full_res = ""
            try:
                system_prompt = f"""
                你是一位擁有 20 年經驗、專精於情緒調節的『職能治療教學高級督導 (OT Supervisor)』。
                你只解答與「職能治療、情緒調節團體、10項臨床活動方案設計、感覺統合、CBT/DBT臨床應用、SOAP寫作、臨床推理督導」相關的專業問題。
                請完全結合以下 10 大職能介入活動方案資料回答：
                {str(OT_PROGRAMS)}
                {cloud_reference_text}
                """
                messages_payload = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.clinical_messages:
                    messages_payload.append(msg)
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages_payload,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
            except Exception as e:
                full_res = generate_clinical_mock_response(user_input)
                placeholder.markdown(full_res)
        else:
            full_res = generate_clinical_mock_response(user_input)
            import time
            typed_res = ""
            for char in full_res:
                typed_res += char
                placeholder.markdown(typed_res + "▌")
                time.sleep(0.002)
            placeholder.markdown(full_res)
            
    st.session_state.clinical_messages.append({"role": "assistant", "content": full_res})

# 8. 倫理責任與聲明
st.markdown("---")
with st.expander("🛡️ 臨床與教學安全覆核倫理規範 (Responsible AI & Supervisor Checklist)"):
    st.checkbox("1. 本系統由亞大職能治療學系團隊(陳芝萍、宋宜珊、鄭彩君)設計，所提供之企畫初稿與建議僅供教學輔助與臨床推理學習使用。")
    st.checkbox("2. 本系統之任何分析、活動建議與企畫，正式應用於教學或個案前，必須由授課教師或臨床督導進行人工覆核、事實查核與調整核准。")
    st.warning("""
**【臨床界線與轉介指標】** 
若服務對象出現：持續性情緒明顯惡化影響生理功能、有自傷傷人或失控想法、兒童遭受疑似受虐或暴力事件、長者突然產生譫妄、幻覺或定向障礙、完全喪失基本自我照顧能力等，實習生應立即停止常規活動引導，並主動上報督導老師，轉介真人醫療、精神專科、心理諮商或緊急危機處理系統支持！
""")
