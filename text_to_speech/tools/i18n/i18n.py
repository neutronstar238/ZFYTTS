#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的 i18n 模块 - 用于推理
"""

def scan_language_list():
    """返回支持的语言列表"""
    return ["zh_CN", "en_US", "ja_JP"]

class I18nAuto:
    def __init__(self, language=None):
        self.language = language or "zh_CN"
        # 预定义关键词翻译
        self.translations = {
            "中文": "中文",
            "英文": "英文",
            "日文": "日文",
            "中英混合": "中英混合",
            "日英混合": "日英混合",
            "多语种混合": "多语种混合",
            "多语种混合(粤语)": "多语种混合(粤语)",
            "韩文": "韩文",
            "粤语": "粤语",
            "不切": "不切",
            "凑四句一切": "凑四句一切",
            "凑50字一切": "凑50字一切",
            "按中文句号。切": "按中文句号。切",
            "按英文句号.切": "按英文句号.切",
            "按标点符号切": "按标点符号切",
        }
    
    def __call__(self, key):
        """返回翻译后的文本"""
        return self.translations.get(key, key)
