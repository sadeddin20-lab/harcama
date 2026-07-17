import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sado Başkan Harcama Takip", page_icon="💰")
st.title("💰 Sado Başkan Harcama Takip")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7W0zpkVGhVfGTzarFLHZaHJrFgI3OxUae987DAKdGhC18JsNvKYFZtSHzGo4R06iEgh8b0IzTjgFP/pub?output=csv"

@st.cache_data(ttl=5)
def veri_cek():
    df = pd.read_csv(SHEET_URL)
    # Sütun isimlerindeki boşlukları temizleyelim reisim
    df.columns = df.columns.str.strip()
    return df

try:
    df = veri_cek()
    
    # Artık boşluksuz halleriyle (Tutar, Tür, Kategori, Açıklama) çalışabiliriz
    toplam_gelir = df[df['Tür'] == 'Gelir']['Tutar'].sum()
    toplam_gider = df[df['Tür'] == 'Gider']['Tutar'].sum()
    net_bakiye = toplam_gelir - toplam_gider

    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Gelir", f"{toplam_gelir:,.2f} TL")
    col2.metric("Toplam Gider", f"{toplam_gider:,.2f} TL")
    col3.metric("Net Bakiye", f"{net_bakiye:,.2f} TL")

    st.subheader("📊 Harcama Dağılımı")
    st.bar_chart(df.groupby(["Tür", "Kategori"])["Tutar"].sum())
    
    st.subheader("📋 Detaylı Kayıtlar")
    st.dataframe(df)

except Exception as e:
    st.error(f"Reisim, sistem çalışmaya hazır, ilk verinizi girin! Hata detayı: {e}")
