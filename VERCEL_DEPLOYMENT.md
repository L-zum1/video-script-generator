# Vercel 部署指南

## 方法一：通过GitHub集成（推荐）

这是最简单、最推荐的部署方式，支持自动部署。

### 步骤1：准备GitHub仓库
确保您的代码已推送到GitHub仓库。如果还没有，请执行：
```bash
git add .
git commit -m "准备部署到Vercel"
git push origin main
```

### 步骤2：注册并登录Vercel
1. 访问 [vercel.com](https://vercel.com)
2. 点击"Sign Up"注册账号
3. 选择使用GitHub账号登录（推荐）

### 步骤3：导入项目
1. 登录后，点击"New Project"
2. 在"Import Git Repository"部分，选择您的video-script-generator仓库
3. 点击"Import"

### 步骤4：配置项目
1. **Framework Preset**: 选择"Other"
2. **Root Directory**: 保持默认（根目录）
3. **Build Command**: 留空（Vercel会自动检测Python项目）
4. **Output Directory**: 留空
5. **Install Command**: `pip install -r requirements.txt`

### 步骤5：设置环境变量（可选）
如果您想设置默认API密钥：
1. 在"Environment Variables"部分添加：
   - Name: `ARK_API_KEY`
   - Value: 您的API密钥
2. 确保选择"Production"、"Preview"和"Development"环境

### 步骤6：部署
1. 点击"Deploy"按钮
2. 等待部署完成（通常需要2-3分钟）
3. 部署成功后，您会获得一个`.vercel.app`域名

### 步骤7：测试应用
访问您的应用URL（如`https://your-project-name.vercel.app`），测试：
- 页面是否正常加载
- API密钥输入功能
- 脚本生成功能

## 方法二：使用Vercel CLI

如果您已安装Node.js和npm，可以使用Vercel CLI：

### 安装Vercel CLI
```bash
npm install -g vercel
```

### 登录和部署
```bash
# 登录Vercel
vercel login

# 在项目目录中部署
vercel

# 按照提示操作：
# 1. 链接到现有项目或创建新项目
# 2. 确认设置
# 3. 部署
```

## 部署后配置

### 自定义域名（可选）
1. 在Vercel控制台中，点击您的项目
2. 转到"Settings" → "Domains"
3. 添加您的自定义域名

### 自动部署
通过GitHub集成，每次您推送代码到main分支时，Vercel会自动重新部署。

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
在`vercel.json`中增加超时时间：
```json
{
  "functions": {
    "index.py": {
      "maxDuration": 60
    }
  }
}
```

### 3. 静态文件404错误
确保`index.py`正确处理静态文件路由：
```python
from app import app
handler = app
```

### 4. 环境变量不生效
1. 检查环境变量名称是否正确
2. 确保在代码中正确使用`os.getenv()`
3. 重新部署项目以应用环境变量

## 性能优化建议

1. **使用缓存**：对于频繁请求的数据，考虑使用缓存
2. **优化依赖**：移除不必要的依赖以减小部署包大小
3. **异步处理**：对于长时间运行的任务，考虑使用Vercel的无服务器函数

## 监控和日志

1. 在Vercel控制台中查看"Functions"标签页监控函数执行
2. 使用"Logs"标签页查看应用日志
3. 设置"Analytics"跟踪网站使用情况

部署完成后，您的Flask应用将在Vercel的无服务器环境中运行，享受全球CDN加速和自动扩展的好处。