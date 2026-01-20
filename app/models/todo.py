from app import db
from datetime import datetime


class Todo(db.Model):
    __tablename__ = 'todo'

    # 1. 基础字段
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # 待办内容

    # 2. 特殊字段（待办特有的）
    # is_done: True=已完成, False=未完成 (默认False)
    is_done = db.Column(db.Boolean, default=False)
    # priority: 优先级 (1=低, 2=中, 3=高)，用数字方便排序
    priority = db.Column(db.Integer, default=2)
    # deadline: 截止时间，为了简单，我们直接存字符串 (例如 "2023-12-31")
    deadline = db.Column(db.String(20), nullable=True)

    # 3. 关联字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 4. 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'is_done': self.is_done,
            'priority': self.priority,
            'deadline': self.deadline,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }