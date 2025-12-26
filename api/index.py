# Vercel API函数
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import sys

# 导入工具模块
try:
    from untils import generate_script
except ImportError as e:
    print(f"❌ 导入 untils 模块失败: {e}")
    sys.exit(1)

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 主页路由
@app.route('/')
def index():
    """主页面"""
    return send_from_directory('..', 'main.html')

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({'status': 'ok', 'message': '服务器运行正常'})

# 生成脚本端点
@app.route('/api/generate', methods=['POST'])
def generate():
    """生成视频脚本的 API 端点"""
    try:
        # 检查请求数据
        if not request.is_json:
            return jsonify({'error': '请求必须是JSON格式'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        # 验证输入
        subject = data.get('subject', '').strip()
        api_key = data.get('api_key', '').strip()
        video_length = data.get('video_length', 1)
        creativity = data.get('creativity', 0.7)
        
        if not subject:
            return jsonify({'error': '请输入视频主题'}), 400
        
        if not (0 <= creativity <= 1):
            return jsonify({'error': '创造力参数必须在 0 到 1 之间'}), 400
        
        if not (0 < video_length <= 60):
            return jsonify({'error': '视频时长必须在 1 到 60 分钟之间'}), 400
        
        # 使用用户提供的API密钥或环境变量中的API密钥
        effective_api_key = api_key or os.getenv('ARK_API_KEY')
        if not effective_api_key:
            return jsonify({'error': '请提供API密钥：可以通过前端输入或设置环境变量 ARK_API_KEY'}), 500
        
        # 调用生成函数
        search_result, title, script = generate_script(
            subject=subject,
            video_length=video_length,
            creativity=creativity,
            api_key=effective_api_key
        )
        
        return jsonify({
            'title': title or '暂无标题',
            'script': script or '暂无脚本',
            'search_result': search_result or '暂无参考信息'
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

# Vercel入口点
def handler(request):
    """Vercel请求处理器"""
    return app(request.environ, lambda status, headers: None)

# 如果直接运行此文件，启动本地开发服务器
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)