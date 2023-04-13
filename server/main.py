import uvicorn
import psycopg2 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dbfunctions import dsn
from dbfunctions import insert_data
from pydantic import BaseModel

app = FastAPI(
    title="471 Server",
)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class NewUser(BaseModel):
    fname: str
    lname: str
    email: str
    password: str
    city: str
    country: str

@app.post("/register")
async def register(new_user: NewUser):
    conn = psycopg2.connect(dsn.DSN)
   # Call the new_user_info function with the user data
    insert_data.new_user_info(
        new_user.email,
        new_user.fname,
        new_user.lname,
        new_user.password,
        new_user.city,
        new_user.country,
        conn,
    )
    conn.close()

class LoginUser(BaseModel):
    email: str
    password: str

# Create a /login endpoint
@app.post("/login")
async def login(login_user: LoginUser):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(dsn.DSN)

    # Call the check_user_credentials function with the user data
    is_valid_user = insert_data.check_user_credentials(login_user.email, login_user.password, conn)

    # Close the database connection
    conn.close()

    # Return the result
    if is_valid_user:
        return {"message": "Logged in successfully"}
    else:
        return {"message": "Invalid email or password"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
