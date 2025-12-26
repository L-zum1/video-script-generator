# 部署指南

## PythonAnywhere 部署步骤

PythonAnywhere 是一个非常适合部署Python应用的云平台，提供免费套餐。

### 1. 注册账户

1. 访问 [PythonAnywhere](https://www.pythonanywhere.com/)
2. 注册一个免费账户

### 2. 创建Web应用

1. 登录后，点击 "Web" 选项卡
2. 点击 "Add a new web app"
3. 选择 "Flask" 框架
4. 选择 "Python 3.9" 版本
5. 点击 "Next" 和 "Create"

### 3. 上传代码

有两种方式上传代码：

#### 方式一：使用Git（推荐）

1. 在PythonAnywhere的 "Bash" 控制台中：
   ```bash
   git clone https://github.com/L-zum1/video-script-generator.git
   cd video-script-generator
   ```

#### 方式二：手动上传

1. 将项目文件打包成zip
2. 在 "Files" 选项卡中上传并解压

### 4. 配置Web应用

1. 在 "Web" 选项卡中，编辑 "WSGI configuration file"
2. 将内容替换为：

```python
import sys
# 添加项目目录到Python路径
project_home = u'/home/你的用户名/video-script-generator'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# 导入Flask应用实例
from app import app as application
```

### 5. 安装依赖

1. 在 "Bash" 控制台中：
   ```bash
   cd video-script-generator
   pip install -r requirements.txt
   ```

### 6. 设置环境变量（可选）

如果您想设置默认的API密钥：

1. 在 "Web" 选项卡中，点击 "Source code"
2. 在 "Environment variables" 部分添加：
   - Key: `ARK_API_KEY`
   - Value: 您的API密钥

### 7. 重载Web应用

1. 在 "Web" 选项卡中，点击绿色的 "Reload" 按钮
2. 等待几秒钟，然后访问您的应用URL

## 其他部署选项

### 1. Vercel（需要Node.js环境）

如果您有Node.js环境，可以使用Vercel CLI：

```bash
npm install -g vercel
vercel
```

### 2. Railway

1. 访问 [Railway](https://railway.app/)
2. 使用GitHub登录
3. 导入您的GitHub仓库
4. Railway会自动检测并部署Flask应用

### 3. Render

1. 访问 [Render](https://render.com/)
2. 注册并连接GitHub账户
3. 选择 "New Web Service"
4. 连接您的GitHub仓库
5. Render会自动部署

## 注意事项

1. **API密钥安全**：不要将API密钥硬编码在代码中，始终使用环境变量
2. **免费限制**：大多数免费平台都有使用限制，如请求次数、运行时间等
3. **域名**：免费平台通常提供子域名，如需自定义域名需要付费

## 故障排除

1. **500错误**：检查日志，通常是依赖缺失或代码错误
2. **导入错误**：确保所有依赖都已正确安装
3. **环境变量**：确认API密钥等环境变量已正确设置

部署完成后，您就可以通过互联网访问您的视频脚本生成器了！