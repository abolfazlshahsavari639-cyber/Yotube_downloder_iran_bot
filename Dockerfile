FROM python:3.11
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y nodejs ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U yt-dlp
EXPOSE 10000
CMD ["python", "bot.py"]
