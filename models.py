
from enum import Enum


class Tag:
    def __init__(self, tag):
        self.id = tag["id"]
        self.name = tag["name"]

class Manga:
    def __init__(self, manga: dict):
        self.id = manga.get("id")
        self.originalName = manga.get("originalName")
        self.otherName = manga.get("otherName")
        self.description = manga.get("description")
        self.thumbnail = manga.get("thumbnail")
        self.lastUpdate = manga.get("lastUpdate")
        self.authors = [Author(x) for x in manga.get("author")]
        if(manga.get("tag") is not None):
            self.tag = [Tag(x) for x in manga.get("tag")]
        else:
            self.tag = []
        if(manga.get("chapters") is not None):
            self.chapters = [ChapterInfo(x) for x in manga.get("chapters")]
        else:
            self.chapters = []
    def __repr__(self) -> str:
        return str("Manga<id={},originalName={},otherName={},authors={}>".format(self.id, self.originalName, self.otherName, self.authors))
    

class ChapterInfo:
    def __init__(self, chapter: dict):
        self.id = chapter.get("id")
        self.name = chapter.get("name")
        self.date = chapter.get("date")

class Chapter:
    def __init__(self, yuri):
        self.id = yuri.get("id")
        self.name = yuri.get("name")
        self.date = yuri.get("date")
        self.manga_id = yuri.get("mangaID")
        self.max_id = yuri.get("maxID")
        self.urls = []
        if(self.max_id is not None):
            for x in range(1, self.max_id+1):
                self.urls.append("https://storage.yurineko.net/manga/{0}/chapters/{1}/{2}.jpeg".format(self.manga_id, self.id, x))
    def __repr__(self) -> str:
        return str(self.urls)

class AuthorType(Enum):
    Writers = 'Writers', 
    Pencillers = 'Pencillers', 
    Inkers = 'Inkers', 
    Colorists = 'Colorists'


class Author:
    def __init__(self, author: dict):
        self.id = author.get("id")
        self.name = author.get("name")
        self.type = self.get_author_type(author.get("id"))
    
    def get_author_type(self, id: int):
        return AuthorType.Writers

    def __repr__(self) -> str:
        return str("Author<id={},name={},type={}>".format(self.id, self.name, self.type))