#!/usr/bin/env python3
"""
测试服务器连接的脚本
"""
import requests
import sys

def test_server(port=5001):
    """测试服务器是否运行"""
    base_url = f"http://localhost:{port}"
    
    print(f"🔍 正在测试服务器连接...")
    print(f"📍 测试地址: {base_url}")
    print("-" * 60)
    
    # 测试健康检查端点
    try:
        print("1️⃣ 测试健康检查端点 /api/health...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ 健康检查成功: {response.json()}")
        else:
            print(f"   ❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ 无法连接到服务器！")
        print(f"   💡 请确保 Flask 服务器正在运行:")
        print(f"      python app.py")
        return False
    except requests.exceptions.Timeout:
        print(f"   ❌ 连接超时！")
        return False
    except Exception as e:
        print(f"   ❌ 发生错误: {e}")
        return False
    
    # 测试主页
    try:
        print("\n2️⃣ 测试主页 /...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ 主页加载成功 (内容长度: {len(response.text)} 字符)")
        else:
            print(f"   ❌ 主页加载失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 发生错误: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！服务器运行正常")
    print(f"🌐 请在浏览器中访问: {base_url}")
    print("=" * 60)
    return True

if __name__ == '__main__':
    # 尝试多个端口
    ports = [5001, 5002, 5003, 5000]
    
    for port in ports:
        print(f"\n尝试端口 {port}...")
        if test_server(port):
            sys.exit(0)
    
    print("\n❌ 所有端口测试失败！")
    print("请确保 Flask 服务器正在运行:")
    print("  python app.py")
    sys.exit(1)
