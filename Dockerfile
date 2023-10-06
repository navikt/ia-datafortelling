FROM python:3.11-slim AS runner-image

USER root

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]