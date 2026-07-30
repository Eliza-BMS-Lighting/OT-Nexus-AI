import streamlit as st
import openai
import os
import pandas as pd

# 1. 網頁基本設定 (專業臨床版風格)
st.set_page_config(
    page_title="OT-Nexus AI: 職能治療數位督導與臨床決策系統",
    page_icon="🧠",
    layout="wide"
)

# 2. 專業臨床知識庫與理論對照表
OT_THEORIES = [
    {"理論架構": "人類職能模式 (MOHO)", "臨床指標項目": "職能動機、角色認同、生活節奏與環境支持系統評估"},
    {"理論架構": "PEO／PEOP 模式", "臨床指標項目": "個人能力(P)、物理/社會環境條件(E)與職能活動要求(O)之適配性分析"},
    {"理論架構": "加拿大職能表現模式 (CMOP-E)", "臨床指標項目": "自我照顧、生產力與休閒活動之職能投入與意義建構"},
    {"理論架構": "感覺統合理論／感覺調節", "臨床指標項目": "過度喚醒(Hyper-arousal)或低度喚醒(Hypo-arousal)之感官閾值調節與本體覺/前庭覺介入"},
    {"理論架構": "認知行為取向 (CBT)", "臨床指標項目": "情境-想法-情緒-身體反應之自動化思考連結與認知重塑"},
    {"理論架構": "辯證行為治療技巧 (DBT)", "臨床指標項目": "正念覺察、痛苦耐受(Distress Tolerance)、情緒調節與人際效能訓練"},
    {"理論架構": "復元模式 (Recovery Model)", "臨床指標項目": "自我效能、希望感建立、主動選擇權與有意義的生活職能參與"},
    {"理論架構": "活躍老化與生命回顧", "臨床指標項目": "高齡個案之自主感維持、生命故事重塑與社會角色再造"}
]

CLINICAL_DATABASE = {
    "兒童期 (Children)": {
        "focus": "建立基礎情緒認知、感官閾值調節，以及透過治療性遊戲 (Therapeutic Play) 探索安全的情緒宣洩管道。",
        "tasks": "認識並命名情緒、連結情緒與身體反應、從共同調節 (Co-regulation) 渡至自我調節、學習等待與面對挫折。",
        "activities": {
            "簡易": {
                "name": "🌦️ 情緒天氣站",
                "target_sensory": "觸覺、本體覺、本體感官回饋",
                "methods": "引導個案以氣象隱喻表徵內在狀態，指出心跳快、手握緊等生理反應。提供2-3分鐘本體覺或深壓覺活動。",
                "options": ["抱枕頭或包裹重力毯 (深壓覺輸入)", "推牆 10 次 (本體覺抗阻阻力運動)", "吹泡泡或慢吹風車 (呼氣控制/副交感神經刺激)"],
                "use_of_self": "治療師應採用具體、簡短、高圖像感且具安全感的語調。避免進行過度抽象的因果追問。"
            },
            "中等": {
                "name": "🚦 情緒交通號誌",
                "target_sensory": "前庭覺、動作計畫與衝動控制",
                "methods": "以紅黃綠燈隱喻衝動控制：紅燈停（停止動作，確保安全）；黃燈想（辨識生理訊號與內在需要）；綠燈行（執行適當替代行動）。",
                "options": ["「弟弟拿玩具」情境模擬訓練", "動作紅綠燈遊戲 (訓練抑制控制反應能力)"],
                "use_of_self": "治療師需在紅燈時展現堅定且清晰的指令界線；在黃燈時扮演共同調節者，引導個案口語化生理感受。"
            },
            "進階": {
                "name": "🎒 我的冷靜任務包",
                "target_sensory": "多重感官整合與問題解決策略",
                "methods": "引導兒童共同建構個人化「情緒工具箱」（包含身體、感覺、想法、人際與回歸生活職能之工具），並建立自我監控機制。",
                "options": ["感覺工具：使用減壓耳罩與降噪空間", "想法工具：畫出內在擔心並進行轉念", "回歸工具：調節後重新投入課堂或整理書包"],
                "use_of_self": "治療師扮演協作者 (Facilitator)，引導個案主動評估工具效能，建立其自我效能感 (Self-efficacy)。"
            }
        }
    },
    "青少年與成人期 (Adolescents & Adults)": {
        "focus": "建立實時生理壓力覺察、自動化思考重塑、日常生活重整與價值導向的職能投入。",
        "tasks": "身分認同、時間管理、壓力累積辨識、在焦慮共存下執行符合長期價值的行動。",
        "activities": {
            "簡易": {
                "name": "🔌 五分鐘重新開機",
                "target_sensory": "自主神經系統調節與肌肉放鬆",
                "methods": "個案面臨過載時，引導其評估即時職能需求（降低強度/恢復精神/停止反覆思考/找下一步），並執行 5 分鐘微介入。",
                "options": ["離開螢幕並進行肩頸神經肌肉伸展", "到戶外或走廊進行 3 分鐘本體覺步行", "寫下『現在不必處理的事情』"],
                "use_of_self": "治療師應完全尊重個案之自主權 (Autonomy)，避免說教或過度正向化 (Toxic Positivity)，協助其在可控制範圍內做選擇。"
            },
            "中等": {
                "name": "🗺️ 情境—身體—想法—行動地圖",
                "target_sensory": "認知行為重塑與內省能力",
                "methods": "運用結構化 6 問，釐清「工作訊息未回覆」等情境中的自動化思考、身體訊號、情緒衝動與適應性行為抉擇。",
                "options": ["CBT 職能記錄單填寫", "辨識事實與想像之客觀證據比對", "安排 10 分鐘可獨立執行之小工作項目"],
                "use_of_self": "治療師採用蘇格拉底式提問 (Socratic Questioning)，引導個案自行發現思考盲點並比對客觀證據。"
            },
            "進階": {
                "name": "🧪 價值導向的一週生活實驗",
                "target_sensory": "職能平衡 (Occupational Balance) 與日常重整",
                "methods": "針對睡眠失調、常因焦慮拖延等情境，將長期生活目標拆解為一週可觀察、可執行的「最小行動實驗」。",
                "options": ["設定焦慮 > 6 分時之步行 10 分鐘備用計畫", "晚上 9 點後關閉工作通知之環境調適", "每日記錄情緒與活動效能對照表"],
                "use_of_self": "治療師擔任個案的臨床教練 (Co-active Coach)，與個案共同協商實驗變因，強化其日常生活控制感。"
            }
        }
    },
    "銀髮族 (The Elderly)": {
        "focus": "維持大腦情感連結、減少黃昏症候群(Sundowning)之焦躁激動、重塑角色認同與建立具期待感的生活節奏。",
        "tasks": "退休適應、疾病與功能喪失適應、面對失落與社交網絡縮減、整合生命經驗與維持日常尊嚴。",
        "activities": {
            "簡易": {
                "name": "🌸 今日三件安定小事",
                "target_sensory": "環境定向與規律日常建立",
                "methods": "每日從拉開窗簾看看天氣、喝水、走動、整理熟知物品等低負荷職能活動中選擇三項執行，建立安全且可預測的日常。",
                "options": ["拉開窗簾，建立晝夜節律環境調適", "整理一件充滿個人意義的熟悉物品", "聽一首熟悉且具正向情感連結的懷舊歌曲"],
                "use_of_self": "治療師應採取大字、短句、單一步驟的語音引導。語速減慢、音量適中，並給予個案充足的反應時間。"
            },
            "中等": {
                "name": "📦 生活記憶箱",
                "target_sensory": "認知活化與情感回溯",
                "methods": "利用老照片、舊物或食譜，引導個案說出相關的人、地、事，描述當時感受及自己展現的能力，並將該能力連結至當前生活角色中。",
                "options": ["進行老照片的情感連結與命名", "將過去「很會照顧人」轉化為教導晚輩一道菜之角色重塑"],
                "use_of_self": "治療師扮演積極聆聽與接納的角色，著重於確認個案既有的優勢與成功經驗，而非評估其記憶缺損。"
            },
            "進階": {
                "name": "📅 我的一週角色與連結計畫",
                "target_sensory": "社會參與與多重職能平衡",
                "methods": "每週系統化安排身體 (散步)、認知 (桌遊)、關係 (社區聚點) 與意義 (志工或生命故事整理) 四大類活動，建立期待感。",
                "options": ["安排社區據點社會連結活動", "教導晚輩或參與社區志工服務", "建立保留長者選擇權與適度縮短時間的彈性計畫"],
                "use_of_self": "治療師需扮演尊嚴的維護者，引導家屬與個案共同決策，保留長者之主控感與尊嚴。"
            }
        }
    }
}

# 3. 網頁視覺與側邊欄設計 (專業黑/藍色調，凸顯醫學與督導定位)
st.title("🧠 OT-Nexus AI 職能治療數位督導系統")
st.subheader("【臨床專業決策與介入活動設計模組】")
st.write("本平台專為 **臨床職能治療師 (OT)、實習治療師 (OT Interns) 及臨床督導 (Supervisors)** 設計。依據《AI情緒調節職能治療引擎》之實證架構，提供高度專業的個案活動分析、調適方案與治療師「Use of Self」自我引導指南。")
st.markdown("---")

# 側邊欄設計
st.sidebar.image("https://img.icons8.com/illustrations/lex/112/brain.png", width=90)
st.sidebar.header("🧭 臨床督導導航儀")

# 【甲方案】安全讀取 OpenAI API 金鑰 (Streamlit Secrets 機制)
api_key = ""
api_key_configured = False

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
    api_key_configured = True
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")
    api_key_configured = True

# 載入相容 OpenAI 1.0.0+ 之最新 SDK Client
if api_key_configured:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"臨床督導 AI 模組初始化失敗：{str(e)}")

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
st.sidebar.subheader("🔍 實證職能治療知識庫")
target_group = st.sidebar.selectbox("請選擇評估個案年齡層：", list(CLINICAL_DATABASE.keys()))

if target_group:
    st.sidebar.markdown(f"**📌 {target_group} 臨床介入焦點：**")
    st.sidebar.write(CLINICAL_DATABASE[target_group]["focus"])
    st.sidebar.markdown(f"**🎯 核心發展關鍵任務：**\n{CLINICAL_DATABASE[target_group]['tasks']}")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 推薦核心介入活動方案")
    for level, act in CLINICAL_DATABASE[target_group]["activities"].items():
        with st.sidebar.expander(f"【{level}】{act['name'] if 'name' in act else act['intervention']}"):
            st.markdown(f"**🎯 目標感覺系統/學理：**\n`{act['target_sensory']}`")
            st.markdown(f"**👣 臨床介入步驟與原理：**\n{act['methods']}")
            st.markdown(f"**🛠️ 可選職能活動選項：**")
            for opt in act["options"]:
                st.markdown(f"- {opt}")
            st.markdown(f"**💬 治療師 Use of Self 臨床引導指南：**\n*{act['use_of_self'] if 'use_of_self' in act else '提供結構化引導，保留自主權。'}*")

# 側邊欄顯示理論架構 (MOHO, PEO, CMOP-E...)
with st.sidebar.expander("📚 臨床理論架構與介入對照表"):
    df_theories = pd.DataFrame(OT_THEORIES)
    st.dataframe(df_theories, hide_index=True)

# 4. 主畫面：Section 1 - 臨床個案情境分析與活動分級模組 (100% 免金鑰，離線可用)
st.header("📋 第一階段：個案職能需求分析與分級治療設計")
st.write("請治療師或實習生依據評估與觀察，輸入個案身心訊號與情境。系統將依據職能治療核心原理，即時生成客製化的活動分析報告與 SOAP 記錄草稿：")

col1, col2 = st.columns(2)
with col1:
    user_age = st.selectbox("1. 個案目標群組：", list(CLINICAL_DATABASE.keys()))
    case_event = st.text_input("2. 觸發事件與情境脈絡：", placeholder="例如：ASD兒童被拒絕後推人 / 工作訊息未回覆極度焦慮...")
    physical_arousal = st.text_input("3. 生理訊號與喚醒狀態評估：", placeholder="例如：心跳快、手握拳、呼吸急促 (Hyper-arousal)...")
    
with col2:
    arousal_intensity = st.slider("4. 情緒與喚醒強度評估 (0～10分)：", 0, 10, 5)
    ot_goal = st.selectbox(
        "5. 核心職能治療目標 (OT Goal)：",
        ["調節感覺閾值 / 平靜身體 (Sensory Modulation)", "重建認知思考 / 正向轉念 (Cognitive Reframing)", "建立日常平衡 / 生活重整 (Occupational Balance)", "促進社會參與 / 尋求支持 (Social Participation)"]
    )
    activity_level = st.selectbox("6. 評估現在適合什麼難度的活動？", ["簡易", "中等", "進階"])

if st.button("🚀 生成標準化職能治療活動分析報告"):
    selected_act = CLINICAL_DATABASE[user_age]["activities"][activity_level]
    
    st.success("✨ 職能治療臨床介入方案生成成功！")
    
    # 標準活動分析報告輸出
    st.markdown("### 📋 您的專屬生活調節活動選單")
    
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.info(f"**🎯 推薦核心方案：{selected_act['name'] if 'name' in selected_act else selected_act['intervention']} ({activity_level})**")
        st.markdown(f"**• 目標感覺系統／認知學理：** `{selected_act['target_sensory']}`")
        st.markdown(f"**• 臨床介入原理與步驟：**\n{selected_act['methods']}")
        st.markdown("**• 臨床可執行之具體活動選項（建議維持 2~4 個）：**")
        for opt in selected_act["options"]:
            st.markdown(f"  👉 `{opt}`")
        st.markdown(f"**• 治療師臨床 Use of Self 自我引導指南：**\n*{selected_act['use_of_self'] if 'use_of_self' in selected_act else '尊重自主、提供選項，避免直接代為決策。'}*")
    with col_b:
        # 專業病歷記錄單 (SOAP Draft)
        st.warning("**📝 臨床電子病歷 SOAP 紀錄草稿 (SOAP Note Draft)**")
        soap_box = f"""
【S (Subjective) 主觀敘述】：
個案主訴「{case_event if case_event else '未填寫'}」，自覺目前壓力強度約為 {arousal_intensity} 分。

【O (Objective) 客觀觀察】：
個案呈現「{physical_arousal if physical_arousal else '生理訊號不明顯'}」之身心反應，情緒強度評估為 {arousal_intensity}/10 分。

【A (Assessment) 臨床評估】：
個案面臨情境時，表現出生理與情緒調節失衡。本次介入預計透過 {ot_goal} 之學理架構，提供【{activity_level}】難度之職能活動，調節個案之感官閾值與動作計畫能力，以協助其重新建立日常生活功能。

【P (Plan) 介入計畫】：
預計引導個案進行「{selected_act['name'] if 'name' in selected_act else selected_act['intervention']}」。
介入活動包含：
1. {selected_act['options'][0]}
2. {selected_act['options'][1] if len(selected_act['options']) > 1 else '依個案反應適度調整'}

後續將追蹤個案活動後的情緒強度變化，並評估其能否重新回歸並投入有意義的日常職能中。
"""
        st.code(soap_box, language="markdown")

st.markdown("---")

# 5. 主畫面：Section 2 - 臨床數位督導與個案研討 AI 對話模組 (需要管理端 Secrets 啟用)
st.header("💬 第二階段：臨床專家督導與個案決策 AI 對話")
st.write("本對話模組為 **「數位臨床督導系統」**。AI 已被賦予 System Prompt，僅接受職能治療實務、理論、活動分級調適與臨床 Use of Self 的個案研討諮詢，非提供一般大眾生活問答。")

if api_key_configured:
    # 建立 System Prompt
    if "clinical_messages" not in st.session_state:
        st.session_state.clinical_messages = []

    # 每個對話回合都將最新雲端上傳的文件動態打包進去，完成雲端實時 RAG！
    system_prompt = f"""
    你是一位擁有 20 年經驗、專精於情緒調節的『職能治療專家與臨床高級督導 (OT Supervisor)』。
    你的對話對象是「臨床職能治療師、在校實習生或健康照護專業人員」。
    你的任務是協助他們進行臨床推論、活動分析、個案分級調適(Grading & Adapting)與 Use of Self 的決策探討。
    
    請務必完全遵循以下《AI情緒調節職能治療引擎》的核心原則來回答：
    
    1. 職能治療核心價值：
       - 以個案為中心、職能導向 (日常職能如起床、上學、工作、家務、休閒、睡眠等)。
       - 優勢與復元觀點。
       - 人-環境-職能適配 (PEO)。
       - 分級與調適。
       - 共同決策：提供選項，但不直接替使用者作決定。
       
    2. 結合的理論架構：MOHO, PEO/PEOP, CMOP-E, 感覺統合理論, CBT, DBT, 復元模式, 社會情緒學習 (SEL), 生命回顧。
    
    3. 溝通與回答準則：
       - 【兒童】：使用具體、簡短、且具圖像感的語言，避免抽象分析 or 連續追問。
       - 【青少年/成人】：尊重自主，避免說教、過度正向化，或直接替其作決定。
       - 【銀髮族】：採大字、短句、單一步驟操作之引導。
       
    4. 每次對話引導的基本流程 (先詢問 or 確認)：
       - 現在發生了什麼事？
       - 情緒強度 0~10 分是幾分？
       - 身體哪裡非常有感覺？
       - 想要「先平靜、增加精神、整理想法，還是找人陪伴」？
       - 適合簡易、中等還是進階活動？
       - 做完後推測能否回到一項重要的生活活動？
       
    5. 安全原則與界線：
       - 情緒持續惡化、影響睡眠飲食。
       - 有自傷、傷人、失控等不安全想法。
       - 兒童遭受霸凌、暴力或疑似虐待。
       - 長者突然意識混亂、疑似譫妄。
       - 無法基本自理或明顯精神症狀。
       
    =============================================
    🌟【雲端即時文獻庫 RAG 擴充指引】🌟
    重要！以下是治療師「剛剛在網頁上即時上傳」的最新臨床指引文獻內容。
    請在回答相關問題時，優先參考、提煉並動態嵌入這些文獻中的介入規則、遊戲建議或學理：
    {cloud_reference_text if cloud_reference_text else "（目前治療師無拖曳上傳新文獻，請以系統基礎資料庫為主）"}
    =============================================
    
    你的口吻必須溫暖、專業、具有極高的同理心。多利用條列式與表格引導。
    """
    
    # 確保 system prompt 隨時在對話最頂端維持更新
    messages_payload = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.clinical_messages:
        messages_payload.append(msg)

    # 顯示對話歷史
    for msg in st.session_state.clinical_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 接收臨床問題輸入
    if user_input := st.chat_input("請描述您想與督導討論的個案情境、臨床評估或 SOAP 撰寫問題..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.clinical_messages.append({"role": "user", "content": user_input})
        messages_payload.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            try:
                # 呼叫
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
                st.error(f"呼叫督導 AI 模組時發生錯誤：{str(e)}")
                
        st.session_state.clinical_messages.append({"role": "assistant", "content": full_res})
else:
    st.warning("⚠️ 系統偵測到『OpenAI API 金鑰』尚未設定，目前不開放臨床督導 AI 實時對話。\n\n**【管理員提示】** 為了確保個資安全與運作，請於本地建立 `.streamlit/secrets.toml` 檔案並設定 `OPENAI_API_KEY`；或於部署平台後台設定，即可安全開啟。")

# 6. 專業人員責任與合規性聲明 (底部常駐提示)
st.markdown("---")
with st.expander("🛡️ 臨床專家安全覆核與倫理責任 (Responsible AI Checklist)"):
    st.checkbox("1. 本系統所提供之報告與 AI 建議僅供決策輔助，不具備獨立臨床處方與診斷權力。")
    st.checkbox("2. 臨床最終決策、個案安全管理與病歷簽章核定，必須由具有持照之職能治療師核可負責。")
    st.checkbox("3. 每次將建議應用於個案前，必須由治療師與督導進行臨床事實查核與「人-環境-職能(PEO)」適配性覆核。")
    st.warning("""
**【臨床界線警告】** 凡個案面臨：情緒持續明顯惡化長期影響生理作息、有自傷/傷人或失控想法、兒童遭受霸凌暴力或疑似受虐、長者突然譫妄或空間定向障礙、完全喪失基本自我照顧能力等，**應立即終止 AI 引導計畫，並轉介精神科專科醫療、心理治療或緊急危機處理系統支持。**
""")
