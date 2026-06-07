import streamlit as st
import sys
from google import genai
from google.genai.errors import APIError

# --- 🎨 ตั้งค่าหน้าตาของเว็บไซต์ Chatbot ---
st.set_page_config(page_title="AI 3.5 Flash Chatbot", page_icon="🚀", layout="centered")

st.title("🚀 AI 3.5 Flash: เจนใหม่ความเร็วแสง")
st.write("🤖 **รุ่นความเร็วสูง (AI-3.5-flash.py)** | เหมาะสำหรับคุยทั่วไป หาไอเดีย หรือถามตอบด่วน")
st.markdown("---")

# --- 🔑 ตั้งค่าคีย์และการเชื่อมต่อ ---
# ระบบจะดึงกุญแจลับจาก Secrets หลังบ้านบน Streamlit Cloud อัตโนมัติ (ปลอดภัย 100%)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    # เผื่อไว้ใช้ตอนคุณรันเปิดเล่นทดสอบในคอมตัวเอง ให้เอาคีย์ใหม่วางตรงนี้ได้ครับ
    API_KEY = "ใส่คีย์จริงของคุณตรงนี้สำหรับรันในคอม"

if "client" not in st.session_state:
    try:
        st.session_state.client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"❌ ระบบเชื่อมต่อผิดพลาด: {e}")

# --- 🧠 ระบบจำประวัติแชต (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 💬 แสดงประวัติการคุยเก่าๆ บนหน้าเว็บ ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 📥 กล่องรับข้อความพิมพ์คุย (Chat Input) ---
if user_message := st.chat_input("พิมพ์ข้อความของคุณที่นี่... (เช่น ชวนคุย, ขอไอเดีย)"):

    # 1. แสดงข้อความที่เราพิมพ์ฝั่งขวา
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 2. เรียกบอทให้ตอบและแสดงผลแบบสตรีมไหลลื่น (Streaming)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # สร้างกล่องว่างๆ รอข้อความไหลลงมา
        full_response = ""

        try:
            # 🚀 เรียกใช้โมเดลรุ่นใหม่ล่าสุดปี 2026 แบบ Stream
            response_stream = st.session_state.client.models.generate_content_stream(
                model="gemini-3.5-flash",
                contents=user_message
            )

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    # อัปเดตข้อความบนหน้าเว็บทีละคำแบบพิมพ์สด
                    message_placeholder.markdown(full_response + "▌")

            # เมื่อพิมพ์จบ ให้เอาขีดกะพริบออก
            message_placeholder.markdown(full_response)

            # บันทึกคำตอบของบอทลงประวัติแชต
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except APIError as e:
            message_placeholder.empty()  # เคลียร์กล่องทิ้ง
            st.error(f"⚠️ โควตาเต็มหรือเซิร์ฟเวอร์หนาแน่น (โค้ด: {e.code})")
        except Exception as e:
            message_placeholder.empty()
            st.error(f"❌ เกิดข้อผิดพลาดในการรับข้อมูล: {e}")