from fastapi import FastAPI

app = FastAPI(title="DevDocs AI",
              description="Code documentation generator", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "healthy",
            "service": "DevDocs AI",
            "version": "0.1.0"}


@app.get("/")
def read_root():
    return {"message": "Welcome to DevDocs AI",
            "docs": "/docs"}
