# Transcribe Server

## Build & Run
```
export TS_VERSION=1.0.0
docker build -t timmson/transcriber-server:$TS_VERSION .
docker push timmson/transcriber-server:$TS_VERSION
docker run -v "./data:/app/data" -p "5000:5000" --env-file=.env transriber-server:$TS_VERSION
```

## HowTo
1. Place model from [https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo/tree/main]() to ./model
2. docker compose up
3. Call ```curl -F "file=@./data/file.mp3" http://localhost:5000/upload```
4. Copy "job-id" and wait
5. Call ```curl http://localhost:5000/download/<job-id>```