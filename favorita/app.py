import streamlit as st
import pandas as pd
from favorita.functions_model import grid_search, get_forecast, store_selection
from favorita.data_viz import preproc_viz, get_graph_monthly, get_graph_highest, get_graph_lowest, get_graph_pred, MAPE
from PIL import Image
import os

# Main page

st.title("Retail Sales Dashboard")

tab1, tab2 = st.tabs(['Forecast Q2-2017','Get your predictions'])

with tab1:
    #logo
    st.image('https://www.corporacionfavorita.com/wp-content/uploads/2020/03/logo-cf-footer.png', width= 200)

    #headers
    #st.markdown("Forecast Q2-2017")
    #st.write(os.getcwd())
    dir = os.path.dirname(__file__)
    image1 = Image.open(os.path.join(dir,'charts_and_csv/components.png'))
    image2 = Image.open(os.path.join(dir, 'charts_and_csv/Q2_2017.png'))
    image3 = Image.open(os.path.join(dir, 'charts_and_csv/April_2017.png'))
    st.write("Cross-val score **MDAPE: 7.8%**")

    st.markdown("Forecast Q2 2017")
    st.image(image2)
    st.markdown("Forecast on April 2017 - Intra-month view")
    st.image(image3)
    st.markdown("Components of the model")
    st.image(image1)
    st.markdown("Download full quarter forecast (.csv format)")
    with open(os.path.join(dir,"charts_and_csv/forecast_Q2_2017.csv")) as file:
        btn = st.download_button(label="Download",data=file,file_name='forecast.csv')

with tab2:
    #logo
    st.image('https://www.corporacionfavorita.com/wp-content/uploads/2020/03/logo-cf-footer.png', width= 200)

    # headers
    st.header("Get your predictions")
    st.markdown("Choose the store to include in the analysis:")

    # select a store number
    stores = range(1,55)
    value = st.selectbox('Select a store number', stores)
    df_store_raw, df_store, df_store_train = store_selection(value)
    #st.dataframe(df_store)

    # add a button
    if st.button("Run the app"):

        # df to use
        # df= regressor_delimitor(df_store)
        #st.write(df)

        #plot monthly sales
        st.markdown(f'**Store number {value} - sales analysis**')
        data_preproc = preproc_viz(df_store_raw, value)
        data_viz= get_graph_monthly(data_preproc)
        st.pyplot(data_viz)

        #plot flop 5 families
        data_viz_lowest= get_graph_lowest(data_preproc)
        st.plotly_chart(data_viz_lowest)

        #plot top 5 families
        data_viz_highest= get_graph_highest(data_preproc)
        st.plotly_chart(data_viz_highest)

        # Get the new values of params for this store
        #st.warning("work in progress. Estimated wait time : 20min")
        st.markdown("Get your Q2-2017 predictions")
        best_params = grid_search(df_store_train)
        #st.dataframe(best_params)

        # Get predictions
        #  st.markdown("Q2-2017: Predictions of the model")
        m, df_pred, pred_q2=get_forecast(df_store, df_store_train,best_params)
        st.dataframe(pred_q2)

        #plot prophet's components
        st.markdown("Components of the model")
        plot_comp = m.plot_components(df_pred)
        st.pyplot(plot_comp)

        # #plot predictions
        st.markdown("Q2-2017: Comparision between the predictions and the true sales")
        plot_pred = get_graph_pred(df_store, df_pred)
        st.pyplot(plot_pred)

        st.markdown("Score of the model")
        #st.dataframe(df_pred)
        #st.dataframe(df_store)
        MAPE = MAPE(df_store,df_pred)
        st.write(f'MAPE  **{MAPE:.2f} %**')
