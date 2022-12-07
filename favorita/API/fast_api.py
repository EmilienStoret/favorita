# $WIPE_BEGIN
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from favorita.split_push import download_blob
from favorita.functions_model import *
from favorita.data_viz import preproc_viz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return dict(greeting = "Hello")

@app.get("/predict")
def predict(store_nbr:int):
    file_name = f"split_data_bystore/store{store_nbr}.csv"
    destination_name=f"{store_nbr}.csv"
    download_blob(
        "favorita_batch1002",
        file_name,
        destination_name
        )

    df = pd.read_csv(destination_name)

    df = regressor_delimitor(df)

    # Get the new values of params for this store
    best_params = grid_search(df)

    # Get predictions
    pred, _ = get_forecast(df,best_params)


    return pred.to_json()
