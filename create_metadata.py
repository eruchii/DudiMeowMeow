import os
import json
import pickle
from fuzzywuzzy import fuzz, process
import preload
from xml.dom import minidom
import string
import random
import re
import zipfile


global data


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_author(authors):
    if(len(authors) == 0):
        return "Unknown"
    return ", ".join([x.name for x in authors])


def get_volume(name, value_if_failed=1):
    volume = re.findall(r"Vol\.? ?(\d+)", name)
    if len(volume) != 0:
        return int(volume[0])
    volume = re.findall(r"v(\d+)", name)
    if len(volume) != 0:
        return int(volume[0])
    volume = re.findall(r"Part\.? ?(\d+)", name)
    if len(volume) != 0:
        return int(volume[0])
    print("Failed to get volume for {}".format(name))
    return value_if_failed


def create_xml_file(path, manga_path, series, volume, authors):
    root = minidom.Document()
    xml = root.createElement('ComicInfo')

    xml.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    xml.setAttribute('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")

    series_node = root.createElement('Series')
    series_node.appendChild(root.createTextNode(series))
    xml.appendChild(series_node)

    if(volume != None):
        volume_node = root.createElement('Volume')
        volume_node.appendChild(root.createTextNode(str(volume)))
        xml.appendChild(volume_node)
    authors_node = root.createElement('Writer')
    authors_node.appendChild(root.createTextNode(create_author(authors)))
    xml.appendChild(authors_node)

    root.appendChild(xml)

    xml_str = root.toprettyxml(indent="\t")
    # save_path_file = "{}/{} - {}_{}.xml".format(path, series, volume, id_generator())
    name = re.sub('[^A-Za-z0-9()! ]+', '', series)
    save_path_file = "{}/{} - {}.xml".format(path, name, volume)
    with open(save_path_file, "w") as f:
        f.write(xml_str)
    with zipfile.ZipFile(manga_path, 'a') as zipf:
        listfiles = zipf.namelist()
        if("ComicInfo.xml" not in listfiles):
            zipf.write(save_path_file, "ComicInfo.xml")
            print("Add metadata for {}".format(manga_path))
        else:
            print("Exists metadata for {}".format(manga_path))
    os.remove(save_path_file)
    return save_path_file


def set_metadata_mangas(path, ext="cbz"):
    print(path)
    mangas = [x for x in os.listdir(path) if x.endswith(ext)]
    for idx, manga in enumerate(mangas):
        print("Processing {} ({}/{})".format(manga, idx + 1, len(mangas)))
        metadata = find_by_name(manga.replace(ext, ""))
        if len(metadata) == 0:
            print("No metadata found for {}".format(manga))
            continue
        manga_object, series, score = metadata[0]
        volume = get_volume(manga, None)
        print("Found {} - {} with score {}".format(series, volume, score))
        print(manga_object)
        manga_path = "{}/{}".format(path, manga)
        file = create_xml_file(path, manga_path, series, volume, manga_object.authors)


def get_manga_list(reload=False):
    if reload:
        preload.preload()
    with open("manga.dat", "rb") as f:
        data = pickle.load(f)
    return data


def find_by_name(name, threshold=80):
    global data
    ans = []
    for manga in data:
        original_score = fuzz.token_set_ratio(name, manga.originalName)
        if original_score > threshold:
            ans.append((manga, manga.originalName, original_score))
        else:
            other_names = [x for x in manga.otherName.split("; ")]
            string, other_score = process.extractOne(
                name, other_names, scorer=fuzz.token_set_ratio)
            if other_score > threshold:
                ans.append((manga, string, other_score))
    return ans


def find_by_author_name(author_name, threshold=10):
    global data
    ans = []
    for manga in data:
        for author in manga.authors:
            ratio = fuzz.partial_ratio(
                author_name.lower(), author.name.lower())
            if ratio > threshold:
                ans.append((manga, author, ratio))
    return ans


data = get_manga_list(reload=False)
# test = find_by_name("Chainsaw Man")
# print(test)
os.chdir("E:/Ebook/")
paths = [x for x in os.listdir() if "[Manga]" in x]
for path in paths:
    set_metadata_mangas(path, "cbz")
