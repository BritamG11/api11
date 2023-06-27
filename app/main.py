import time
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from app.routers import company, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_company = [{"title": "J&Js", "content": "Hardware Store", "id": 1}, {
    "title": "Pizzarian", "content": "favourite foods", "id": 2}]


def find_company(id):
    for p in my_company:
        if p["id"] == id:
            return p


def find_index_company(id):
    for i, p in enumerate(my_company):
        if p['id'] == id:
            return i


app.include_router(company.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "This is Vision API"}
