import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import time

# Set page configuration
st.set_page_config(page_title="Analisis Korelasi", 
                   page_icon=":cat:", 
                   layout="wide") 

# Upload data
st.title("Aplikasi Analisis Korelasi")
st.write("Unggah data Anda dalam format CSV:")
if st.button("Peringatan (klik disini)"):
    st.info("Bersihkan data sebelum menganalisis korelasi!")
    time.sleep(3)
    st.empty()
uploaded_file = st.file_uploader("Pilih file CSV:", type=["csv"])

# Jika data diunggah
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# Tampilkan dataset
    st.subheader("Data Anda:")
    st.dataframe(df, height=200)

# Pilih kolom untuk analisis
    st.sidebar.subheader("Pilih Variabel/Kolom untuk Analisis Korelasi:")
    columns = df.columns
    selected_columns = st.sidebar.multiselect("Pilih Variabel/Kolom", columns)

# Metode Korelasi
    st.sidebar.subheader("Pilih Metode Korelasi:")
    correlation_method = st.sidebar.radio("Metode Korelasi:", ("Pearson", "Spearman", "Kendall's Tau"))

# DataFrame hasil analisis
    corr_result = pd.DataFrame()

# Analisis Korelasi
    if len(selected_columns) > 1:
        st.subheader("Hasil Analisis Korelasi:")
        if correlation_method == "Pearson":
            correlation_matrix = df[selected_columns].corr(method="pearson")
        elif correlation_method == "Spearman":
            correlation_matrix = df[selected_columns].corr(method="spearman")
        elif correlation_method == "Kendall's Tau":
            correlation_matrix = df[selected_columns].corr(method="kendall")

# Simpan hasilnya
        corr_result = correlation_matrix

# Opsi ngurutin
        sort_option = st.selectbox("Urutkan dari:",["None","Tinggi ke Rendah","Rendah ke Tinggi"])
        if sort_option == "None":
            correlation_stack = correlation_matrix.stack().reset_index()
            correlation_stack.columns = ["Kolom 1", "Kolom 2", "Nilai Korelasi"]
            sorted_correlation = correlation_stack
        elif sort_option == "Tinggi ke Rendah":
            correlation_stack = correlation_matrix.stack().reset_index()
            correlation_stack.columns = ["Kolom 1", "Kolom 2", "Nilai Korelasi"]
            sorted_correlation = correlation_stack.sort_values(by="Nilai Korelasi", ascending=False)
        elif sort_option == "Rendah ke Tinggi":
            correlation_stack = correlation_matrix.stack().reset_index()
            correlation_stack.columns = ["Kolom 1", "Kolom 2", "Nilai Korelasi"]
            sorted_correlation = correlation_stack.sort_values(by="Nilai Korelasi")

# Tampilkan hasil (tabel)
        st.subheader("Tabel Hasil Analisis Korelasi:")
        st.dataframe(sorted_correlation, height=200)

# Pilihan visualisasi
        st.sidebar.subheader("Pilih Tampilan Visualisasi")
        vis_option = st.sidebar.radio("Pilihan Visualisasi:",("Heatmap","Scatter Plot"))

# Heatmap
        if vis_option == "Heatmap":
            heatmap_color = st.sidebar.selectbox("Pilih Warna Heatmap", 
                                                ["coolwarm", "YlGnBu", "Reds", 
                                                "viridis", "cividis"], key="heatmap_select")
            st.subheader("Visualisasi Heatmap:")
            fig, ax = plt.subplots()
            sns.heatmap(correlation_matrix, annot=True, cmap=heatmap_color, linewidths=0.5, ax=ax)
            st.pyplot(fig)
# Scatter Plot
        elif vis_option == "Scatter Plot":
            st.subheader("Visualisasi Scatter Plot:")
            x_col = st.selectbox("Pilih Kolom X:",selected_columns)
            y_col = st.selectbox("Pilih komom Y:",selected_columns)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            fig, ax = plt.subplots()
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_col, y=y_col)
            st.pyplot()

# Opsi menampilakan perbandingan
        st.subheader("Ingin membandingkan hasil analisis korelasi antar metode?")
        compare = st.radio("Pilih:",("Tidak", "Iya"))
        
        if compare == "Iya":
            st.subheader("Perbandingan Metode Korelasi:")
            compare_options = st.selectbox ("Pilih metode untuk dibandingkan:",
                                            ["Pearson dengan Spearman",
                                            "Pearson dengan Kendall's Tau",
                                            "Spearman dengan Kendall's Tau"])
            methods = {"Pearson dengan Spearman": ("pearson", "spearman"),
                        "Pearson dengan Kendall's Tau": ("pearson", "kendall"),
                        "Spearman dengan Kendall's Tau": ("spearman", "kendall")
                        }
            if compare_options in methods:
                method1, method2 = methods[compare_options]
                correlation_matrix = df[selected_columns].corr(method=method1)
                correlation_matrix1 = df[selected_columns].corr(method=method2)
                st.write(f"Metode {compare_options} :",correlation_matrix,correlation_matrix1)
            else:
                st.write("Pilih metode perbandingan")
        else:
            st.write("OK, tidak dibandingkan")
    
# Link buat download
        def get_csv_download_link(dataframe, filename):
            csv = dataframe.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Unduh CSV</a>'
            return href
        st.write("Klik tautan di bawah ini untuk mengunduh hasil analisis korelasi:")
        st.markdown(get_csv_download_link(sorted_correlation, "analisis_korelasi"), unsafe_allow_html=True)

    else:
        st.warning("Pilih minimal dua kolom/variabel untuk analisis korelasi. Pilihan kolom/variabel ada di sidebar(kiri, atas)")