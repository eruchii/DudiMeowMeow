
def paginate(data: list, page: int = 1, page_size: int = 8):
    if(page_size == 0 or page == 0):
        return []
    size = len(data)
    start = (page-1)*page_size 
    end = page*page_size - 1
    return data[start: end]