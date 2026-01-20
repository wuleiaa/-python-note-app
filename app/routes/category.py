from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from app.utils.auth import login_required

category_bp = Blueprint('category', __name__, url_prefix='/api/category')


# ✅ 1. 添加自定义分类
@category_bp.route('/add', methods=['POST'])
@login_required
def add_category(current_user):
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'code': 400, 'msg': '分类名不能为空'}), 400

    # 检查是否重复
    exists = Category.query.filter_by(user_id=current_user.id, name=name).first()
    if exists:
        return jsonify({'code': 400, 'msg': '分类已存在'}), 400

    new_cat = Category(name=name, user_id=current_user.id)
    db.session.add(new_cat)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '添加成功', 'data': new_cat.to_dict()})


# ✅ 2. 获取分类列表
@category_bp.route('/list', methods=['GET'])
@login_required
def get_categories(current_user):
    cats = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'code': 200,
        'msg': '获取成功',
        'data': [c.to_dict() for c in cats]
    })


# ✅ 3. 删除分类
@category_bp.route('/delete', methods=['POST'])
@login_required
def delete_category(current_user):
    data = request.get_json()
    cat_id = data.get('id')

    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({'code': 404, 'msg': '分类不存在'}), 404

    db.session.delete(cat)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})