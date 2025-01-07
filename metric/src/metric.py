import pika
import json
from pathlib import Path

# Путь к файлу лога
log_path = Path("/usr/src/app/logs/metric_log.csv")

# Инициализация заголовков в CSV-файле
if not log_path.exists():
    with open(log_path, "w") as file:
        file.write("id,y_true,y_pred,absolute_error\n")

# Временное хранилище для сообщений
messages = {}


def save_to_csv(id, y_true, y_pred, absolute_error):
    """Функция для записи в CSV-файл."""
    row = f"{id},{y_true},{y_pred},{absolute_error}\n"
    with open(log_path, "a") as file:
        file.write(row)


def process_message(channel, method, properties, body):
    data = json.loads(body)
    message_id = data["id"]
    value = data["body"]

    if message_id in messages:
        # Если сообщение с таким же ID уже пришло, то считаем ошибку
        other_value = messages.pop(message_id)
        if method.routing_key == "y_true":
            y_true = value
            y_pred = other_value
        else:
            y_true = other_value
            y_pred = value

        absolute_error = abs(y_true - y_pred)
        save_to_csv(message_id, y_true, y_pred, absolute_error)
    else:
        # Сохраняем сообщение во временном хранилище
        messages[message_id] = value


try:
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Объявление очередей
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Функции обратного вызова для обработки сообщений
    channel.basic_consume(queue='y_true', on_message_callback=process_message, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=process_message, auto_ack=True)

    # Ожидание новых сообщений
    print("Ожидание сообщений...")
    channel.start_consuming()

except Exception as e:
    print(f"Произошла ошибка при обработке сообщений: {e}")