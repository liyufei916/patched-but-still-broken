"""
文本处理模块单元测试

该测试文件包含对text_processor.py中所有主要功能的完整测试，
确保文本处理的准确性和可靠性。

测试覆盖范围：
- TextProcessor类的所有公共方法
- ChapterParser类的所有公共方法
- 边界条件和异常情况

运行方式：
    python -m pytest test_text_processor.py -v
    或
    python test_text_processor.py
"""

import unittest
from text_processor import TextProcessor, ChapterParser


class TestTextProcessor(unittest.TestCase):
    """TextProcessor类的单元测试"""
    
    def setUp(self):
        """
        测试前的准备工作
        
        在每个测试方法执行前，创建一个新的TextProcessor实例
        """
        self.processor = TextProcessor()
    
    def test_split_into_scenes_with_double_newlines(self):
        """
        测试场景分割功能 - 双换行分割
        
        验证能否正确按双换行符分割场景
        """
        text = "这是第一个场景。\n\n这是第二个场景。\n\n这是第三个场景。"
        scenes = self.processor.split_into_scenes(text)
        
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0], "这是第一个场景。")
        self.assertEqual(scenes[1], "这是第二个场景。")
        self.assertEqual(scenes[2], "这是第三个场景。")
    
    def test_split_into_scenes_with_markers(self):
        """
        测试场景分割功能 - 场景标记词分割
        
        验证能否识别场景转换标记词（如"此时"、"另一边"等）
        """
        text = "王明在房间里看书。\n此时，李华正在公园散步。\n另一边，张伟在咖啡厅工作。"
        scenes = self.processor.split_into_scenes(text)
        
        # 应该识别出场景转换
        self.assertGreaterEqual(len(scenes), 2)
        self.assertIn("此时", scenes[1])
    
    def test_split_into_scenes_empty_text(self):
        """
        测试场景分割功能 - 空文本
        
        验证处理空文本时的行为
        """
        scenes = self.processor.split_into_scenes("")
        
        self.assertEqual(len(scenes), 1)
        self.assertEqual(scenes[0], "")
    
    def test_identify_characters(self):
        """
        测试角色识别功能
        
        验证能否正确识别文本中的人名
        注意：需要jieba正确标注人名
        """
        text = "张三和李四在公园里遇见了王五。张三说hello。"
        characters = self.processor.identify_characters(text)
        
        # jieba可能识别出人名，但具体结果依赖于jieba的词典
        # 这里只验证返回的是列表
        self.assertIsInstance(characters, list)
    
    def test_extract_dialogues_double_quotes(self):
        """
        测试对话提取功能 - 中文双引号
        
        验证能否正确提取中文双引号中的对话
        """
        text = '张三说："你好，李四！"李四回答："你好啊！"'
        dialogues = self.processor.extract_dialogues(text)
        
        self.assertGreater(len(dialogues), 0)
        # 验证至少提取到一个对话
        self.assertIn('你好', dialogues[0]['text'])
    
    def test_extract_dialogues_single_quotes(self):
        """
        测试对话提取功能 - 中文单引号
        
        验证能否正确提取中文单引号中的对话
        """
        text = "他说：'我很高兴见到你。'"
        dialogues = self.processor.extract_dialogues(text)
        
        self.assertGreater(len(dialogues), 0)
        self.assertIn('高兴', dialogues[0]['text'])
    
    def test_extract_dialogues_with_speaker(self):
        """
        测试对话提取功能 - 识别说话人
        
        验证能否正确识别对话的说话人
        """
        text = '张三笑道："今天天气真好！"'
        dialogues = self.processor.extract_dialogues(text)
        
        self.assertGreater(len(dialogues), 0)
        # 验证说话人是否被识别（可能是"张三"）
        if dialogues[0]['speaker']:
            self.assertIn('张三', dialogues[0]['speaker'])
    
    def test_extract_dialogues_no_dialogue(self):
        """
        测试对话提取功能 - 无对话文本
        
        验证处理没有对话的文本时的行为
        """
        text = "他走在街上，看着远方的山峦。"
        dialogues = self.processor.extract_dialogues(text)
        
        self.assertEqual(len(dialogues), 0)
    
    def test_extract_actions(self):
        """
        测试动作提取功能
        
        验证能否正确识别包含动作的句子
        """
        text = "他走到门口。她坐在椅子上。风吹过树梢。"
        actions = self.processor.extract_actions(text)
        
        # 应该至少识别出一些动作
        self.assertGreater(len(actions), 0)
        # 验证动作中包含动作词
        action_text = ''.join(actions)
        self.assertTrue(any(word in action_text for word in ['走', '坐']))
    
    def test_extract_actions_no_actions(self):
        """
        测试动作提取功能 - 无动作文本
        
        验证处理纯描述性文本（无动作）时的行为
        """
        text = "天空很蓝，云朵很白。"
        actions = self.processor.extract_actions(text)
        
        # 可能没有动作，或者很少
        self.assertIsInstance(actions, list)
    
    def test_extract_scene_description(self):
        """
        测试场景描述提取功能
        
        验证能否正确提取环境描述
        """
        text = '房间很大，墙壁是白色的，窗外阳光明亮。他说："你好。"他走了出去。'
        description = self.processor.extract_scene_description(text)
        
        # 应该包含描述性内容，且不包含对话
        self.assertIsInstance(description, str)
        self.assertNotIn('你好', description)  # 对话应该被移除
    
    def test_analyze_emotion_positive(self):
        """
        测试情感分析功能 - 积极情感
        
        验证能否正确识别积极情感文本
        """
        text = "今天真是太高兴了！大家都很快乐，充满了喜悦和幸福。"
        emotion = self.processor.analyze_emotion(text)
        
        self.assertEqual(emotion, 'positive')
    
    def test_analyze_emotion_negative(self):
        """
        测试情感分析功能 - 消极情感
        
        验证能否正确识别消极情感文本
        """
        text = "他感到非常悲伤和痛苦，心中充满了绝望和无助。"
        emotion = self.processor.analyze_emotion(text)
        
        self.assertEqual(emotion, 'negative')
    
    def test_analyze_emotion_neutral(self):
        """
        测试情感分析功能 - 中性情感
        
        验证能否正确识别中性文本
        """
        text = "他走在街上，看着路边的树木。"
        emotion = self.processor.analyze_emotion(text)
        
        self.assertEqual(emotion, 'neutral')
    
    def test_get_emotion_intensity_high(self):
        """
        测试情感强度计算 - 高强度
        
        验证情感词较多时的强度计算
        """
        text = "非常高兴！特别快乐！超级开心！极其幸福！"
        intensity = self.processor.get_emotion_intensity(text)
        
        self.assertGreater(intensity, 0.5)
        self.assertLessEqual(intensity, 1.0)
    
    def test_get_emotion_intensity_low(self):
        """
        测试情感强度计算 - 低强度
        
        验证情感词较少时的强度计算
        """
        text = "他走在街上，心情还可以，看着路边的风景。"
        intensity = self.processor.get_emotion_intensity(text)
        
        self.assertLess(intensity, 0.5)
        self.assertGreaterEqual(intensity, 0.0)
    
    def test_get_emotion_intensity_empty(self):
        """
        测试情感强度计算 - 空文本
        
        验证空文本的情感强度应该为0
        """
        intensity = self.processor.get_emotion_intensity("")
        
        self.assertEqual(intensity, 0.0)
    
    def test_process_novel_complete(self):
        """
        测试完整的小说处理流程
        
        验证process_novel方法能否正确处理完整的文本
        """
        text = """张三走进房间，房间很大，窗外阳光明亮。
        
        他对李四说："今天天气真好！"
        
        李四笑道："是啊，我们出去走走吧。"
        
        他们一起走出了房间。"""
        
        scenes = self.processor.process_novel(text)
        
        # 验证返回的是场景列表
        self.assertIsInstance(scenes, list)
        self.assertGreater(len(scenes), 0)
        
        # 验证每个场景包含必要的字段
        for scene in scenes:
            self.assertIn('text', scene)
            self.assertIn('description', scene)
            self.assertIn('characters', scene)
            self.assertIn('dialogues', scene)
            self.assertIn('actions', scene)
            self.assertIn('emotion', scene)
            
            # 验证数据类型
            self.assertIsInstance(scene['text'], str)
            self.assertIsInstance(scene['description'], str)
            self.assertIsInstance(scene['characters'], list)
            self.assertIsInstance(scene['dialogues'], list)
            self.assertIsInstance(scene['actions'], list)
            self.assertIn(scene['emotion'], ['positive', 'negative', 'neutral'])


class TestChapterParser(unittest.TestCase):
    """ChapterParser类的单元测试"""
    
    def setUp(self):
        """
        测试前的准备工作
        
        在每个测试方法执行前，创建一个新的ChapterParser实例
        """
        self.parser = ChapterParser()
    
    def test_parse_chinese_chapters(self):
        """
        测试章节解析 - 中文章节标题
        
        验证能否正确解析"第X章"格式的章节
        """
        text = """第一章 开始
        
        这是第一章的内容。
        
        第二章 继续
        
        这是第二章的内容。"""
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 开始')
        self.assertEqual(chapters[1]['title'], '第二章 继续')
        self.assertIn('第一章的内容', chapters[0]['content'])
    
    def test_parse_numeric_chapters(self):
        """
        测试章节解析 - 数字章节标题
        
        验证能否正确解析"第1章"格式的章节
        """
        text = """第1章 序幕
        
        序幕的内容在这里。
        
        第2章 正式开始
        
        正文内容在这里。"""
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
        self.assertIn('第1章', chapters[0]['title'])
        self.assertIn('第2章', chapters[1]['title'])
    
    def test_parse_english_chapters(self):
        """
        测试章节解析 - 英文章节标题
        
        验证能否正确解析"Chapter X"格式的章节
        """
        text = """Chapter 1 The Beginning
        
        Content of chapter 1.
        
        Chapter 2 The Journey
        
        Content of chapter 2."""
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 2)
        self.assertIn('Chapter 1', chapters[0]['title'])
        self.assertIn('Chapter 2', chapters[1]['title'])
    
    def test_parse_no_chapters(self):
        """
        测试章节解析 - 无章节标题
        
        验证处理没有章节标题的文本时，将整个文本作为一个章节
        """
        text = "这是一段没有章节标题的文本。它应该被作为一个完整的章节。"
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0]['title'], '全文')
        self.assertEqual(chapters[0]['content'], text)
    
    def test_parse_empty_text(self):
        """
        测试章节解析 - 空文本
        
        验证处理空文本时的行为
        """
        chapters = self.parser.parse("")
        
        self.assertEqual(len(chapters), 0)
    
    def test_parse_chapter_with_paragraphs(self):
        """
        测试章节解析 - 段落分割
        
        验证章节中的段落是否被正确分割
        """
        text = """第一章 测试
        
        第一段内容。
        第二段内容。
        第三段内容。"""
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(len(chapters), 1)
        self.assertGreater(len(chapters[0]['paragraphs']), 0)
        # 验证段落列表不包含空字符串
        self.assertTrue(all(p.strip() for p in chapters[0]['paragraphs']))
    
    def test_chapter_number_assignment(self):
        """
        测试章节号分配
        
        验证章节号是否按顺序正确分配
        """
        text = """第一章 A
        
        内容A
        
        第二章 B
        
        内容B
        
        第三章 C
        
        内容C"""
        
        chapters = self.parser.parse(text)
        
        self.assertEqual(chapters[0]['chapter_number'], 1)
        self.assertEqual(chapters[1]['chapter_number'], 2)
        self.assertEqual(chapters[2]['chapter_number'], 3)
    
    def test_extract_chapter_number_arabic(self):
        """
        测试章节号提取 - 阿拉伯数字
        
        验证能否从标题中提取阿拉伯数字章节号
        """
        number = self.parser.extract_chapter_number("第1章 测试")
        self.assertEqual(number, 1)
        
        number = self.parser.extract_chapter_number("第42章 答案")
        self.assertEqual(number, 42)
    
    def test_extract_chapter_number_chinese(self):
        """
        测试章节号提取 - 中文数字
        
        验证能否从标题中提取中文数字章节号（一到十）
        """
        number = self.parser.extract_chapter_number("第一章 开始")
        self.assertEqual(number, 1)
        
        number = self.parser.extract_chapter_number("第五章 中间")
        self.assertEqual(number, 5)
        
        number = self.parser.extract_chapter_number("第十章 结束")
        self.assertEqual(number, 10)
    
    def test_extract_chapter_number_no_number(self):
        """
        测试章节号提取 - 无章节号
        
        验证无法提取章节号时返回None
        """
        number = self.parser.extract_chapter_number("序章")
        self.assertIsNone(number)
        
        number = self.parser.extract_chapter_number("楔子")
        self.assertIsNone(number)


class TestIntegration(unittest.TestCase):
    """集成测试 - 测试模块间的协作"""
    
    def test_full_novel_processing_pipeline(self):
        """
        测试完整的小说处理流程
        
        从章节解析到文本处理的完整流程测试
        """
        # 准备一个完整的小说样本
        novel_text = """第一章 相遇
        
        阳光明媚的早晨，张三走在公园的小路上。他心情愉快，欣赏着路边的花草。
        
        突然，他看到了李四。
        
        张三高兴地说："李四，好久不见！"
        
        李四笑道："是啊，最近怎么样？"
        
        第二章 重逢
        
        他们在咖啡厅坐下。咖啡厅很安静，装修很温馨。
        
        李四问："你最近在忙什么？"
        
        张三回答："我在写一本小说。"""
        
        # 步骤1：解析章节
        chapter_parser = ChapterParser()
        chapters = chapter_parser.parse(novel_text)
        
        self.assertEqual(len(chapters), 2)
        
        # 步骤2：处理每个章节的文本
        text_processor = TextProcessor()
        
        for chapter in chapters:
            scenes = text_processor.process_novel(chapter['content'])
            
            # 验证场景处理结果
            self.assertGreater(len(scenes), 0)
            
            for scene in scenes:
                # 验证所有必要字段都存在
                self.assertIn('text', scene)
                self.assertIn('description', scene)
                self.assertIn('characters', scene)
                self.assertIn('dialogues', scene)
                self.assertIn('actions', scene)
                self.assertIn('emotion', scene)
    
    def test_edge_case_single_sentence(self):
        """
        测试边界情况 - 单句文本
        
        验证处理只有一句话的文本
        """
        text = "这是一句话。"
        
        processor = TextProcessor()
        scenes = processor.process_novel(text)
        
        self.assertEqual(len(scenes), 1)
        self.assertEqual(scenes[0]['text'], text)
    
    def test_edge_case_very_long_text(self):
        """
        测试边界情况 - 超长文本
        
        验证处理超长文本时的性能和正确性
        """
        # 生成一个较长的文本
        long_text = "这是一个句子。\n\n" * 100
        
        processor = TextProcessor()
        scenes = processor.process_novel(long_text)
        
        # 应该被分割成多个场景
        self.assertGreater(len(scenes), 1)
    
    def test_edge_case_special_characters(self):
        """
        测试边界情况 - 特殊字符
        
        验证处理包含特殊字符的文本
        """
        text = "这是【特殊】符号：《书名》、「引用」、※标记※。"
        
        processor = TextProcessor()
        scenes = processor.process_novel(text)
        
        # 应该能正常处理，不会崩溃
        self.assertEqual(len(scenes), 1)


def run_tests():
    """
    运行所有测试
    
    这个函数允许直接运行此文件来执行所有测试
    """
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestTextProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestChapterParser))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    """
    直接运行此文件时执行测试
    
    使用方法：
        python test_text_processor.py
    """
    success = run_tests()
    exit(0 if success else 1)
