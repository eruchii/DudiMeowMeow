import json

import pickle
import json
import os

from models import Manga

def path_builder(sub):
    return "./data/{}".format(sub)

mangas = [x for x in os.listdir("./data/") if os.path.isdir(path_builder(x))]
res = []

for manga in mangas:
    with open(path_builder("{manga_id}/{manga_id}.json".format(manga_id=manga)), "r", encoding="utf-8") as f:
        data = json.load(f)
        if(data["status"] == 4):
            res.append(data["id"])

with open("update_list", "w") as f:
    for x in res:
        f.write("{}\n".format(x))
