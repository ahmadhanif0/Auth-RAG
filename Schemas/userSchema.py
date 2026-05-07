from pydantic import BaseModel

class Signup(BaseModel):
    name : str
    email : str
    password : str

class VerifyOTP(BaseModel):
    email: str
    otp: str


