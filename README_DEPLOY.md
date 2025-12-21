# 🚀 快速部署指南

## 最简单的部署方法：Render（5分钟部署）

### 步骤1：准备GitHub仓库

```bash
# 初始化Git仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 推送到GitHub
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 步骤2：在Render部署

1. 访问 [render.com](https://render.com) 并注册/登录
2. 点击 "New +" → "Web Service"
3. 连接您的GitHub仓库
4. 配置如下：
   - **Name**: `video-script-generator`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: 
     - Key: `ARK_API_KEY`
     - Value: 您的API密钥
5. 点击 "Create Web Service"
6. 等待3-5分钟部署完成

✅ 完成！您现在会得到一个公共URL，例如：`https://video-script-generator.onrender.com`

---

## 其他部署选项

查看 `部署指南.md` 了解：
- Railway 部署
- Fly.io 部署  
- PythonAnywhere 部署

---

## 重要提示

⚠️ **环境变量**
- 部署时必须设置 `ARK_API_KEY` 环境变量
- 不要将API密钥提交到Git仓库

✅ **检查部署**
- 部署后访问：`https://你的域名/api/health`
- 应该看到：`{"status":"ok","message":"服务器运行正常"}`

📝 **本地测试**
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ARK_API_KEY='your-api-key'

# 测试生产环境
gunicorn app:app --bind 0.0.0.0:5000
```

