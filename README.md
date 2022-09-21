初始账户: 
ybw:test



请求发过来之后，中间件进行add_session：

1. 请求cookie的sess作为key 去 SESSIONS字典里面找value，如果找不到就删除请求cookie的sess
2. 如果有就拿value出来，复制给req.ctx.session



登录的话，

```python
user = User(id=user_record.id, name=username)   # 模块提供了session的数据格式
auth.login_user(request, user)                  # 把User 序列化 赋值给 request.ctx.session

cookie_sess = hashit(username+password)					# username+passwd+salt 一起哈希
resp = response.redirect('/')

SESSIONS[cookie_sess] = request.ctx.session     # 存储session
resp.cookies['sess'] = cookie_sess
return resp
```

后续我们登陆的时候

```python
@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(content)
```

login_required会把session中 序列化的 数据结构 User 解析成为 user，作为参数传入函数



所以sanic-auth就是

- 提供数据结构User，可以序列化 存入session，反序列化 从session中加载
- login_required，提供反序列化的User
- login_user，序列化，赋值到request.ctx.session