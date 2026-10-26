from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Server",
    description="FastAPI REST API Server",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "FastAPI Server Running"}

@app.get("/health")
async def health():
    return {"status": "UP"}