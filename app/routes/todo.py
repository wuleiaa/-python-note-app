from flask import Blueprint, request, jsonify
from app import db
from app.models.todo import Todo
from app.utils.auth import login_required

todo_bp = Blueprint('todo', __name__, url_prefix='/api/todo')


# ✅ 1. 新建待办
@todo_bp.route('/add', methods=['POST'])
@login_required
def add_todo(current_user):
    data = request.get_json()
    content = data.get('content')
    priority = data.get('priority', 2)  # 默认中(2)
    deadline = data.get('deadline')  # 截止日期字符串

    if not content:
        return jsonify({'code': 400, 'msg': '内容不能为空'}), 400

    new_todo = Todo(
        content=content,
        priority=priority,
        deadline=deadline,
        user_id=current_user.id
    )

    try:
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '添加成功', 'data': new_todo.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': str(e)}), 500


# ✅ 2. 获取待办列表
@todo_bp.route('/list', methods=['GET'])
@login_required
def get_todos(current_user):
    # 按照 "未完成在前(is_done=False)" 和 "优先级从高到低" 排序
    todos = Todo.query.filter_by(user_id=current_user.id) \
        .order_by(Todo.is_done.asc(), Todo.priority.desc(), Todo.create_time.desc()) \
        .all()

    return jsonify({
        'code': 200,
        'msg': '获取成功',
        'data': [t.to_dict() for t in todos]
    })


# ✅ 3. 修改状态/内容（最常用：打钩标记完成）
@todo_bp.route('/edit', methods=['POST'])
@login_required
def edit_todo(current_user):
    data = request.get_json()
    todo_id = data.get('id')

    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'code': 404, 'msg': '待办不存在'}), 404

    # 如果前端传了 is_done，就更新状态
    if 'is_done' in data:
        todo.is_done = data.get('is_done')

    # 如果前端传了 content，就更新内容
    if 'content' in data:
        todo.content = data.get('content')

    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': todo.to_dict()})


# ✅ 4. 删除待办
@todo_bp.route('/delete', methods=['POST'])
@login_required
def delete_todo(current_user):
    data = request.get_json()
    todo_id = data.get('id')

    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'code': 404, 'msg': '待办不存在'}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})