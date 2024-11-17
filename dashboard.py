import streamlit as st
from merge import prepare
import pandas as pd
import plotly.express as px

def main():
    st.title("Phân Tích Điểm THPT 2022-2024")
    combined_data= prepare()
    df =pd.DataFrame(combined_data)
    st.subheader("First 10 Records")
    st.dataframe(df.head(10))


if __name__ == "__main__":
    main()