from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import sys

# 尝试导入 untils 模块
try:
    from untils import generate_script
    print("✅ 成功导入 untils 模块")
except ImportError as e:
    print(f"❌ 导入 untils 模块失败: {e}")
    print("请确保 untils.py 文件存在且没有语法错误")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# 添加请求日志
@app.before_request
def log_request_info():
    print(f'📥 收到请求: {request.method} {request.path}')

@app.route('/')
def index():
    """主页面"""
    return send_from_directory('.', 'main.html')

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    print('✅ 健康检查请求成功')
    return jsonify({
        'status': 'ok', 
        'message': '服务器运行正常',
        'port': request.environ.get('SERVER_PORT', 'unknown')
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    """生成视频脚本的 API 端点"""
    # 确保始终返回JSON响应
    try:
        # 检查请求数据
        if not request.is_json:
            print('❌ 请求不是JSON格式')
            return jsonify({'error': '请求必须是JSON格式'}), 400, {'Content-Type': 'application/json'}
        
        data = request.get_json()
        if not data:
            print('❌ 请求数据为空')
            return jsonify({'error': '请求数据为空'}), 400, {'Content-Type': 'application/json'}
        
        # 验证输入
        subject = data.get('subject', '').strip()
        video_length = data.get('video_length', 1)
        creativity = data.get('creativity', 0.7)
        
        if not subject:
            return jsonify({'error': '请输入视频主题'}), 400, {'Content-Type': 'application/json'}
        
        if not (0 <= creativity <= 1):
            return jsonify({'error': '创造力参数必须在 0 到 1 之间'}), 400, {'Content-Type': 'application/json'}
        
        if not (0 < video_length <= 60):
            return jsonify({'error': '视频时长必须在 1 到 60 分钟之间'}), 400, {'Content-Type': 'application/json'}
        
        # 检查API密钥
        api_key = os.getenv('ARK_API_KEY')
        if not api_key:
            print('❌ API密钥未设置')
            return jsonify({'error': 'API密钥未设置。请在环境变量中设置 ARK_API_KEY'}), 500, {'Content-Type': 'application/json'}
        
        # 调用生成函数
        print(f'📝 开始生成脚本: 主题={subject}, 时长={video_length}, 创造力={creativity}')
        try:
            search_result, title, script = generate_script(
                subject=subject,
                video_length=video_length,
                creativity=creativity
            )
            print(f'✅ 脚本生成成功')
        except ValueError as ve:
            # API密钥相关的ValueError
            print(f'❌ generate_script ValueError: {ve}')
            error_msg = str(ve)
            return jsonify({'error': f'参数错误: {error_msg}'}), 400, {'Content-Type': 'application/json'}
        except Exception as gen_error:
            print(f'❌ generate_script 执行失败: {gen_error}')
            import traceback
            traceback.print_exc()
            # 根据错误类型返回不同的错误信息
            error_msg = str(gen_error)
            if 'API' in error_msg or 'api' in error_msg or 'key' in error_msg.lower() or '401' in error_msg or '403' in error_msg:
                return jsonify({'error': f'API调用失败: {error_msg}。请检查API密钥是否正确'}), 500, {'Content-Type': 'application/json'}
            elif 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                return jsonify({'error': '请求超时，请稍后重试'}), 500, {'Content-Type': 'application/json'}
            else:
                # 截断过长的错误信息
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + '...'
                return jsonify({'error': f'生成失败: {error_msg}'}), 500, {'Content-Type': 'application/json'}
        
        return jsonify({
            'title': title or '暂无标题',
            'script': script or '暂无脚本',
            'search_result': search_result or '暂无参考信息'
        }), 200, {'Content-Type': 'application/json'}
        
    except ValueError as e:
        print(f'❌ 参数错误: {e}')
        return jsonify({'error': str(e)}), 400, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f'❌ 未知错误: {e}')
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if len(error_msg) > 200:
            error_msg = error_msg[:200] + '...'
        return jsonify({'error': f'服务器错误: {error_msg}'}), 500, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # 检查环境变量
    if not os.getenv('ARK_API_KEY'):
        print("警告: 未设置 ARK_API_KEY 环境变量")
        print("请设置: export ARK_API_KEY='your-api-key'")
    
    # 生产环境使用环境变量中的PORT，开发环境使用5001
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # 尝试使用端口（避免 macOS AirPlay Receiver 占用 5000）
    if port == 5001 and not os.environ.get('PORT'):
        import socket
        
        def find_free_port(start_port=5001):
            """查找可用端口"""
            for port in range(start_port, start_port + 10):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('', port))
                        return port
                except OSError:
                    continue
            return start_port  # 如果都不可用，返回默认端口
        
        port = find_free_port(5001)
    
    print(f"\n{'='*60}")
    print(f"🚀 Flask 服务器正在启动...")
    print(f"📡 监听地址: http://0.0.0.0:{port}")
    print(f"🌐 本地访问: http://localhost:{port}")
    print(f"🌐 网络访问: http://127.0.0.1:{port}")
    print(f"{'='*60}")
    print(f"📝 请在浏览器中访问上述地址之一")
    print(f"💡 如果无法连接，请检查：")
    print(f"   1. 防火墙设置")
    print(f"   2. 浏览器控制台是否有错误（F12）")
    print(f"   3. 确保使用 http://localhost:{port} 而不是直接打开 HTML 文件")
    print(f"{'='*60}\n")
    
    try:
        app.run(debug=debug, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        print(f"请检查端口 {port} 是否被占用")
        sys.exit(1)
