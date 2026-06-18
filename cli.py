import backend

def run_search():
    search_term = input("Search> ")
    videos = backend.searchVideosYoutube(search_term)
    return videos

if __name__ == "__main__":
    while True:
        videos = run_search()
        for v in range(len(videos)):
            print(str(v)+") ", videos[v]['title'], "|", videos[v]['duration'], "|", videos[v]['views'])
        selection = int(input("Download (number)> "))
        backend.downloadVideoYoutube(videos[selection]['id'])

