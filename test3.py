from flask import Flask, request, Response
import time

app = Flask(__name__)
messages = []


@app.route('/say', methods=['POST'])
def say():
    data = request.get_json()
    word = data.get('слово', '')
    if word:
        messages.append(word)
        return '', 200
    return '', 400


@app.route('/listen')
def listen():
    def event_stream():
        sent_count = 0
        while sent_count < len(messages):
            while sent_count < len(messages):
                yield f"слово: {messages[sent_count]}\n\n"
                sent_count += 1
            time.sleep(0.1)
    return Response(event_stream(), mimetype="text/event-stream")


def create_client(role, word=None):
    client = app.test_client()
    if role == "говорун" and word:
        response = client.post('/say', json={"слово": word})  # Исправлен маршрут
        assert response.status_code == 200  # Успешно
        return response
    elif role == "слушатель":
        response = client.get('/listen')
        assert response.status_code == 200  # Успешно
        return response
    return None


def test_multiple_clients():
    num_speakers = int(input('Введите количество говорунов: '))
    num_listeners = int(input('Введите количество слушателей: '))
    print(f"Тест c: {num_speakers} говорунами и {num_listeners} слушателями...")

    # Говоруны с их сообщениями
    for i in range(1, num_speakers + 1):
        word = f"test_message_{i}"
        speaker_response = create_client("говорун", word=word)
        assert speaker_response.status_code == 200
        print(f"Говорун {i} отправил: {word}")

    # Слушатели
    listeners = [create_client("слушатель") for _ in range(num_listeners)]

    # Проверка на получение сообщений
    for i, listener in enumerate(listeners, start=1):
        received_data = listener.data.decode().splitlines()
        received_messages = [
            line.replace("слово: ", "") for line in received_data if line.startswith("слово: ")
        ]
        print(f"Слушатель {i} получил сообщения: {received_messages}")

        # Проверка на получение всех сообщений от говорунов
        for j in range(1, num_speakers + 1):
            assert f"test_message_{j}" in received_messages

    # Проверка на отправку сообщений
    assert len(messages) == num_speakers
    for i in range(1, num_speakers + 1):
        assert f"test_message_{i}" in messages


if __name__ == "__main__":
    test_multiple_clients()
