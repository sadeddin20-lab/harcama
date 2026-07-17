import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sado Başkan Harcama Takip", page_icon="💰")
st.title("💰 Sado Başkan Harcama Takip")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7W0zpkVGhVfGTzarFLHZaHJrFgI3OxUae987DAKdGhC18JsNvKYFZtSHzGo4R06iEgh8b0IzTjgFP/pub?output=csv"

@st.cache_data(ttl=5)
def veri_cek():
    return pd.read_csv(SHEET_URL)

try:
    df = veri_cek()
    # Tablodaki sütun isimlerini ekrana yazdıralım ki hata yapmayalım
    st.write("Tablo Başlıkları:", df.columns.tolist())
    
    # Eğer "Tutar" sütununu bulamıyorsa, buraya gelen listedeki isme göre düzeltiriz
    toplam_gelir = df[df['Tür'] == 'Gelir']['Tutar'].sum()
    toplam_gider = df[df['Tür'] == 'Gider']['Tutar'].sum()
    
    st.metric("Net Bakiye", f"{toplam_gelir - toplam_gider:,.2f} TL")
    st.dataframe(df)

except Exception as e:
    st.error(f"Reisim, hata şurada: {e}")
