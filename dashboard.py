import streamlit as st
from merge import prepare
import pandas as pd
import plotly.express as px


combined_data= prepare()
df =pd.DataFrame(combined_data)

def main():
    st.title("hello world")
    st.dataframe(df.head(10))

if __name__ == '__main__':
    main()