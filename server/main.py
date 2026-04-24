from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/recommendation')
def recommendation(request: SearchRequest):
    return{'Recommendations': [
        { "artist": "Radiohead", "album": "OK Computer", "title": "Karma Police", "reason": "You like alternative rock" },
        { "artist": "Guns N' Roses", "album": "Appetite for Destruction", "title": "Welcome to the Jungle", "reason": "It Rocks!" },
        { "artist": "Van Halen", "album": "1984", "title": "Jump", "reason": "High energy classic rock" },
    ]}

@app.get("/")
def root():
    return{"message" : "Needledrop Api is Running"}