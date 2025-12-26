# Vercel入口文件
from app import app

# Vercel需要这个handler函数来处理请求
# 在无服务器环境中，我们需要确保正确处理请求
handler = app

# 导出为Vercel兼容的函数
def lambda_handler(event, context):
    """AWS Lambda兼容的处理器，Vercel也使用这种格式"""
    return handler(event, context)

if __name__ == "__main__":
    # 本地开发时使用
    app.run(debug=True, host='0.0.0.0', port=5000)