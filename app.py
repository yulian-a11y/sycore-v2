import streamlit as st
from groq import Groq

# 1. API KEY (Kunci Akses Groq Kamu)
API_KEY = "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"

# 2. KONFIGURASI HALAMAN & TAMPILAN (CSS)
st.set_page_config(page_title="SY-Core Genesis v2", page_icon="🌐", layout="centered")

# CSS Kustom untuk Tampilan Modern & Tombol di Tengah
st.markdown("""
    <style>
    /* Latar belakang gelap & teks putih */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Gaya Judul Utama */
    .main-title { text-align: center; color: #00f2fe; font-size: 3rem; font-weight: bold; text-shadow: 0 0 10px #4facfe; }
    .sub-title { text-align: center; color: #a1a1a1; font-size: 1rem; margin-bottom: 2rem; }

    /* Gaya Kotak Pesan Chat */
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #1f2937; border: 1px solid #4facfe; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #111827; border: 1px solid #00f2fe; }

    /* Gaya Input Bar di Tengah-Tengah (Bottom) */
    .stChatInput { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 80%; max-width: 600px; z-index: 1000; background-color: #1f2937; border-radius: 30px; border: 2px solid #00f2fe; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3); padding: 5px; }
    
    /* Gaya Tombol Mikrofon */
    .mic-button { display: flex; align-items: center; justify-content: center; background-color: #ff4b4b; color: white; border-radius: 50%; width: 50px; height: 50px; font-size: 24px; cursor: pointer; border: none; box-shadow: 0 4px 10px rgba(255, 75, 75, 0.4); transition: transform 0.2s; position: fixed; bottom: 25px; right: 10%; z-index: 1001; }
    .mic-button:hover { transform: scale(1.1); background-color: #ff6b6b; }
    .mic-button:active { transform: scale(0.9); }

    /* Penyesuaian area chat agar tidak tertutup input bar */
    .stChatFloatingInputContainer { background-color: transparent !important; }
    .element-container:last-child { margin-bottom: 100px; }
    
    /* Sembunyikan Header & Footer Default Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER APLIKASI
st.markdown("<div class='main-title'>SY-Core Genesis</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Sistem AI Sinkron | Developer: Slamet Yulianto</div>", unsafe_allow_html=True)

# 4. KONEKSI KE GROQ
try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Gagal inisialisasi AI: {e}")

# 5. MEMORI PERCAKAPAN
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. TOMBOL MIKROFON (Hanya Visual)
st.markdown("""
    <button class='mic-button' title='Fitur Suara (Segera Hadir)'>
        🎤
    </button>
    """, unsafe_allow_html=True)

# 7. INPUT & RESPON AI (Otomatis di Tengah Bawah)
if prompt := st.chat_input("Apa yang ingin kamu tanyakan ke SY-Core?"):
    # Simpan pesan kamu
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("SY-Core sedang berpikir..."):
            try:
                # Menggunakan Llama 3 yang gesit
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "Kamu adalah SY-Core Genesis v2, asisten AI cerdas buatan Slamet Yulianto. Jawablah dengan ramah, cerdas, dan sinkron."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                # Simpan pesan AI
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Maaf Met, koneksi terputus: {e}")
