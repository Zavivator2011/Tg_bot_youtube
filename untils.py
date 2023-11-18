from pytube import YouTube


async def download_video_by_url(url: str, user_id):
    try:
        yt = YouTube(url=url)
        
        filesize = yt.streams.get_highest_resolution().filesize
        
        if round(filesize / 1024 / 1024) <= 50:
            filename = f"user_{user_id}.mp4"
            yt.streams.get_highest_resolution().download(filename=filename)

            return filename
        else:
            return False

    except:
        return 1