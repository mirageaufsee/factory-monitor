from fastapi import FastAPI

app = FastAPI(title="Factory Monitor API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Factory Monitor is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}