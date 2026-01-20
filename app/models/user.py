from app import db  # 稍后在 __init__.py 中定义 db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'  # 数据库表名

    # 定义字段
    id = db.Column(db.Integer, primary_key=True)  # 主键 ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一
    password_hash = db.Column(db.String(128), nullable=False)  # 加密后的密码
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间

    def to_dict(self):
        """将模型转换为字典，用于API返回"""
        return {
            'id': self.id,
            'username': self.username,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }