# Создание микросервисов с использованием очереди сообщений
## Перечень сервисов, используемых в решение, и решаемых ими задач:
### Брокер сообщений
* Передача сообщений между другими сервисами
* Формирование очереди сообщений

### Генерация данных для обработки (Features)
* Получение данных dataset о диабете
* Выбор произвольной строки dataset
* Создание очереди фактических значений y_true
* Сериализация значения y полученной ранее строки и публикация в очередь y_true
* Создание очереди признаков features
* Сериализация признаков полученной ранее строки и публикация в очередь features

### Предсказание значений
* Загрузка серилизованной модели из файла
* Объявление очереди признаков features
* Создание очереди предсказанных значений y_pred
* Считывание из очереди features значений признаков
* Предсказание y_pred моделью на основе значений признаков
* Публикация значений y_pred в очередь y_pred

### Расчет метрик
* Объявление очередей y_pred, y_true
* Считывание из очередей y_pred, y_true значений y_pred, y_true
* Расчет абсолютного отклонения
* Сохранение значения метрики в файл c метриками

### Построение гистограммы на основе файла с метриками
* Получение файла с метриками
* Сохранение изображения с гистограммой

Каждый сервис запускается в отдельном контейнере, параметры сборки контейнеров описаны в докерфайлах.
Оркестрация сервисами выполняется при помощи docker-compose.


