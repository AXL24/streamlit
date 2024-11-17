import streamlit as st
from merge import prepare
import pandas as pd
import plotly.express as px


combined_data= prepare()
print(combined_data)
