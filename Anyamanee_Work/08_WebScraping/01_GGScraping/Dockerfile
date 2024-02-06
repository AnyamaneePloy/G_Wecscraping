FROM python:3.10
RUN apt-get update && apt-get install -y \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt ./
RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.mainGG:app", "--host", "0.0.0.0", "--port", "400","--reload"]
