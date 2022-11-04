import os
import json
import shutil
import re

def format_number(number, digit = 4):
    s = str(number)
    l = len(s)
    for i in range(0, digit - l):
        s = "0"+s
    return s
def format_name(manga, chapter, page, ext):
    return "{} - c{} - p{}.{}".format(manga, format_number(chapter), format_number(page), ext)

def gen_path(chapter, image):
    return os.path.join(chapter, image)

def create_ebook(name, chapters, add_thumb = True, thumb = "thumbnail.jpeg", skip=0):
    if(not os.path.exists("output")):
        os.mkdir("output")
    else:
        print("Cleaning output folder")
        shutil.rmtree("output")
        os.mkdir("output")
    if(add_thumb):
        print("Adding Cover")
        ext = thumb.split(".")[-1]
        shutil.copy2(thumb, gen_path("output", format_name(name, 0, 0, ext)))
    page_count = 1
    for idx, chapter in enumerate(chapters):
        if(not os.path.exists(str(chapter["id"]))):
            pass
        images = os.listdir(str(chapter["id"]))
        images.sort(key = lambda x: len(x))
        if(skip != None):
            images = images[:len(images)-skip]
        print(chapter)
        for image in images:
            ext = image.split(".")[-1]
            shutil.copy2(gen_path(str(chapter["id"]), image), gen_path("output", format_name(name, idx+1, page_count, ext)))
            page_count += 1
    print("Creating zip file")
    shutil.make_archive(name, 'zip', "output")
    print("Changing ext")
    os.rename(name+".zip", name+".cbz")
    print("Cleaning")
    shutil.rmtree("output")
    shutil.move(name+".cbz", "E:\Ebook")
    print("Done")

def create_segment_ebook(id, part = None, start = None, end = None, thumb_as_cover = True, skip = None):
    manga_id = str(id)
    try:
        os.chdir("data/{}".format(manga_id))
    except:
        pass
    data = json.load(open("{}.json".format(manga_id),"r", encoding="utf-8"))
    name = data["otherName"]
    name = re.sub('[^A-Za-z0-9()! ]+', '', name)
    if(part != None):
        name = "{} Part {}".format(name, format_number(part,2))
    id = data["id"]
    
    chapters = data["chapters"][::-1]
    if(start != None and end != None):
        chapters = chapters[start:end]
    
    create_ebook(name, chapters, add_thumb=thumb_as_cover, skip=skip)
    

def create_multipart_ebook(id, size, start_part = 1):
    manga_id = str(id)
    data = json.load(open("data/{id}/{id}.json".format(id = manga_id),"r", encoding="utf-8"))
    chapters = data["chapters"]
    part = start_part
    for i in range(size*(start_part-1), len(chapters), size):
        create_segment_ebook(id, part, i, i + size, True)
        part = part + 1

def create_vol(id, vol, start_id = None, end_id = None, add_thumb = True, cover = "thumbnail.jpeg", skip = 0, skip_bonus = False):
    manga_id = str(id)
    try:
        os.chdir("data/{}".format(manga_id))
    except:
        pass
    data = json.load(open("{}.json".format(manga_id),"r", encoding="utf-8"))
    name = data["originalName"]
    # name = data["otherName"]
    # name = re.sub('[^A-Za-z0-9()! ]+', '', name)
    name = "{} Vol. {}".format(name, format_number(vol, 2))
    id = data["id"]
    
    chapters = data["chapters"][::-1]
    if(start_id and end_id):
        start = [idx for idx, chapter in enumerate(chapters) if chapter["id"] == start_id][0]
        end = [idx for idx, chapter in enumerate(chapters) if chapter["id"] == end_id][0]
        chapters = chapters[start:end+1]
    if skip_bonus:
        chapters = [c for c in chapters if "." not in c["name"]]
    # ski
    create_ebook(name, chapters, add_thumb, cover, skip)

# create_vol(200, 12, 15194, 15197, True, "12.jpg")
# create_vol(648, 1, add_thumb=True, cover="1.jpg")
create_multipart_ebook(1902, 10, 6)