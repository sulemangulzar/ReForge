from fastapi import FastAPI

app = FastAPI(
    title="ReForge",
    description="A Health Tracking App.",
    version="0.1.0"
)

@app.get("/")
def health():
    return {"message" : "Running"}
