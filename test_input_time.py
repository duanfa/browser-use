"""
测试InputTimeAction功能的简单测试文件
"""

import pytest
from browser_use.controller.views import InputTimeAction


def test_input_time_action_creation():
    """测试InputTimeAction的创建"""
    
    # 测试基本创建
    action = InputTimeAction(
        index=0,
        time_value="2024-12-25 14:30"
    )
    
    assert action.index == 0
    assert action.time_value == "2024-12-25 14:30"
    assert action.time_format is None
    assert action.xpath is None
    
    # 测试带格式的创建
    action_with_format = InputTimeAction(
        index=1,
        time_value="14:30",
        time_format="time"
    )
    
    assert action_with_format.index == 1
    assert action_with_format.time_value == "14:30"
    assert action_with_format.time_format == "time"
    
    # 测试带xpath的创建
    action_with_xpath = InputTimeAction(
        index=2,
        time_value="2024-12-25",
        time_format="date",
        xpath="//input[@type='date']"
    )
    
    assert action_with_xpath.xpath == "//input[@type='date']"


def test_input_time_action_validation():
    """测试InputTimeAction的验证"""
    
    # 测试必需参数
    with pytest.raises(ValueError):
        InputTimeAction(
            time_value="14:30"  # 缺少index
        )
    
    with pytest.raises(ValueError):
        InputTimeAction(
            index=0  # 缺少time_value
        )
    
    # 测试有效的时间值
    valid_times = [
        "14:30",
        "14:30:45", 
        "2024-12-25",
        "2024-12-25T14:30",
        "2024-12-25T14:30:45"
    ]
    
    for time_val in valid_times:
        action = InputTimeAction(index=0, time_value=time_val)
        assert action.time_value == time_val


def test_input_time_action_serialization():
    """测试InputTimeAction的序列化"""
    
    action = InputTimeAction(
        index=5,
        time_value="2024-12-25T09:00",
        time_format="datetime-local",
        xpath="//input[@type='datetime-local']"
    )
    
    # 转换为字典
    action_dict = action.model_dump()
    
    assert action_dict["index"] == 5
    assert action_dict["time_value"] == "2024-12-25T09:00"
    assert action_dict["time_format"] == "datetime-local"
    assert action_dict["xpath"] == "//input[@type='datetime-local']"
    
    # 从字典创建
    new_action = InputTimeAction(**action_dict)
    assert new_action.index == action.index
    assert new_action.time_value == action.time_value
    assert new_action.time_format == action.time_format
    assert new_action.xpath == action.xpath


if __name__ == "__main__":
    # 运行测试
    test_input_time_action_creation()
    test_input_time_action_validation()
    test_input_time_action_serialization()
    print("✅ 所有测试通过！")
