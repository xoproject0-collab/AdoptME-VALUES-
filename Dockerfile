# Используем стабильный Python
FROM python:3.10-slim

# Рабочая папка
WORKDIR /app

# Копируем файлы
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 10000

# Запуск приложения (ТОЛЬКО сайт, без бота)
CMD ["python", "app.py"]
