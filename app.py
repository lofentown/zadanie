from flask import Flask, jsonify, request

app = Flask(__name__)

state = {"слово": ""}
@app.route('/say', methods=['POST'])
def say():
    try:
        word = request.json.get('слово')
        if not word:
            return jsonify({"ошмбка": "пустое сообщение"}), 400

        state["word"] = word
        return jsonify({"сообщение": "Обновление успешно"}), 200
    except Exception as e:
        # ошибки
        return jsonify({"ошибка": f"Бесконечный цикл: {str(e)}"}), 500

@app.route('/listen', methods=['GET'])
def listen():
    return jsonify(state), 200

if __name__ == '__main__':
    app.run(debug=True)
