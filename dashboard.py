import streamlit as st
import pandas as pd
import plotly.express as px
from merge import load_combined_data

# MongoDB Configuration
MONGO_URI = "mongodb+srv://axellent2004:0964212618@bigdata.l07vk.mongodb.net/"
DATABASE_NAME = "thpt"

# Streamlit App
def main():
    st.title("Phân Tích Điểm THPT Với MongoDB")

    # Load data
    with st.spinner("Đang tải dữ liệu..."):
        data = load_combined_data(MONGO_URI, DATABASE_NAME)

    # Sidebar filters
    st.sidebar.header("Bộ lọc")
    years = st.sidebar.multiselect("Chọn năm", [2022, 2023, 2024], [2022, 2023, 2024])
    subjects = st.sidebar.multiselect(
        "Chọn môn học",
        ["toan", "ngu_van", "ngoai_ngu", "vat_li", "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdcd"],
        ["toan", "ngu_van"]
    )
    roll_number = st.sidebar.text_input("Nhập số báo danh")
    selected_year = st.sidebar.selectbox("Chọn năm để tìm kiếm", [2022, 2023, 2024])

    # Filter data
    filtered_data = data[data["nam"].isin(years)]

    # Search by roll number
    st.subheader("1. Tìm kiếm dữ liệu theo số báo danh")
    if roll_number:
        search_results = filtered_data[(filtered_data["nam"] == selected_year) & (filtered_data["sbd"] == roll_number)]
        if not search_results.empty:
            st.write(f"Kết quả tìm kiếm cho SBD: {roll_number}, năm {selected_year}")
            st.dataframe(search_results)
        else:
            st.warning(f"Không tìm thấy kết quả cho SBD: {roll_number}, năm {selected_year}")

    # Show data
    st.subheader("2. Bộ dữ liệu tham khảo")
    st.write(f"Tổng số bản ghi: {len(filtered_data)}")
    st.dataframe(filtered_data.head(100))

    # Analyze and visualize data
    if not filtered_data.empty:
        st.subheader("3. Phân Tích Điểm Trung Bình")
        avg_scores = filtered_data[subjects].mean().reset_index()
        avg_scores.columns = ["Môn", "Điểm trung bình"]
        st.dataframe(avg_scores)
        st.plotly_chart(px.bar(avg_scores, x="Môn", y="Điểm trung bình", title="Điểm Trung Bình Theo Môn"))

        st.subheader("4. Phân Phối Điểm")
        for subject in subjects:
            st.plotly_chart(px.histogram(filtered_data, x=subject, nbins=20, title=f"Phân Phối Điểm {subject}"))

        st.subheader("5. Xu Hướng Điểm Qua Các Năm")
        trends = filtered_data.groupby("nam")[subjects].mean().reset_index()
        trends = pd.melt(trends, id_vars="nam", var_name="Môn", value_name="Điểm trung bình")
        st.plotly_chart(px.line(trends, x="nam", y="Điểm trung bình", color="Môn", title="Xu Hướng Điểm Theo Năm"))

if __name__ == "__main__":
    main()