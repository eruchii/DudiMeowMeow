
import dateutil.parser
import pickle
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import os
import json

import aiofiles
import asyncio
from bs4 import BeautifulSoup
from models import Chapter
from paginate import paginate

from preload import preload

app = FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global data
data = []

@app.on_event("startup")
async def startup():
    preload()
    global data
    with open("manga.dat", "rb") as f:
        data = pickle.load(f)
    data.sort(reverse=True, key = lambda x: dateutil.parser.isoparse(x.lastUpdate))

@app.get("/api/mangas")
async def get_mangas(page: int = 1, page_size: int = 8):
    return { "data" : paginate(data, page, page_size), "page": page, "page_size": page_size, "total": len(data) }

@app.get("/api/mangas/{id}")
async def get_manga(id: int = None):
    if(id == None):
        raise HTTPException(status_code=500, detail="???")
    for manga in data:
        if(manga.id == id):
            return manga
    raise HTTPException(status_code=404, detail="Manga not found")

@app.get("/api/mangas/{manga_id}/chapters")
async def get_chapters(manga_id: int = None):
    if(manga_id == None):
        raise HTTPException(status_code=500, detail="???")
    for manga in data:
        if(manga.id == manga_id):
            return manga.chapters
    raise HTTPException(status_code=404, detail="Manga not found")

@app.get("/api/mangas/{manga_id}/chapters/{chapter_id}")
async def get_chapters(manga_id: int = None, chapter_id: int = None):
    if(manga_id == None or chapter_id == None):
        raise HTTPException(status_code=500, detail="???")
    chapters = None
    for manga in data:
        if(manga.id == manga_id):
            chapters = manga.chapters
            break
    if(chapters == None):
        raise HTTPException(status_code=404, detail="Manga not found")
    chapter = None
    for c in chapters:
        if(c.id == chapter_id):
            chapter = c
            break
    if(chapter == None):
        raise HTTPException(status_code=404, detail="Chapter not found")
    path = "./data/{}/{}".format(manga_id, chapter_id)
    if(not os.path.exists(path)):
        raise HTTPException(status_code=404, detail="Resource not found")
    d = c.__dict__
    d["maxID"] = len(os.listdir(path))+1
    d["mangaID"] = manga_id 
    return Chapter(d)
    
    