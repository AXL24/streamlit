import streamlit as st
from merge import prepare
import pandas as pd
import plotly.express as px


combined_data= prepare()
df =pd.DataFrame(combined_data)
print(df.head(10))
