# 视频脚本生成器

基于 Flask 和 AI 的视频脚本生成器。

## 功能特点

- 输入视频主题、时长和创造力参数
- 自动生成视频标题和脚本
- 集成维基百科搜索作为参考信息

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
export ARK_API_KEY='your-api-key-here'
```

3. 运行应用：
```bash
python app.py
```

4. 在浏览器中访问显示的地址（通常是 http://localhost:5001）

## 文件说明

- `main.html` - 前端页面
- `app.py` - Flask 后端服务器
- `untils.py` - 核心生成逻辑
- `requirements.txt` - 项目依赖