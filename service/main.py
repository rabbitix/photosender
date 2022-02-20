import uvicorn
from fastapi import Request, FastAPI, File, UploadFile
from fastapi import Form
from telegram import Bot
from pydantic import BaseModel
from telegram.utils.request import Request

app = FastAPI()


@app.post('/send')
async def send_photo(token: str = Form(...), channel_id: str = Form(...), file: UploadFile = None):
    bot = Bot(token=token,
              # request=Request(proxy_url="socks5h://127.0.0.1:9050", connect_timeout=500)
              )
    content = await file.read()
    pm = bot.send_photo(chat_id=channel_id, photo=content)
    bot.send_document(chat_id=channel_id, document=content, filename=file.filename, reply_to_message_id=pm.message_id)

    return {"status": "done"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
