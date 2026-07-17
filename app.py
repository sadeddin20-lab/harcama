import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sado Başkan Harcama Takip", page_icon="💰")
st.title("💰 Sado Başkan Harcama Takip")

# Google Sheets'ten yayınladığınız CSV linkini buraya yapıştırın
SHEET_URL = "BURAYA_CSV_LINKINIZI_YAPISTIRIN"

@st.cache_data(ttl=60)
def veri_cek():
    return pd.read_csv(SHEET_URL)

try:
    df = veri_cek()
    
    # Sütun isimlerinizin Google Form'daki ile aynı olduğundan emin olun (Tutar, Tür, Kategori)
    # Metrikleri hesaplayalım
    toplam_gelir = df[df['Tür'] == 'Gelir']['Tutar'].sum()
    toplam_gider = df[df['Tür'] == 'Gider']['Tutar'].sum()
    net_bakiye = toplam_gelir - toplam_gider

    # Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Gelir", f"{toplam_gelir:,.2f} TL")
    col2.metric("Toplam Gider", f"{toplam_gider:,.2f} TL")
    col3.metric("Net Bakiye", f"{net_bakiye:,.2f} TL")

    st.subheader("📊 Sado Başkan Harcama Takip Özeti")
    st.bar_chart(df.groupby(["Tür", "Kategori"])["Tutar"].sum())
    
    with st.expander("Tüm Kayıtları Gör"):
        st.dataframe(df)

except Exception as e:
    st.info("Reisim, henüz veri girişi yok veya bağlantı bekleniyor.")
