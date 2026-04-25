from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

listening_history = {}

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
def recommendation():
    global listening_history
    history_dumped = json.dumps(listening_history)
    message = client.messages.create(
        model='claude-sonnet-4-5',
        max_tokens = 1024,
        messages=[
            {"role": "user", "content": f"Based on this music listening history: {history_dumped}, recommend 12 songs that are similar in style and mood.DO NOT include bands/artists that are present in listening history. Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"}
        ]
    )
    recs = json.loads(message.content[0].text)
    return{'Recommendations': recs}

@app.get("/")
def root():
    return{"message" : "Needledrop Api is Running"}

@app.post('/import')
async def upload_scrobbler(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode('UTF-8')
    lines = text.splitlines()
    tracks = []
    listens = {}
    global listening_history

    for line in lines:
        if '#' not in line:
            split_lines = line.split('\t')
            tracks.append({'Artist': split_lines[0],
                          'Album': split_lines[1],
                          'Track': split_lines[2],
                          'Completion': split_lines[5]})
            
            listens_check = split_lines[0]  + ' - ' + split_lines[2]
            
            if split_lines[5] == 'L' :
                if listens_check not in listens:
                    listens[listens_check] = {'plays': 0}
                listens[listens_check]['plays'] += 1
        
    listening_history = listens
    
    return{"tracks": tracks, 'Listens': listens}