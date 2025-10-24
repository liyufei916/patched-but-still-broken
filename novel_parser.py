"""
小说解析器模块

该模块提供基础的小说文本解析功能，主要用于按章节分割小说文本。

功能：
- 按章节标题分割小说
- 提取章节内容和段落
- 支持多种章节标题格式

作者：AI Assistant  
版本：1.0
日期：2024-10-24
"""

import re
import jieba
from typing import List, Dict


class NovelParser:
    """
    小说解析器类
    
    用于解析小说文本，将其分割成章节，并提取每个章节的标题、内容和段落。
    
    属性:
        novel_text (str): 原始小说文本
        chapters (List[Dict]): 解析后的章节列表
    """
    
    def __init__(self, novel_text: str):
        """
        初始化小说解析器
        
        参数:
            novel_text (str): 要解析的完整小说文本
        """
        self.novel_text = novel_text
        self.chapters = []
        
    def parse(self) -> List[Dict]:
        """
        解析小说文本
        
        将小说文本按章节分割，并返回结构化的章节数据。
        
        返回:
            List[Dict]: 章节列表，每个章节包含：
                - title: 章节标题
                - content: 章节完整内容
                - paragraphs: 段落列表
        """
        self.chapters = self._split_into_chapters()
        return self.chapters
    
    def _split_into_chapters(self) -> List[Dict]:
        """
        内部方法：将文本分割成章节
        
        使用正则表达式识别章节标题（如"第一章"、"第1章"、"第一回"等），
        并按章节标题分割文本。
        
        返回:
            List[Dict]: 分割后的章节列表
        """
        # 章节标题的正则模式，支持：
        # - 第X章（X可以是中文数字或阿拉伯数字）
        # - 第X回
        # - 第X节
        chapter_pattern = r'第[一二三四五六七八九十百千\d]+[章回节].*'
        
        # 使用正则表达式分割文本，保留分隔符（章节标题）
        parts = re.split(f'({chapter_pattern})', self.novel_text)
        
        chapters = []
        # 遍历分割后的部分，每两个部分组成一个章节
        # parts[0]是第一个章节标题之前的内容（通常为空或序言）
        # parts[1]是第一个章节标题
        # parts[2]是第一个章节内容
        # parts[3]是第二个章节标题
        # ...以此类推
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                chapter_title = parts[i].strip()
                chapter_content = parts[i + 1].strip()
                
                # 将章节内容按行分割成段落，去除空行
                paragraphs = [p.strip() for p in chapter_content.split('\n') if p.strip()]
                
                chapters.append({
                    'title': chapter_title,
                    'content': chapter_content,
                    'paragraphs': paragraphs
                })
        
        # 如果没有找到任何章节标题，将整个文本作为一个章节
        if not chapters and self.novel_text.strip():
            paragraphs = [p.strip() for p in self.novel_text.split('\n') if p.strip()]
            chapters.append({
                'title': '全文',
                'content': self.novel_text,
                'paragraphs': paragraphs
            })
        
        return chapters
    
    def get_chapter(self, index: int) -> Dict:
        """
        获取指定索引的章节
        
        参数:
            index (int): 章节索引（从0开始）
            
        返回:
            Dict: 章节数据，如果索引无效则返回None
        """
        if 0 <= index < len(self.chapters):
            return self.chapters[index]
        return None
    
    def get_total_chapters(self) -> int:
        """
        获取章节总数
        
        返回:
            int: 章节总数
        """
        return len(self.chapters)
