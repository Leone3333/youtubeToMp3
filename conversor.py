import os
import base64
import yt_dlp
from flask import Flask, jsonify, send_file, request, safe_join

app = Flask(__name__)

# Rota para baixar o áudio do YouTube como MP3
@app.route('/converter', methods=['POST'])
def download_audio():
    ytb_url = request.json.get('ytb_url')  # URL do YouTube passada no corpo da requisição
    if not ytb_url:
        return jsonify({"erro": "A URL do YouTube é necessária!"}), 400

    # Decodificar cookies do ambiente
    cookies_base64 = os.environ.get('YOUTUBE_COOKIES')
    with open('cookies.txt', 'wb') as f:
        f.write(base64.b64decode(cookies_base64))
    
    # Opções do yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',
        'outtmpl': '/tmp/temp_audio.%(ext)s',  # Salvar temporariamente no servidor
    }

    try:
        # Fazer o download e conversão com yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(ytb_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Garantir que o arquivo MP3 foi criado
        mp3_path = filename.replace('.webm', '.mp3')
        if os.path.exists(mp3_path):
            # Usar safe_join para evitar problemas de path traversal
            safe_mp3_path = safe_join('/tmp', os.path.basename(mp3_path))
            return send_file(safe_mp3_path, as_attachment=True, download_name=f"{info_dict['title']}.mp3", mimetype='audio/mpeg')
        else:
            return jsonify({"erro": "Arquivo MP3 não encontrado!"}), 500

    except Exception as e:
        return jsonify({"erro_downloading_conversor": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
