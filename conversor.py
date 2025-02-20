import os
import yt_dlp

# output_directory = r"C:\Users\Desktop\Documents\Rockstar Games\GTA V\User Music"
# musics teste: https://youtu.be/ZyfrHUV6nH0?si=HgcWDv_4Oz0nnyQc 
# https://youtu.be/nd_m17VsRh0?si=af5-8Zi4CawLRL5s
from flask import jsonify

# recebe UMA url de video no youtube e baixa o audio
def download_audio(ytb_url):    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytb_url])
        print(f"Downlading {ytb_url} bem sucedido!")
    except Exception as e:
        return jsonify({"erro_downloading_conversor": e})

# def conversor():
#     for ytb_url in ytb_url_list:
#         try:
#             download_audio(ytb_url)
#         except Exception as e:
#             print(f"Error downloading: {ytb_url}")
#             print(e)
#     print("Done")

# conversor()
