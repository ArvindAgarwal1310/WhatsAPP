import json
from fastapi import FastAPI,Request
from views import verify,handle_message
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="Data Dine")

@app.get("/webhook")
async def webhook_get(request: Request):
    raw_body = await request.body()
    raw_body = json.loads(raw_body)
    print(raw_body)
    return verify(raw_body)

@app.post("/webhook")
async def webhook_post(request: Request):
    raw_body = await request.body()
    raw_body=json.loads(raw_body)
    print(raw_body)
    return handle_message(body=raw_body)

# creating origin list
origins = ['*']

# config CORSM
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
