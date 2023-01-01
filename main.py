from sanic import Sanic
from sanic.response import text
import sanic
from tortoise.contrib.sanic import register_tortoise
from models import Account
app = Sanic.get_app("hello", force_create=True)

@app.get("/get")    # query
async def some_get(request: sanic.Request):
    querys = await Account.all()
    num = len(querys)
    return text(f'num of account: {num}')

register_tortoise(
    app, db_url="sqlite://db.sqlite3", modules={"models": ["models"]}, generate_schemas=True
)

# ref:  https://tortoise.github.io/examples/sanic.html#main-py

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8000, debug=True)