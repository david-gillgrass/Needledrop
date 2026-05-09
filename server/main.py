from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from anthropic import Anthropic
from dotenv import load_dotenv
from groq import Groq
import json
import httpx
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse

load_dotenv()
client_claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
lastfm_api = os.getenv("LASTFM_API_KEY")
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
spotify_token = None

sp_oauth = SpotifyOAuth(
    client_id = spotify_client_id,
    client_secret = spotify_client_secret,
    redirect_uri = spotify_redirect_uri,
    scope="user-top-read, user-read-recently-played"
)

listening_history = {}
spotify_artists = []

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

def get_artwork(recs):
    global spotify_token
    for rec in recs:
        
        if spotify_token:
            try:
                sp = spotipy.Spotify(auth=spotify_token)
                artwork = sp.search(rec['artist'],limit=5, type='artist')
                print(artwork)
                items = artwork['artists']['items']
                for item in items:
                    if items and item['name'].lower() == rec['artist'].lower():
                        rec['image'] = item['images'][0]['url']
                        break
                    else:
                        rec['image'] = ''
            except:
                    try:
                        response = httpx.get(
                        f'https://en.wikipedia.org/api/rest_v1/page/summary/{rec['artist'].replace(" ","_")}',
                        follow_redirects = True,
                        headers ={"User-Agent": "NeedleDrop/1.0 (https://github.com/david-gillgrass/needledrop; david.gillgrass@gmail.com)"}
                    )
                        data = response.json()
                        rec['image'] = data.get('thumbnail', {}).get('source', '')
                    except Exception as ex:
                        print(f"Error for {rec['artist']}: {ex}")
                        rec['image'] = ''
        else:
            try:
                response = httpx.get(
                    f'https://en.wikipedia.org/api/rest_v1/page/summary/{rec['artist'].replace(" ","_")}',
                    follow_redirects = True,
                    headers ={"User-Agent": "NeedleDrop/1.0 (https://github.com/david-gillgrass/needledrop; david.gillgrass@gmail.com)"}
                )
                data = response.json()
                rec['image'] = data.get('thumbnail', {}).get('source', '')
            except Exception as ex:
                print(f"Error for {rec['artist']}: {ex}")
                rec['image'] = ''
    return recs



@app.post('/recommendation')
def recommendation(request: SearchRequest):
    print(request.aiAgent)
    global listening_history
    global spotify_artists
    context = ''

    artists_dumped = json.dumps(spotify_artists) if spotify_artists else ''
    history_dumped = json.dumps(listening_history) if listening_history else ''

    if artists_dumped:
        context += f'Spotify artists: {artists_dumped} '
    if history_dumped:
        context += f'Scrobbler artists: {history_dumped}'

    
    if (listening_history or artists_dumped) and request.query:
        prompt = f"Based on this music listening history: {context}, and user search {request.query} recommend 12 songs that are similar to listening history, try to include a recommendation for the most common genres in the history. Avoid bands/artists that are present in listening history. In the reason include which artist they are similar to. Do NOT recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    elif listening_history or artists_dumped:
        prompt = f"Based on this music listening history: {context}, recommend 12 songs that are similar to listening history, try to include a recommendation for the most common genres in the history. Avoid bands/artists that are present in listening history. In the reason include which artist they are similar to. Do NOT recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    elif request.query:
        prompt = f"Based on this music related user search: {request.query}, recommend 12 songs that are relevant to the user search try to include a recommendation for the most common genres similar to the search. In the reason include which artist they are similar to. Do NOT recommend the same artists on consecutive runs! Return ONLY a JSON array with no markdown, no backticks, just raw JSON in this exact format: [{{\"artist\": \"name\", \"album\": \"name\", \"title\": \"name\", \"reason\": \"reason\"}}]"
    else:
        return {"Recommendations":[],"error":"Please login to Spotify, upload a scrobbler file or enter a query."}
    
    if request.aiAgent == "claude":
        message = client_claude.messages.create(
            model='claude-sonnet-4-5',
            max_tokens = 1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    else:
        message = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile" if request.aiAgent == "groq+" else "llama-3.1-8b-instant",
            max_tokens = 1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    content = message.content[0].text if request.aiAgent == 'claude' else message.choices[0].message.content
    start = content.find('[')
    end = content.rfind(']')+1
    content = content[start:end]
    recs = json.loads(content)

    get_artwork(recs)

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

@app.get('/spotify/login')
def Spotifylogin():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@app.get('/callback')
def spotifyCallback(code: str):
    global spotify_token
    token_info = sp_oauth.get_access_token(code)
    spotify_token = token_info['access_token']
    return RedirectResponse('http://localhost:5173?spotify=connected')

@app.get('/spotify/top-artists')
def get_top_artists():
    global spotify_token
    global spotify_artists
    
    if not spotify_token:
        return {"Error": "User not logged in to spotify"}
    
    sp = spotipy.Spotify(auth=spotify_token)
    top_artists = sp.current_user_top_artists(limit=20, time_range='medium_term')

    artists = []

    for artist in top_artists['items']:
        artists.append({
            'name' : artist['name'],
            'image' : artist['images'][0]['url'] if artist['images'] else ''
        })
    
    for artist in artists:
        spotify_artists.append(artist['name'])

    return{'artists' : artists}

@app.get('/spotify/track')
def find_id(artist:str, title:str):
    global spotify_token

    if not spotify_token:
        return{"Error":"Not Connected to Spotify"}
    else:
        sp = spotipy.Spotify(auth=spotify_token)
        result = sp.search(f'{artist} {title}', limit=1, type='track')
        track_id = result['tracks']['items'][0]['id']
    
    return {"track_id": track_id}
