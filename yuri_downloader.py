import json
from time import sleep
import aiofiles
from matplotlib import image
import requests
import os

from models import Chapter
from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def load_manga(id: str, update: bool = False):
    print("Manga_id = {}".format(id))
    if(not update):
        if(os.path.exists("./data/" + id)):
            return
    res = []
    manga_url = "https://api.yurineko.net/manga/{}".format(id)
    try:
        os.mkdir("./data/{0}".format(id))
    except Exception:
        pass
    manga = requests.get(manga_url)
    with open("./data/{}/{}.json".format(id, id), "w", encoding="utf-8") as f:
        f.write(manga.text)

    manga_json = json.loads(manga.text)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "https://yurineko.net/",
        "Connection": "keep-alive"
    }
    latest_chapter_url = "https://yurineko.net/read/{}/{}".format(
        id, manga_json["chapters"][0]["id"])
    latest_chapter = requests.get(latest_chapter_url, headers=headers)
    soup = BeautifulSoup(latest_chapter.content, "html.parser")
    chapters_data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
    with open("./data/{}/chapters.json".format(id), "w", encoding="utf-8") as f:
        f.write(chapters_data.text)


async def download_image(session, url, path):
    if(not os.path.exists(path)):
        req = await session.get(url)
        data = await req.content.read()
        async with aiofiles.open(path, "wb") as f:
            await f.write(data)
        print("Finish: {}".format(url))

async def download_images(chapter: Chapter, update = False):
    images = chapter.urls
    if(not update and os.path.exists("./data/{0}/{1}".format(chapter.manga_id, chapter.id))):
        return
    try:
        os.mkdir("./data/{0}".format(chapter.manga_id))
    except Exception:
        pass
    try:
        os.mkdir("./data/{0}/{1}".format(chapter.manga_id, chapter.id))
    except Exception:
        pass
    
    tasks = []
    async with aiohttp.ClientSession(connector =  aiohttp.TCPConnector(limit=4), headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "https://yurineko.net/",
        "Connection": "keep-alive"
    }) as session:
        for image in images:
            filename = "./data/{0}/{1}/{2}".format(chapter.manga_id, chapter.id, image.split("/")[-1])
            task = asyncio.ensure_future(download_image(session, image, filename))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print("Downloaded chapter: {}".format(chapter.id))

async def load_chapters(manga_id: str):
    print("Start manga_id = {}".format(manga_id))
    with open("./data/{}/chapters.json".format(manga_id), "r", encoding="utf-8") as f:
        chapters_json = json.load(f)
    try:
        chapters_data = chapters_json["props"]["pageProps"]["chapterData"]["listChapter"]
    except:
        print("Failed manga_id = {}".format(manga_id))
        return
    for chapter in chapters_data:
        chapter_data = Chapter(chapter)
        await download_images(chapter_data)
    print("Finished manga_id = {}".format(manga_id))

async def load_thumb(manga_id: str):
    if(not os.path.exists("./data/{}/thumbnail.jpeg")):
        with open("./data/{}/{}.json".format(manga_id, manga_id), encoding="utf-8") as f:
            data = json.load(f)
        async with aiohttp.ClientSession(connector =  aiohttp.TCPConnector(limit=4), headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "https://yurineko.net/",
        "Connection": "keep-alive"
        }) as session:
            await download_image(session, data["thumbnail"], "./data/{}/thumbnail.jpeg".format(manga_id))

def main():
    with open("update_list", "r") as f:
        mangas = f.readlines()
    loop = asyncio.get_event_loop()
    tasks = []
    for manga in mangas:
        task = loop.create_task(load_manga(manga.strip("\n"), True))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    tasks = []
    for manga in mangas:
        task = loop.create_task(load_chapters(manga.strip("\n")))
        tasks.append(task)
    # loop.run_until_complete(asyncio.ensure_future(tasks))
    loop.run_until_complete(asyncio.wait(tasks))
    # tasks = []
    # for manga in mangas:
    #     task = loop.create_task(load_thumb(manga.strip("\n")))
    #     loop.run_until_complete(asyncio.ensure_future(task))

if __name__ == '__main__':
    main()
	