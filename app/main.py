from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent
MP3_DIR = BASE_DIR.parent / "mp3"
HLS_DIR = BASE_DIR / "hls"

HLS_DIR.mkdir(parents=True, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    playlist = BASE_DIR / "playlist.txt"

    with open(playlist, "w", encoding="utf-8") as f:
        for i in range(1, 5):
            path = (MP3_DIR / f"audio{i}.mp3").resolve()
            f.write(f"file '{path}'\n")

    command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-f", "concat",
        "-safe", "0",
        "-i", str(playlist),

        "-vn",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",

        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "5",
        "-hls_flags", "delete_segments+omit_endlist",
        "-hls_segment_filename", str(HLS_DIR / "segment_%06d.ts"),
        str(HLS_DIR / "live.m3u8"),
    ]
    process = subprocess.Popen(command)
    app.state.ffmpeg = process

    print("FFmpeg 스트리밍 시작")

    yield
    # 서버 종료 시 실행
    print("FFmpeg 스트리밍 종료")

    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

app = FastAPI(
    title="My FastAPI Server",
    description="FastAPI REST API Server",
    version="1.0.0",
    lifespan=lifespan  # 추가
)

print("HLS_DIR:", HLS_DIR)
print("live.m3u8 exists:", (HLS_DIR / "live.m3u8").is_file())

app.mount("/hls", StaticFiles(directory=HLS_DIR), name="hls")


@app.get("/")
async def root():
    return {"message": "FastAPI Server Running"}

@app.get("/health")
async def health():
    return {"status": "UP"}
