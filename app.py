import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sado Başkan Harcama Takip", page_icon="💰")
st.title("💰 Sado Başkan Harcama Takip")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7W0zpkVGhVfGTzarFLHZaHJrFgI3OxUae987DAKdGhC18JsNvKYFZtSHzGo4R06iEgh8b0IzTjgFP/pub?output=csv"

@st.cache_data(ttl=5)
def veri_cek():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

df = veri_cek()
df = df[df['Tür'].isin(['Gelir', 'Gider'])]

toplam_gelir = df[df['Tür'] == 'Gelir']['Tutar'].sum()
toplam_gider = df[df['Tür'] == 'Gider']['Tutar'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Gelir", f"{toplam_gelir:,.2f} TL")
col2.metric("Toplam Gider", f"{toplam_gider:,.2f} TL")
col3.metric("Net Bakiye", f"{toplam_gelir - toplam_gider:,.2f} TL")

# GRAFİK KISMI DÜZELTİLDİ:
st.subheader("📊 Harcama Dağılımı")
chart_data = df.groupby(["Tür", "Kategori"])["Tutar"].sum().reset_index()
st.bar_chart(chart_data, x="Kategori", y="Tutar", color="Tür")

st.subheader("📋 Detaylı Kayıtlar")
st.dataframe(df)
