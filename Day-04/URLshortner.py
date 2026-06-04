from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime
import random
import string

app = FastAPI(
    title= "URL Shortner API",
    description="Mini Bitly Clone using FastAPI"
)

class URLRequest(BaseModel):
    url: str
    custom_code: str | None = None


url_database = {}

def generate_short_code(length = 6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = ""

        for _ in range(length):
            short_code += random.choice(characters)

        if short_code not in url_database:
            return short_code
        

@app.get("/home")
def home():
    return{
        "message":"Welcome to URL Shortner API"
    }

@app.post("/shorten", status_code=201)
def shorten_url(request:URLRequest):
    original_url = request.url
    custom_code = request.custom_code

    if custom_code:
        if custom_code in url_database:
            raise HTTPException(
                status_code=400,
                detail ="Custom short code already exists"
            )
        short_code = custom_code
    else:
        short_code = generate_short_code()

    shorten_url = f"http://127.0.0.1:8000/{short_code}"

    url_database[short_code] ={
        "original_url":original_url,
        "short_url":shorten_url,
        "clicks":0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return {
        "message":"Short URL created successfully",
        "short_code":short_code,
        "short_url": shorten_url
    }

@app.get("/urls")
def view_all_urls():
    return{
        "total_urls": len(url_database),
        "urls": url_database
    }

@app.get("/analytics/{short_code}")
def analytics(short_code:str):
    if short_code not in url_database:
        raise HTTPException(
            status_code=404,
            detail = "Short code not found"
        )
    
    return {
        "short_code": short_code,
        "original_url": url_database[short_code]["original_url"],
        "short_url": url_database[short_code]["short_url"],
        "clicks":url_database[short_code]["clicks"],
        "created_at": url_database[short_code]["created_at"]
    }


@app.get("/{short_code}")
def redirect_to_url(short_code:str):
    if short_code not in url_database:
        raise HTTPException(
            status_code=404,
            detail="Short code not found"
        )
    
    url_database[short_code]["clicks"] += 1

    return RedirectResponse(url=url_database[short_code]["original_url"])