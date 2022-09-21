from sanic import Sanic, response
from tortoise import Tortoise, run_async
import sanic
from sanic_auth import Auth, User
from models import Account
from utils import hashit

app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'    # 
auth = Auth(app)

# NOTE
# For demonstration purpose, we use a mock-up globally-shared session object.
SESSIONS = {}
@app.middleware('request')
async def add_session(request: sanic.Request):
    if 'sess' in request.cookies:
        # case session outdated
        if request.cookies['sess'] not in SESSIONS:
            del request.cookies['sess']
            request.ctx.session = {}
        else:
            request.ctx.session = SESSIONS[request.cookies['sess']]
    else:
        request.ctx.session = {}

def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)

LOGIN_FORM = '''
<h2>Please sign in, you can try:</h2>
<dl>
<dt>Username</dt> <dd>demo</dd>
<dt>Password</dt> <dd>1234</dd>
</dl>
<p>{}</p>
<form action="" method="POST">
  <input class="username" id="name" name="username"
    placeholder="username" type="text" value=""><br>
  <input class="password" id="password" name="password"
    placeholder="password" type="password" value=""><br>
  <input id="submit" name="submit" type="submit" value="Sign In">
</form>
'''


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password = hashit(password)
        user_record = await Account.filter(username=username)
        user_record = None if user_record == [] else user_record[0]
        if not user_record:
            return response.json({'error': 'user not exist'})
        elif user_record.password == password:
            user = User(id=user_record.id, name=username)   # 模块提供了session的数据格式
            auth.login_user(request, user)                  # 把User 序列化 赋值给 request.ctx.session
            resp = response.redirect('/')
            cookie_sess = hashit(username+password)
            SESSIONS[cookie_sess] = request.ctx.session     # 存储session
            resp.cookies['sess'] = cookie_sess
            return resp
        else:
            return response.json({'error': 'password wrong'})

    return response.html(LOGIN_FORM.format(message))


@app.route('/logout')
@auth.login_required    # 拿到request.ctx.session 并且解析
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(content)


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)

@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.name))

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())
    app.run(host='127.0.0.1', port=8000, debug=True)