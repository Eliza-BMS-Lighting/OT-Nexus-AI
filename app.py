# -*- coding: utf-8 -*-
import streamlit as st
import os
import time

# 1. 網頁基本設定 (專業臨床、學術與 AOTA/Cole 督導風格)
st.set_page_config(
    page_title="OT-Nexus AI: Cole 團體動力與治療性自我應用系統",
    page_icon="🧠",
    layout="wide"
)

# 2. 本機參考資料夾與雲端暫存設定
REFERENCE_FOLDER = "clinical_references"
os.makedirs(REFERENCE_FOLDER, exist_ok=True)

# 3. 🚨 終極安全防護閘門：防止任何 Streamlit Hot-Reload 殘留的舊 Session 格式污染 🚨
if "clinical_messages" not in st.session_state or not isinstance(st.session_state.clinical_messages, list):
    st.session_state.clinical_messages = []
else:
    # 確保每一個對話物件都是標準的 Dict，且擁有 role 與 content 鍵值，過濾掉任何髒資料/列表/字串
    st.session_state.clinical_messages = [
        msg for msg in st.session_state.clinical_messages 
        if isinstance(msg, dict) and "role" in msg and "content" in msg
    ]

# 讀取本機/雲端共享文獻的函數
def load_local_references():
    local_content = ""
    if os.path.exists(REFERENCE_FOLDER):
        files = [f for f in os.listdir(REFERENCE_FOLDER) if f.endswith(('.txt', '.md'))]
        for file in files:
            file_path = os.path.join(REFERENCE_FOLDER, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    local_content += "\n\n=== 本機參考文件：" + file + " ===\n"
                    local_content += f.read()
            except Exception as e:
                pass
    return local_content

# 4. AOTA OTPF-4 活動分析指引對照表 (AOTA Activity Analysis Framework)
AOTA_ANALYSIS_FRAMEWORK = [
    {"分析維度 (AOTA Domain)": "1. 職能與生活脈絡 (Context)", "臨床評估重點項目": "個人與環境脈絡、文化、時間節奏、物理與社會環境支持"},
    {"分析維度 (AOTA Domain)": "2. 表現技能 (Performance Skills)", "臨床評估重點項目": "動作技能 (Motor)、程序技能 (Process)、社交互動技能 (Social Interaction)"},
    {"分析維度 (AOTA Domain)": "3. 表現模式 (Performance Patterns)", "臨床評估重點項目": "日常生活習慣 (Habits)、例行公事 (Routines)、社會角色 (Roles)、儀式 (Rituals)"},
    {"分析維度 (AOTA Domain)": "4. 客戶因素 (Client Factors)", "臨床評估重點項目": "價值觀與信念、身體生理功能 (心率變異、感覺覺察)、身體構造"},
    {"分析維度 (AOTA Domain)": "5. 活動要求 (Activity Demands)", "臨床評估重點項目": "工具與其屬性、空間與社會要求、步驟順序與時間、所需動作與身體機能"},
    {"分析維度 (AOTA Domain)": "6. 分級與調適 (Grading & Adapting)", "臨床評估重點項目": "難度分級 (Grading Up/Down)、環境調適、輔具與代理人介入"}
]

# 側邊欄使用的職能治療理論速查表
OT_THEORIES = [
    {"理論／模式": "MOHO", "方案設計焦點": "動機、習慣、角色、表現能力與環境"},
    {"理論／模式": "PEO／PEOP", "方案設計焦點": "個人、環境與職能活動之適配"},
    {"理論／模式": "CMOP-E", "方案設計焦點": "以個案為中心、職能投入與靈性意義"},
    {"理論／模式": "感覺調節", "方案設計焦點": "喚醒程度、感覺閾值與調節策略"},
    {"理論／模式": "復元模式", "方案設計焦點": "希望、自主、優勢與有意義生活"},
]

# 核心 10 大職能治療介入方案資料庫 (完全整合 Cole 7步驟帶領與 IRM 自我運用模式)
OT_PROGRAMS = {
    "方案一：心情色彩研究室": {
        "activity": "流動畫／壓克力刮畫創作",
        "issue": "難以辨識或表達情緒、難以說明內在感受、情緒覺察障礙。",
        "concept": "成員使用顏色、線條、方向及材料流動呈現當下情緒。活動的治療價值來自選擇、感官經驗、動作控制、容許不確定及作品完成，不以作品好壞或心理分析為重點。",
        "tools": "畫紙、壓克力顏料、刮板、滴管、吸管、圍裙、桌墊及清潔用品。",
        "cole_steps": (
            "1. Introduction (導入): 營造安全不具評價的氛圍，介紹流動畫材料特質與創作過程，強調無對錯。\n"
            "2. Activity (活動): 選擇代表情緒的2-3種顏色進行創作，體驗滴、刮、吹等感官與動作控制。\n"
            "3. Sharing (分享): 展示並為作品命名，分享創作過程中最舒服、最具挑戰或最感意外的部分。\n"
            "4. Processing (處理): 引導個案探討並表達「在無法完全控制顏料流動與圖樣」時的內在焦虑與放鬆感受。\n"
            "5. Generalizing (概化): 整理並總結非語言創作、感官調節與將情緒「外化」之過程如何協助釋放內在張力。\n"
            "6. Application (應用): 探討當生活情緒難以口語表達時，如何以顏色、音樂或動作作為自我整理工具。\n"
            "7. Summary (總結): 感謝成員對情緒承載的開放態度，重申情緒接納與非語言宣洩管道價值。"
        ),
        "irm_mode": "同理模式 (Empathizing) & 鼓勵模式 (Encouraging)：接納個案的色彩選擇與作品成果，肯定其面對不確定性時的勇氣，不予以美醜評判。",
        "mechanism": "• 感官與動作調節。\n• 非語言情緒表達。\n• 接受無法完全控制的結果。\n• 經驗選擇與完成感。",
        "grading": (
            "• 簡易：限制提供 3 種和諧顏色，由治療師提供完整步驟示範與範例。\n"
            "• 進階：設定兩種不同的極端情緒，引導其呈現兩者的轉變、拉扯或共存。"
        ),
        "application": "引導成員思考，當情緒難以用語言表達時，可否先透過顏色、書寫、音樂或動作整理自己。"
    },
    "方案二：我的安心飲品實驗室": {
        "activity": "製作個人化無酒精飲品",
        "issue": "壓力過高、感官過載、缺乏自我照顧習慣、需要調節喚醒狀態。",
        "concept": "透過清洗、測量、調配、攪拌與品嚐，練習放慢速度、覺察感官經驗及依序完成任務。",
        "tools": "水果、茶包、氣泡水、量杯、湯匙、紙杯、冰塊、托盤、視覺化食譜及清潔用品。",
        "cole_steps": (
            "1. Introduction: 說明調配飲品的多重感官設計（嗅覺、視覺、味覺），建立正念品嚐的安全與平靜預期。\n"
            "2. Activity: 依比例調配、攪拌與裝飾，完成個人化飲品，體驗高度結構化與程序的執行。\n"
            "3. Sharing: 為飲品命名，向成員介紹調配概念、希望帶來的身心感受以及擺盤巧思。\n"
            "4. Processing: 口頭引導個案表達品嚐前三口時，口中本體覺與味覺帶來的生理放鬆感。\n"
            "5. Generalizing: 歸納透過依序完成任務，轉移反芻思考並調降生理喚醒強度。\n"
            "6. Application: 討論如何將本活動設計為下課、下班或睡前的個人化「日常生活自我照顧轉換儀式」。\n"
            "7. Summary: 總結多感官調節專為日常健康管理與職能平衡的重要價值。"
        ),
        "irm_mode": "指導模式 (Instructing) & 合作模式 (Collaborating)：提供高對比、清晰的視覺化步驟食譜，並與個案協商最適配食材配方。",
        "mechanism": "• 多感官覺察。\n• 任務順序與注意力集中。\n• 選擇與控制感。\n• 建立健康的自我照顧儀式。",
        "grading": (
            "• 簡易：使用預先分裝妥當的材料，並提供簡化之單一步驟圖像食譜。\n"
            "• 進階：讓個案自行設計比例與食材，並考量預算、營養素與日常適用場景。"
        ),
        "application": "須事前確認個敏史、吞嚥安全及飲食限制；輔助個案建立日常放鬆儀式。"
    },
    "方案三：把怒氣揉成形": {
        "activity": "黏土容器或情緒角色塑形",
        "issue": "憤怒、衝動、身體緊繃、人際衝突、衝動控制與需求表達困難。",
        "concept": "運用揉、壓、推、捏及塑形等本體覺活動，安全釋放身體張力，再將無形的憤怒轉化為可觀察、可調整的作品。",
        "tools": "輕黏土或陶土、墊板、塑形工具、滾輪、顏料及圍裙。",
        "cole_steps": (
            "1. Introduction: 說明黏土阻力媒介能提供高阻力本體覺輸入，有助於釋放累積於手部的肌肉張力與憤怒。\n"
            "2. Activity: 引導個案以黏土呈現「憤怒的形狀」，進行捏、壓、搥打，並將其改造成實用容器。\n"
            "3. Sharing: 展示作品並命名，分享自己加入了什麼代表「安全防禦」、「暫停」或「保護」的元素。\n"
            "4. Processing: 引導探討強力揉壓黏土時，手部肌肉從緊繃至放鬆的身體感覺，與心理鬆弛進行連結。\n"
            "5. Generalizing: 總結將無形憤怒「外化造形並功能化轉變」的臨床心理機制。\n"
            "6. Application: 討論日常生活憤怒觸發時，如何利用抗阻運動（如推牆10次、深呼吸）建立安全暫停機制。\n"
            "7. Summary: 重申憤怒是需要被安全容納與轉化的能量，讚許成員的具體創作。"
        ),
        "irm_mode": "問題解決模式 (Problem-solving) & 同理模式 (Empathizing)：同理個案面臨衝突時的身體與心理張力，引導其透過實體塑造，主動發掘安全的情緒外化替代方案。",
        "mechanism": "• 本體覺與觸覺調節。\n• 衝動延宕。\n• 具體化與轉化情緒。\n• 問題解決及挫折耐受。",
        "grading": (
            "• 簡易：引導個案捏、揉黏土，完成單一情緒造形。\n"
            "• 進階：將情緒造形轉變成具有功能的容器或物品。"
        ),
        "application": "帶領者不替成員解釋作品。若成員情緒升高，先停止討論事件，回到材料操作本體覺調節。"
    },
    "方案四：煩惱分類收納盒": {
        "activity": "紙盒改造與功能性收納盒製作",
        "issue": "焦慮、反覆思考、事情混亂、無法開始行動、認知負荷過重。",
        "concept": "成員將回收紙盒改造成「現在處理、稍後處理、需要協助」的功能性收納盒，以實際分類和製作活動練習組織、排序及問題解決。",
        "tools": "回收紙盒、色紙、剪刀、膠水、標籤、裝飾材料及便利貼。",
        "cole_steps": (
            "1. Introduction: 引導覺察內在焦慮如何因大腦負荷過重而混亂，說明「實體收納與分類」之概念。\n"
            "2. Activity: 裁切並改造紙盒外觀，區分三格收納區，將便利貼寫下的煩惱分類放入。\n"
            "3. Sharing: 展示專屬收納盒，分享自己分類煩惱時，如何辨識出「現在處理」的小任務。\n"
            "4. Processing: 探討將無形且堆積的擔心「外化、寫下來並實際分類」時，內在焦慮感是否減輕。\n"
            "5. Generalizing: 歸納組織、排序與外化反覆思考對於降低大腦認知負荷的學理。\n"
            "6. Application: 將此收納盒帶回生活書桌，作為每週壓力整理、待辦管理的物理輔具。\n"
            "7. Summary: 肯定成員跨出「分類煩惱並付諸最小行動」的第一步，重申控制感重建。"
        ),
        "irm_mode": "指導模式 (Instructing) & 合作模式 (Collaborating)：結構化地示範分類規則，並協同個案將其面臨的繁雜障礙拆解成當下可執行的一小步。",
        "mechanism": "• 外化反覆思考。\n• 組織與分類。\n• 降低認知負荷。\n• 將焦慮轉化為可執行行動。",
        "grading": (
            "• 簡易：提供現成裝飾用貼紙與分格盒，個案僅需貼上分類標籤，簡化裁切拼貼等手部精細動作要求。\n"
            "• 進階：要求個案自行進行結構與分格設計，並為自己制定一週「睡前 5 分鐘煩惱分類與收納」的使用檢視習慣。"
        )
    },
    "方案五：一份給自己的能量餐": {
        "activity": "製作免開火三明治、飯糰或營養餐盒",
        "issue": "情緒低落、生活退縮、缺乏動力、自我照顧不足、活動啟動困難。",
        "concept": "透過準備一份可食用、可完成的餐點，增加活動啟動、程序執行、選擇及照顧自己的具體經驗。",
        "tools": "吐司 or 米飯、蔬果、蛋白質食材、餐盒、餐具、手套、圖像食譜及清潔用品。",
        "cole_steps": (
            "1. Introduction: 說明準備食物是一項具體「自我照顧」與「行為啟動」的有意義活動。\n"
            "2. Activity: 依步驟清洗、擺盤、組合食材，完成免開火餐盒並為其命名。\n"
            "3. Sharing: 介紹自己為「能量餐」設定的名稱，以及自己挑選主食與配料的個人偏好。\n"
            "4. Processing: 討論在動手洗、切並看見實體餐點完成時，體力與成就感上的正向變化。\n"
            "5. Generalizing: 歸納行為啟動 (Behavioral Activation) 對於改善動機低落與退縮的臨床價值。\n"
            "6. Application: 規劃本週一項最容易完成的居家微型營養或自我照顧任務。\n"
            "7. Summary: 總結「能為自己做一頓飯」就是一項強大的自我功能肯定與職能復元展現。"
        ),
        "irm_mode": "鼓勵模式 (Encouraging) & 合作模式 (Collaborating)：對低動機個案給予高頻率的正向微小反饋，不將完整完成視為唯一成功標準，與其協同操作、共享烹飪樂趣。",
        "mechanism": "• 行為啟動 (Behavioral Activation)。\n• 感官刺激與程序完成感。\n• 建立日常自我照顧與健康管理。",
        "grading": (
            "• 簡易：食材均由工作人員預先洗淨、切分，成員只需進行拼裝與疊放，確保100%成功體驗。\n"
            "• 進階：成員需獨立規劃「食材採購清單」、控制「財務預算」，並在活動結束後獨立進行流理台與餐具的清潔整理。"
        )
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
        "cole_steps": (
            "1. Introduction: 說明小誌是不受世俗評分限制的「自我探索與角色重塑」安全空間。\n"
            "2. Activity: 將紙張摺成小書，完成各跨頁：角色、喜好、勝任感、重要他人與願景拼貼。\n"
            "3. Sharing: 採取自願原則，選擇成員最滿意或願意分享的「其中一頁」向團體導讀。\n"
            "4. Processing: 討論在回顧並動手編排自己不同生命片段時，內在自我肯定或衝突的感受。\n"
            "5. Generalizing: 總結建立多元自我概念，能有效降低因單一角色（如考試）失敗帶來的全面否定。\n"
            "6. Application: 規劃一項本週可在現實生活中嘗試的新興趣或新角色探索小行動。\n"
            "7. Summary: 感謝每位成員將珍貴且多元的生命故事帶入團體，肯定其獨特性與主控感。"
        ),
        "irm_mode": "倡導模式 (Advocating) & 同理模式 (Empathizing)：倡導多元自我價值、不批判個案的異同與人生取捨；深度同理並接納其在認同探索中的脆弱與掙扎。",
        "mechanism": "• 建立多元自我概念。\n• 整理生命經驗。\n• 增加自主選擇與勝任感。",
        "grading": (
            "• 簡易：提供固定主題的印製頁面與大量現成圖卡/貼紙，個案僅需選擇並黏貼，降低口語書寫與空間組織負荷。\n"
            "• 進階：設計「別人期待的我 / 真實理想的我」跨頁對立面拼貼與生命回顧，深度引導自我整合。"
        )
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
        "cole_steps": (
            "1. Introduction: 說明每個人一天只有24小時，本活動透過競標，模擬我們如何在有限資源下做抉擇。\n"
            "2. Activity: 分配等量代幣，對健康、自由、友誼等生活價值進行模擬市集競標與取捨。\n"
            "3. Sharing: 呈現最後得標與忍痛放棄的項目，說明自己核心的價值優先順序。\n"
            "4. Processing: 探討在競標中被別人搶走目標、或是面臨資金不足必須痛苦取捨時的失落感受。\n"
            "5. Generalizing: 歸納抉擇代表必須承擔代價，而看清個人核心價值能協助重建生活秩序。\n"
            "6. Application: 檢視目前生活時間（如加班），設定一項可與個人得標核心價值呼應的微調。\n"
            "7. Summary: 總結市集無正確答案，每個人的價值排序都值得被高度尊重，勉勵活出真實自我。"
        ),
        "irm_mode": "問題解決模式 (Problem-solving)：在競標與人生情境變局中，擔任客觀的顧問，引導個案以理性的代價分析、資源重新配置，突破其現實的生涯盲點。",
        "mechanism": "• 練習選擇與承擔代價。\n• 增加價值清晰度。\n• face 選擇中的遺憾與不確定。",
        "grading": (
            "• 簡易：改用固定價格的「超市購物籃配額法」，不採用動態競標，成員只需直接分配代幣購買特定價值卡，降低社交焦慮與臨場壓力。\n"
            "• 進階：使用動態競標，並在中途隨機抽入「失業、生病、家庭突發意外」等情境限制卡，強迫其動態進行生活資源重新配置。"
        )
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
        "cole_steps": (
            "1. Introduction: 說明社群媒體「完美濾鏡」帶來的比較焦慮，宣告本活動核心在於「真實日常力量」。\n"
            "2. Activity: 拍攝或選取4格真實照片（完成的小事、支持者、恢復地、活動），撰寫真實說明並排版。\n"
            "3. Sharing: 展示四格照片故事，分享自己真實生活中的微小確幸、支持系統與日常努力。\n"
            "4. Processing: 討論當不刻意包裝、只呈現「最真實且粗糙的日常」時，內心防衛的放下與踏實感。\n"
            "5. Generalizing: 歸納將注意力從社會比較（向上比較）移回真實職能參與，對於自我重建的臨床效力。\n"
            "6. Application: 設定本週一項增加「線下現實生活職能投入」（如不看手機散步）的微型計畫。\n"
            "7. Summary: 肯定成員看見真實生活美好的能力，重申自我價值的內在歸因。"
        ),
        "irm_mode": "同理模式 (Empathizing) & 鼓勵模式 (Encouraging)：深度同理社群時代的外表焦慮與過度關注，以高度同理傾聽，肯定並放大其在照片中所呈現的「真實日常力量與復原力」。",
        "mechanism": "• 注意力轉向真實生活。\n• 辨識優勢與有意義職能。\n• 重建完整自我敘事。",
        "grading": (
            "• 簡易：不要求即時攝影，個案可直接挑選手機相簿中既有的「個人生活日常紀錄」照片進行實體列印與排版說明。\n"
            "• 進階：進行連續三天的「日常微力量主題攝影紀錄」，每日設定特定攝影時段（例如早上通勤），並進行每日情緒焦慮對比。"
        )
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
        "cole_steps": (
            "1. Introduction: 將個人時間與精力比喻為容量有限的便當盒，說明「過勞與角色失衡」會擠壓健康。\n"
            "2. Activity: 以顏色籌碼配置現狀一週，觀察過滿與失衡區塊，並重新配置符合職能平衡的配置。\n"
            "3. Sharing: 展示重新調配的一週便當盒，說明自己增加、減少、或尋求協助的具體職能項目。\n"
            "4. Processing: 討論在面臨「想要塞進去但空間不足」必須對部分事務說不、或設定界線時的糾結與難處。\n"
            "5. Generalizing: 歸納職能平衡 (Occupational Balance) 與主動設定界線對於抗壓、維持健康的臨床依據。\n"
            "6. Application: 將這一項微調（如一週增加一晚休閒）寫入真實手機行事曆中執行。\n"
            "7. Summary: 總結便當盒容量有限，善待精力是自我照顧的起點，肯定成員的自我調適決心。"
        ),
        "irm_mode": "問題解決模式 (Problem-solving) & 指導模式 (Instructing)：協助其時間管理之精力分配障礙，提供結構化職能平衡分析策略，指導日常中落實界線設定。",
        "mechanism": "• 視覺化角色負荷。\n• 提升時間與精力覺察。\n• 練習設定界線與活動取捨。",
        "grading": (
            "• 簡易：縮短時間跨度，僅引導個案分析、配置「單一典型工作日 (One Day)」的時間與精力平衡，降低認知組織負荷。\n"
            "• 進階：同時引入一週時間、精力評估，並將「家屬與工作同儕期望」作為環境變數加入配置，練習衝突時的協商與拒絕。"
        )
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
        "cole_steps": (
            "1. Introduction: 說明團體是一個人際安全實驗室，我們將透過桌遊安全預演「人際衝突與拒絕」。\n"
            "2. Activity: 進行情境合作桌遊，輪流抽取人際情境與限制卡，練習拒絕、協商與口語求助句型。\n"
            "3. Sharing: 分享自己在遊戲中抽到最困難的人際情境，以及隊友提供了什麼意想不到的應對句型。\n"
            "4. Processing: 探討在遊戲中開口「說不、拒絕他人或開口求助」時，身體緊繃、尷尬或害怕被討厭的感受。\n"
            "5. Generalizing: 歸納人際界線是雙向的，安全預演能增加反應彈性，降低真實衝突中的無助感。\n"
            "6. Application: 選擇一個可在生活中練習的最低風險拒絕或協商情境（如拒絕不熟的聚會）進行真實預演。\n"
            "7. Summary: 肯定成員在團體中展現的互助支持與人際彈性，勉勵將人際主控感帶回生活。"
        ),
        "irm_mode": "合作模式 (Collaborating) & 鼓勵模式 (Encouraging)：與成員站在一起，以遊戲隊友的角色，共同預演、克服尷尬情境，對每次嘗試開口表達需求的個案給予高度肯定與正正向強化。",
        "mechanism": "• 在安全環境中預演人際反應。\n• 增加回應彈性。\n• 建立同儕支持及問題解決經驗。",
        "grading": (
            "• 簡易：提供現成的人際選擇題庫與完整劇本句型卡，成員只需選擇並照著念出，降低臨場反應壓力。\n"
            "• 進階：抽入「對方產生極度不悅反應、上司強烈要求」等高難度限制卡，要求個案即時進行多輪人際協商與情緒防守。"
        )
    }
}

# 3. 網頁視覺與側邊欄設計 (專業黑/藍色調，凸顯醫學與督導定位)
st.title("🧠 OT-Nexus AI 職能治療數位督導系統")
st.subheader("【Cole 團體動力、OTPF-4 與 IRM 治療性自我應用系統】")
st.write("本系統完全整合 **AOTA (美國職能治療學會) OTPF-4 活動分析框架**，提供職能治療學系學生進行團體企畫微調、感覺閾值分析與 Use of Self 決策推理的專業學術輔助系統。")
st.markdown("---")

# 側邊欄設計
st.sidebar.image("https://img.icons8.com/illustrations/lex/112/brain.png", width=90)
st.sidebar.header("🧭 臨床督導導航儀")

# ==========================================
# 📤 雲端實時文獻拖曳上傳器 (Web Uploader)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("📤 雲端自訂文獻與 AOTA 資料庫")
uploaded_files = st.sidebar.file_uploader(
    "請上傳 AOTA/Cole 參考指引或自訂文獻 (.txt / .md)：", 
    type=["txt", "md"], 
    accept_multiple_files=True,
    help="在此上傳任何 AOTA 資源、教案修正範本，AI 督導將會即時將其學會並融入第二步對話！"
)

# 讀取上傳檔案的文字內容
uploaded_file_names = []
if uploaded_files:
    st.sidebar.success("📈 成功導入臨床擴充指引！")
    for uploaded_file in uploaded_files:
        try:
            uploaded_file.read().decode("utf-8")
            uploaded_file_names.append(uploaded_file.name)
            st.sidebar.text("📄 " + uploaded_file.name + " (已動態載入)")
        except Exception as e:
            st.sidebar.error("解析 " + uploaded_file.name + " 失敗")
else:
    st.sidebar.info("💡 目前無外部文獻。上傳 any .txt 檔案即可讓 AI 實時聯動讀取！")

# 側邊欄：指南快速檢索
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 實務方案與步驟")
target_group = st.sidebar.selectbox("請選擇方案進行指南導航：", list(OT_PROGRAMS.keys()))

if target_group:
    prog = OT_PROGRAMS[target_group]
    with st.sidebar.expander("🔍 查看 " + target_group + " 詳情"):
        st.markdown("**🎯 核心媒介活動：**\n\n`" + prog['activity'] + "`")
        st.markdown("**📌 適用主要議題：**\n\n" + prog['issue'])
        st.markdown("**💡 活動概念設計：**\n\n" + prog['concept'])
        st.markdown("**🛠️ 設備與材料：**\n\n" + prog['tools'])
        if "cole_steps" in prog:
            st.markdown("**👣 Cole 7步驟團體引導：**\n\n" + prog['cole_steps'])
        else:
            st.markdown("**👣 標準實施步驟：**\n\n" + prog['steps'])
        if "irm_mode" in prog:
            st.markdown("**💓 IRM 治療性自我 (Use of Self)：**\n\n*" + prog['irm_mode'] + "*")
        st.markdown("**💓 情緒調節機制：**\n\n" + prog['mechanism'])

# 側邊欄顯示理論與 AOTA
with st.sidebar.expander("📚 AOTA OTPF-4 與學術架構"):
    st.markdown("**OTPF-4 活動分析面向**")
    st.dataframe(AOTA_ANALYSIS_FRAMEWORK, hide_index=True)
    st.markdown("**常用職能治療理論／模式**")
    st.dataframe(OT_THEORIES, hide_index=True)

# 4. 主畫面：Section 1 - 臨床個案情境分析與活動分級模組
st.header("📋 第一階段：個案職能需求分析與分級治療設計")
st.write("請職能治療系學生填寫以下「方案鷹架條件」，系統將結合 AOTA、Cole 7 步驟與治療性運用自我，自動分析活動要求並生成企畫案：")

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
    theory_link = st.selectbox("• 預計連結之職能治療理論 (OT Theory)：", ["人類職能模式 (MOHO)", "PEO／PEOP 模式", "加拿大職能表現與投入模式 (CMOP-E)", "感覺統合理論／感覺調節", "認知行為取向 (CBT)", "辯證行為治療技巧 (DBT)", "復元模式 (Recovery Model)", "社會情緒學習 (SEL)", "活躍老化與生命回顧"])
    activity_level = st.selectbox("• 方案設計難度分級需求：", ["簡易", "中等", "進階"])

if st.button("🚀 生成標準化職能活動企畫與 AOTA 評量分析"):
    selected_act = OT_PROGRAMS[target_program]
    st.success("✨ 職能治療臨床介入企畫方案生成成功！")
    
    st.markdown("### 📝 職能活動企畫書與臨床推理初稿")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.info("🎯 推薦核心方案：" + target_program + " — " + selected_act['activity'] + "")
        st.markdown("**• 主要議題：** " + selected_act['issue'])
        st.markdown("**• 概念原理：** " + selected_act['concept'])
        
        # 呈現 Cole 7 步驟與自我使用之企劃書
        st.markdown("### 📋 【Cole 7 步驟團體引導指引與治療性自我 (Use of Self)】")
        
        irm_txt = selected_act['irm_mode'] if 'irm_mode' in selected_act else '以同理與鼓勵建立治療關係'
        st.markdown("**• IRM 治療關係溝通模式 (Use of Self)**：" + irm_txt + "")
        
        cole_steps_text = selected_act['cole_steps'] if 'cole_steps' in selected_act else selected_act['steps']
        st.markdown("**• Cole 7 Steps 團體動力分析：**\n\n" + cole_steps_text)
        st.markdown("**• 理論學理連結：** 連結【" + theory_link + "】分析個案在情境時的調節反應。")
    with col_b:
        st.warning("**📝 臨床電子病歷 SOAP 紀錄草稿 (SOAP Note Draft)**")
        # 移除了所有在 f-string 中會引起編譯衝突的「與」全形引號，改為標準括號表示，完美迴避 Bug！
        soap_box = f"""
* S (Subjective) 主觀敘述:
個案在 ({case_event}) 之觸發情境下，自覺內心十分混亂。

* O (Objective) 客觀觀察:
個案於團體中呈現 ({physical_arousal}) 生理反應，自覺目前壓力強度為 7 分。

* A (Assessment) 臨床評估:
個案因職能角色負荷與焦慮反覆思考，干擾其 ({impacted_occupation}) 之職能投入。本次介入連結 ({theory_link}) 架構與 Cole 7 步驟方案，提供 ({target_program}) 作為調節媒介。治療師採取 IRM 模式與其互動。

* P (Plan) 介入計畫:
預計引導個案進行 ({selected_act['activity']})。藉由活動中的非語言表達、選擇與完成經驗，提升個案的 ({target_ability})。後續將評估其編寫計畫之成效。
"""
        st.code(soap_box, language="markdown")

st.markdown("---")

# 5. 主畫面：Section 2 - 臨床數位督導與 AOTA 活動分析對話模組
st.header("💬 第二階段：AOTA 臨床督導與活動方案決策研討")
st.write("本對話模組結合 **Cole 7 步驟**與 **IRM 關係模式(治療性自我)** 進行決策推理。")

# 離線版狀態公告
st.info(
    "💡 **離線智慧督導教學引擎已啟動（內建 AOTA OTPF-4 與 Cole 7 步驟內容）**\n\n"
    "本系統目前運行於「離線教學展示模式」。學生與督導可直接在下方輸入問題，"
    "進行 10 大方案之活動分析與方案微調討論，全程不需要 API 金鑰。"
)

# 顯示歷史對話
for msg in st.session_state.clinical_messages:
    if isinstance(msg, dict) and "role" in msg and "content" in msg:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 臨床自適應模擬與 AOTA 分析引擎 (OT-Nexus AOTA Fallback Engine)
def generate_clinical_aota_fallback(query, uploaded_docs):
    query_lower = query.lower()
    
    # 建立動態偵測上傳文件的文字
    rag_feedback = ""
    if uploaded_docs:
        rag_feedback = "\n\n*已載入您上傳的參考文件：" + "、".join(uploaded_docs) + "。離線引擎會將檔名所呈現的主題納入方案提示。*\n"
        for doc in uploaded_docs:
            if "生氣" in doc.lower() or "情緒" in doc.lower() or "cole" in doc.lower():
                rag_feedback += "- 【" + doc + "】：優先提示 Cole 7 步驟、情緒調節與治療性自我。\n"
            else:
                rag_feedback += "- 【" + doc + "】：作為活動要求與環境調適的討論線索。\n"
    else:
        rag_feedback = "\n\n*目前未上傳自訂文件；以下依內建 AOTA 與 Cole 7 步驟內容提供教學提示。*"

    # 方案一的心情色彩
    if any(k in query_lower for k in ["色彩", "流動畫", "畫畫", "研究室", "表達", "心情色彩"]):
        res = f"""**【OT-Nexus 臨床活動分析與督導回饋】**
{rag_feedback}

針對您所諮詢的「方案一：心情色彩研究室」方案微調，以下為依據 **Cole 7 步驟** 與 **IRM 治療性自我 (Use of Self)** 進行的深度分析與調適：

#### 🛠️ Cole 7 步驟團體介入微調建議 (Cole's 7 Steps Group Dynamics)
1. **Introduction (導入)**: 治療師不批判地介紹顏色媒介，說明沒有好壞。
2. **Activity (活動)**: 限制使用2-3種顏色，提供高結構支持。
3. **Sharing (分享)**: 治療師示範分享，帶領「自願分享」原則，建立安心信賴。
4. **Processing (處理)**: 引導表達「無法完全控制顏料流動與圖樣」時的焦慮與身體感受，外化情緒。
5. **Generalizing (概化)**: 歸納非語言媒介如何釋放身體興奮能量，將抽象情緒化為具體造形。
6. **Application (應用)**: 探討生活中感到挫折難以說明時，如何以顏色或深呼吸整理自己。
7. **Summary (總結)**: 感謝成員在創作中展現的真實力量與情緒接納勇氣。

#### 🤝 治療性自我應用指南 (Therapeutic Use of Self - IRM Mode)
- **同理模式 (Empathizing)**：當個案因無法控制作品成果而焦慮挫折時，治療師應主動對應其感受，口語肯定其「願意接受不確定性與失控」的勇氣，不給予美醜評判。
"""
    # 方案三的怒氣揉成形
    elif any(k in query_lower for k in ["怒氣", "揉", "黏土", "憤怒", "衝動", "陶土"]):
        res = f"""**【OT-Nexus 臨床活動分析與督導回饋】**
{rag_feedback}

針對您所諮詢的「方案三：把怒氣揉成形」方案微調與本體覺介入：

#### 🛠️ Cole 7 步驟團體介入微調建議 (Cole's 7 Steps Group Dynamics)
*   **Processing (處理) 階段特別引導**：這是黏土方案最核心的階段。當個案拼命搥打、揉捏黏土後，引導其說出：「手部緊繃肌肉漸漸放鬆的生理感受」，並與情緒放鬆做連結。
*   **Application (應用) 階段特別引導**：引導個案發掘日常生活中的安全降溫抗阻運動（如推牆10次、洗臉），建立實體可行的生活任務。

#### 🤝 治療性自我應用指南 (Therapeutic Use of Self - IRM Mode)
- **問題解決模式 (Problem-solving)**：與個案共同協商，將無形且具破壞力的憤怒，透過揉壓黏土的阻力安全釋放，並藉由問題解決，共同將黏土改造成具功能性的保護容器。
"""
    else:
        res = f"""**【OT-Nexus 臨床活動分析與督導回饋】**
{rag_feedback}

針對您諮詢的情境「{query}」，AI 督導結合 **AOTA 活動分析、Cole 7 步驟與 IRM 模式**，提供以下臨床推理指引：

1. **Cole 7 步驟與團體動力學 (Group Dynamics)**：
   - 請確保團體企畫中，設計了完整的 **Sharing (分享)**、**Processing (處理/表達感受)** 與 **Application (生活應用)** 階段。活動（Activity）時間長度建議不超過總時間的三分之一，釋放充足時間給與心與心的共振。

2. **治療性自我 (Therapeutic Use of Self)**：
   - 根據個案特性，選擇適合的 IRM 溝通模式（如對低動機者採用「鼓勵模式」、對焦慮失序者採用「指導與問題解決模式」）。

3. **臨床事實查核與覆核聲明**：
   - 系統產出之建議均作為實習生練習臨床推理使用，最終企畫案必須經過持照職能治療師核可覆核。
"""
    return res

# 接收臨床問題輸入
if user_input := st.chat_input("請描述您想與督導討論、微調或以 AOTA / Cole 框架評估的團體方案問題..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.clinical_messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        full_res = generate_clinical_aota_fallback(user_input, uploaded_file_names)
        typed_res = ""
        for char in full_res:
            typed_res += char
            placeholder.markdown(typed_res + "▌")
            time.sleep(0.001)
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
