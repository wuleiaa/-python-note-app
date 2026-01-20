from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from app.utils.auth import generate_token, login_required

# 创建蓝图，URL 前缀为 /api/user
user_bp = Blueprint('user', __name__, url_prefix='/api/user')


# ✅ 1. 用户注册接口
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 基础校验
    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400
    if len(password) < 6:
        return jsonify({'code': 400, 'msg': '密码长度不能少于6位'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'}), 400

    # 创建新用户（密码存 Hash 值）
    new_user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        # 注册成功后自动登录，返回 Token
        token = generate_token(new_user.id)
        return jsonify({
            'code': 200,
            'msg': '注册成功',
            'data': {'token': token, 'user': new_user.to_dict()}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': f'注册失败: {str(e)}'}), 500


# ✅ 2. 用户登录接口
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 查询用户
    user = User.query.filter_by(username=username).first()

    # 校验密码：将输入的密码 Hash 后与数据库比对
    if user and check_password_hash(user.password_hash, password):
        token = generate_token(user.id)
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {'token': token, 'user': user.to_dict()}
        })

    return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401


# ✅ 3. 修改密码接口 (需要登录)
@user_bp.route('/change_password', methods=['POST'])
@login_required  # 鉴权装饰器
def change_password(current_user):
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # 校验旧密码
    if not check_password_hash(current_user.password_hash, old_password):
        return jsonify({'code': 400, 'msg': '原密码错误'}), 400

    # 校验新密码长度
    if len(new_password) < 6:
        return jsonify({'code': 400, 'msg': '新密码长度不能少于6位'}), 400

    # 更新密码
    current_user.password_hash = generate_password_hash(new_password)
    try:
        db.session.commit()
        return jsonify({'code': 200, 'msg': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '修改失败'}), 500