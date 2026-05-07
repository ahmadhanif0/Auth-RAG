from fastapi import APIRouter, HTTPException, Depends
from Schemas.userSchema import Signup, VerifyOTP
from models.user import User
from helpers.user_helper import ph, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from helpers.email_helpers import send_email
from datetime import datetime, timezone, timedelta
import random
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()

@user_router.post('/create_user')
async def create_user(data: Signup):

    user_exist = await User.get_or_none(email=data.email)
    if user_exist:
        raise HTTPException(status_code=400, detail="User already registered")
    
    hash = ph.hash(data.password)

    otp = str(random.randint(100000, 999999))
    
    user = await User.create(
        name = data.name,
        email = data.email,
        password = hash,
        otp_code=otp,
        otp_expiry=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    await send_email(
        to_email=user.email,
        subject="OTP your account",
        body=f"Your OTP is: {otp}. It expires in 5 minutes."
    )
    return {
        "message": "User created successfully",
        "email": user.email,
        "otp": user.otp_code
        }

@user_router.post('/verify')
async def verify_otp(data: VerifyOTP):
    user = await User.get_or_none(email = data.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    
    if user.is_verified:
        return{"message":"User is verified"}
    
    if user.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="OTP is not valid")
    
    if not user.otp_expiry or user.otp_expiry<datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP is expired")
    
    user.is_verified = True
    await user.save()
    return {"message":"User has been verified."}




@user_router.post('/login')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    try:
        ph.verify(user.password, form_data.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

@user_router.get("/profile")
async def profile(user: User = Depends(get_current_user)):
    return user