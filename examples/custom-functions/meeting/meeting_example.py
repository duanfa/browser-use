# 文件路径: browser-use/examples/custom-functions/meeting_example.py

"""
会议管理功能使用示例

演示如何使用 MeetingController 来管理会议
"""

import asyncio
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser, BrowserContext
from examples.custom_functions.meeting_controller import MeetingController

async def main():
    """主函数 - 演示会议管理功能"""
    
    # 加载环境变量
    load_dotenv()
    
    # 创建浏览器实例
    browser = Browser()
    
    async with await browser.new_context() as context:
        # 创建会议控制器
        meeting_controller = MeetingController()
        
        # 创建 LLM 实例
        llm = ChatOpenAI(model='gpt-4o')
        
        # 创建会议管理 Agent
        meeting_agent = Agent(
            task="""
            在会议管理页面执行以下操作：
            1. 选择参会人员：张三、李四、王五
            2. 设置会议时间为明天下午2点
            3. 填写会议主题为"项目进度讨论"
            """,
            llm=llm,
            browser_context=context,
            controller=meeting_controller,
            extend_system_message="""
            你是一个专门用于会议管理的 AI 助手。
            
            当前页面是会议管理页面，你可以：
            - 选择会议参会人员
            - 设置会议时间和主题
            - 管理会议设置
            
            请根据用户的任务要求，选择合适的操作来完成。
            """
        )
        
        # 运行 Agent
        await meeting_agent.run()

if __name__ == '__main__':
    asyncio.run(main())