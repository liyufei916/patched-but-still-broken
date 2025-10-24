"""
文本处理模块演示程序

本程序演示text_processor模块的各项功能，包括：
1. TextProcessor基本功能演示
2. ChapterParser基本功能演示
3. 完整处理流程演示
4. 统计报告生成

运行方式:
    python3 demo_text_processor.py

作者：AI Assistant
创建日期：2024-10-24
"""

from text_processor import TextProcessor, ChapterParser


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70 + "\n")


def demo_text_processor_basic():
    """演示TextProcessor的基本功能"""
    print_section("演示1: TextProcessor 基本功能")
    
    processor = TextProcessor()
    
    # 示例文本
    sample_text = """张三走进房间，房间很大，窗外阳光明亮。
    
李四已经在里面等着了。他笑着说："你来了！"

张三点点头，坐了下来。他说："今天天气真好。"

两人愉快地交谈起来。"""
    
    print("原始文本:")
    print("-" * 70)
    print(sample_text)
    print("-" * 70)
    
    # 1. 场景分割
    print("\n【1】场景分割:")
    scenes = processor.split_into_scenes(sample_text)
    for i, scene in enumerate(scenes, 1):
        print(f"\n场景 {i}:")
        print(f"  {scene[:50]}..." if len(scene) > 50 else f"  {scene}")
    
    # 2. 角色识别
    print("\n【2】角色识别:")
    characters = processor.identify_characters(sample_text)
    print(f"  识别到的角色: {characters if characters else '无'}")
    
    # 3. 对话提取
    print("\n【3】对话提取:")
    dialogues = processor.extract_dialogues(sample_text)
    for i, dialogue in enumerate(dialogues, 1):
        print(f"  对话 {i}:")
        print(f"    说话人: {dialogue['speaker']}")
        print(f"    内容: {dialogue['text']}")
    
    # 4. 动作识别
    print("\n【4】动作识别:")
    actions = processor.extract_actions(sample_text)
    for i, action in enumerate(actions, 1):
        print(f"  动作 {i}: {action}")
    
    # 5. 场景描述
    print("\n【5】场景描述:")
    description = processor.extract_scene_description(sample_text)
    print(f"  {description if description else '无明显场景描述'}")
    
    # 6. 情感分析
    print("\n【6】情感分析:")
    emotion = processor.analyze_emotion(sample_text)
    intensity = processor.get_emotion_intensity(sample_text)
    print(f"  情感类别: {emotion}")
    print(f"  情感强度: {intensity:.2f} (0-1范围)")


def demo_chapter_parser_basic():
    """演示ChapterParser的基本功能"""
    print_section("演示2: ChapterParser 基本功能")
    
    parser = ChapterParser()
    
    # 示例章节文本
    chapter_text = """第一章 相遇

春天的早晨，阳光明媚。

张三走在街上，心情很好。他刚刚完成了一个重要项目。

突然，他看到了多年未见的老朋友李四。

"李四！"他激动地喊道。

第二章 重逢

李四转过身来，看到张三也很惊喜。

"张三！好久不见！"李四走上前握住他的手。

两人找了一家咖啡馆，坐下来聊起了往事。

第三章 告别

时间过得很快，天色渐晚。

"我该走了。"张三站起身来。

"保持联系！"李四说。

两人挥手告别。"""
    
    print("原始文本:")
    print("-" * 70)
    print(chapter_text[:200] + "...\n")
    print("-" * 70)
    
    # 解析章节
    chapters = parser.parse(chapter_text)
    
    print(f"\n共识别到 {len(chapters)} 个章节:\n")
    
    for chapter in chapters:
        print(f"【章节 {chapter['chapter_number']}】")
        print(f"  标题: {chapter['title']}")
        print(f"  段落数: {len(chapter['paragraphs'])}")
        print(f"  内容预览: {chapter['content'][:50]}...")
        print()


def demo_full_workflow():
    """演示完整的处理流程"""
    print_section("演示3: 完整处理流程")
    
    # 创建解析器和处理器
    chapter_parser = ChapterParser()
    text_processor = TextProcessor()
    
    # 完整的小说示例
    novel_text = """第一章 开始

这是一个美好的早晨。

张三醒来，看着窗外的阳光，心情很好。他想："今天一定是个好日子。"

他起床，洗漱，准备开始新的一天。

第二章 挑战

中午时分，张三遇到了一个难题。

他皱着眉头，感到有些焦虑。"这可怎么办？"他自言自语道。

李四走过来问："需要帮助吗？"

"太好了！"张三高兴地说。

第三章 成功

在李四的帮助下，问题很快解决了。

张三激动地说："谢谢你！你真是帮了大忙！"

两人相视而笑。夕阳西下，他们并肩走在回家的路上。"""
    
    print("正在处理小说...")
    print("-" * 70)
    
    # 第一步：解析章节
    chapters = chapter_parser.parse(novel_text)
    print(f"\n✓ 解析到 {len(chapters)} 个章节")
    
    # 第二步：处理每个章节
    all_results = []
    
    for i, chapter in enumerate(chapters, 1):
        print(f"\n处理章节 {i}: {chapter['title']}")
        print("-" * 70)
        
        # 处理章节内容
        scenes = text_processor.process_novel(chapter['content'])
        
        chapter_result = {
            'chapter': chapter,
            'scenes': scenes
        }
        all_results.append(chapter_result)
        
        # 打印场景信息
        for j, scene in enumerate(scenes, 1):
            print(f"\n  场景 {j}:")
            print(f"    文本长度: {len(scene['text'])} 字符")
            print(f"    角色: {', '.join(scene['characters']) if scene['characters'] else '无'}")
            print(f"    对话数: {len(scene['dialogues'])}")
            print(f"    动作数: {len(scene['actions'])}")
            print(f"    情感: {scene['emotion']} (强度: {scene['emotion_intensity']:.2f})")
            
            # 显示对话内容
            if scene['dialogues']:
                print(f"    对话内容:")
                for dialogue in scene['dialogues']:
                    print(f"      - {dialogue['speaker']}: {dialogue['text'][:30]}...")
    
    # 第三步：生成统计报告
    print("\n" + "=" * 70)
    print(" 统计报告")
    print("=" * 70)
    
    generate_statistics_report(all_results)


def generate_statistics_report(results):
    """生成统计报告"""
    
    # 统计各种数据
    total_chapters = len(results)
    total_scenes = sum(len(r['scenes']) for r in results)
    total_characters = set()
    total_dialogues = 0
    total_actions = 0
    
    emotion_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for result in results:
        for scene in result['scenes']:
            total_characters.update(scene['characters'])
            total_dialogues += len(scene['dialogues'])
            total_actions += len(scene['actions'])
            emotion_counts[scene['emotion']] += 1
    
    # 打印报告
    print(f"\n【基本信息】")
    print(f"  章节数: {total_chapters}")
    print(f"  场景数: {total_scenes}")
    print(f"  角色数: {len(total_characters)}")
    print(f"  角色列表: {', '.join(total_characters) if total_characters else '无'}")
    
    print(f"\n【内容统计】")
    print(f"  对话总数: {total_dialogues}")
    print(f"  动作总数: {total_actions}")
    print(f"  平均每场景对话数: {total_dialogues/total_scenes:.1f}")
    print(f"  平均每场景动作数: {total_actions/total_scenes:.1f}")
    
    print(f"\n【情感分析】")
    print(f"  正面场景: {emotion_counts['positive']} ({emotion_counts['positive']/total_scenes*100:.1f}%)")
    print(f"  负面场景: {emotion_counts['negative']} ({emotion_counts['negative']/total_scenes*100:.1f}%)")
    print(f"  中性场景: {emotion_counts['neutral']} ({emotion_counts['neutral']/total_scenes*100:.1f}%)")
    
    # 章节详情
    print(f"\n【章节详情】")
    for i, result in enumerate(results, 1):
        chapter = result['chapter']
        scenes = result['scenes']
        
        # 统计该章节的情感
        chapter_emotions = [s['emotion'] for s in scenes]
        dominant_emotion = max(set(chapter_emotions), key=chapter_emotions.count)
        
        print(f"\n  章节 {i}: {chapter['title']}")
        print(f"    场景数: {len(scenes)}")
        print(f"    主要情感: {dominant_emotion}")
        print(f"    平均情感强度: {sum(s['emotion_intensity'] for s in scenes)/len(scenes):.2f}")


def demo_advanced_features():
    """演示高级功能"""
    print_section("演示4: 高级功能")
    
    processor = TextProcessor()
    
    # 测试不同类型的文本
    
    print("【测试1】处理纯对话文本:")
    dialogue_text = '''张三问："你吃饭了吗？"
李四答："还没有。"
张三说："那我们一起去吧。"'''
    
    result = processor.process_novel(dialogue_text)
    print(f"  识别到 {len(result[0]['dialogues'])} 段对话")
    for d in result[0]['dialogues']:
        print(f"    {d['speaker']}: {d['text']}")
    
    print("\n【测试2】处理纯描写文本:")
    description_text = """房间很大，装修精美。墙上挂着几幅画。
窗外可以看到美丽的花园。阳光透过窗帘洒进来，温暖而明亮。"""
    
    result = processor.process_novel(description_text)
    print(f"  场景描述: {result[0]['description'][:50]}...")
    print(f"  情感: {result[0]['emotion']}")
    
    print("\n【测试3】处理动作密集文本:")
    action_text = """他跑进房间，抓起钥匙，转身就冲了出去。
他跳上车，发动引擎，踩下油门。
车子飞快地驶向远方。"""
    
    result = processor.process_novel(action_text)
    print(f"  识别到 {len(result[0]['actions'])} 个动作:")
    for action in result[0]['actions'][:3]:
        print(f"    - {action}")
    
    print("\n【测试4】情感对比:")
    texts = {
        "快乐文本": "他非常高兴，笑得合不拢嘴。阳光灿烂，一切都很美好。",
        "悲伤文本": "他非常难过，忍不住哭了。天空阴沉，一切都很糟糕。",
        "中性文本": "他走进房间，看了看四周，然后坐了下来。"
    }
    
    for label, text in texts.items():
        result = processor.process_novel(text)
        emotion = result[0]['emotion']
        intensity = result[0]['emotion_intensity']
        print(f"  {label}: {emotion} (强度: {intensity:.2f})")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print(" 文本处理模块演示程序")
    print(" Text Processor Demo")
    print("=" * 70)
    
    try:
        # 运行所有演示
        demo_text_processor_basic()
        demo_chapter_parser_basic()
        demo_full_workflow()
        demo_advanced_features()
        
        print("\n" + "=" * 70)
        print(" 演示完成！")
        print("=" * 70)
        print("\n提示: 您可以查看源代码了解更多使用方法")
        print("      或运行 python3 test_text_processor.py 执行单元测试\n")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
