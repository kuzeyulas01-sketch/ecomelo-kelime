import streamlit as st
import os
import random

# Sayfa Ayarları ve Kalp İkonu
st.set_page_config(page_title="Quizlet Kelime Kartlarım", page_icon="❤️", layout="centered")

# 🔐 GÜVENLİK VE GİRİŞ KONTROLÜ
DOGRU_KULLANICI = "ecomelo"
DOGRU_SIFRE = "ivandor"

if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

if not st.session_state["giris_yapildi"]:
    st.title("🔒 Özel Kelime Kartları")
    st.write("Bu siteye sadece yetkili kişiler erişebilir. Lütfen giriş yap:")
    kullanici_adi = st.text_input("Kullanıcı Adı:")
    sifre = st.text_input("Şifre:", type="password")
    if st.button("Giriş Yap 🚀", use_container_width=True):
        if kullanici_adi == DOGRU_KULLANICI and sifre == DOGRU_SIFRE:
            st.session_state["giris_yapildi"] = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre! ❌")
    st.stop()

# ---------------------------------------------------------------------
# 📚 TXT DOSYASINDAN KELİMELERİ OKUYAN SİSTEM
# ---------------------------------------------------------------------
@st.cache_data
def kelimeleri_yukle():
    kelime_listesi = []
    if os.path.exists("kelimeler.txt"):
        with open("kelimeler.txt", "r", encoding="utf-8", errors="ignore") as f:
            for satir in f:
                satir_temiz = satir.strip()
                if not satir_temiz:
                    continue
                if " - " in satir_temiz:
                    parcalar = satir_temiz.split(" - ", 1)
                    kelime_listesi.append({"ing": parcalar[0].strip(), "tr": parcalar[1].strip()})
    return kelime_listesi

KELIMELER = kelimeleri_yukle()

# Hafızada aktif kelimeyi tutmak için session state
if "aktif_kart" not in st.session_state and KELIMELER:
    st.session_state["aktif_kart"] = random.choice(KELIMELER)

# ⚙️ QUIZLET TARZI CSS TASARIMI (3D DÖNME EFEKTİ)
st.markdown("""
<style>
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 250px;
        perspective: 1000px;
        margin: 20px 0;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    /* Karta dokunulduğunda veya mouse üzerine geldiğinde dönecek */
    .flip-card:hover .flip-card-inner, .flip-card:active .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        padding: 20px;
    }
    /* Ön Yüz Tasarımı (Quizlet Mavisi/Morusu) */
    .flip-card-front {
        background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%);
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    /* Arka Yüz Tasarımı (Temiz Beyaz ve Pembe Detay) */
    .flip-card-back {
        background-color: #ffffff;
        color: #333333;
        transform: rotateY(180deg);
        font-size: 24px;
        border: 3px solid #8E2DE2;
    }
    .hint-text {
        font-size: 13px;
        margin-top: 15px;
        opacity: 0.7;
        font-weight: normal;
    }
</style>
""", unsafe_allow_html=True)

# Arayüz Başlığı
st.title("🎴 Quizlet Kelime Kartlarım")
st.write("Kartın üzerine gelerek veya dokunarak arkasındaki Türkçe anlamını görebilirsin! ✨")

# Üst Butonlar (Rastgele ve Çıkış)
col_cikis, col_random = st.columns([1, 1])
with col_cikis:
    if st.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state["giris_yapildi"] = False
        st.clear_checkpoint()
        st.rerun()
with col_random:
    if st.button("🎲 Rastgele Kelime Getir", type="primary", use_container_width=True):
        if KELIMELER:
            st.session_state["aktif_kart"] = random.choice(KELIMELER)
            st.rerun()

st.divider()

# Kartı Ekrana Basma
if KELIMELER and "aktif_kart" in st.session_state:
    kart = st.session_state["aktif_kart"]
    
    card_html = f"""
    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <div>🇬🇧 {kart['ing'].upper()}</div>
                <div class="hint-text">Anlamını görmek için dokun veya üzerinde dur 🔄</div>
            </div>
            <div class="flip-card-back">
                <div style="font-size: 14px; color: #8E2DE2; margin-bottom: 10px; font-weight: bold;">TÜRKÇE KARŞILIĞI</div>
                <div>🇹🇷 {kart['tr']}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
else:
    st.error("⚠️ kelimeler.txt dosyasından kelimeler okunamadı!")
