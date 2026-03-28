# -------------------------------
# Полный Dockerfile для проекта
# Включает OpenCV, Playwright, Flask и Telegram Bot
# -------------------------------

# Базовый образ Python
FROM python:3.10-slim

# Рабочая папка
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем системные библиотеки для OpenCV и Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libgl1 \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chromium для Playwright
RUN playwright install chromium

# Открываем порт Flask
EXPOSE 10000

# Запуск приложения (Flask + Telegram бот + Parser + AI)
CMD ["python", "app.py"]
