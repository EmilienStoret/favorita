import streamlit as st
import pandas as pd
from PIL import Image

# Main page

st.title("Retail Sales Dashboard")

tab1, tab2, tab4 = st.tabs(['Favorita Sales', 'Retail Sales', 'Forecast Q2 2017'])

with tab1:
    st.header("")
    ## Load data

    ## What is favorita, etc.


with tab2:
    st.header("Upload your own data")
    st.markdown("Choose components to include in the analysis:")
    holydays = st.checkbox("Holydays")
    promotions = st.checkbox("Promotions")
    oilPrice = st.checkbox("Oil Price")

    ## Load data
    format = "id: int, date: datetime, sales: float, storeNbr: int, itemFamily: string" + (", isHoliday: bool" if holydays else '') + (", isPromo: bool" if promotions else '') + (", oilPrice: float" if oilPrice else '')
    columns = ["id", "date", "sales", "storeNbr", "itemFamily"] + (["isHoliday"] if holydays else []) + (["isPromo"] if promotions else []) + (["oilPrice"] if oilPrice else [])
    st.markdown(f"_Your data must be a csv file in the following format:_ ```{format}```")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, parse_dates=['date'], usecols=columns, index_col='id')
            # assert set(df.columns) == set(columns), "Wrong columns"
            st.write(df.head())
        except Exception as e:
            st.markdown(f"__Wrong column format:__\n\n__{e}__")

with tab4:
    image1 = Image.open('charts_and_csv/components.png')
    image2 = Image.open('charts_and_csv/Q2_2017.png')
    image3 = Image.open('charts_and_csv/April_2017.png')
    st.header("Cross-val score MDAPE: 7.8%" )

    st.header("Forecast Q2 2017")
    st.image(image2)
    st.header("Forecast on April 2017 - Intra-month view")
    st.image(image3)
    st.header("Components of the model")
    st.image(image1)
    st.header("Download full quarter forecast (.csv format)")
    with open("charts_and_csv/forecast_Q2_2017.csv") as file:
        btn = st.download_button(
                label="Download",
                data=file,
                file_name='forecast.csv'
            )

# Predictions for the next quarter: give a range of dates and a prediction for period
# Give error metrics and confidence intervals


## Prediction Charts and Data Analysis plots
#st.plotly_chart("plotly chart")
# st.markdown("""--> Overall Prediction Plots \n \n Give some stats, etc.""")



# Causal Inference and Insights
