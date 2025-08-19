"""
时间控件填充时间值的示例

这个示例展示了如何使用新创建的InputTimeAction来填充各种类型的时间控件，
包括HTML5的datetime-local、time、date等输入类型。
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
from browser_use.controller.views import InputTimeAction


async def main():
    """主函数：演示时间控件填充功能"""
    
    # 创建浏览器实例
    browser = Browser()
    
    try:
        # 创建浏览器上下文
        context = await browser.new_context()
        
        # 创建新标签页并导航到测试页面
        test_page_url = "https://ant.design/~demos/date-picker-demo-time"
        await context.create_new_tab(test_page_url)
        
        print("🌐 已导航到测试页面")
        
        # 等待页面加载
        await asyncio.sleep(5)
        
        # 获取当前页面
        page = await context.get_current_page()
        
        # 获取页面上的时间控件元素
        # 这里需要根据实际页面结构调整选择器

        
        time_input_selector = "//*[@id='root']/div/div/div[1]/div/div/input"
        
        try:
            # 等待时间控件出现
            time_input = await page.wait_for_selector(time_input_selector, timeout=10000)
            if time_input:
                print("✅ 找到时间控件")
                
                # 直接使用playwright填充时间值
                await time_input.fill("2024-12-25 14:30")
                print("⏰ 已填充时间值: 2024-12-2514:30")
                
                # 获取填充后的值
                filled_value = await time_input.input_value()
                print(f"📝 当前时间值: {filled_value}")
                
            else:
                print("❌ 未找到时间控件")
                
        except Exception as e:
            print(f"❌ 操作时间控件时出错: {str(e)}")
            
        # 演示其他时间格式
        print("\n🔄 演示其他时间格式...")
        
        # 时间格式示例
        time_formats = [
            ("14:30", "time"),           # HH:MM
            ("14:30:45", "time"),        # HH:MM:SS  
            ("2024-12-25", "date"),      # YYYY-MM-DD
            ("2024-12-25 14:30:45", "datetime"),  # YYYY-MM-DD HH:MM:SS
            ("2024-12-25 14:30", "datetime"),  # YYYY-MM-DD HH:MM
            ("2024-12-25T14:30:45", "datetime-local"),  # YYYY-MM-DDTHH:MM:SS
        ]
        
        for time_value, format_type in time_formats:
            print(f"  尝试填充 {format_type} 格式: {time_value}")
            
            try:
                # 这里可以根据不同的时间控件类型选择不同的选择器
                if format_type == "time":
                    selector = "input[type='time']"
                elif format_type == "date":
                    selector = "input[type='date']"
                else:
                    selector = "input[type='datetime-local']"
                
                # 尝试找到对应的时间控件
                time_element = await page.query_selector(selector)
                if time_element:
                    await time_element.fill(time_value)
                    print(f"    ✅ 成功填充 {time_value}")
                else:
                    print(f"    ⚠️ 未找到 {format_type} 类型的控件")
                    
            except Exception as e:
                print(f"    ❌ 失败: {str(e)}")
            
            await asyncio.sleep(1)  # 等待一下再尝试下一个
        
        print("\n🎉 时间控件填充演示完成！")
        
        # 等待用户查看结果
        input("按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        
    finally:
        # 关闭浏览器
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
