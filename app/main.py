import uvicorn
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from validetion import validtion_of_file
from db import get_db_connection, init_connection_pool, insert_data_to_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    get_db_connection()
    init_connection_pool()



@app.post("/upload")
def get_file_weapon(file:UploadFile = File(...)):
    file_weapon = pd.read_csv(file.file, encoding="utf-8")
    claen_data = validtion_of_file(file_weapon)
    response = insert_data_to_db(claen_data)
    return response



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost",port=8000 , reload=True)
