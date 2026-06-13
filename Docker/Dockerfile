FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3-tk libglib2.0-0 libgl1-mesa-glx libxrender1 libxext6 libsm6 xvfb x11-xserver-utils

WORKDIR /app

COPY . /app

RUN pip install pygame pillow

CMD ["xvfb-run", "-a", "python", "main.py"]
