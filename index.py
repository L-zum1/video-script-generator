# Vercel入口文件
from app import app

# Vercel需要这个handler函数来处理请求
handler = app

if __name__ == "__main__":
    app.run()