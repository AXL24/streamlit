import streamlit as st
from merge import connect_to_mongodb, load_data_by_filter
import plotly.express as px
import pandas as pd

# Kết nối MongoDB
MONGO_URI = "mongodb+srv://axellent2004:0964212618@bigdata.l07vk.mongodb.net/"  # Thay bằng MongoDB URI của bạn
DATABASE_NAME = "thpt"

# Kích hoạt cache để lưu dữ liệu
@st.cache_data
def get_filtered_data(years, subjects):
    db = connect_to_mongodb(MONGO_URI, DATABASE_NAME)
    data = load_data_by_filter(db, year=years, subject=subjects)
    return data

# Ứng dụng chính
def main():
    st.title("Phân Tích Điểm THPT (1.5 triệu bản ghi)")

    # Sidebar: Chọn bộ lọc
    st.sidebar.header("Bộ lọc")
    years = st.sidebar.multiselect("Chọn năm", [2023, 2024], default=[2023, 2024])
    subjects = st.sidebar.multiselect(
        "Chọn môn học",
        ["toan", "ngu_van", "ngoai_ngu", "vat_li", "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdcd"],
        default=["toan", "ngu_van"],
    )

    # Lấy dữ liệu theo bộ lọc
    with st.spinner("Đang tải dữ liệu..."):
        data = get_filtered_data(years, subjects)

    # Hiển thị tổng quan dữ liệu
    st.subheader("Dữ liệu tổng quan")
    st.write(f"Số lượng bản ghi: {len(data)}")
    st.write(data.head(10))  # Hiển thị 10 dòng đầu tiên

    # Tính điểm trung bình theo môn học
    if not data.empty:
        st.subheader("Điểm trung bình theo môn học")
        avg_scores = data[subjects].mean().reset_index()
        avg_scores.columns = ["Subject", "Average Score"]
        st.write(avg_scores)

        # Biểu đồ điểm trung bình
        fig_avg = px.bar(avg_scores, x="Subject", y="Average Score", title="Điểm trung bình theo môn học")
        st.plotly_chart(fig_avg)

        # Biểu đồ phân phối điểm
        st.subheader("Phân phối điểm")
        for subject in subjects:
            fig_dist = px.histogram(data, x=subject, nbins=20, title=f"Phân phối điểm {subject}")
            st.plotly_chart(fig_dist)

        # Biểu đồ xu hướng điểm qua các năm
        st.subheader("Xu hướng điểm qua các năm")
        trend_data = data.groupby(["Year"])[subjects].mean().reset_index()
        trend_data = pd.melt(trend_data, id_vars=["Year"], var_name="Subject", value_name="Average Score")
        fig_trend = px.line(trend_data, x="Year", y="Average Score", color="Subject", title="Xu hướng điểm theo năm")
        st.plotly_chart(fig_trend)

if __name__ == "__main__":
    main()