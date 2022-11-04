# Dudi MeowMeow
Some functions for download and create ebook from [Yurineko](https://yurineko.com/) for offline reading.
You may need to read the source code to understand how to use it.

## USAGE

### Dudi Downloader
- `yuri_downloader.py`: Generate Dudi Data from Yurineko.
- `update_list.py`: Generate the list of manga to update.

### Dudi API
- `app.py`: Simple API for Dudi Data. Return manga info, chapter info and chapter images.\
To start server: `uvicorn app:app --host 0.0.0.0 --port 80`.\
You can write your own UI for Dudi API.

### Create Ebook from Dudi Data
- `create_manga.py`: Create `CBZ` file from Dudi Data. Combine with `Kindle Comic Converter` to create `MOBI` file.\
**Implementation**:
    - `create_vol`: Manual split volume. Tips: Go to [mangadex.org](https://mangadex.org) and check manga info like volume, chapter, cover, etc.
    - `create_multipart_ebook`: Split a manga into multiple parts with a given number of chapters per part. 
- `remove_image.py`: Find and delete all images equal to a given image. Useful for removing credit images.\
**Implementation**:
    - Select an image, then calculate the hash value of first 1024 bytes.
    - Find all images that have the same file size as the selected image.
    - Calculate first 1024 bytes of each image and compare with the hash value of the selected image.
- `create_metadata.py`: Batch create metadata `ComicInfo.xml` for all manga in a given folder. This metadata can be used by `Kindle Comic Converter`.\
**Implementation**:
    - Use `fuzzywuzzy` to find the best match manga from Dudi Data by file name.
    - If manga is not from Dudi Meowmeow, you can manually create it.
    - File name format can either have volume or not.\
    Example:
        - `{series} - Vol. {vol}.cbz` \
            e.g. `Bloom into You - Vol. 1.cbz`
        - `{series} v{vol}.cbz` \
            e.g. `I'm in Love with the Villainess v01.cbz`
        - `{series} Part {vol}.cbz` \
            e.g. `Please Bully Me Miss Villainess! Part 01.cbz`
        - `{series}.cbz` \
            e.g. `JK-chan and Her Male Classmate's Mom.cbz`
    - If metadata already exists, it will be skipped. To update / remove metadata, you need open `CBZ` file with `7zip` or `WinRAR` and delete `ComicInfo.xml` file.