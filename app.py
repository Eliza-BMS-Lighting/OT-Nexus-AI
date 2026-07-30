# -*- coding: utf-8 -*-
import streamlit as st
import openai
import os
import pandas as pd
import time

# 1. 網頁基本設定 (專業臨床、學術與 AOTA/Cole 督導風格)
st.set_page_config(
    page_title="OT-Nexus AI: AOTA 職能治療活動分析與團體設計系統",
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
                    local_content += "\\n\\n=== 雲端共享文獻：" + file + " ===\\n"
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
        "irm_mode": 
