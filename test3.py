import pytest
from flask import Flask, request, Response
import time

app = Flask(__name__)
messages = []  # Список для хранения сообщений


@app.route('/say', methods=['POST'])
def say():
    data = request.get_json()
    word = data.get('word', '')
    if word:
        messages.append(word)
        return '', 200
    return '', 400


@app.route('/listen')
def listen():
    def event_stream():
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            if messages:
                yield f"data: {messages[-1]}\n\n"
                break
            time.sleep(0.1)
            attempts += 1
    return Response(event_stream(), mimetype="text/event-stream")


def create_client(role):
    client = app.test_client()
    if role == "speaker":
        response = client.post('/say', json={"word": "test_message"})
        assert response.status_code == 200  # Проверка успешной отправки
        return response
    elif role == "listener":
        response = client.get('/listen')
        assert response.status_code == 200  # Проверка успешного соединения
        return response
    return None


def test_multiple_clients():
    num_listeners = int(input('Введите кол-во слушателей: '))
    print(f"Testing with {num_listeners} listeners...")

    # Создаем говоруна и слушателей
    speaker_response = create_client("speaker")
    assert speaker_response.status_code == 200

    listeners = [create_client("listener") for _ in range(num_listeners)]

    # Проверяем получение сообщений
    for i, listener in enumerate(listeners, start=1):
        assert listener.status_code == 200
        data = listener.data.decode().strip()
        print(f"Listener {i} received: {data}")
        assert data.startswith("data:")  # Проверка, что формат корректен
        assert "test_message" in data  # Проверка, что сообщение передано правильно

    # Проверяем, что сообщение было отправлено
    assert len(messages) == 1
    assert messages[0] == "test_message"
