from app import db
from datetime import datetime


class Note(db.Model):
    __tablename__ = 'note'

    # 1. 基础字段
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=True)  # 正文（Text类型可以存长文本）
    category = db.Column(db.String(20), default="默认")  # 分类（工作/生活等）

    # 2. 关联字段（核心！）
    # user_id 存储的是 user 表的 id，这样我们就知道笔记属于哪个用户
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 3. 时间字段
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 修改时间（每次修改自动更新）

    def to_dict(self):
        """转字典，方便返回给前端"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }