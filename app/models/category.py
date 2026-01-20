from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False) # 分类名称
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 关联用户
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }