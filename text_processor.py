"""
文本处理模块 - 小说转动漫系统的核心文本分析组件

本模块提供了两个主要类：
1. TextProcessor: 用于处理小说文本，提取场景、角色、对话、动作等信息
2. ChapterParser: 用于解析章节结构，支持多种章节标题格式

主要功能：
- 场景分割：将长文本按段落、场景标记词等智能分割
- 角色识别：基于jieba分词识别人名
- 对话提取：提取引号内的对话内容，并识别说话人
- 动作识别：识别包含动作动词的句子
- 场景描述提取：提取环境和氛围描述
- 情感分析：分析文本情感倾向（正面/负面/中性）

作者：AI Assistant
创建日期：2024-10-24
"""

import re
import jieba
import jieba.posseg as pseg
from typing import List, Dict, Tuple, Optional


class TextProcessor:
    """
    文本处理器类
    
    用于处理小说文本，提取各种结构化信息，包括场景、角色、对话、动作和情感等。
    
    属性:
        scene_markers (list): 场景标记词列表，用于识别场景切换
        action_verbs (list): 动作动词列表，用于识别动作描述
        positive_words (set): 正面情感词集合
        negative_words (set): 负面情感词集合
    """
    
    def __init__(self):
        """初始化文本处理器，设置各种识别词典"""
        # 场景标记词：用于识别场景切换的关键词
        self.scene_markers = [
            '此时', '这时', '突然', '忽然', '后来', '接着', 
            '随后', '然后', '于是', '过了', '不久', '片刻',
            '第二天', '次日', '翌日', '当天', '傍晚', '黄昏',
            '清晨', '早上', '中午', '下午', '晚上', '深夜'
        ]
        
        # 动作动词：用于识别动作描述
        self.action_verbs = [
            '走', '跑', '跳', '站', '坐', '躺', '看', '听', '说', '笑',
            '哭', '喊', '叫', '转', '回', '来', '去', '拿', '放', '打',
            '推', '拉', '抓', '握', '指', '摇', '点', '抬', '低', '举'
        ]
        
        # 情感词典：用于情感分析
        self.positive_words = {
            '高兴', '快乐', '开心', '愉快', '欣喜', '兴奋', '激动',
            '喜悦', '欢乐', '幸福', '美好', '温暖', '舒适', '满意',
            '笑', '微笑', '欢笑', '明亮', '灿烂', '阳光'
        }
        
        self.negative_words = {
            '悲伤', '难过', '痛苦', '忧伤', '伤心', '沮丧', '失望',
            '绝望', '恐惧', '害怕', '担心', '焦虑', '愤怒', '生气',
            '哭', '流泪', '黑暗', '阴沉', '冷', '冰冷'
        }
    
    def split_into_scenes(self, text: str) -> List[str]:
        """
        将文本分割成多个场景
        
        分割策略：
        1. 按空行（段落）分割
        2. 识别场景标记词
        3. 检测时间变化
        
        参数:
            text (str): 待分割的文本
            
        返回:
            List[str]: 场景列表，每个元素是一个场景的文本
            
        示例:
            >>> processor = TextProcessor()
            >>> text = "张三走进房间。\\n\\n李四在等他。"
            >>> scenes = processor.split_into_scenes(text)
            >>> len(scenes)
            2
        """
        if not text or not text.strip():
            return []
        
        # 首先按段落分割（空行分隔）
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            # 如果没有空行，按单个换行符分割
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        scenes = []
        current_scene = []
        
        for para in paragraphs:
            # 检查是否包含场景标记词
            has_scene_marker = any(marker in para for marker in self.scene_markers)
            
            if has_scene_marker and current_scene:
                # 如果包含场景标记且已有当前场景，保存当前场景并开始新场景
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
        识别文本中的角色名称
        
        使用jieba分词的词性标注功能，识别人名（nr标记）
        
        参数:
            text (str): 待分析的文本
            
        返回:
            List[str]: 识别出的角色名称列表（去重）
            
        示例:
            >>> processor = TextProcessor()
            >>> text = "张三对李四说：'你好！'"
            >>> characters = processor.identify_characters(text)
            >>> '张三' in characters and '李四' in characters
            True
            
        注意:
            - 依赖jieba的词性标注，可能不够精确
            - 建议结合自定义词典提高准确性
        """
        if not text or not text.strip():
            return []
        
        # 使用jieba词性标注
        words = pseg.cut(text)
        
        # 提取人名（词性为nr的词）
        characters = []
        for word, flag in words:
            if flag == 'nr':  # nr表示人名
                characters.append(word)
        
        # 去重并保持顺序
        seen = set()
        unique_characters = []
        for char in characters:
            if char not in seen:
                seen.add(char)
                unique_characters.append(char)
        
        return unique_characters
    
    def extract_dialogues(self, text: str) -> List[Dict[str, str]]:
        """
        提取文本中的对话内容
        
        支持的对话格式：
        - "对话内容"
        - '对话内容'
        - "对话内容"
        - '对话内容'
        
        同时尝试识别说话人（通过"XXX说"、"XXX道"等模式）
        
        参数:
            text (str): 待分析的文本
            
        返回:
            List[Dict[str, str]]: 对话列表，每个元素包含：
                - speaker (str): 说话人，可能为"未知"
                - text (str): 对话内容
                
        示例:
            >>> processor = TextProcessor()
            >>> text = '张三说："你好！"'
            >>> dialogues = processor.extract_dialogues(text)
            >>> dialogues[0]['speaker']
            '张三'
            >>> dialogues[0]['text']
            '你好！'
        """
        if not text or not text.strip():
            return []
        
        dialogues = []
        
        # 支持多种引号格式
        quote_patterns = [
            r'"([^"]+)"',   # 中文双引号
            r"'([^']+)'",   # 中文单引号
            r'"([^"]+)"',   # 英文双引号
            r"'([^']+)'",   # 英文单引号
        ]
        
        # 提取所有对话
        all_quotes = []
        for pattern in quote_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                all_quotes.append({
                    'text': match.group(1),
                    'start': match.start(),
                    'end': match.end()
                })
        
        # 按位置排序
        all_quotes.sort(key=lambda x: x['start'])
        
        # 为每个对话识别说话人
        for quote in all_quotes:
            speaker = self._identify_speaker(text, quote['start'])
            dialogues.append({
                'speaker': speaker,
                'text': quote['text']
            })
        
        return dialogues
    
    def _identify_speaker(self, text: str, quote_start: int) -> str:
        """
        识别对话的说话人
        
        在引号前查找"XXX说"、"XXX道"、"XXX问"、"XXX答"等模式
        
        参数:
            text (str): 完整文本
            quote_start (int): 引号开始位置
            
        返回:
            str: 说话人名称，如果无法识别则返回"未知"
        """
        # 获取引号前的文本（最多往前取50个字符）
        prefix = text[max(0, quote_start - 50):quote_start]
        
        # 尝试匹配"XXX说"、"XXX道"等模式
        speaker_patterns = [
            r'([^，。！？\s]{2,4})[说道问答喊叫][:：]?$',
            r'([^，。！？\s]{2,4})[说道问答喊叫][着了][:：]?$',
        ]
        
        for pattern in speaker_patterns:
            match = re.search(pattern, prefix)
            if match:
                return match.group(1)
        
        return "未知"
    
    def extract_actions(self, text: str) -> List[str]:
        """
        提取文本中的动作描述
        
        识别包含动作动词的句子作为动作描述
        
        参数:
            text (str): 待分析的文本
            
        返回:
            List[str]: 动作描述列表
            
        示例:
            >>> processor = TextProcessor()
            >>> text = "他走进房间。房间很大。他坐下来。"
            >>> actions = processor.extract_actions(text)
            >>> len(actions) >= 2
            True
        """
        if not text or not text.strip():
            return []
        
        # 按句子分割（根据句号、问号、感叹号）
        sentences = re.split(r'[。！？\n]', text)
        
        actions = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 检查句子中是否包含动作动词
            for verb in self.action_verbs:
                if verb in sentence:
                    actions.append(sentence)
                    break  # 避免重复添加同一个句子
        
        return actions
    
    def extract_scene_description(self, text: str) -> str:
        """
        提取场景描述（环境、氛围等）
        
        提取不包含对话和动作的句子，这些通常是环境描述
        
        参数:
            text (str): 待分析的文本
            
        返回:
            str: 场景描述文本
            
        示例:
            >>> processor = TextProcessor()
            >>> text = "房间很大。窗外阳光明亮。他走进来。"
            >>> desc = processor.extract_scene_description(text)
            >>> "房间很大" in desc
            True
        """
        if not text or not text.strip():
            return ""
        
        # 移除对话内容 (移除所有引号中的内容)
        # 支持中文和英文引号
        text_without_dialogue = re.sub(r'"[^"]*"', '', text)  # 中文双引号
        text_without_dialogue = re.sub(r'"[^"]*"', '', text_without_dialogue)  # 英文双引号
        text_without_dialogue = re.sub(r"'[^']*'", '', text_without_dialogue)  # 中文单引号
        text_without_dialogue = re.sub(r"'[^']*'", '', text_without_dialogue)  # 英文单引号
        
        # 按句子分割
        sentences = re.split(r'[。！？\n]', text_without_dialogue)
        
        descriptions = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 检查是否是动作句（包含动作动词）
            is_action = any(verb in sentence for verb in self.action_verbs)
            
            if not is_action:
                # 不是动作句，可能是场景描述
                descriptions.append(sentence)
        
        return '。'.join(descriptions) if descriptions else ""
    
    def analyze_emotion(self, text: str) -> str:
        """
        分析文本的情感倾向
        
        基于情感词典进行简单的情感分析
        
        参数:
            text (str): 待分析的文本
            
        返回:
            str: 情感类别，可能的值：
                - 'positive': 正面情感
                - 'negative': 负面情感
                - 'neutral': 中性
                
        示例:
            >>> processor = TextProcessor()
            >>> text = "他很高兴，笑得很开心。"
            >>> processor.analyze_emotion(text)
            'positive'
        """
        if not text or not text.strip():
            return 'neutral'
        
        # 分词
        words = jieba.cut(text)
        
        # 统计正负面词汇
        positive_count = 0
        negative_count = 0
        
        for word in words:
            if word in self.positive_words:
                positive_count += 1
            elif word in self.negative_words:
                negative_count += 1
        
        # 判断情感
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_emotion_intensity(self, text: str) -> float:
        """
        计算情感强度
        
        返回0-1之间的值，表示情感的强烈程度
        
        参数:
            text (str): 待分析的文本
            
        返回:
            float: 情感强度，范围0.0-1.0
                - 0.0: 完全中性
                - 1.0: 极强情感
                
        示例:
            >>> processor = TextProcessor()
            >>> text = "他非常高兴，激动得热泪盈眶！"
            >>> intensity = processor.get_emotion_intensity(text)
            >>> intensity > 0.5
            True
        """
        if not text or not text.strip():
            return 0.0
        
        words = list(jieba.cut(text))
        if not words:
            return 0.0
        
        # 统计情感词数量
        emotion_word_count = 0
        for word in words:
            if word in self.positive_words or word in self.negative_words:
                emotion_word_count += 1
        
        # 计算情感词占比
        intensity = emotion_word_count / len(words)
        
        # 限制在0-1范围内
        return min(1.0, intensity * 3)  # 乘以3来增强效果
    
    def process_novel(self, text: str) -> List[Dict]:
        """
        处理小说文本，提取所有结构化信息
        
        这是主要的处理方法，整合了所有分析功能
        
        参数:
            text (str): 小说文本
            
        返回:
            List[Dict]: 场景数据列表，每个元素包含：
                - text (str): 场景原文
                - description (str): 场景描述
                - characters (List[str]): 角色列表
                - dialogues (List[Dict]): 对话列表
                - actions (List[str]): 动作列表
                - emotion (str): 情感类别
                - emotion_intensity (float): 情感强度
                
        示例:
            >>> processor = TextProcessor()
            >>> text = "张三走进房间，房间很大。他对李四说：'你好！'"
            >>> scenes = processor.process_novel(text)
            >>> len(scenes) > 0
            True
            >>> 'characters' in scenes[0]
            True
        """
        if not text or not text.strip():
            return []
        
        # 1. 分割场景
        scenes = self.split_into_scenes(text)
        
        # 2. 处理每个场景
        structured_data = []
        for scene in scenes:
            scene_data = {
                'text': scene,
                'description': self.extract_scene_description(scene),
                'characters': self.identify_characters(scene),
                'dialogues': self.extract_dialogues(scene),
                'actions': self.extract_actions(scene),
                'emotion': self.analyze_emotion(scene),
                'emotion_intensity': self.get_emotion_intensity(scene)
            }
            structured_data.append(scene_data)
        
        return structured_data


class ChapterParser:
    """
    章节解析器类
    
    用于解析小说的章节结构，支持多种章节标题格式
    
    支持的章节格式：
    - 第X章 标题
    - 第X回 标题
    - 第X节 标题
    - Chapter X 标题
    - 第一章、第二章等中文数字
    """
    
    def __init__(self):
        """初始化章节解析器"""
        # 中文数字映射
        self.chinese_numbers = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '百': 100, '千': 1000
        }
    
    def parse(self, text: str) -> List[Dict]:
        """
        解析小说章节
        
        参数:
            text (str): 小说全文
            
        返回:
            List[Dict]: 章节列表，每个元素包含：
                - title (str): 章节标题
                - content (str): 章节内容
                - paragraphs (List[str]): 段落列表
                - chapter_number (int): 章节序号（如果能识别）
                
        示例:
            >>> parser = ChapterParser()
            >>> text = "第一章 开始\\n这是第一章。\\n\\n第二章 继续\\n这是第二章。"
            >>> chapters = parser.parse(text)
            >>> len(chapters)
            2
        """
        if not text or not text.strip():
            return []
        
        # 章节标题模式（支持多种格式）
        chapter_patterns = [
            r'第[一二三四五六七八九十百千\d]+[章回节].*',
            r'Chapter\s+\d+.*',
            r'CHAPTER\s+\d+.*',
            r'第\d+章.*',
            r'第\d+回.*',
            r'第\d+节.*',
        ]
        
        # 合并所有模式
        combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)
        
        # 分割章节
        parts = re.split(f'({combined_pattern})', text, flags=re.IGNORECASE)
        
        chapters = []
        i = 0
        while i < len(parts):
            # 跳过空白部分
            if not parts[i].strip():
                i += 1
                continue
            
            # 检查是否是章节标题
            is_title = False
            for pattern in chapter_patterns:
                if re.match(pattern, parts[i].strip(), re.IGNORECASE):
                    is_title = True
                    break
            
            if is_title and i + 1 < len(parts):
                # 找到章节标题和内容
                title = parts[i].strip()
                i += 1
                
                # 收集内容，直到下一个章节标题
                content_parts = []
                while i < len(parts):
                    next_is_title = False
                    for pattern in chapter_patterns:
                        if re.match(pattern, parts[i].strip(), re.IGNORECASE):
                            next_is_title = True
                            break
                    
                    if next_is_title:
                        break
                    
                    if parts[i].strip():
                        content_parts.append(parts[i].strip())
                    i += 1
                
                content = '\n'.join(content_parts)
                paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
                
                chapter_data = {
                    'title': title,
                    'content': content,
                    'paragraphs': paragraphs,
                    'chapter_number': self.extract_chapter_number(title)
                }
                chapters.append(chapter_data)
            else:
                i += 1
        
        # 如果没有识别到章节，将全文作为单个章节
        if not chapters and text.strip():
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            chapters.append({
                'title': '全文',
                'content': text.strip(),
                'paragraphs': paragraphs,
                'chapter_number': 1
            })
        
        return chapters
    
    def extract_chapter_number(self, title: str) -> Optional[int]:
        """
        从章节标题中提取章节号
        
        参数:
            title (str): 章节标题
            
        返回:
            Optional[int]: 章节序号，如果无法提取则返回None
            
        示例:
            >>> parser = ChapterParser()
            >>> parser.extract_chapter_number("第一章 开始")
            1
            >>> parser.extract_chapter_number("Chapter 5")
            5
        """
        # 尝试提取阿拉伯数字
        arabic_match = re.search(r'\d+', title)
        if arabic_match:
            return int(arabic_match.group())
        
        # 尝试提取中文数字
        chinese_match = re.search(r'第([一二三四五六七八九十百千]+)[章回节]', title)
        if chinese_match:
            chinese_num = chinese_match.group(1)
            return self._chinese_to_arabic(chinese_num)
        
        return None
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """
        将中文数字转换为阿拉伯数字
        
        参数:
            chinese_num (str): 中文数字字符串
            
        返回:
            int: 对应的阿拉伯数字
            
        示例:
            >>> parser = ChapterParser()
            >>> parser._chinese_to_arabic("一")
            1
            >>> parser._chinese_to_arabic("十")
            10
        """
        result = 0
        temp = 0
        
        for char in chinese_num:
            if char in self.chinese_numbers:
                num = self.chinese_numbers[char]
                if num >= 10:
                    # 十、百、千
                    if temp == 0:
                        temp = 1
                    result += temp * num
                    temp = 0
                else:
                    # 个位数
                    temp = num
        
        # 加上最后的个位数
        result += temp
        
        return result if result > 0 else 1


# 使用示例
if __name__ == "__main__":
    # 创建文本处理器
    processor = TextProcessor()
    
    # 示例文本
    sample_text = """张三走进房间，房间很大，窗外阳光明亮。
    
李四已经在里面等着了。他笑着说："你来了！"

张三点点头，坐了下来。他说："今天天气真好。"

两人愉快地交谈起来。"""
    
    # 处理文本
    scenes = processor.process_novel(sample_text)
    
    # 打印结果
    for i, scene in enumerate(scenes, 1):
        print(f"\n=== 场景 {i} ===")
        print(f"文本: {scene['text'][:50]}...")
        print(f"角色: {scene['characters']}")
        print(f"对话数量: {len(scene['dialogues'])}")
        print(f"动作数量: {len(scene['actions'])}")
        print(f"情感: {scene['emotion']} (强度: {scene['emotion_intensity']:.2f})")
    
    # 测试章节解析
    chapter_parser = ChapterParser()
    chapter_text = """第一章 相遇
    
这是第一章的内容。

第二章 离别

这是第二章的内容。"""
    
    chapters = chapter_parser.parse(chapter_text)
    print(f"\n\n=== 章节解析 ===")
    for chapter in chapters:
        print(f"标题: {chapter['title']}")
        print(f"章节号: {chapter['chapter_number']}")
        print(f"段落数: {len(chapter['paragraphs'])}")
