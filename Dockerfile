FROM python:3.10

# Создаем директорию в которой будут храниться файлы, пакеты и модули
RUN mkdir /fastapi_test

# Объявляем ее рабочей
WORKDIR /fastapi_test

# Копируем в рабочую директорию файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем все файлы в рабочую директорию
COPY . .
