import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps
from app.models.user import User


def generate_token(user_id):
    """生成 JWT Token"""
    try:
        payload = {
            'user_id': user_id,
            # Token 有效期设置，这里设为 7 天
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        # 使用配置中的 SECRET_KEY 进行加密
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        return str(e)


def login_required(f):
    """装饰器：用户必须登录才能访问接口"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # 前端需要在 Header 中传递 'Authorization': 'Bearer <token>'
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'code': 401, 'msg': '未提供 Token，请登录'}), 401

        try:
            # 解码 Token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            # 查询当前用户
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise Exception('用户不存在')
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 401, 'msg': 'Token 已过期，请重新登录'}), 401
        except Exception as e:
            return jsonify({'code': 401, 'msg': 'Token 无效'}), 401

        # 将当前用户对象传递给路由函数
        return f(current_user, *args, **kwargs)

    return decorated