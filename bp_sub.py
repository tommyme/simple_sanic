from sanic import Sanic, Blueprint
from sanic.response import text,json
import sanic

bp = Blueprint("sub", url_prefix='sub')


@bp.route("/123")
async def bp_root(request):
    return json({"my": "sub"})