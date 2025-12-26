# Vercel 部署指南

## 快速部署步骤

### 1. 准备工作
- 项目代码已推送到GitHub（已完成）
- Vercel配置文件已准备好（`vercel.json`和`api/index.py`）

### 2. 在Vercel上创建项目
1. 访问 [vercel.com](https://vercel.com) 并使用GitHub账号登录
2. 点击"New Project"
3. 选择您的`video-script-generator`仓库
4. 点击"Import"

### 3. 配置项目设置
- **Framework Preset**: 选择"Other"
- **Root Directory**: 保持默认
- **Build Command**: 留空
- **Output Directory**: 留空
- **Install Command**: `pip install -r requirements.txt`

### 4. 设置环境变量（可选）
如果您想设置默认API密钥，添加：
- Name: `ARK_API_KEY`
- Value: 您的API密钥

### 5. 部署
点击"Deploy"按钮，等待2-3分钟即可完成部署。

## 项目结构说明

项目已按照Vercel推荐的结构组织：

```
video-script-generator/
├── api/
│   └── index.py          # Vercel API函数
├── main.html             # 前端页面
├── untils.py             # 工具函数
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
└── app.py               # 原始Flask应用（保留用于本地开发）
```

## 常见问题解决

### 1. 构建失败：依赖安装问题
确保`requirements.txt`包含所有必要的依赖：
```
Flask
flask-cors
langchain
langchain-core
langchain-community
langchain-openai
openai
wikipedia
beautifulsoup4
pydantic
requests
```

### 2. 函数超时错误
在`vercel.json`中已设置超时时间为60秒，这应该足够处理大多数请求。

### 3. 静态文件404错误
确保`main.html`文件在项目根目录，API函数会正确处理静态文件路由。

## 部署后

部署成功后，您将获得一个`.vercel.app`域名，可以通过这个URL访问您的视频脚本生成器应用。每次您推送代码到GitHub时，Vercel会自动重新部署最新版本。

## 环境变量

在Vercel控制台中，您可以设置以下环境变量：
- `ARK_API_KEY`: 默认的API密钥（可选）

用户也可以在前端界面中输入自己的API密钥，这会覆盖默认设置。