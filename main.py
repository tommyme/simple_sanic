import sanic
from sanic import Sanic
from sanic.response import text, json
from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import Parameter, RequestBody, Response
from pydantic import BaseModel, Field

class Test(BaseModel):
    foo: str = Field(description="Foo Description", example="FOOO")
    bar: str = "test"

app = Sanic("hello")

@app.route("/")
@openapi.definition(
    summary="ROOT route",
    description="路由的简介",
    tag="ybw",
    parameter=[
        Parameter("a", str, "query", description="一个简单的query参数", required=True),
        Parameter("head", str, "header", description="一个简单的header参数", required=True)
    ],
    response=Response({"application/json" : Test.schema()}, 200, description="一个简单的response")
)
# @openapi.summary("ROOT route")
# @openapi.description('openapi.description is shown here')
# @openapi.tag("ybw") # tagged route will grouped together
# # @openapi.operation('changedName')    # 暂时没什么用 命名冲突的时候可以看看
# @openapi.parameter("a", str, location="query", required=True)  # location query 表示是get参数，数据类型不能用dict
# @openapi.parameter("head", str, location="header", required=True)
# @openapi.response(200, {"application/json" : Test.schema()}, description='hello resp')
async def test(request: sanic.Request):
    data = {'headers': dict(request.headers), 'query': dict(request.args)}
    return json(data)


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