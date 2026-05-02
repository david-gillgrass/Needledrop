from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from anthropic import Anthropic
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
client_claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

listening_history = {}

class SearchRequest(BaseModel):
    query: str = ''
    aiAgent: str = ''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/recommendation')
def recommendation(request: SearchRequest):
    print(request.aiAgent)
    global listening_history
    history_dumped = json.dumps(listening_history) if listening_history else ''
    if listening_history and request.query:
        prompt = f"Based on this music listening history: {history_dumped}, and user search {request.query} recommend 12 songs that are similar to listening history, try to include a recommendation for the most common genres in the history. Avoid bands/artists that are present in listening history. In the reason include which artist they are similar to. Do Not recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    elif listening_history:
        prompt = f"Based on this music listening history: {history_dumped}, recommend 12 songs that are similar to listening history, try to include a recommendation for the most common genres in the history. Avoid bands/artists that are present in listening history. In the reason include which artist they are similar to. Do Not recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    elif request.query:
        prompt = f"Based on this music related user search: {request.query}, recommend 12 songs that are relevant to the user search try to include a recommendation for the most common genres similar to the search. In the reason include which artist they are similar to. Do Not recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    else:
        return {"Recommendations":[],"error":"Please upload a scrobbler file or enter a query."}
    
    if request.aiAgent == "claude":
        message = client_claude.messages.create(
            model='claude-sonnet-4-5',
            max_tokens = 1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        recs = json.loads(message.content[0].text)
    else:
        message = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens = 1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        recs = json.loads(message.choices[0].message.content)

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