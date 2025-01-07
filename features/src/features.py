import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
from datetime import datetime
import time

# Загрузка датасета
X, y = load_diabetes(return_X_y=True)

# Бесконечный цикл для отправки сообщений
while True:
    try:
        # Генерация случайного индекса строки
        random_row = np.random.randint(0, X.shape[0] - 1)

        # Генерация уникального идентификатора
        message_id = int(datetime.timestamp(datetime.now()))

        # Форматируем сообщения
        message_y_true = {
            "id": message_id,
            "body": y[random_row]
        }
        message_features = {
            "id": message_id,
            "body": list(X[random_row])
        }

        # Подключение к RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Объявление очередей
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')

        # Отправка сообщений
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        print(f"Сообщение с правильным ответом (ID: {message_id}) отправлено в очередь.")

        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        print(f"Сообщение с признаками (ID: {message_id}) отправлено в очередь.")

        # Закрытие подключения
        connection.close()

        # Задержка перед следующей итерацией
        time.sleep(10)

    except Exception as e:
        print(f"Произошла ошибка при попытке отправить сообщение: {e}")