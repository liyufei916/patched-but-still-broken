"""
文本处理模块 - 小说文本智能分析和处理

该模块提供完整的小说文本处理功能，包括：
- 场景分割：将文本按场景自动划分
- 角色识别：识别文本中的角色及其对话
- 对话提取：提取角色对话内容
- 情感分析：分析文本的情感倾向
- 动作识别：识别文本中的动作描述
- 场景描述提取：提取环境和场景描述

作者：AI Assistant
日期：2024-10-24
"""

import re
import jieba
import jieba.posseg as pseg
from typing import List, Dict, Tuple, Optional
from collections import Counter


class TextProcessor:
    """
    文本处理器主类
    
    负责将小说文本进行智能分析和结构化处理，为后续的多模态生成提供基础数据。
    """
    
    def __init__(self):
        """
        初始化文本处理器
        
        设置常用的正则表达式模式和情感词典
        """
        # 对话提取的正则模式（支持多种引号格式）
        self.dialogue_patterns = [
            r'[""]([^""]+)[""]',  # 双引号
            r'['']([^'']+)['']',  # 单引号
            r'"([^"]+)"',          # 英文双引号
            r"'([^']+)'",          # 英文单引号
        ]
        
        # 动作词汇列表（常见的动作动词）
        self.action_words = {
            '走', '跑', '跳', '站', '坐', '躺', '转', '看', '望', '瞧',
            '听', '说', '笑', '哭', '叫', '喊', '拿', '抓', '扔', '打',
            '推', '拉', '举', '放', '开', '关', '穿', '脱', '吃', '喝',
            '睡', '醒', '起', '飞', '游', '爬', '摔', '倒', '倾', '握',
            '指', '挥', '摇', '点', '摸', '碰', '踢', '撞', '靠', '倚'
        }
        
        # 积极情感词汇
        self.positive_words = {
            '高兴', '快乐', '开心', '幸福', '喜悦', '愉快', '兴奋', '激动',
            '欢乐', '美好', '温暖', '甜蜜', '满足', '欣慰', '舒适', '轻松',
            '愉悦', '欢喜', '喜爱', '欢笑', '笑容', '微笑', '灿烂', '明亮'
        }
        
        # 消极情感词汇
        self.negative_words = {
            '悲伤', '难过', '痛苦', '伤心', '哀愁', '忧伤', '悲痛', '凄凉',
            '沮丧', '失望', '绝望', '无助', '孤独', '寂寞', '冷清', '凄惨',
            '恐惧', '害怕', '担心', '焦虑', '紧张', '不安', '愤怒', '生气',
            '愤恨', '仇恨', '厌恶', '憎恨', '烦躁', '烦恼', '苦恼', '忧虑'
        }
        
    def process_novel(self, text: str) -> List[Dict]:
        """
        处理整部小说文本
        
        这是主要的处理入口，将文本分割成多个场景，并对每个场景进行深入分析。
        
        参数:
            text (str): 完整的小说文本
            
        返回:
            List[Dict]: 结构化的场景数据列表，每个场景包含：
                - description: 场景描述
                - characters: 出现的角色列表
                - dialogues: 对话内容列表
                - actions: 动作描述列表
                - emotion: 情感倾向（positive/negative/neutral）
                - text: 原始文本
        """
        # 第一步：将文本分割成多个场景
        scenes = self.split_into_scenes(text)
        
        # 第二步：对每个场景进行详细分析
        structured_data = []
        for scene_text in scenes:
            scene_data = {
                'text': scene_text,
                'description': self.extract_scene_description(scene_text),
                'characters': self.identify_characters(scene_text),
                'dialogues': self.extract_dialogues(scene_text),
                'actions': self.extract_actions(scene_text),
                'emotion': self.analyze_emotion(scene_text)
            }
            structured_data.append(scene_data)
        
        return structured_data
    
    def split_into_scenes(self, text: str) -> List[str]:
        """
        将文本分割成多个场景
        
        场景分割的依据：
        1. 段落换行（连续两个换行符）
        2. 场景转换标识词（如：此时、与此同时、另一边等）
        3. 时间变化（如：第二天、一小时后等）
        
        参数:
            text (str): 输入文本
            
        返回:
            List[str]: 分割后的场景文本列表
        """
        # 首先按段落分割
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # 如果没有双换行，尝试按单换行分割
        if len(paragraphs) <= 1:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # 场景转换关键词
        scene_markers = [
            '此时', '这时', '那时', '与此同时', '同时', '另一边', '另一方面',
            '第二天', '次日', '翌日', '过了', '之后', '后来', '不久',
            '突然', '忽然', '猛然', '转眼', '一晃', '片刻'
        ]
        
        scenes = []
        current_scene = []
        
        for para in paragraphs:
            # 检查是否包含场景转换标记
            is_new_scene = any(para.startswith(marker) for marker in scene_markers)
            
            if is_new_scene and current_scene:
                # 如果是新场景且当前场景非空，保存当前场景
                scenes.append('\n'.join(current_scene))
                current_scene = [para]
            else:
                # 否则添加到当前场景
                current_scene.append(para)
        
        # 添加最后一个场景
        if current_scene:
            scenes.append('\n'.join(current_scene))
        
        return scenes if scenes else [text]
    
    def identify_characters(self, text: str) -> List[str]:
        """
        识别文本中出现的角色
        
        使用jieba的词性标注功能识别人名（nr标签），
        并统计出现频率，返回主要角色。
        
        参数:
            text (str): 输入文本
            
        返回:
            List[str]: 识别出的角色名称列表（按出现频率降序）
        """
        # 使用词性标注识别人名
        words = pseg.cut(text)
        
        # 收集所有标记为人名(nr)的词
        person_names = []
        for word, flag in words:
            if flag == 'nr':  # nr表示人名
                person_names.append(word)
        
        # 统计人名出现频率
        name_counter = Counter(person_names)
        
        # 返回出现次数最多的角色（至少出现1次）
        characters = [name for name, count in name_counter.most_common() if count >= 1]
        
        return characters
    
    def extract_dialogues(self, text: str) -> List[Dict[str, str]]:
        """
        提取文本中的对话内容
        
        识别引号内的对话，并尝试匹配说话人。
        
        参数:
            text (str): 输入文本
            
        返回:
            List[Dict[str, str]]: 对话列表，每项包含：
                - speaker: 说话人（如果能识别）
                - text: 对话内容
        """
        dialogues = []
        
        # 尝试所有对话模式
        for pattern in self.dialogue_patterns:
            matches = re.finditer(pattern, text)
            
            for match in matches:
                dialogue_text = match.group(1).strip()
                
                # 尝试查找说话人
                # 查找对话前的内容，看是否有"XXX说"、"XXX道"等
                start_pos = match.start()
                before_text = text[max(0, start_pos-20):start_pos]
                
                speaker = self._find_speaker(before_text)
                
                dialogues.append({
                    'speaker': speaker,
                    'text': dialogue_text
                })
        
        return dialogues
    
    def _find_speaker(self, before_text: str) -> Optional[str]:
        """
        从对话前的文本中查找说话人
        
        查找"XXX说"、"XXX道"、"XXX笑道"等模式。
        
        参数:
            before_text (str): 对话之前的文本
            
        返回:
            Optional[str]: 说话人名称，如果找不到返回None
        """
        # 匹配"XXX说"、"XXX道"等模式
        speaker_pattern = r'([^，。！？；：\s]{2,4})(说|道|问|答|笑道|冷笑|怒道|喝道)'
        match = re.search(speaker_pattern, before_text)
        
        if match:
            return match.group(1)
        
        return None
    
    def extract_actions(self, text: str) -> List[str]:
        """
        提取文本中的动作描述
        
        识别包含动作动词的句子或短语。
        
        参数:
            text (str): 输入文本
            
        返回:
            List[str]: 动作描述列表
        """
        actions = []
        
        # 按句子分割（使用中文标点）
        sentences = re.split(r'[。！？；]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 使用jieba分词
            words = jieba.lcut(sentence)
            
            # 检查句子中是否包含动作词
            has_action = any(word in self.action_words for word in words)
            
            if has_action:
                actions.append(sentence)
        
        return actions
    
    def extract_scene_description(self, text: str) -> str:
        """
        提取场景描述（环境描写）
        
        识别描述性的句子，通常包含环境、外观、氛围等描述。
        
        参数:
            text (str): 输入文本
            
        返回:
            str: 场景描述文本
        """
        # 移除对话（引号内容）
        clean_text = text
        for pattern in self.dialogue_patterns:
            clean_text = re.sub(pattern, '', clean_text)
        
        # 按句子分割
        sentences = re.split(r'[。！？]', clean_text)
        
        # 描述性词汇（形容词、方位词等）
        descriptive_words = {
            '高', '低', '大', '小', '长', '短', '宽', '窄', '明亮', '昏暗',
            '华丽', '简朴', '古老', '现代', '宁静', '喧嚣', '美丽', '丑陋',
            '东', '西', '南', '北', '左', '右', '上', '下', '前', '后',
            '远', '近', '深', '浅', '明', '暗', '红', '黄', '蓝', '绿'
        }
        
        # 收集包含描述性词汇的句子
        descriptions = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            words = jieba.lcut(sentence)
            # 检查是否包含描述性词汇
            has_description = any(word in descriptive_words for word in words)
            
            if has_description:
                descriptions.append(sentence)
        
        # 返回前3个描述性句子，合并成场景描述
        return '。'.join(descriptions[:3]) + ('。' if descriptions else '')
    
    def analyze_emotion(self, text: str) -> str:
        """
        分析文本的情感倾向
        
        基于情感词典，统计积极和消极词汇的出现次数，
        判断文本的整体情感倾向。
        
        参数:
            text (str): 输入文本
            
        返回:
            str: 情感类型 - 'positive'（积极）、'negative'（消极）或'neutral'（中性）
        """
        # 分词
        words = jieba.lcut(text)
        
        # 统计积极和消极词汇的数量
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # 判断情感倾向
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_emotion_intensity(self, text: str) -> float:
        """
        计算情感强度
        
        返回一个0-1之间的值，表示情感的强烈程度。
        
        参数:
            text (str): 输入文本
            
        返回:
            float: 情感强度值（0-1之间）
        """
        words = jieba.lcut(text)
        
        # 统计情感词汇总数
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        emotion_count = positive_count + negative_count
        
        # 计算情感词占比作为强度
        if len(words) == 0:
            return 0.0
        
        intensity = emotion_count / len(words)
        
        # 归一化到0-1范围（通常情感词占比不会超过0.3）
        return min(intensity * 3, 1.0)


class ChapterParser:
    """
    章节解析器
    
    负责解析小说的章节结构，提取章节标题和内容。
    """
    
    def __init__(self):
        """
        初始化章节解析器
        
        设置章节标题的正则模式
        """
        # 支持多种章节标题格式
        self.chapter_patterns = [
            r'第[一二三四五六七八九十百千万\d]+[章回节].*',  # 第X章
            r'第[一二三四五六七八九十百千万\d]+卷.*',        # 第X卷
            r'[一二三四五六七八九十百千万\d]+、.*',          # X、标题
            r'Chapter\s+\d+.*',                               # Chapter X
            r'Part\s+\d+.*',                                  # Part X
        ]
    
    def parse(self, text: str) -> List[Dict]:
        """
        解析小说章节
        
        参数:
            text (str): 完整的小说文本
            
        返回:
            List[Dict]: 章节列表，每个章节包含：
                - title: 章节标题
                - content: 章节内容
                - paragraphs: 段落列表
                - chapter_number: 章节序号
        """
        chapters = []
        
        # 尝试每种章节模式
        for pattern in self.chapter_patterns:
            parts = re.split(f'({pattern})', text)
            
            if len(parts) > 1:  # 找到了章节分隔
                chapters = self._parse_chapters(parts, pattern)
                break
        
        # 如果没有找到章节，将整个文本作为一个章节
        if not chapters and text.strip():
            chapters = [{
                'title': '全文',
                'content': text,
                'paragraphs': [p.strip() for p in text.split('\n') if p.strip()],
                'chapter_number': 1
            }]
        
        return chapters
    
    def _parse_chapters(self, parts: List[str], pattern: str) -> List[Dict]:
        """
        从分割的文本部分中解析章节
        
        参数:
            parts (List[str]): 分割后的文本部分
            pattern (str): 使用的正则模式
            
        返回:
            List[Dict]: 解析后的章节列表
        """
        chapters = []
        chapter_num = 1
        
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                title = parts[i].strip()
                content = parts[i + 1].strip()
                
                # 分割段落
                paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
                
                chapters.append({
                    'title': title,
                    'content': content,
                    'paragraphs': paragraphs,
                    'chapter_number': chapter_num
                })
                
                chapter_num += 1
        
        return chapters
    
    def extract_chapter_number(self, title: str) -> Optional[int]:
        """
        从章节标题中提取章节号
        
        参数:
            title (str): 章节标题
            
        返回:
            Optional[int]: 章节号，如果提取失败返回None
        """
        # 中文数字映射
        chinese_numbers = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '百': 100, '千': 1000, '万': 10000
        }
        
        # 尝试提取阿拉伯数字
        match = re.search(r'\d+', title)
        if match:
            return int(match.group())
        
        # 尝试提取中文数字（简单情况）
        match = re.search(r'第([一二三四五六七八九十百千万]+)[章回节卷]', title)
        if match:
            chinese_num = match.group(1)
            # 简单转换（仅支持一到十）
            if chinese_num in chinese_numbers:
                return chinese_numbers[chinese_num]
        
        return None
