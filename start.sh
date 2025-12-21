#!/bin/bash

# 视频脚本生成器 - 启动脚本

echo "🚀 视频脚本生成器启动脚本"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 未找到 app.py 文件"
    echo "请确保在项目根目录运行此脚本"
    exit 1
fi

# 检查环境变量
if [ -z "$ARK_API_KEY" ]; then
    echo "⚠️  警告: 未设置 ARK_API_KEY 环境变量"
    echo "   如果还没有设置，请运行:"
    echo "   export ARK_API_KEY='your-api-key-here'"
    echo ""
    read -p "是否继续启动服务器？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查依赖
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install Flask flask-cors requests
fi

echo ""
echo "✅ 准备就绪，正在启动服务器..."
echo ""

# 启动服务器
python3 app.py
