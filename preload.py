import pickle
import json
import os

from models import Manga

def path_builder(sub):
    return "./data/{}".format(sub)

def preload():
    mangas = [x for x in os.listdir("./data/") if os.path.isdir(path_builder(x))]
    res = []

    for manga in mangas:
        with open(path_builder("{manga_id}/{manga_id}.json".format(manga_id=manga)), "r", encoding="utf-8") as f:
            data = json.load(f)
            res.append(Manga(data))

    with open("manga.dat", "wb") as f:
        pickle.dump(res, f)
    
    print("Loaded {} manga(s)".format(len(res)))
