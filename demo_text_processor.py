"""
文本处理模块使用示例

该脚本演示如何使用text_processor模块处理小说文本。

注意：运行此脚本前，请确保已安装所需依赖：
    pip install jieba

使用方法：
    python3 demo_text_processor.py
"""

# 尝试导入模块（如果jieba未安装会提示）
try:
    from text_processor import TextProcessor, ChapterParser
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"警告：无法导入模块 - {e}")
    print("请先安装依赖：pip install -r requirements.txt")
    MODULES_AVAILABLE = False


def demo_text_processor():
    """演示TextProcessor的基本功能"""
    
    if not MODULES_AVAILABLE:
        print("\n❌ 模块未正确导入，无法运行演示")
        return
    
    print("=" * 60)
    print("文本处理模块演示")
    print("=" * 60)
    
    # 示例小说文本
    sample_text = """张三走进房间，房间很大，墙壁洁白，窗外阳光明亮。

他心情愉快，欣赏着房间的装饰。

此时，李四推门而入。

张三高兴地说："李四，你来了！今天天气真好。"

李四笑道："是啊，我们出去走走吧。"

他们一起走出了房间，来到花园。花园里花香四溢，蝴蝶飞舞。"""
    
    # 创建文本处理器
    processor = TextProcessor()
    
    print("\n📖 原始文本：")
    print("-" * 60)
    print(sample_text)
    print("-" * 60)
    
    # 处理文本
    print("\n🔍 开始处理文本...\n")
    scenes = processor.process_novel(sample_text)
    
    # 显示处理结果
    print(f"✅ 共识别出 {len(scenes)} 个场景\n")
    
    for idx, scene in enumerate(scenes, 1):
        print(f"{'=' * 60}")
        print(f"场景 {idx}")
        print(f"{'=' * 60}")
        
        print(f"\n📝 原始文本:")
        print(f"   {scene['text'][:100]}..." if len(scene['text']) > 100 else f"   {scene['text']}")
        
        print(f"\n🎬 场景描述:")
        print(f"   {scene['description'][:100]}..." if scene['description'] and len(scene['description']) > 100 else f"   {scene['description'] or '(无)'}")
        
        print(f"\n👥 出现的角色: {', '.join(scene['characters']) if scene['characters'] else '(未识别到)'}")
        
        print(f"\n💬 对话内容:")
        if scene['dialogues']:
            for dialogue in scene['dialogues']:
                speaker = dialogue['speaker'] or '(未知)'
                print(f"   {speaker}: {dialogue['text']}")
        else:
            print("   (无对话)")
        
        print(f"\n🎭 动作描述:")
        if scene['actions']:
            for action in scene['actions'][:3]:  # 只显示前3个
                print(f"   - {action}")
        else:
            print("   (无明显动作)")
        
        print(f"\n😊 情感倾向: {scene['emotion']}")
        print()


def demo_chapter_parser():
    """演示ChapterParser的基本功能"""
    
    if not MODULES_AVAILABLE:
        print("\n❌ 模块未正确导入，无法运行演示")
        return
    
    print("\n" + "=" * 60)
    print("章节解析模块演示")
    print("=" * 60)
    
    # 示例小说（带章节标题）
    sample_novel = """第一章 相遇

阳光明媚的早晨，张三走在公园的小路上。

他心情愉快，欣赏着路边的花草。

第二章 重逢

几天后，张三再次来到公园。

这次他遇到了李四。

第三章 友谊

从那以后，他们成了好朋友。"""
    
    # 创建章节解析器
    parser = ChapterParser()
    
    print("\n📚 原始小说文本：")
    print("-" * 60)
    print(sample_novel)
    print("-" * 60)
    
    # 解析章节
    print("\n🔍 开始解析章节...\n")
    chapters = parser.parse(sample_novel)
    
    # 显示解析结果
    print(f"✅ 共解析出 {len(chapters)} 个章节\n")
    
    for chapter in chapters:
        print(f"{'=' * 60}")
        print(f"📖 {chapter['title']} (第{chapter['chapter_number']}章)")
        print(f"{'=' * 60}")
        
        print(f"\n内容长度: {len(chapter['content'])} 字符")
        print(f"段落数量: {len(chapter['paragraphs'])} 段")
        
        print(f"\n前100字:")
        content_preview = chapter['content'][:100]
        print(f"   {content_preview}...")
        print()
        
        # 提取章节号
        chapter_num = parser.extract_chapter_number(chapter['title'])
        if chapter_num:
            print(f"章节号: {chapter_num}\n")


def demo_integration():
    """演示完整的处理流程"""
    
    if not MODULES_AVAILABLE:
        print("\n❌ 模块未正确导入，无法运行演示")
        return
    
    print("\n" + "=" * 60)
    print("完整处理流程演示")
    print("=" * 60)
    
    # 完整的小说示例
    full_novel = """第一章 清晨

阳光透过窗帘洒进房间，温暖而明亮。

张三醒来，伸了个懒腰。他心情愉快地说："今天又是美好的一天！"

他起床，洗漱，准备开始新的一天。

第二章 相遇

公园里，鸟儿在歌唱，花儿在绽放。

张三正在散步，突然看到了李四。

张三惊喜地喊道："李四！好久不见！"

李四转过身，露出了笑容："张三！真巧啊！"""
    
    print("\n📚 示例小说:")
    print("-" * 60)
    print(full_novel[:200] + "...")
    print("-" * 60)
    
    # 步骤1：解析章节
    print("\n【步骤1】解析章节结构...")
    chapter_parser = ChapterParser()
    chapters = chapter_parser.parse(full_novel)
    print(f"✅ 解析出 {len(chapters)} 个章节")
    
    # 步骤2：处理每个章节
    print("\n【步骤2】处理每个章节的文本...")
    text_processor = TextProcessor()
    
    all_results = []
    for chapter in chapters:
        print(f"\n处理章节: {chapter['title']}")
        scenes = text_processor.process_novel(chapter['content'])
        print(f"  - 识别出 {len(scenes)} 个场景")
        
        all_results.append({
            'chapter': chapter,
            'scenes': scenes
        })
    
    # 步骤3：生成统计报告
    print("\n【步骤3】生成统计报告...")
    print("\n" + "=" * 60)
    print("📊 处理结果统计")
    print("=" * 60)
    
    total_scenes = sum(len(result['scenes']) for result in all_results)
    total_dialogues = sum(
        len(scene['dialogues']) 
        for result in all_results 
        for scene in result['scenes']
    )
    total_actions = sum(
        len(scene['actions']) 
        for result in all_results 
        for scene in result['scenes']
    )
    
    print(f"\n总章节数: {len(chapters)}")
    print(f"总场景数: {total_scenes}")
    print(f"总对话数: {total_dialogues}")
    print(f"总动作数: {total_actions}")
    
    # 情感分布
    emotions = [
        scene['emotion']
        for result in all_results
        for scene in result['scenes']
    ]
    from collections import Counter
    emotion_count = Counter(emotions)
    
    print(f"\n情感分布:")
    print(f"  - 积极: {emotion_count.get('positive', 0)} 个场景")
    print(f"  - 消极: {emotion_count.get('negative', 0)} 个场景")
    print(f"  - 中性: {emotion_count.get('neutral', 0)} 个场景")
    
    print("\n✅ 处理完成！")


def main():
    """主函数"""
    
    print("\n" + "🌟" * 30)
    print("欢迎使用文本处理模块演示程序")
    print("🌟" * 30)
    
    if not MODULES_AVAILABLE:
        print("\n⚠️  依赖项未安装")
        print("\n请运行以下命令安装依赖：")
        print("    pip install -r requirements.txt")
        print("\n或者单独安装jieba：")
        print("    pip install jieba")
        return
    
    # 运行演示
    demo_text_processor()
    input("\n按回车继续章节解析演示...")
    
    demo_chapter_parser()
    input("\n按回车继续完整流程演示...")
    
    demo_integration()
    
    print("\n" + "=" * 60)
    print("演示结束，谢谢使用！")
    print("=" * 60)
    print("\n💡 提示：")
    print("  - 查看 text_processor.py 了解详细实现")
    print("  - 查看 test_text_processor.py 了解完整测试")
    print("  - 运行测试：python3 test_text_processor.py")
    print()


if __name__ == '__main__':
    main()
