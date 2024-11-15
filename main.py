from sanic import Sanic
from sanic.response import text
import sanic
from sanic_cors import CORS

app = Sanic("hello")
CORS(app)

@app.get("/get")    # query
async def some_get(request: sanic.Request):
    return text('get')

@app.delete('/del') # query
async def some_del(request: sanic.Request):
    return text('del')

@app.post('/post')  # body json query
async def some_post(request: sanic.Request):
    return text('post')

@app.put('/put')    # body json query
async def some_put(request: sanic.Request):
    return text('put')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)