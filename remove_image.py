from operator import ge
import os
import hashlib

def chunk_reader(fobj, chunk_size=1024):
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed

os.chdir("./data/200")

target_img = "16.jpeg"

file_size = os.path.getsize(target_img)
file_hash = get_hash(target_img)
imgs = []
print(file_hash)
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        imgs.append(os.path.join(root, name))

for i in imgs:
    size = os.path.getsize(i)
    if(size == file_size):
        f_hash = get_hash(i)
        if(f_hash == file_hash):
            os.remove(i)



