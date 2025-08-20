from browser_use import Controller, ActionResult, BrowserContext
from pydantic import BaseModel
from playwright.async_api import Page
import asyncio

class MeetingController(Controller):
    def __init__(self):
        super().__init__()
        self._register_meeting_actions()
    
    def _register_meeting_actions(self):
        """注册会议管理相关的 actions"""
        
        def is_meeting_page(page: Page) -> bool:
            """判断是否为会议管理页面"""
            return 'meeting.do' in page.url and 'seeyoncloud.com' in page.url
        
        @self.registry.action(
            '选择会议参会人员 - 点击"与会人员"输入框并搜索用户',
            domains=['*.seeyoncloud.com'],
            page_filter=is_meeting_page
        )
        async def select_meeting_participants(browser: BrowserContext, participant_names: list[str]):
            """
            选择会议参会人员
            
            Args:
                participant_names: 参会人员姓名列表，如 ['张三', '李四']
            """
            page = await browser.get_current_page()
            
            try:
                # 1. 查找并点击"与会人员"后面的输入框
                await self._click_participant_input(page)
                
                # 2. 等待弹出窗口出现
                await self._wait_for_participant_popup(page)
                
                # 3. 为每个参会人员执行搜索和选择
                selected_participants = []
                for name in participant_names:
                    participant = await self._search_and_select_participant(page, name)
                    if participant:
                        selected_participants.append(participant)
                
                return ActionResult(
                    extracted_content=f'成功选择参会人员: {", ".join(selected_participants)}',
                    include_in_memory=True
                )
                
            except Exception as e:
                return ActionResult(
                    error=f'选择参会人员时出错: {str(e)}',
                    include_in_memory=True
                )
    
    async def _click_participant_input(self, page: Page):
        """点击"与会人员"输入框"""
        # 尝试多种选择器来定位输入框
        selectors = [
            'input[placeholder*="点击选择参会人员"]',
            'input[placeholder*="参会人员"]',
            'input[name*="participant"]',
            'input[id*="participant"]',
            '//input[contains(@placeholder, "点击选择参会人员")]',  # XPath
            '//input[contains(@placeholder, "参会人员")]',  # XPath
        ]
        
        for selector in selectors:
            try:
                if selector.startswith('//'):
                    # XPath 选择器
                    element = page.locator(f"xpath={selector}")
                else:
                    # CSS 选择器
                    element = page.locator(selector)
                
                if await element.count() > 0:
                    await element.first.click()
                    print(f"成功点击参会人员输入框，使用选择器: {selector}")
                    return
            except Exception as e:
                print(f"选择器 {selector} 失败: {e}")
                continue
        
        # 如果所有选择器都失败，尝试通过文本查找
        try:
            # 查找包含"与会人员"文本的元素
            participant_label = page.locator('text=与会人员')
            if await participant_label.count() > 0:
                # 查找标签后面的输入框
                input_element = participant_label.locator('xpath=following-sibling::input | following-sibling::*//input')
                if await input_element.count() > 0:
                    await input_element.first.click()
                    print("通过文本标签找到并点击了参会人员输入框")
                    return
        except Exception as e:
            print(f"通过文本标签查找失败: {e}")
        
        raise Exception("无法找到参会人员输入框")
    
    async def _wait_for_participant_popup(self, page: Page):
        """等待参会人员选择弹窗出现"""
        # 等待弹窗出现，可能的选择器
        popup_selectors = [
            '.participant-popup',
            '.user-select-popup',
            '.search-popup',
            '[class*="popup"]',
            '[class*="modal"]',
            '[class*="dialog"]',
            '//div[contains(@class, "popup")]',  # XPath
            '//div[contains(@class, "modal")]',  # XPath
        ]
        
        for selector in popup_selectors:
            try:
                if selector.startswith('//'):
                    element = page.locator(f"xpath={selector}")
                else:
                    element = page.locator(selector)
                
                await element.wait_for(state='visible', timeout=5000)
                print(f"弹窗已出现，使用选择器: {selector}")
                return
            except Exception:
                continue
        
        # 如果没找到弹窗，等待一下让页面加载
        await asyncio.sleep(2)
        print("等待弹窗加载完成")
    
    async def _search_and_select_participant(self, page: Page, participant_name: str):
        """搜索并选择特定参会人员"""
        try:
            # 1. 查找搜索框
            search_selectors = [
                'input[placeholder*="搜索"]',
                'input[placeholder*="请输入"]',
                'input[type="text"]',
                '//input[contains(@placeholder, "搜索")]',
                '//input[contains(@placeholder, "请输入")]',
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    if selector.startswith('//'):
                        element = page.locator(f"xpath={selector}")
                    else:
                        element = page.locator(selector)
                    
                    if await element.count() > 0:
                        search_input = element.first
                        break
                except Exception:
                    continue
            
            if not search_input:
                raise Exception("无法找到搜索框")
            
            # 2. 清空搜索框并输入姓名
            await search_input.clear()
            await search_input.fill(participant_name)
            print(f"在搜索框中输入: {participant_name}")
            
            # 3. 等待搜索结果
            await asyncio.sleep(1)
            
            # 4. 查找并点击搜索结果
            result_selectors = [
                f'text={participant_name}',
                f'//*[contains(text(), "{participant_name}")]',
                '.search-result-item',
                '[class*="result"]',
            ]
            
            for selector in result_selectors:
                try:
                    if selector.startswith('//'):
                        element = page.locator(f"xpath={selector}")
                    else:
                        element = page.locator(selector)
                    
                    if await element.count() > 0:
                        await element.first.click()
                        print(f"成功选择参会人员: {participant_name}")
                        return participant_name
                except Exception:
                    continue
            
            print(f"未找到参会人员: {participant_name}")
            return None
            
        except Exception as e:
            print(f"搜索参会人员 {participant_name} 时出错: {e}")
            return None