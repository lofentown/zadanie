from flask import Flask, jsonify, request

app = Flask(__name__)

# Хранилище состояния
state = {"word": ""}


@app.route('/say', methods=['POST'])
def say():
    try:
        # Получаем слово из JSON
        word = request.json.get('word')

        if not word:  # Если 'word' отсутствует или пустое
            return jsonify({"error": "Missing or empty 'word' in request"}), 400

        state["word"] = word  # Обновляем состояние
        return jsonify({"message": "State updated successfully"}), 200
    except Exception as e:
        # Логирование ошибки и возврат подробной информации
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/listen', methods=['GET'])
def listen():
    return jsonify(state), 200


if __name__ == '__main__':
    app.run(debug=True)
