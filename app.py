import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Sado Başkan Harcama Takip", page_icon="💰")
st.title("💰 Sado Başkan Harcama Takip")

# Google Sheets'ten yayınlanan CSV linkiniz
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7W0zpkVGhVfGTzarFLHZaHJrFgI3OxUae987DAKdGhC18JsNvKYFZtSHzGo4R06iEgh8b0IzTjgFP/pub?output=csv"

@st.cache_data(ttl=10) 
def veri_cek():
    # Google Formlardan gelen veriyi çeker
    return pd.read_csv(SHEET_URL)

try:
    df = veri_cek()
    
    # Sütun isimlerinin Google Form'daki ile aynı olduğundan emin olun.
    # Google Formlar genellikle Türkçe karakterli başlıklar oluşturur.
    # Eğer tablonuzda farklılık olursa, buradaki isimleri tablonuzdaki başlıklarla değiştirin.
    
    # Metrik hesaplamaları
    toplam_gelir = df[df['Tür'] == 'Gelir']['Tutar'].sum()
    toplam_gider = df[df['Tür'] == 'Gider']['Tutar'].sum()
    net_bakiye = toplam_gelir - toplam_gider

    # Dashboard Görünümü
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Gelir", f"{toplam_gelir:,.2f} TL")
    col2.metric("Toplam Gider", f"{toplam_gider:,.2f} TL")
    col3.metric("Net Bakiye", f"{net_bakiye:,.2f} TL")

    # Grafik
    st.subheader("📊 Harcama ve Gelir Dağılımı")
    st.bar_chart(df.groupby(["Tür", "Kategori"])["Tutar"].sum())
    
    # Veri Tablosu
    st.subheader("📋 Detaylı Kayıtlar")
    st.dataframe(df.sort_values(by="Zaman Damgası", ascending=False))

except Exception as e:
    st.warning("Reisim, henüz veri girişi yok veya tablonuz boş. Lütfen formunuzu kullanarak ilk kaydınızı oluşturun!")
    st.write("Eğer hata devam ederse, tablonuzdaki sütun isimlerini (Tutar, Tür, Kategori) kontrol edin.")
