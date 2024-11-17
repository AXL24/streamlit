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
    

        # Xu hướng điểm qua các năm
        