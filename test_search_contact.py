"""
测试SearchContactAction功能的简单测试文件
"""

import pytest
from browser_use.controller.views import SearchContactAction


def test_search_contact_action_creation():
    """测试SearchContactAction的创建"""
    
    # 测试基本创建
    action = SearchContactAction(
        index=0,
        search_query="John Doe"
    )
    
    assert action.index == 0
    assert action.search_query == "John Doe"
    assert action.search_type is None
    assert action.wait_for_results is True
    assert action.select_first_result is False
    assert action.xpath is None
    
    # 测试带搜索类型的创建
    action_with_type = SearchContactAction(
        index=1,
        search_query="john@example.com",
        search_type="email"
    )
    
    assert action_with_type.index == 1
    assert action_with_type.search_query == "john@example.com"
    assert action_with_type.search_type == "email"
    
    # 测试带所有参数的创建
    action_with_all_params = SearchContactAction(
        index=2,
        search_query="Microsoft",
        search_type="company",
        wait_for_results=False,
        select_first_result=True,
        xpath="//input[@placeholder='搜索公司']"
    )
    
    assert action_with_all_params.index == 2
    assert action_with_all_params.search_query == "Microsoft"
    assert action_with_all_params.search_type == "company"
    assert action_with_all_params.wait_for_results is False
    assert action_with_all_params.select_first_result is True
    assert action_with_all_params.xpath == "//input[@placeholder='搜索公司']"


def test_search_contact_action_validation():
    """测试SearchContactAction的验证"""
    
    # 测试必需参数
    with pytest.raises(ValueError):
        SearchContactAction(
            search_query="John Doe"  # 缺少index
        )
    
    with pytest.raises(ValueError):
        SearchContactAction(
            index=0  # 缺少search_query
        )
    
    # 测试有效的搜索查询
    valid_queries = [
        "John Doe",
        "john@example.com",
        "+1-555-123-4567",
        "Microsoft",
        "张三",
        "zhangsan@example.com",
        "13800138000",
        "阿里巴巴"
    ]
    
    for query in valid_queries:
        action = SearchContactAction(index=0, search_query=query)
        assert action.search_query == query
    
    # 测试有效的搜索类型
    valid_types = ["name", "email", "phone", "company", "all"]
    
    for search_type in valid_types:
        action = SearchContactAction(index=0, search_query="test", search_type=search_type)
        assert action.search_type == search_type


def test_search_contact_action_serialization():
    """测试SearchContactAction的序列化"""
    
    action = SearchContactAction(
        index=5,
        search_query="张经理",
        search_type="name",
        wait_for_results=True,
        select_first_result=True,
        xpath="//input[@placeholder='搜索联系人']"
    )
    
    # 转换为字典
    action_dict = action.model_dump()
    
    assert action_dict["index"] == 5
    assert action_dict["search_query"] == "张经理"
    assert action_dict["search_type"] == "name"
    assert action_dict["wait_for_results"] is True
    assert action_dict["select_first_result"] is True
    assert action_dict["xpath"] == "//input[@placeholder='搜索联系人']"
    
    # 从字典创建
    new_action = SearchContactAction(**action_dict)
    assert new_action.index == action.index
    assert new_action.search_query == action.search_query
    assert new_action.search_type == action.search_type
    assert new_action.wait_for_results == action.wait_for_results
    assert new_action.select_first_result == action.select_first_result
    assert new_action.xpath == action.xpath


def test_search_contact_action_defaults():
    """测试SearchContactAction的默认值"""
    
    action = SearchContactAction(
        index=0,
        search_query="test"
    )
    
    # 测试默认值
    assert action.wait_for_results is True
    assert action.select_first_result is False
    assert action.search_type is None
    assert action.xpath is None


def test_search_contact_action_edge_cases():
    """测试SearchContactAction的边界情况"""
    
    # 测试空字符串搜索查询
    action_empty_query = SearchContactAction(
        index=0,
        search_query=""
    )
    assert action_empty_query.search_query == ""
    
    # 测试特殊字符搜索查询
    action_special_chars = SearchContactAction(
        index=0,
        search_query="!@#$%^&*()_+-=[]{}|;':\",./<>?"
    )
    assert action_special_chars.search_query == "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    
    # 测试长搜索查询
    long_query = "A" * 1000
    action_long_query = SearchContactAction(
        index=0,
        search_query=long_query
    )
    assert action_long_query.search_query == long_query


if __name__ == "__main__":
    # 运行测试
    test_search_contact_action_creation()
    test_search_contact_action_validation()
    test_search_contact_action_serialization()
    test_search_contact_action_defaults()
    test_search_contact_action_edge_cases()
    print("✅ 所有测试通过！")
