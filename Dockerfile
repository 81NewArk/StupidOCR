FROM python:3.9

RUN mkdir /app

COPY . /app/

WORKDIR /app

RUN pip install fastapi uvicorn aiofiles fastapi-async-sqlalchemy python-multipart

RUN pip install ddddocr

CMD ["python3", "StupidOCR.py","--host", "0.0.0.0", "--port", "6688"]