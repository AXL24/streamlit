import streamlit as st
from merge import prepare
import pandas as pd
import plotly.express as px


combined_data= prepare()
df =pd.DataFrame(combined_data)

def calculate_average_scores(data):
    subject_columns = ["toan", "ngu_van", "ngoai_ngu", "vat_li", "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdcd"]
    averages = data[subject_columns].mean().reset_index()
    averages.columns = ["Subject", "Average_Score"]
    return averages


def main():
    st.title("Phân Tích Điểm THPT 2022-2024")

    # Sidebar lọc dữ liệu
    st.sidebar.header("Bộ lọc")
    years = combined_data["Year"].unique()
    selected_years = st.sidebar.multiselect("Chọn năm", years, default=years)

    sbd_list = combined_data["sbd"].unique()
    selected_sbd = st.sidebar.multiselect("Chọn SBD", sbd_list, default=sbd_list)

    # Lọc dữ liệu (moved inside functions)
    def get_filtered_data():
        return combined_data[(combined_data["Year"].isin(selected_years)) & (combined_data["sbd"].isin(selected_sbd))]

    # Hiển thị dữ liệu
    filtered_data = get_filtered_data()  # Call the function
    st.subheader("Dữ liệu điểm đã lọc")
    if not filtered_data.empty:
        st.write(filtered_data)

        # Điểm trung bình các môn
        st.subheader("Điểm trung bình các môn")
        avg_scores = calculate_average_scores(filtered_data)
        st.write(avg_scores)

        # Biểu đồ phân phối điểm
        st.subheader("Phân phối điểm")
        if not filtered_data.empty:
            fig = px.histogram(filtered_data, x="toan", nbins=10, title="Phân phối điểm Toán")
            st.plotly_chart(fig)

        # Điểm trung bình theo từng môn học
        st.subheader("Điểm trung bình theo môn học")
        if not filtered_data.empty:
            fig = px.bar(avg_scores, x="Subject", y="Average_Score", title="Điểm trung bình theo môn")
            st.plotly_chart(fig)

        # Xu hướng điểm qua các năm
        st.subheader("Xu hướng điểm qua các năm")
        if not filtered_data.empty:
            trend_data = filtered_data.groupby(["Year"]).mean().reset_index()
            fig = px.line(trend_data, x="Year", y="toan", title="Xu hướng điểm Toán qua các")