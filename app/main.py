import uvicorn
from fastapi import FastAPI, UploadFile
import pandas as pd
from db import validtion_of_file

app = FastAPI()


@app.post("/upload")
def get_file_weapon(file:UploadFile):
    file = pd.read_csv(file.file)
    return validtion_of_file(file)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost",port=8000 , reload=True)
