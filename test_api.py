#!/usr/bin/env python3
"""
测试API密钥和生成功能的脚本
"""

import os
import sys
from untils import generate_script

def test_api_key():
    """测试API密钥是否设置"""
    api_key = os.getenv('ARK_API_KEY')
    if not api_key:
        print("❌ 错误: ARK_API_KEY 环境变量未设置")
        print("\n请设置API密钥:")
        print("  export ARK_API_KEY='your-api-key-here'")
        return False
    
    print(f"✅ API密钥已设置: {api_key[:10]}...{api_key[-4:]}")
    return True

def test_generate():
    """测试生成功能"""
    print("\n🧪 测试生成功能...")
    print("=" * 60)
    
    try:
        # 使用简单的测试主题
        subject = "人工智能"
        video_length = 1
        creativity = 0.7
        
        print(f"主题: {subject}")
        print(f"时长: {video_length} 分钟")
        print(f"创造力: {creativity}")
        print("\n⏳ 正在生成（这可能需要一些时间）...")
        
        search_result, title, script = generate_script(
            subject=subject,
            video_length=video_length,
            creativity=creativity
        )
        
        print("\n✅ 生成成功！")
        print("=" * 60)
        print(f"\n📝 标题: {title}")
        print(f"\n📄 脚本长度: {len(script)} 字符")
        print(f"\n📚 参考信息长度: {len(search_result)} 字符")
        
        return True
        
    except ValueError as e:
        print(f"\n❌ 参数错误: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        print(f"\n错误类型: {type(e).__name__}")
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔍 API测试工具")
    print("=" * 60)
    
    # 测试API密钥
    if not test_api_key():
        sys.exit(1)
    
    # 询问是否进行完整测试
    print("\n⚠️  注意: 完整测试将调用AI API，可能会消耗API额度")
    response = input("是否继续测试生成功能？(y/n): ")
    
    if response.lower() in ['y', 'yes', '是']:
        success = test_generate()
        if success:
            print("\n✅ 所有测试通过！")
            sys.exit(0)
        else:
            print("\n❌ 测试失败，请检查错误信息")
            sys.exit(1)
    else:
        print("\n⏭️  跳过生成测试")
        sys.exit(0)

