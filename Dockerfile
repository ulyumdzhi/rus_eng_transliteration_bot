FROM python:slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV TOKEN='your_telegram_token'
COPY . .
RUN pip install -r requirements.txt
CMD python bot.py
