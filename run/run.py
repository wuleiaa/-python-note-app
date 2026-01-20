from app import create_app

app = create_app()

if __name__ == '__main__':
    # 启动开发服务器
    print("🚀 后端服务启动中: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)