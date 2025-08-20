"""
联系人搜索控件示例

这个示例展示了如何使用新创建的SearchContactAction来搜索联系人，
支持各种搜索类型和自动结果选择。
"""

import sys
import os

# 添加browser_use模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
browser_use_path = os.path.join(current_dir, '..', '..')
sys.path.insert(0, browser_use_path)

import asyncio
from browser_use.browser.browser import Browser
from browser_use.controller.service import Controller
from browser_use.controller.views import SearchContactAction


async def main():
    """主函数：演示联系人搜索功能"""
    
    # 创建浏览器实例
    browser = Browser()
    
    try:
        # 创建浏览器上下文
        context = await browser.new_context()
        
        # 创建新标签页并导航到测试页面
        # 使用一个包含联系人搜索功能的测试页面
        test_page_url = "https://ant.design/components/select#components-select-demo-search"
        await context.create_new_tab(test_page_url)
        
        print("🌐 已导航到测试页面")
        
        # 等待页面加载
        await asyncio.sleep(5)
        
        # 获取当前页面
        page = await context.get_current_page()
        
        # 创建控制器
        controller = Controller()
        
        # 演示不同的联系人搜索场景
        print("\n🔍 演示联系人搜索功能...")
        
        # 场景1: 基本联系人搜索
        print("\n📋 场景1: 基本联系人搜索")
        try:
            # 查找搜索输入框
            search_input = await page.wait_for_selector('input[placeholder*="search"], input[placeholder*="搜索"], .ant-select-selection-search input', timeout=10000)
            
            if search_input:
                print("✅ 找到搜索输入框")
                
                # 获取元素的索引（这里需要根据实际DOM结构调整）
                # 在实际使用中，应该通过browser_use的DOM分析获取正确的索引
                search_index = 0  # 假设是第一个可交互元素
                
                # 创建联系人搜索动作
                contact_search_action = SearchContactAction(
                    index=search_index,
                    search_query="John Doe",
                    search_type="name",
                    wait_for_results=True,
                    select_first_result=False
                )
                
                print(f"🔍 准备搜索联系人: {contact_search_action.search_query}")
                
                # 执行搜索动作
                result = await controller.act(
                    action=contact_search_action,
                    browser_context=context
                )
                
                if result.success:
                    print(f"✅ 搜索成功: {result.extracted_content}")
                else:
                    print(f"❌ 搜索失败: {result.error}")
                    
            else:
                print("❌ 未找到搜索输入框")
                
        except Exception as e:
            print(f"❌ 基本搜索演示失败: {str(e)}")
        
        # 场景2: 邮箱搜索
        print("\n📧 场景2: 邮箱搜索")
        try:
            email_search_action = SearchContactAction(
                index=0,
                search_query="john.doe@example.com",
                search_type="email",
                wait_for_results=True,
                select_first_result=True
            )
            
            print(f"📧 准备搜索邮箱: {email_search_action.search_query}")
            
            # 这里可以执行搜索，但需要正确的元素索引
            print("   ⚠️  需要正确的元素索引才能执行搜索")
            
        except Exception as e:
            print(f"❌ 邮箱搜索演示失败: {str(e)}")
        
        # 场景3: 公司搜索
        print("\n🏢 场景3: 公司搜索")
        try:
            company_search_action = SearchContactAction(
                index=0,
                search_query="Microsoft",
                search_type="company",
                wait_for_results=True,
                select_first_result=False
            )
            
            print(f"🏢 准备搜索公司: {company_search_action.search_query}")
            print("   ⚠️  需要正确的元素索引才能执行搜索")
            
        except Exception as e:
            print(f"❌ 公司搜索演示失败: {str(e)}")
        
        # 场景4: 电话号码搜索
        print("\n📞 场景4: 电话号码搜索")
        try:
            phone_search_action = SearchContactAction(
                index=0,
                search_query="+1-555-123-4567",
                search_type="phone",
                wait_for_results=True,
                select_first_result=True
            )
            
            print(f"📞 准备搜索电话: {phone_search_action.search_query}")
            print("   ⚠️  需要正确的元素索引才能执行搜索")
            
        except Exception as e:
            print(f"❌ 电话号码搜索演示失败: {str(e)}")
        
        # 场景5: 通用搜索（自动检测类型）
        print("\n🔍 场景5: 通用搜索（自动检测类型）")
        try:
            general_search_action = SearchContactAction(
                index=0,
                search_query="张三",
                wait_for_results=True,
                select_first_result=False
            )
            
            print(f"🔍 准备通用搜索: {general_search_action.search_query}")
            print("   ⚠️  需要正确的元素索引才能执行搜索")
            
        except Exception as e:
            print(f"❌ 通用搜索演示失败: {str(e)}")
        
        # 演示搜索类型检测
        print("\n🔄 演示搜索类型检测...")
        
        search_types = [
            ("name", "姓名搜索"),
            ("email", "邮箱搜索"),
            ("phone", "电话搜索"),
            ("company", "公司搜索"),
            ("all", "全字段搜索")
        ]
        
        for search_type, description in search_types:
            print(f"   {description}: {search_type}")
        
        print("\n🎉 联系人搜索演示完成！")
        
        # 等待用户查看结果
        input("按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        
    finally:
        # 关闭浏览器
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
