from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
    message = client.messages.create(
        model='claude-sonnet-4-5',
        max_tokens = 1024,
        messages=[
            {"role": "user", "content": f"Based on this music query: {request.query}, recommend 3 songs. Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"}
        ]
    )
    import json
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
    for line in lines:
        if '#' not in line:
            split_lines = line.split('\t')
            tracks.append({'Artist': split_lines[0],
                          'Album': split_lines[1],
                          'Track': split_lines[2],
                          'Completion': split_lines[5]})
            
            listens_check = split_lines[0]  + ' - ' + split_lines[2]
            if listens_check not in listens:
                listens[listens_check] = {'plays': 0, 'skips': 0}
            
            if split_lines[5] == 'L':
                listens[listens_check]['plays'] += 1
            else:
                listens[listens_check]['skips'] += 1

    
    return{"tracks": tracks, 'Listens': listens}