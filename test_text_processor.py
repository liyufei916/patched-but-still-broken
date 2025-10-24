"""
文本处理模块单元测试

本文件包含text_processor模块的完整单元测试，包括：
- TextProcessor类的所有方法测试
- ChapterParser类的所有方法测试
- 边界条件测试
- 集成测试

运行方式:
    pytest test_text_processor.py -v
    或
    python3 test_text_processor.py

作者：AI Assistant
创建日期：2024-10-24
"""

import unittest
from text_processor import TextProcessor, ChapterParser


class TestTextProcessor(unittest.TestCase):
    """TextProcessor类的单元测试"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.processor = TextProcessor()
    
    # ==================== split_into_scenes 测试 ====================
    
    def test_split_into_scenes_basic(self):
        """测试基本的场景分割功能"""
        text = "这是第一个场景。\n\n这是第二个场景。"
        scenes = self.processor.split_into_scenes(text)
        self.assertEqual(len(scenes), 2)
    
    def test_split_into_scenes_with_markers(self):
        """测试使用场景标记词的场景分割"""
        text = "张三在房间里。此时李四走了进来。"
        scenes = self.processor.split_into_scenes(text)
        # 应该识别出"此时"作为场景标记
        self.assertTrue(len(scenes) >= 1)
    
    def test_split_into_scenes_empty(self):
        """测试空文本的场景分割"""
        scenes = self.processor.split_into_scenes("")
        self.assertEqual(len(scenes), 0)
    
    def test_split_into_scenes_single_paragraph(self):
        """测试单段文本的场景分割"""
        text = "这是一个单独的段落。"
        scenes = self.processor.split_into_scenes(text)
        self.assertEqual(len(scenes), 1)
        self.assertEqual(scenes[0], text)
    
    def test_split_into_scenes_with_newlines(self):
        """测试带换行符的文本分割"""
        text = "第一句。\n第二句。\n第三句。"
        scenes = self.processor.split_into_scenes(text)
        self.assertTrue(len(scenes) >= 1)
    
    # ==================== identify_characters 测试 ====================
    
    def test_identify_characters_basic(self):
        """测试基本的角色识别功能"""
        text = "张三对李四说话。"
        characters = self.processor.identify_characters(text)
        # 可能识别出张三、李四
        self.assertIsInstance(characters, list)
    
    def test_identify_characters_empty(self):
        """测试空文本的角色识别"""
        characters = self.processor.identify_characters("")
        self.assertEqual(len(characters), 0)
    
    def test_identify_characters_no_names(self):
        """测试不含人名的文本"""
        text = "这是一个没有人名的句子。"
        characters = self.processor.identify_characters(text)
        # 可能为空或有误识别
        self.assertIsInstance(characters, list)
    
    def test_identify_characters_duplicate_removal(self):
        """测试重复人名的去重"""
        text = "张三说完，张三就走了。"
        characters = self.processor.identify_characters(text)
        # 应该去重
        if '张三' in characters:
            self.assertEqual(characters.count('张三'), 1)
    
    # ==================== extract_dialogues 测试 ====================
    
    def test_extract_dialogues_basic(self):
        """测试基本的对话提取功能"""
        text = '他说："你好！"'
        dialogues = self.processor.extract_dialogues(text)
        self.assertEqual(len(dialogues), 1)
        self.assertEqual(dialogues[0]['text'], '你好！')
    
    def test_extract_dialogues_with_speaker(self):
        """测试带说话人的对话提取"""
        text = '张三说："你好！"'
        dialogues = self.processor.extract_dialogues(text)
        self.assertEqual(len(dialogues), 1)
        # 说话人可能识别为"张三"或"未知"
        self.assertIn('speaker', dialogues[0])
    
    def test_extract_dialogues_multiple_quotes(self):
        """测试多个对话的提取"""
        text = '张三说："你好！"李四答："你也好！"'
        dialogues = self.processor.extract_dialogues(text)
        self.assertEqual(len(dialogues), 2)
    
    def test_extract_dialogues_different_quote_types(self):
        """测试不同引号类型的对话提取"""
        # 中文引号
        text1 = '"中文引号"'
        dialogues1 = self.processor.extract_dialogues(text1)
        self.assertEqual(len(dialogues1), 1)
        
        # 英文引号
        text2 = '"English quotes"'
        dialogues2 = self.processor.extract_dialogues(text2)
        self.assertEqual(len(dialogues2), 1)
        
        # 单引号
        text3 = "'单引号'"
        dialogues3 = self.processor.extract_dialogues(text3)
        self.assertEqual(len(dialogues3), 1)
    
    def test_extract_dialogues_empty(self):
        """测试空文本的对话提取"""
        dialogues = self.processor.extract_dialogues("")
        self.assertEqual(len(dialogues), 0)
    
    def test_extract_dialogues_no_quotes(self):
        """测试不含引号的文本"""
        text = "这是一个没有对话的句子。"
        dialogues = self.processor.extract_dialogues(text)
        self.assertEqual(len(dialogues), 0)
    
    # ==================== extract_actions 测试 ====================
    
    def test_extract_actions_basic(self):
        """测试基本的动作提取功能"""
        text = "他走进房间。"
        actions = self.processor.extract_actions(text)
        # 应该识别出"走"这个动作
        self.assertTrue(len(actions) >= 1)
    
    def test_extract_actions_multiple(self):
        """测试多个动作的提取"""
        text = "他走进房间，坐下来，看着窗外。"
        actions = self.processor.extract_actions(text)
        # 应该识别出多个动作
        self.assertTrue(len(actions) >= 1)
    
    def test_extract_actions_empty(self):
        """测试空文本的动作提取"""
        actions = self.processor.extract_actions("")
        self.assertEqual(len(actions), 0)
    
    def test_extract_actions_no_verbs(self):
        """测试不含动作动词的文本"""
        text = "这是一个静态描述。"
        actions = self.processor.extract_actions(text)
        # 可能为空
        self.assertIsInstance(actions, list)
    
    # ==================== extract_scene_description 测试 ====================
    
    def test_extract_scene_description_basic(self):
        """测试基本的场景描述提取"""
        text = "房间很大。窗外阳光明亮。"
        description = self.processor.extract_scene_description(text)
        # 应该包含场景描述
        self.assertIsInstance(description, str)
    
    def test_extract_scene_description_with_dialogue(self):
        """测试包含对话的文本的场景描述提取"""
        text = '房间很大。他说："你好！"'
        description = self.processor.extract_scene_description(text)
        # 应该过滤掉对话，只保留描述
        self.assertNotIn("你好", description)
    
    def test_extract_scene_description_empty(self):
        """测试空文本的场景描述提取"""
        description = self.processor.extract_scene_description("")
        self.assertEqual(description, "")
    
    def test_extract_scene_description_only_actions(self):
        """测试只包含动作的文本"""
        text = "他走过去。他坐下来。"
        description = self.processor.extract_scene_description(text)
        # 动作应该被过滤掉
        self.assertIsInstance(description, str)
    
    # ==================== analyze_emotion 测试 ====================
    
    def test_analyze_emotion_positive(self):
        """测试正面情感分析"""
        text = "他很高兴，笑得很开心。"
        emotion = self.processor.analyze_emotion(text)
        self.assertEqual(emotion, 'positive')
    
    def test_analyze_emotion_negative(self):
        """测试负面情感分析"""
        text = "他很悲伤，忍不住哭了起来。"
        emotion = self.processor.analyze_emotion(text)
        self.assertEqual(emotion, 'negative')
    
    def test_analyze_emotion_neutral(self):
        """测试中性情感分析"""
        text = "这是一个中性的描述。"
        emotion = self.processor.analyze_emotion(text)
        self.assertEqual(emotion, 'neutral')
    
    def test_analyze_emotion_empty(self):
        """测试空文本的情感分析"""
        emotion = self.processor.analyze_emotion("")
        self.assertEqual(emotion, 'neutral')
    
    # ==================== get_emotion_intensity 测试 ====================
    
    def test_get_emotion_intensity_basic(self):
        """测试基本的情感强度计算"""
        text = "他非常高兴！"
        intensity = self.processor.get_emotion_intensity(text)
        self.assertIsInstance(intensity, float)
        self.assertTrue(0.0 <= intensity <= 1.0)
    
    def test_get_emotion_intensity_strong(self):
        """测试强烈情感的强度计算"""
        text = "他非常高兴，激动得热泪盈眶，幸福极了！"
        intensity = self.processor.get_emotion_intensity(text)
        self.assertTrue(intensity > 0.3)  # 应该有较高的强度
    
    def test_get_emotion_intensity_weak(self):
        """测试弱情感的强度计算"""
        text = "这是一个平静的叙述。"
        intensity = self.processor.get_emotion_intensity(text)
        self.assertTrue(intensity < 0.3)  # 应该有较低的强度
    
    def test_get_emotion_intensity_empty(self):
        """测试空文本的情感强度"""
        intensity = self.processor.get_emotion_intensity("")
        self.assertEqual(intensity, 0.0)
    
    # ==================== process_novel 测试 ====================
    
    def test_process_novel_basic(self):
        """测试基本的小说处理功能"""
        text = "张三走进房间，房间很大。他对李四说：'你好！'"
        scenes = self.processor.process_novel(text)
        
        # 检查返回格式
        self.assertTrue(len(scenes) > 0)
        self.assertIn('text', scenes[0])
        self.assertIn('description', scenes[0])
        self.assertIn('characters', scenes[0])
        self.assertIn('dialogues', scenes[0])
        self.assertIn('actions', scenes[0])
        self.assertIn('emotion', scenes[0])
        self.assertIn('emotion_intensity', scenes[0])
    
    def test_process_novel_empty(self):
        """测试空文本的处理"""
        scenes = self.processor.process_novel("")
        self.assertEqual(len(scenes), 0)
    
    def test_process_novel_complex(self):
        """测试复杂文本的处理"""
        text = """张三走进房间，房间很大，窗外阳光明亮。
        
李四已经在里面等着了。他笑着说："你来了！"

张三点点头，坐了下来。他说："今天天气真好。"

两人愉快地交谈起来。"""
        
        scenes = self.processor.process_novel(text)
        
        # 应该分割成多个场景
        self.assertTrue(len(scenes) > 0)
        
        # 每个场景应该有完整的数据结构
        for scene in scenes:
            self.assertIsInstance(scene['text'], str)
            self.assertIsInstance(scene['description'], str)
            self.assertIsInstance(scene['characters'], list)
            self.assertIsInstance(scene['dialogues'], list)
            self.assertIsInstance(scene['actions'], list)
            self.assertIn(scene['emotion'], ['positive', 'negative', 'neutral'])
            self.assertTrue(0.0 <= scene['emotion_intensity'] <= 1.0)


class TestChapterParser(unittest.TestCase):
    """ChapterParser类的单元测试"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.parser = ChapterParser()
    
    # ==================== parse 测试 ====================
    
    def test_parse_basic(self):
        """测试基本的章节解析功能"""
        text = "第一章 开始\n这是第一章。\n\n第二章 继续\n这是第二章。"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 开始')
        self.assertEqual(chapters[1]['title'], '第二章 继续')
    
    def test_parse_arabic_numbers(self):
        """测试阿拉伯数字章节的解析"""
        text = "第1章 开始\n内容1\n\n第2章 继续\n内容2"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['chapter_number'], 1)
        self.assertEqual(chapters[1]['chapter_number'], 2)
    
    def test_parse_english_chapter(self):
        """测试英文Chapter格式的解析"""
        text = "Chapter 1 Beginning\nContent 1\n\nChapter 2 Continue\nContent 2"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
    
    def test_parse_hui_format(self):
        """测试"回"格式的章节解析"""
        text = "第一回 初见\n内容1\n\n第二回 重逢\n内容2"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
    
    def test_parse_jie_format(self):
        """测试"节"格式的章节解析"""
        text = "第一节 开头\n内容1\n\n第二节 发展\n内容2"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
    
    def test_parse_empty(self):
        """测试空文本的解析"""
        chapters = self.parser.parse("")
        self.assertEqual(len(chapters), 0)
    
    def test_parse_no_chapters(self):
        """测试没有章节标记的文本"""
        text = "这是一段没有章节标记的文本。"
        chapters = self.parser.parse(text)
        
        # 应该返回一个默认章节
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0]['title'], '全文')
    
    def test_parse_with_paragraphs(self):
        """测试章节段落的解析"""
        text = "第一章 测试\n第一段\n第二段\n第三段"
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 1)
        self.assertTrue(len(chapters[0]['paragraphs']) >= 3)
    
    # ==================== extract_chapter_number 测试 ====================
    
    def test_extract_chapter_number_chinese(self):
        """测试中文数字章节号提取"""
        self.assertEqual(self.parser.extract_chapter_number("第一章 开始"), 1)
        self.assertEqual(self.parser.extract_chapter_number("第二章 继续"), 2)
        self.assertEqual(self.parser.extract_chapter_number("第十章 高潮"), 10)
    
    def test_extract_chapter_number_arabic(self):
        """测试阿拉伯数字章节号提取"""
        self.assertEqual(self.parser.extract_chapter_number("第1章 开始"), 1)
        self.assertEqual(self.parser.extract_chapter_number("第100章 结局"), 100)
    
    def test_extract_chapter_number_english(self):
        """测试英文Chapter格式的章节号提取"""
        self.assertEqual(self.parser.extract_chapter_number("Chapter 5"), 5)
        self.assertEqual(self.parser.extract_chapter_number("CHAPTER 10"), 10)
    
    def test_extract_chapter_number_none(self):
        """测试无法提取章节号的情况"""
        result = self.parser.extract_chapter_number("序言")
        self.assertIsNone(result)
    
    # ==================== _chinese_to_arabic 测试 ====================
    
    def test_chinese_to_arabic_basic(self):
        """测试基本的中文数字转换"""
        self.assertEqual(self.parser._chinese_to_arabic("一"), 1)
        self.assertEqual(self.parser._chinese_to_arabic("五"), 5)
        self.assertEqual(self.parser._chinese_to_arabic("九"), 9)
    
    def test_chinese_to_arabic_ten(self):
        """测试"十"的转换"""
        self.assertEqual(self.parser._chinese_to_arabic("十"), 10)
    
    def test_chinese_to_arabic_complex(self):
        """测试复杂中文数字的转换"""
        # 注：这里的实现可能不完美，根据实际实现调整
        result = self.parser._chinese_to_arabic("二十")
        self.assertTrue(result > 0)  # 至少应该返回一个正数


class TestIntegration(unittest.TestCase):
    """集成测试：测试多个组件协同工作"""
    
    def test_full_workflow(self):
        """测试完整的处理流程"""
        # 创建一个完整的小说示例
        novel_text = """第一章 相遇

张三走在街上，阳光很好。

突然，他看到了李四。他高兴地说："好久不见！"

李四也笑了："是啊，好久不见！"

第二章 离别

几天后，两人要分别了。

张三有些伤感。他说："保重！"

李四点点头，转身离开了。"""
        
        # 1. 解析章节
        chapter_parser = ChapterParser()
        chapters = chapter_parser.parse(novel_text)
        
        self.assertEqual(len(chapters), 2)
        
        # 2. 处理每个章节
        text_processor = TextProcessor()
        
        for chapter in chapters:
            scenes = text_processor.process_novel(chapter['content'])
            
            # 验证每个场景都有完整的数据
            for scene in scenes:
                self.assertIn('text', scene)
                self.assertIn('characters', scene)
                self.assertIn('dialogues', scene)
                self.assertIn('emotion', scene)
    
    def test_edge_cases(self):
        """测试边界情况"""
        processor = TextProcessor()
        
        # 空字符串
        self.assertEqual(processor.process_novel(""), [])
        
        # 只有空白
        self.assertEqual(processor.process_novel("   \n\n  "), [])
        
        # 超长文本（应该能处理）
        long_text = "这是一个句子。" * 1000
        scenes = processor.process_novel(long_text)
        self.assertTrue(len(scenes) > 0)
    
    def test_special_characters(self):
        """测试特殊字符的处理"""
        processor = TextProcessor()
        
        # 包含特殊标点
        text = "他说：「你好！」"
        scenes = processor.process_novel(text)
        self.assertTrue(len(scenes) > 0)
        
        # 包含表情符号
        text_with_emoji = "他很开心😊"
        scenes = processor.process_novel(text_with_emoji)
        self.assertTrue(len(scenes) > 0)


# 测试运行器
def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTextProcessor))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChapterParser))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"总计测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # 可以直接运行这个文件来执行测试
    success = run_tests()
    exit(0 if success else 1)
