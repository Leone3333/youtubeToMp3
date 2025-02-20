from flask import Flask, request, render_template,jsonify
from conversor import download_audio 

app = Flask(__name__)

# define a rota para a pag
@app.route('/')
def index_homepage():
    return render_template('index.html')

# rota que recebe as urls do front
@app.route('/converter', methods=["POST"])
def converter():
    try:
        urls = request.json
        if not urls or "dados" not in urls:
            return jsonify({"error": "Nenhum dado recebido ou formato inválido"}), 400
        
        for ytb_url in urls["dados"]: 
            try:
                download_audio(ytb_url)
            except Exception as e: 
                    return jsonify({"error": f"Erro ao baixar o áudio: {str(e)}"}), 500
                        
        return jsonify({"message": "Downlading bem sucedido","data": urls})

    except Exception as e:
        return jsonify({"error": f"Erro no servidor: {str(e)}"}),500

if __name__ == '__main__':
    app.run(debug=True)