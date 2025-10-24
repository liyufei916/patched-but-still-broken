# 文本处理模块文档

## 📚 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [核心类](#核心类)
  - [TextProcessor](#textprocessor)
  - [ChapterParser](#chapterparser)
- [详细API文档](#详细api文档)
- [使用示例](#使用示例)
- [测试](#测试)
- [性能考虑](#性能考虑)
- [注意事项](#注意事项)

---

## 概述

文本处理模块是小说转动漫系统的核心组件，负责将原始小说文本转换为结构化数据，为后续的图像生成、语音合成等模块提供基础。

### 主要功能

- ✅ **场景分割**: 智能识别场景切换点，将长文本分割成独立场景
- ✅ **角色识别**: 基于NLP技术识别文本中的角色
- ✅ **对话提取**: 提取引号内的对话内容，并尝试识别说话人
- ✅ **动作识别**: 识别包含动作动词的句子
- ✅ **场景描述**: 提取环境和氛围描述
- ✅ **情感分析**: 分析文本的情感倾向和强度
- ✅ **章节解析**: 支持多种章节标题格式的解析

### 技术特点

- 🚀 纯Python实现，无需外部服务
- 📦 依赖少，易于部署
- 🧪 完整的单元测试覆盖
- 📝 详细的中文注释
- 🎯 针对中文小说优化

---

## 快速开始

### 安装依赖

```bash
pip install jieba
pip install pytest  # 如果需要运行测试
```

### 基本使用

```python
from text_processor import TextProcessor

# 创建处理器
processor = TextProcessor()

# 处理小说文本
text = """张三走进房间，房间很大。
他对李四说："你好！"""

# 一键处理，获取所有结构化信息
scenes = processor.process_novel(text)

# 查看结果
for scene in scenes:
    print(f"角色: {scene['characters']}")
    print(f"对话: {scene['dialogues']}")
    print(f"情感: {scene['emotion']}")
```

### 运行演示

```bash
# 查看功能演示
python3 demo_text_processor.py

# 运行单元测试
python3 test_text_processor.py
# 或
pytest test_text_processor.py -v
```

---

## 核心类

### TextProcessor

文本处理器类，提供全面的文本分析功能。

#### 初始化

```python
processor = TextProcessor()
```

初始化时会自动加载：
- 场景标记词词典
- 动作动词词典
- 情感词词典

#### 主要方法概览

| 方法 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `process_novel()` | 一站式处理 | 文本字符串 | 场景数据列表 |
| `split_into_scenes()` | 场景分割 | 文本字符串 | 场景列表 |
| `identify_characters()` | 角色识别 | 文本字符串 | 角色名称列表 |
| `extract_dialogues()` | 对话提取 | 文本字符串 | 对话数据列表 |
| `extract_actions()` | 动作识别 | 文本字符串 | 动作描述列表 |
| `extract_scene_description()` | 场景描述提取 | 文本字符串 | 描述文本 |
| `analyze_emotion()` | 情感分析 | 文本字符串 | 情感类别 |
| `get_emotion_intensity()` | 情感强度计算 | 文本字符串 | 强度值(0-1) |

### ChapterParser

章节解析器类，用于解析小说的章节结构。

#### 初始化

```python
parser = ChapterParser()
```

#### 主要方法概览

| 方法 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `parse()` | 解析章节 | 小说全文 | 章节数据列表 |
| `extract_chapter_number()` | 提取章节号 | 章节标题 | 章节序号 |

---

## 详细API文档

### TextProcessor.process_novel()

**功能**: 处理小说文本，提取所有结构化信息（推荐使用的主要方法）

**参数**:
- `text` (str): 小说文本

**返回**: `List[Dict]` - 场景数据列表，每个元素包含：
- `text` (str): 场景原文
- `description` (str): 场景描述（环境、氛围等）
- `characters` (List[str]): 角色列表
- `dialogues` (List[Dict]): 对话列表
  - `speaker` (str): 说话人
  - `text` (str): 对话内容
- `actions` (List[str]): 动作列表
- `emotion` (str): 情感类别 ('positive', 'negative', 'neutral')
- `emotion_intensity` (float): 情感强度 (0.0-1.0)

**示例**:

```python
processor = TextProcessor()
text = """张三走进房间，房间很大，窗外阳光明亮。

李四在等他。他笑着说："你来了！"

张三坐下来，说："今天天气真好。"""

scenes = processor.process_novel(text)

print(f"共{len(scenes)}个场景")
for i, scene in enumerate(scenes, 1):
    print(f"\n场景 {i}:")
    print(f"  角色: {scene['characters']}")
    print(f"  对话数: {len(scene['dialogues'])}")
    print(f"  情感: {scene['emotion']}")
```

---

### TextProcessor.split_into_scenes()

**功能**: 将文本分割成多个场景

**分割策略**:
1. 按空行（段落）分割
2. 识别场景标记词（如"此时"、"突然"、"第二天"等）
3. 检测时间变化

**参数**:
- `text` (str): 待分割的文本

**返回**: `List[str]` - 场景列表

**示例**:

```python
text = "张三在房间里。\n\n此时李四走了进来。"
scenes = processor.split_into_scenes(text)
# scenes = ['张三在房间里。', '此时李四走了进来。']
```

---

### TextProcessor.identify_characters()

**功能**: 识别文本中的角色名称

**识别方法**: 使用jieba分词的词性标注，识别人名（nr标记）

**参数**:
- `text` (str): 待分析的文本

**返回**: `List[str]` - 角色名称列表（已去重）

**注意**: 
- 依赖jieba的词性标注，准确性有限
- 建议使用jieba的自定义词典提高准确性

**示例**:

```python
text = "张三对李四说：'你好！'"
characters = processor.identify_characters(text)
# characters = ['张三', '李四']

# 如需提高准确性，可添加自定义词典
import jieba
jieba.load_userdict("custom_names.txt")
```

---

### TextProcessor.extract_dialogues()

**功能**: 提取文本中的对话内容

**支持的引号格式**:
- 中文双引号: `"对话"`
- 中文单引号: `'对话'`
- 英文双引号: `"对话"`
- 英文单引号: `'对话'`

**说话人识别模式**:
- `XXX说："..."`
- `XXX道："..."`
- `XXX问："..."`
- `XXX答："..."`

**参数**:
- `text` (str): 待分析的文本

**返回**: `List[Dict[str, str]]` - 对话列表，每个元素包含：
- `speaker` (str): 说话人（可能为"未知"）
- `text` (str): 对话内容

**示例**:

```python
text = '张三说："你好！"李四答："你也好！"'
dialogues = processor.extract_dialogues(text)

for d in dialogues:
    print(f"{d['speaker']}: {d['text']}")
# 输出:
# 张三: 你好！
# 李四: 你也好！
```

---

### TextProcessor.extract_actions()

**功能**: 提取文本中的动作描述

**识别方法**: 识别包含预定义动作动词的句子

**动作动词列表**: 走、跑、跳、站、坐、躺、看、听、说、笑、哭等

**参数**:
- `text` (str): 待分析的文本

**返回**: `List[str]` - 动作描述列表

**示例**:

```python
text = "他走进房间。房间很大。他坐下来。"
actions = processor.extract_actions(text)
# actions = ['他走进房间', '他坐下来']
```

---

### TextProcessor.extract_scene_description()

**功能**: 提取场景描述（环境、氛围等）

**提取策略**: 
1. 移除对话内容
2. 过滤包含动作动词的句子
3. 保留描述性句子

**参数**:
- `text` (str): 待分析的文本

**返回**: `str` - 场景描述文本

**示例**:

```python
text = "房间很大。窗外阳光明亮。他走进来。"
desc = processor.extract_scene_description(text)
# desc = '房间很大。窗外阳光明亮'
```

---

### TextProcessor.analyze_emotion()

**功能**: 分析文本的情感倾向

**分析方法**: 基于情感词典统计正负面词汇

**参数**:
- `text` (str): 待分析的文本

**返回**: `str` - 情感类别
- `'positive'`: 正面情感
- `'negative'`: 负面情感
- `'neutral'`: 中性

**示例**:

```python
text1 = "他很高兴，笑得很开心。"
emotion1 = processor.analyze_emotion(text1)
# emotion1 = 'positive'

text2 = "他很悲伤，忍不住哭了起来。"
emotion2 = processor.analyze_emotion(text2)
# emotion2 = 'negative'
```

---

### TextProcessor.get_emotion_intensity()

**功能**: 计算情感强度

**计算方法**: 情感词数量 / 总词数 × 3（限制在0-1范围）

**参数**:
- `text` (str): 待分析的文本

**返回**: `float` - 情感强度 (0.0-1.0)
- 0.0: 完全中性
- 1.0: 极强情感

**示例**:

```python
text = "他非常高兴，激动得热泪盈眶！"
intensity = processor.get_emotion_intensity(text)
# intensity ≈ 0.6-0.8
```

---

### ChapterParser.parse()

**功能**: 解析小说章节

**支持的章节格式**:
- `第X章 标题`
- `第X回 标题`
- `第X节 标题`
- `Chapter X 标题`
- 中文数字（第一章、第二章等）
- 阿拉伯数字（第1章、第2章等）

**参数**:
- `text` (str): 小说全文

**返回**: `List[Dict]` - 章节列表，每个元素包含：
- `title` (str): 章节标题
- `content` (str): 章节内容
- `paragraphs` (List[str]): 段落列表
- `chapter_number` (Optional[int]): 章节序号

**示例**:

```python
parser = ChapterParser()

text = """第一章 开始
这是第一章。

第二章 继续
这是第二章。"""

chapters = parser.parse(text)

for chapter in chapters:
    print(f"{chapter['title']}: {chapter['chapter_number']}")
# 输出:
# 第一章 开始: 1
# 第二章 继续: 2
```

---

### ChapterParser.extract_chapter_number()

**功能**: 从章节标题中提取章节号

**支持格式**:
- 阿拉伯数字: "第1章"、"Chapter 5"
- 中文数字: "第一章"、"第十章"

**参数**:
- `title` (str): 章节标题

**返回**: `Optional[int]` - 章节序号，无法提取则返回None

**示例**:

```python
parser = ChapterParser()

parser.extract_chapter_number("第一章 开始")  # 返回: 1
parser.extract_chapter_number("Chapter 5")   # 返回: 5
parser.extract_chapter_number("序言")        # 返回: None
```

---

## 使用示例

### 示例1: 完整的小说处理流程

```python
from text_processor import TextProcessor, ChapterParser

# 小说文本
novel = """第一章 相遇

张三走在街上，阳光很好。

突然，他看到了李四。他高兴地说："好久不见！"

李四也笑了："是啊，好久不见！"

第二章 离别

几天后，两人要分别了。

张三有些伤感。他说："保重！"

李四点点头，转身离开了。"""

# 1. 解析章节
chapter_parser = ChapterParser()
chapters = chapter_parser.parse(novel)

print(f"共{len(chapters)}章")

# 2. 处理每个章节
text_processor = TextProcessor()

for chapter in chapters:
    print(f"\n处理: {chapter['title']}")
    
    # 分析章节内容
    scenes = text_processor.process_novel(chapter['content'])
    
    # 打印统计
    total_dialogues = sum(len(s['dialogues']) for s in scenes)
    emotions = [s['emotion'] for s in scenes]
    
    print(f"  场景数: {len(scenes)}")
    print(f"  对话数: {total_dialogues}")
    print(f"  主要情感: {max(set(emotions), key=emotions.count)}")
```

### 示例2: 提取角色对话

```python
from text_processor import TextProcessor

processor = TextProcessor()

text = """张三问："你吃饭了吗？"
李四答："还没有。"
张三说："那我们一起去吧。"
李四高兴地说："好啊！"""

# 提取所有对话
dialogues = processor.extract_dialogues(text)

# 按角色分组
from collections import defaultdict
dialogues_by_character = defaultdict(list)

for d in dialogues:
    dialogues_by_character[d['speaker']].append(d['text'])

# 打印每个角色的对话
for character, lines in dialogues_by_character.items():
    print(f"\n{character} 的对话:")
    for i, line in enumerate(lines, 1):
        print(f"  {i}. {line}")
```

### 示例3: 情感分析与可视化

```python
from text_processor import TextProcessor

processor = TextProcessor()

# 分析一段小说的情感变化
novel = """他非常高兴，这是最美好的一天。

但是，突然传来了坏消息。他感到非常难过。

经过一段时间，他慢慢平静下来。

最后，在朋友的帮助下，他重新振作起来，充满了希望。"""

scenes = processor.process_novel(novel)

print("情感变化曲线:")
print("-" * 50)

for i, scene in enumerate(scenes, 1):
    emotion = scene['emotion']
    intensity = scene['emotion_intensity']
    
    # 用符号表示情感
    symbol = {
        'positive': '😊',
        'negative': '😢',
        'neutral': '😐'
    }[emotion]
    
    # 用长度表示强度
    bar = '█' * int(intensity * 20)
    
    print(f"场景 {i} {symbol}: {bar} ({intensity:.2f})")
```

### 示例4: 自定义扩展

```python
from text_processor import TextProcessor

class CustomProcessor(TextProcessor):
    """扩展TextProcessor，添加自定义功能"""
    
    def __init__(self):
        super().__init__()
        
        # 添加自定义动作词
        self.action_verbs.extend(['飞', '游', '爬', '跳跃'])
        
        # 添加自定义情感词
        self.positive_words.update(['棒', '赞', '完美'])
        self.negative_words.update(['糟糕', '麻烦', '困难'])
    
    def extract_locations(self, text):
        """
        自定义方法：提取地点信息
        """
        import jieba.posseg as pseg
        words = pseg.cut(text)
        
        locations = []
        for word, flag in words:
            if flag == 'ns':  # ns表示地名
                locations.append(word)
        
        return list(set(locations))

# 使用自定义处理器
processor = CustomProcessor()

text = "张三在北京的公园里散步，心情很棒。"
scenes = processor.process_novel(text)
locations = processor.extract_locations(text)

print(f"地点: {locations}")
print(f"情感: {scenes[0]['emotion']}")
```

---

## 测试

### 运行测试

```bash
# 方法1: 使用pytest（推荐）
pytest test_text_processor.py -v

# 方法2: 直接运行测试文件
python3 test_text_processor.py

# 只运行特定测试类
pytest test_text_processor.py::TestTextProcessor -v

# 只运行特定测试方法
pytest test_text_processor.py::TestTextProcessor::test_split_into_scenes_basic -v
```

### 测试覆盖

测试文件包含 **40+ 个测试用例**，覆盖：

- ✅ 所有公共方法的基本功能
- ✅ 边界条件（空文本、单句、超长文本等）
- ✅ 特殊字符处理
- ✅ 错误情况处理
- ✅ 集成测试

### 测试示例

```python
# test_text_processor.py 节选

def test_extract_dialogues_with_speaker(self):
    """测试带说话人的对话提取"""
    text = '张三说："你好！"'
    dialogues = self.processor.extract_dialogues(text)
    
    self.assertEqual(len(dialogues), 1)
    self.assertIn('speaker', dialogues[0])
    self.assertEqual(dialogues[0]['text'], '你好！')
```

---

## 性能考虑

### 性能特点

- ⚡ **轻量级**: 纯Python实现，无需GPU
- 📊 **处理速度**: 约1000-5000字/秒（取决于硬件）
- 💾 **内存占用**: 主要取决于文本长度和jieba词典

### 优化建议

1. **批处理**:
```python
# 一次处理多个章节
chapters = [chapter1, chapter2, chapter3]
results = [processor.process_novel(ch) for ch in chapters]
```

2. **预加载jieba词典**:
```python
import jieba
jieba.initialize()  # 预加载词典，避免首次调用延迟
```

3. **使用自定义词典提高准确性**:
```python
import jieba
jieba.load_userdict("custom_dict.txt")  # 加载自定义词典

# custom_dict.txt 格式:
# 张三 3 nr
# 李四 3 nr
```

4. **缓存处理结果**:
```python
import pickle

# 保存结果
with open('processed_scenes.pkl', 'wb') as f:
    pickle.dump(scenes, f)

# 加载结果
with open('processed_scenes.pkl', 'rb') as f:
    scenes = pickle.load(f)
```

### 性能测试

```python
import time

processor = TextProcessor()

# 读取测试文本
with open('large_novel.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 计时
start = time.time()
scenes = processor.process_novel(text)
elapsed = time.time() - start

print(f"文本长度: {len(text)} 字符")
print(f"处理时间: {elapsed:.2f} 秒")
print(f"处理速度: {len(text)/elapsed:.0f} 字符/秒")
```

---

## 注意事项

### 已知限制

1. **角色识别准确性**:
   - 依赖jieba的词性标注，可能不够精确
   - 建议使用自定义词典补充常见人名
   - 对于生僻人名可能识别失败

2. **情感分析简单**:
   - 基于词典的简单方法，不考虑上下文
   - 建议后续集成更先进的情感分析模型

3. **对话说话人识别**:
   - 仅支持基本的"XXX说"模式
   - 复杂的对话结构可能识别失败
   - 无法处理隐含的说话人

4. **场景分割**:
   - 主要基于段落和标记词，可能不够智能
   - 建议结合LLM进行更精确的场景分割

### 最佳实践

1. **文本预处理**:
```python
# 清理文本
text = text.strip()
text = text.replace('\r\n', '\n')  # 统一换行符
text = re.sub(r'\n{3,}', '\n\n', text)  # 合并多个空行
```

2. **错误处理**:
```python
try:
    scenes = processor.process_novel(text)
except Exception as e:
    print(f"处理失败: {e}")
    # 使用默认值或降级处理
    scenes = [{
        'text': text,
        'description': '',
        'characters': [],
        'dialogues': [],
        'actions': [],
        'emotion': 'neutral',
        'emotion_intensity': 0.0
    }]
```

3. **结果验证**:
```python
def validate_scene(scene):
    """验证场景数据的完整性"""
    required_keys = [
        'text', 'description', 'characters',
        'dialogues', 'actions', 'emotion', 'emotion_intensity'
    ]
    
    for key in required_keys:
        if key not in scene:
            return False
    
    if not isinstance(scene['characters'], list):
        return False
    
    if scene['emotion'] not in ['positive', 'negative', 'neutral']:
        return False
    
    return True

# 使用
scenes = processor.process_novel(text)
valid_scenes = [s for s in scenes if validate_scene(s)]
```

### 后续改进方向

1. **集成LLM**: 使用GPT-4/Claude进行更精确的文本分析
2. **NER模型**: 使用专门的命名实体识别模型提高角色识别准确性
3. **情感分析模型**: 集成基于BERT的情感分析模型
4. **对话解析**: 改进对话说话人识别算法
5. **多语言支持**: 扩展支持英文等其他语言

---

## 相关资源

- **jieba分词**: https://github.com/fxsjy/jieba
- **Python文本处理**: https://docs.python.org/3/library/text.html
- **pytest文档**: https://docs.pytest.org/

---

## 更新日志

### v1.0.0 (2024-10-24)

- ✨ 初始版本发布
- ✅ 实现TextProcessor和ChapterParser类
- ✅ 完整的单元测试覆盖
- ✅ 详细的中文注释和文档

---

## 联系方式

如有问题或建议，请提交Issue或PR。

---

**文档版本**: 1.0.0  
**最后更新**: 2024-10-24
