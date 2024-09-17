# Usar uma imagem base com Python 3.11
FROM python:3.11-slim

# Instalar Xvfb, tkinter e outras bibliotecas necessárias
RUN apt-get update && apt-get install -y python3-tk libglib2.0-0 libgl1-mesa-glx libxrender1 libxext6 libsm6 xvfb x11-xserver-utils

# Configura o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências e o projeto
COPY . /app

# Instala as dependências do projeto
RUN pip install pygame pillow pyautogui

# Comando para rodar a aplicação usando xvfb-run
CMD ["xvfb-run", "-a", "python", "main.py"]
