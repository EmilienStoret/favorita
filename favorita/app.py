import streamlit as st
import pandas as pd
from favorita.functions_model import grid_search, get_forecast, store_selection, regressor_delimitor
from favorita.data_viz import preproc_viz, get_graph_monthly, get_graph_highest, get_graph_lowest
from PIL import Image

# Main page

st.title("Retail Sales Dashboard")

tab1, tab2, tab3 = st.tabs(['Favorita Sales', 'Upload your own data', 'Get your predictions'])

with tab1:
    st.header("Favorita Sales")
    ## Load data

    ## What is favorita, etc.

    # Predictions for the next quarter: give a range of dates and a prediction for period
    # Give error metrics and confidence intervals


    ## Prediction Charts and Data Analysis plots
    #st.plotly_chart("fig1.png")
    st.markdown("""--> Overall Prediction Plots \n \n Give some stats, etc.""")
    st.markdown("### Favorita Sales by Store")
    st.markdown("### Favorita Sales by Item")
    st.markdown("### Favorita Sales by Store and Item")


    # Causal Inference and Insights

with tab2:
    st.header("Upload your own data")
    st.markdown("Choose components to include in the analysis:")
    holydays = st.checkbox("Holydays")
    promotions = st.checkbox("Promotions")
    oilPrice = st.checkbox("Oil Price")

    st.markdown("_Your data must be a csv file in the following format:_")
    format = "date: datetime, sales: float, storeNbr: int, itemFamily: string" + (", isHoliday: bool" if holydays else '') + (", isPromo: bool" if promotions else '') + (", oilPrice: float" if oilPrice else '')
    columns = ["date", "sales", "storeNbr", "itemFamily"] + (["isHoliday"] if holydays else []) + (["isPromo"] if promotions else []) + (["oilPrice"] if oilPrice else [])
    st.markdown(f"```{format}```")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
       df = pd.read_csv(uploaded_file)
       assert df.columns == columns, "Wrong columns"
       st.write(df)

with tab3:
    #logo
    st.image('https://www.corporacionfavorita.com/wp-content/uploads/2020/03/logo-cf-footer.png', width= 200)

    # headers
    st.header("Get your predictions")
    st.markdown("Choose the store to include in the analysis:")

    # select a store number
    stores = range(1,55)
    value = st.selectbox('Select a store number', stores)
    df_store=store_selection(value)
    #st.dataframe(df_store)

    # add a button
    if st.button("Run the app"):

        # df to use
        df= regressor_delimitor(df_store)
        #st.write(df)

        #plot monthly sales
        data_preproc = preproc_viz(df, value)
        data_viz= get_graph_monthly(data_preproc)
        st.pyplot(data_viz)

        #plot top 5 families
        data_viz_highest= get_graph_highest(data_preproc)
        st.plotly_chart(data_viz_highest)

        #plot flop 5 families
        data_viz_lowest= get_graph_lowest(data_preproc)
        st.plotly_chart(data_viz_lowest)

        # Get the new values of params for this store
        st.warning("work in progress. Estimated wait time : 20min")
        st.markdown("get your Q2-2017 predictions")
        best_params = grid_search(df_store)
        #st.dataframe(best_params)

        # Get predictions
        pred, m=get_forecast(df,best_params)
        st.dataframe(pred)

        #plot prophet's components
        plot_comp = m.plot_components(pred)
        st.pyplot(plot_comp)
