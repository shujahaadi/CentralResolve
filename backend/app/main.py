from fastapi import FastAPI

from app.api.analysis import router as analysis_router


app = FastAPI(title="CentralResolve")

app.include_router(analysis_router)


@app.get("/")
def root():
    return {
        "message": "CentralResolve API is running"
    }