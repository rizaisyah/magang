import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64


def import_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        return None
    
def calculate_correlation(data, selected_columns, correlation_method):
    
    if len(selected_columns) > 1:
        st.subheader(f"Hasil Analisis Korelasi (Metode: {correlation_method}):")
        if correlation_method == "Pearson":
            correlation_matrix = data[selected_columns].corr(method="pearson")
        elif correlation_method == "Spearman":
            correlation_matrix = data[selected_columns].corr(method="spearman")
        elif correlation_method == "Kendall":
            correlation_matrix = data[selected_columns].corr(method="kendall")
       
        sort_option = st.selectbox("Urutkan dari:",["tinggi ke rendah","rendah ke tinggi"])
        if sort_option == "tinggi ke rendah":
            correlation_stack = correlation_matrix.stack().reset_index()
            correlation_stack.columns = ["Kolom 1", "Kolom 2", "Korelasi"]
            sorted_correlation = correlation_stack.sort_values(by="Korelasi", ascending=False)
        elif sort_option == "rendah ke tinggi":
            correlation_stack = correlation_matrix.stack().reset_index()
            correlation_stack.columns = ["Kolom 1", "Kolom 2", "Korelasi"]
            sorted_correlation = correlation_stack.sort_values(by="Korelasi")

        st.subheader("Hasil analisis korelasi")
        st.write(sorted_correlation)

        st.sidebar.subheader("Pilih tampilan visualisasi")
        visualisation = st.sidebar.radio("Pilihan Visualisasi:",("Heatmap",
                                       "Scatter Plot"))
        if visualisation == "Heatmap":
            heatmap_color = st.sidebar.selectbox("Pilih Warna Heatmap", ["Reds", "YlGnBu", "coolwarm", "viridis", "cividis"], key="heatmap_select")
            st.subheader("Visualisasi Heatmap:")
            fig, ax = plt.subplots()
            sns.heatmap(correlation_matrix, annot=True, cmap=heatmap_color, linewidths=0.5, ax=ax)
            st.pyplot(fig)

        # Visualisasi Scatter Plot
        elif visualisation == "Scatter Plot":
            st.subheader("Visualisasi Scatter Plot:")
            x_col = st.selectbox("Pilih Kolom X:", selected_columns)
            y_col = st.selectbox("Pilih komom Y:", selected_columns)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x=x_col, y=y_col)
            st.pyplot(fig)

def main():
    st.set_page_config(
        page_title = "Website Analisis Korelasi",
        layout = "wide"
    )

    st.title("Website Analisis Korelasi")
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

    if uploaded_file is not None:
        data = import_data(uploaded_file)

        #menampilkan data
        st.subheader("Data Anda:")
        st.write(data.head())

        #pilih kolom
        st.sidebar.subheader("Pilih Kolom")
        columns = data.columns
        selected_columns = st.sidebar.multiselect("Pilih kolom yang akan dianalisis", columns)
        
        #pilih korelasi
        st.sidebar.subheader("Pilih Metode Korelasi:")
        correlation_method = st.sidebar.radio("Metode Korelasi:", ("Pearson", "Spearman", "Kendall"))
        
        calculate_correlation(data, selected_columns, correlation_method)    

def get_csv_download_link(dataframe, filename):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Unduh CSV</a>'
    st.write("Klik tautan di bawah ini untuk mengunduh hasil analisis korelasi:")
    st.markdown(get_csv_download_link(correlation_stack, "analisis_korelasi"), unsafe_allow_html=True)
    return href
gghhhhhghghghgh

main()