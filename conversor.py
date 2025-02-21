import os
import base64
import yt_dlp
from flask import Flask, jsonify, send_file, request   

# output_directory = r"C:\Users\Desktop\Documents\Rockstar Games\GTA V\User Music"
# musics teste: https://youtu.be/ZyfrHUV6nH0?si=HgcWDv_4Oz0nnyQc 
# https://youtu.be/nd_m17VsRh0?si=af5-8Zi4CawLRL5s

# recebe UMA url de video no youtube e baixa o audio
def download_audio(ytb_url):    

    cookies_base64 = os.environ.get('YOUTUBE_COOKIES')
    cookies_path = '/tmp/cookies.txt'  # Usar diretório temporário


    with open('cookies.txt', 'wb') as f:
        f.write(base64.b64decode(cookies_base64))
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile':cookies_path,
        'outtmpl': '/tmp/temp_audio.%(ext)s',  # Salvar o arquivo temporariamente no servidor
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(ytb_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        mp3_path = filename.replace('.webm', '.mp3')
        return send_file(mp3_path, as_attachment=True, download_name=f"{info_dict['title']}.mp3")
    except Exception as e:
        return jsonify({"erro_downloading_conversor":   str(e)}), 500

