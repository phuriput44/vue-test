from fastapi import FastAPI, HTTPException, Depends, Response , File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import pandas as pd
import io
from pydantic import BaseModel
import sqlite3

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Database connection
conn = sqlite3.connect('job_register.db')
cursor = conn.cursor()


# Applicant model
class Applicant(BaseModel):
    firstName: str
    lastName: str
    address: str
    salaryExpectation: int
    experience: str


# ฟังก์ชันสำหรับตรวจสอบข้อมูลผู้ใช้ในฐานข้อมูล
def authenticate_user(username: str, password: str):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    return user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user[0], "token_type": "bearer"}


# Add applicant
@app.post("/applicants/")
async def add_applicant(applicant: Applicant):
    query = "INSERT INTO applicant (firstName, lastName, address, salaryExpectation, experience) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (
    applicant.firstName, applicant.lastName, applicant.address, applicant.salaryExpectation, applicant.experience))
    conn.commit()
    return {"message": "Applicant added successfully"}


# Get all applicants
@app.get("/applicants/")
async def get_all_applicants():
    query = "SELECT * FROM applicant"
    cursor.execute(query)
    applicants = cursor.fetchall()
    return [
        {"applicantID": row[0], "firstName": row[1], "lastName": row[2], "address": row[3], "salaryExpectation": row[4],
         "experience": row[5]} for row in applicants]


# Delete applicant
@app.delete("/applicants/{applicant_id}")
async def delete_applicant(applicant_id: int):
    query = "DELETE FROM applicant WHERE applicantID = ?"
    cursor.execute(query, (applicant_id,))
    conn.commit()
    return {"message": "Applicant deleted successfully"}


# Export Excel
@app.get("/export")
async def get_excel_data():
    query = "SELECT * FROM applicant"
    cursor.execute(query)
    applicants = cursor.fetchall()
    df = pd.DataFrame(applicants, columns=["applicantID", "firstName", "lastName", "address", "salaryExpectation", "experience"])

    output = io.BytesIO()
    df.to_csv(output, index=False)
    csv_data = output.getvalue()

    response = Response(content=csv_data, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    return response


# Upload CSV
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(file.file)
        df.to_sql("applicant", conn, if_exists="append", index=False)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error processing file", "detail": str(e)})

    return {"message": "File uploaded successfully"}