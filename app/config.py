import os

# 获取当前文件的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    # SQLALCHEMY_DATABASE_URI: 告诉 Flask 数据库在哪里。这里使用 SQLite。
    # sqlite:/// 表示使用 SQLite 驱动，拼接上文件路径。
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

    # 关闭对模型修改的监控，提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY: 非常重要！用于加密 Token 和 Session。
    # 在真实项目中应该是一串复杂的随机字符。
    SECRET_KEY = 'qingxiang-note-secret-key-demo'