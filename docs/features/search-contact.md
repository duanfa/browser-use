# 联系人搜索功能 (SearchContactAction)

## 概述

`SearchContactAction` 是一个专门用于联系人搜索控件的新action类型，它能够智能识别和处理各种类型的联系人搜索界面，支持多种搜索类型和自动结果处理。

## 功能特性

### 支持的搜索类型

- **name**: 姓名搜索
- **email**: 邮箱搜索  
- **phone**: 电话号码搜索
- **company**: 公司名称搜索
- **all**: 全字段搜索
- **自动检测**: 根据placeholder文本自动识别搜索类型

### 智能识别

- 自动检测搜索输入框的类型
- 根据placeholder文本判断是否为联系人搜索字段
- 支持多种搜索界面模式
- 自动处理焦点和滚动

### 多种搜索策略

1. **输入触发**: 输入搜索内容后自动触发搜索
2. **事件触发**: 模拟各种键盘事件和DOM事件
3. **结果等待**: 智能等待搜索结果加载
4. **结果选择**: 可选的自动选择第一个结果

## 使用方法

### 基本用法

```python
from browser_use.controller.views import SearchContactAction

# 创建联系人搜索动作
contact_search_action = SearchContactAction(
    index=0,  # 页面元素的索引
    search_query="John Doe",  # 搜索查询内容
    search_type="name",  # 搜索类型
    wait_for_results=True,  # 等待搜索结果
    select_first_result=False  # 不自动选择第一个结果
)

# 执行搜索动作
result = await controller.act(
    action=contact_search_action,
    browser_context=browser
)
```

### 搜索类型示例

```python
# 姓名搜索
name_search = SearchContactAction(
    index=0,
    search_query="张三",
    search_type="name",
    wait_for_results=True
)

# 邮箱搜索
email_search = SearchContactAction(
    index=1,
    search_query="zhangsan@example.com",
    search_type="email",
    select_first_result=True
)

# 公司搜索
company_search = SearchContactAction(
    index=2,
    search_query="Microsoft",
    search_type="company",
    wait_for_results=True
)

# 电话号码搜索
phone_search = SearchContactAction(
    index=3,
    search_query="+86-138-0013-8000",
    search_type="phone",
    select_first_result=True
)
```

### 自动类型检测

如果不指定 `search_type`，系统会自动检测搜索字段的类型：

```python
# 自动检测搜索类型
auto_search = SearchContactAction(
    index=0,
    search_query="John Doe",
    wait_for_results=True
)
```

## 参数说明

### SearchContactAction 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `index` | int | 是 | 页面元素的索引 |
| `search_query` | str | 是 | 搜索查询内容 |
| `search_type` | str \| None | 否 | 搜索类型，如果不提供则自动检测 |
| `wait_for_results` | bool | 否 | 是否等待搜索结果加载完成，默认True |
| `select_first_result` | bool | 否 | 是否自动选择第一个搜索结果，默认False |
| `xpath` | str \| None | 否 | 元素的XPath路径 |

### 支持的搜索类型

| 搜索类型 | 描述 | 适用场景 |
|----------|------|----------|
| name | 姓名搜索 | 人员管理、用户查找 |
| email | 邮箱搜索 | 邮件系统、用户认证 |
| phone | 电话搜索 | 通讯录、客户管理 |
| company | 公司搜索 | 企业名录、合作伙伴查找 |
| all | 全字段搜索 | 通用搜索、模糊匹配 |

## 实现细节

### 核心方法

`_search_contact_element_node()` 方法负责实际的联系人搜索操作：

1. **元素定位**: 使用索引或XPath定位目标搜索框
2. **类型检测**: 自动识别搜索字段的类型
3. **内容输入**: 清空并输入搜索查询内容
4. **搜索触发**: 使用多种方法触发搜索
5. **结果等待**: 智能等待搜索结果出现
6. **结果处理**: 提取和选择搜索结果

### 搜索触发策略

系统使用多种方法触发搜索，确保兼容性：

```python
# 方法1: 按Enter键
await element_handle.press('Enter')

# 方法2: 触发input事件
await element_handle.evaluate('el => {el.dispatchEvent(new Event("input", { bubbles: true }));}')

# 方法3: 触发change事件
await element_handle.evaluate('el => {el.dispatchEvent(new Event("change", { bubbles: true }));}')

# 方法4: 触发keyup事件（实时搜索）
await element_handle.evaluate('el => {el.dispatchEvent(new KeyboardEvent("keyup", { key: "a", bubbles: true }));}')
```

### 结果检测策略

系统使用多种策略检测搜索结果：

```python
# 常见的结果选择器
result_selectors = [
    '.search-result', '.contact-result', '.user-result', '.person-result',
    '[data-testid*="result"]', '[class*="result"]', '[class*="item"]',
    '.dropdown-item', '.autocomplete-item', '.suggestion-item',
    'li', '.list-item', '.item'
]
```

### 智能字段识别

系统通过placeholder文本自动识别联系人搜索字段：

```python
contact_keywords = [
    'contact', 'person', 'name', 'email', 'phone', 'telephone', 'mobile',
    'user', 'employee', 'staff', 'member', 'customer', 'client',
    'search', 'find', 'lookup', 'query', 'filter',
    '联系人', '人员', '姓名', '邮箱', '电话', '手机', '用户', '员工', '客户'
]
```

## 使用场景

### 常见应用

1. **CRM系统**: 客户关系管理中的联系人查找
2. **通讯录应用**: 手机、邮箱等通讯录搜索
3. **企业管理系统**: 员工、客户、合作伙伴查找
4. **社交平台**: 用户搜索和好友查找
5. **电子商务**: 客户账户搜索

### 示例场景

```python
# CRM客户搜索
customer_search = SearchContactAction(
    index=5,
    search_query="张经理",
    search_type="name",
    wait_for_results=True,
    select_first_result=True
)

# 员工通讯录搜索
employee_search = SearchContactAction(
    index=10,
    search_query="13800138000",
    search_type="phone",
    wait_for_results=True
)

# 合作伙伴搜索
partner_search = SearchContactAction(
    index=15,
    search_query="阿里巴巴",
    search_type="company",
    wait_for_results=True,
    select_first_result=False
)
```

## 最佳实践

### 搜索查询优化

- 使用准确的搜索关键词
- 考虑搜索字段的特定格式要求
- 避免过于模糊的搜索词

### 结果处理策略

```python
# 等待结果但不自动选择
search_action = SearchContactAction(
    index=0,
    search_query="John Doe",
    wait_for_results=True,
    select_first_result=False
)

# 快速搜索并自动选择第一个结果
quick_search = SearchContactAction(
    index=0,
    search_query="john@example.com",
    wait_for_results=True,
    select_first_result=True
)
```

### 错误处理

```python
try:
    result = await controller.act(
        action=contact_search_action,
        browser_context=browser
    )
    if result.success:
        print(f"搜索成功: {result.extracted_content}")
    else:
        print(f"搜索失败: {result.error}")
except Exception as e:
    print(f"执行搜索动作时发生错误: {str(e)}")
```

## 故障排除

### 常见问题

1. **元素未找到**: 检查索引是否正确，页面是否已加载
2. **搜索未触发**: 确认搜索框支持相应的触发方式
3. **结果未出现**: 检查网络连接和页面状态
4. **类型识别错误**: 手动指定search_type参数

### 调试技巧

- 启用详细日志记录
- 检查搜索框的可交互状态
- 验证搜索查询的有效性
- 使用浏览器开发者工具检查元素

### 性能优化

- 合理设置等待时间
- 避免频繁的搜索操作
- 监控搜索执行性能

## 更新日志

- **v1.0.0**: 初始版本，支持基本的联系人搜索功能
- 支持多种搜索类型（姓名、邮箱、电话、公司）
- 智能字段类型检测和自动识别
- 多种搜索触发策略确保兼容性
- 智能结果检测和自动选择功能
- 完善的错误处理和性能监控
