import pika
import pickle
import numpy as np
import json

# Чтение модели
with open('src/myfile.pkl', 'rb') as file:
    regressor = pickle.load(file)

try:
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Объявление очередей
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')


    # Функция обратного вызова для обработки сообщений
    def callback(ch, method, properties, body):
        print(f"Получено сообщение: {body}")
        message = json.loads(body)
        features = np.array(message["body"]).reshape(1, -1)
        prediction = regressor.predict(features)[0]

        response = {
            "id": message["id"],
            "body": prediction
        }

        channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps(response))
        print(f"Предсказанное значение (ID: {response['id']}) отправлено в очередь y_pred.")


    # Потребление сообщений из очереди features
    channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)

    # Ожидание новых сообщений
    print("Ожидание сообщений...")
    channel.start_consuming()

except Exception as e:
    print(f"Произошла ошибка при обработке сообщений: {e}")