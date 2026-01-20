from flask import Blueprint, request, jsonify
from app import db
from app.models.note import Note
from app.utils.auth import login_required  # 导入鉴权工具

note_bp = Blueprint('note', __name__, url_prefix='/api/note')


# ✅ 1. 新建笔记
@note_bp.route('/add', methods=['POST'])
@login_required
def add_note(current_user):  # 装饰器会自动注入 current_user
    data = request.get_json()
    title = data.get('title')
    content = data.get('content', '')  # 默认为空
    category = data.get('category', '默认')

    if not title:
        return jsonify({'code': 400, 'msg': '标题不能为空'}), 400

    # 创建笔记对象，注意 user_id=current_user.id
    new_note = Note(
        title=title,
        content=content,
        category=category,
        user_id=current_user.id
    )

    try:
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '保存成功', 'data': new_note.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': str(e)}), 500


# ✅ 2. 获取笔记列表（只查自己的！）
@note_bp.route('/list', methods=['GET'])
@login_required
def get_notes(current_user):
    # filter_by(user_id=current_user.id) 保证了数据隔离
    # order_by(Note.create_time.desc()) 按时间倒序，最新的在前面
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.create_time.desc()).all()

    # 把列表里的每个对象都转成字典
    note_list = [note.to_dict() for note in notes]
    return jsonify({'code': 200, 'msg': '获取成功', 'data': note_list})


# ✅ 3. 修改笔记
@note_bp.route('/edit', methods=['POST'])
@login_required
def edit_note(current_user):
    data = request.get_json()
    note_id = data.get('id')

    # 严谨！查询时必须带上 user_id，防止有人恶意修改别人的笔记
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()

    if not note:
        return jsonify({'code': 404, 'msg': '笔记不存在或无权修改'}), 404

    # 更新字段
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.category = data.get('category', note.category)

    db.session.commit()
    return jsonify({'code': 200, 'msg': '修改成功'})


# ✅ 4. 删除笔记
@note_bp.route('/delete', methods=['POST'])
@login_required
def delete_note(current_user):
    data = request.get_json()
    note_id = data.get('id')

    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()

    if not note:
        return jsonify({'code': 404, 'msg': '笔记不存在'}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})