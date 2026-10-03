from fastapi import FastAPI

app = FastAPI(title="CentralResolve")


@app.get("/")
def root():
    return {
        "message": "CentralResolve API is running"
    }