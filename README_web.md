# 视频脚本生成器 Web 应用

这是一个基于 Flask 的视频脚本生成器 Web 应用，使用 uiverse.io 风格的 UI 组件。

## 功能特点

- 🎨 现代化的 UI 设计，使用 uiverse.io 风格的组件
- 📝 输入视频主题、时长和创造力参数
- 🤖 自动生成视频标题和脚本
- 📚 集成维基百科搜索作为参考信息
- ⚡ 实时加载动画和错误提示

## 安装依赖

```bash
pip install -r requirements.txt
```

## 设置环境变量

```bash
export ARK_API_KEY='your-api-key-here'
```

## 运行应用

```bash
python app.py
```

应用会自动查找可用端口（默认从 5001 开始，避免 macOS AirPlay Receiver 占用 5000 端口）。

启动后，终端会显示访问地址，例如：http://localhost:5001

## 使用说明

1. 在"视频主题"输入框中输入你想要生成脚本的主题（例如：Sora模型）
2. 设置视频时长（1-60分钟）
3. 调整创造力参数（0-1之间，值越大越有创意）
4. 点击"生成脚本"按钮
5. 等待生成完成，查看结果

## 文件说明

- `main.html` - 前端页面（包含样式和 JavaScript）
- `app.py` - Flask 后端服务器
- `untils.py` - 核心生成逻辑

## API 端点

### POST /api/generate

生成视频脚本

**请求体：**
```json
{
    "subject": "Sora模型",
    "video_length": 1,
    "creativity": 0.7
}
```

**响应：**
```json
{
    "title": "生成的视频标题",
    "script": "生成的视频脚本内容",
    "search_result": "维基百科搜索结果"
}
```
