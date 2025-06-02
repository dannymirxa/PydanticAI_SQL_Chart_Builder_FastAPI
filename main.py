from fastapi import FastAPI
from app.controller import router

app = FastAPI(title="Chart Generator")
app.include_router(router)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9090, reload=True)
