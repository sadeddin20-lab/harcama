import pandas as pd
import streamlit as st
import os
from datetime import datetime

# Dosya yolu
FILE_NAME = "butce_takip.xlsx"

# Dosya yoksa oluştur
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Tarih", "Tutar", "Kategori", "Açıklama"])
    df.to_excel(FILE_NAME, index=False)

def main():
    st.set_page_config(page_title="Reis'in Bütçe Takibi", page_icon="💰")
    st.title("💰 Reisim Bütçe Takip")

    # Giriş Formu
    with st.form("harcama_formu", clear_on_submit=True):
        tutar = st.number_input("Tutar (TL)", min_value=0.0, step=1.0)
        kategori = st.selectbox("Kategori", ["Gıda", "Sağlık", "Yakıt", "Eğlence", "Fatura", "Diğer"])
        aciklama = st.text_input("Açıklama")
        submit = st.form_submit_button("Kaydet")

        if submit:
            yeni_veri = pd.DataFrame({
                "Tarih": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "Tutar": [tutar],
                "Kategori": [kategori],
                "Açıklama": [aciklama]
            })
            
            df = pd.read_excel(FILE_NAME)
            df = pd.concat([df, yeni_veri], ignore_index=True)
            df.to_excel(FILE_NAME, index=False)
            st.success("Reisim, harcamanız kaydedildi!")

    # Raporlama
    st.subheader("📊 Harcama Raporu")
    df = pd.read_excel(FILE_NAME)
    
    if not df.empty:
        st.dataframe(df.sort_values(by="Tarih", ascending=False))
        
        # Grafik
        st.write("### Kategori Bazlı Dağılım")
        chart_data = df.groupby("Kategori")["Tutar"].sum()
        st.bar_chart(chart_data)
    else:
        st.info("Henüz harcama girişi yok reisim.")

if __name__ == "__main__":
    main()
