from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def test_post():
    return "connecyrdf to api"
