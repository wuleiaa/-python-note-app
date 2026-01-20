from flask import Blueprint, request, jsonify
from sqlalchemy import or_  # 用于模糊查询的 OR 操作
from app.models.note import Note
from app.models.todo import Todo
from app.utils.auth import login_required

tool_bp = Blueprint('tool', __name__, url_prefix='/api/tool')


# ✅ 1. 内容搜索接口（搜标题 或 搜正文）
@tool_bp.route('/search', methods=['POST'])
@login_required
def search(current_user):
    data = request.get_json()
    keyword = data.get('keyword', '')

    if not keyword:
        return jsonify({'code': 400, 'msg': '请输入关键字'}), 400

    # 核心逻辑：查询 belong to current_user AND (title contains keyword OR content contains keyword)
    notes = Note.query.filter(
        Note.user_id == current_user.id,
        or_(
            Note.title.contains(keyword),
            Note.content.contains(keyword)
        )
    ).order_by(Note.create_time.desc()).all()

    return jsonify({
        'code': 200,
        'msg': '搜索成功',
        'data': [note.to_dict() for note in notes]
    })


# ✅ 2. 数据统计接口（首页仪表盘）
@tool_bp.route('/stats', methods=['GET'])
@login_required
def get_stats(current_user):
    # 统计笔记总数
    note_count = Note.query.filter_by(user_id=current_user.id).count()

    # 统计待办总数
    todo_total = Todo.query.filter_by(user_id=current_user.id).count()

    # 统计已完成待办数
    todo_done = Todo.query.filter_by(user_id=current_user.id, is_done=True).count()

    return jsonify({
        'code': 200,
        'msg': '获取成功',
        'data': {
            'note_count': note_count,
            'todo_total': todo_total,
            'todo_done': todo_done
        }
    })