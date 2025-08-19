#!/usr/bin/env python3
"""
测试DOM修复的脚本
"""

import asyncio
import logging
from browser_use.browser.chrome import ChromeBrowser
from browser_use.browser.context import BrowserContext

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_dom_loading():
    """测试DOM加载功能"""
    browser = None
    context = None
    
    try:
        # 启动浏览器
        browser = ChromeBrowser()
        await browser.start()
        
        # 创建上下文
        context = await browser.new_context()
        
        # 测试页面加载
        test_urls = [
            "https://www.example.com",
            "https://httpbin.org/html",
            "about:blank"
        ]
        
        for url in test_urls:
            logger.info(f"测试URL: {url}")
            
            try:
                # 导航到页面
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded")
                
                # 等待页面稳定
                await page.wait_for_timeout(2000)
                
                # 尝试获取DOM状态
                try:
                    dom_state = await context.get_updated_state()
                    logger.info(f"✅ {url} - DOM加载成功，节点数量: {len(dom_state.clickable_elements)}")
                except Exception as e:
                    logger.error(f"❌ {url} - DOM加载失败: {e}")
                    
            except Exception as e:
                logger.error(f"❌ {url} - 页面加载失败: {e}")
            finally:
                if 'page' in locals():
                    await page.close()
                    
    except Exception as e:
        logger.error(f"测试过程中出现错误: {e}")
        
    finally:
        # 清理资源
        if context:
            await context.close()
        if browser:
            await browser.stop()

if __name__ == "__main__":
    asyncio.run(test_dom_loading())


