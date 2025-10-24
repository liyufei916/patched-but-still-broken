# 文本处理模块文档

## 📋 概述

文本处理模块（`text_processor.py`）是小说转动漫系统的核心组件之一，负责对小说文本进行智能分析和结构化处理，为后续的多模态生成（图像、语音、视频等）提供基础数据。

## ✨ 主要功能

### TextProcessor 类

智能文本处理器，提供以下功能：

1. **场景分割** - 将长文本按场景自动划分
2. **角色识别** - 识别文本中出现的人物角色
3. **对话提取** - 提取角色对话及说话人
4. **动作识别** - 识别文本中的动作描述
5. **场景描述提取** - 提取环境和场景描述
6. **情感分析** - 分析文本的情感倾向和强度

### ChapterParser 类

章节解析器，提供以下功能：

1. **章节分割** - 按章节标题自动分割小说
2. **章节信息提取** - 提取标题、内容、段落等
3. **章节号识别** - 从标题中提取章节序号

## 🚀 快速开始

### 安装依赖

```bash
pip install jieba
```

或安装完整依赖：

```bash
pip install -r requirements.txt
```

### 基本使用

#### 1. 文本处理示例

```python
from text_processor import TextProcessor

# 创建文本处理器
processor = TextProcessor()

# 准备文本
text = """张三走进房间，房间很大，窗外阳光明亮。

他对李四说："今天天气真好！"

李四笑道："是啊，我们出去走走吧。"""

# 处理文本
scenes = processor.process_novel(text)

# 查看结果
for scene in scenes:
    print(f"场景文本: {scene['text']}")
    print(f"场景描述: {scene['description']}")
    print(f"角色: {scene['characters']}")
    print(f"对话: {scene['dialogues']}")
    print(f"动作: {scene['actions']}")
    print(f"情感: {scene['emotion']}")
    print("-" * 50)
```

#### 2. 章节解析示例

```python
from text_processor import ChapterParser

# 创建章节解析器
parser = ChapterParser()

# 准备小说文本
novel = """第一章 开始

这是第一章的内容。

第二章 继续

这是第二章的内容。"""

# 解析章节
chapters = parser.parse(novel)

# 查看结果
for chapter in chapters:
    print(f"标题: {chapter['title']}")
    print(f"章节号: {chapter['chapter_number']}")
    print(f"段落数: {len(chapter['paragraphs'])}")
    print("-" * 50)
```

#### 3. 完整处理流程

```python
from text_processor import TextProcessor, ChapterParser

# 步骤1：解析章节
chapter_parser = ChapterParser()
chapters = chapter_parser.parse(novel_text)

# 步骤2：处理每个章节
text_processor = TextProcessor()
for chapter in chapters:
    scenes = text_processor.process_novel(chapter['content'])
    
    # 处理每个场景
    for scene in scenes:
        # 这里可以进行后续处理：
        # - 根据scene['description']生成图像
        # - 根据scene['dialogues']生成语音
        # - 根据scene['emotion']调整音乐
        pass
```

## 📖 API 文档

### TextProcessor 类

#### `__init__()`

初始化文本处理器。

```python
processor = TextProcessor()
```

#### `process_novel(text: str) -> List[Dict]`

处理整部小说文本，这是主要的入口方法。

**参数：**
- `text` (str): 完整的小说文本

**返回：**
- `List[Dict]`: 结构化的场景数据列表，每个场景包含：
  - `text` (str): 原始场景文本
  - `description` (str): 场景描述（环境、氛围等）
  - `characters` (List[str]): 出现的角色列表
  - `dialogues` (List[Dict]): 对话列表，每项包含 `speaker` 和 `text`
  - `actions` (List[str]): 动作描述列表
  - `emotion` (str): 情感倾向 - 'positive'/'negative'/'neutral'

**示例：**
```python
scenes = processor.process_novel("他走在街上，心情愉快...")
```

#### `split_into_scenes(text: str) -> List[str]`

将文本分割成多个场景。

**分割依据：**
- 段落换行（连续两个换行符）
- 场景转换标识词（如：此时、另一边等）
- 时间变化（如：第二天、一小时后等）

**参数：**
- `text` (str): 输入文本

**返回：**
- `List[str]`: 分割后的场景文本列表

#### `identify_characters(text: str) -> List[str]`

识别文本中出现的角色。

使用jieba的词性标注功能识别人名（nr标签）。

**参数：**
- `text` (str): 输入文本

**返回：**
- `List[str]`: 识别出的角色名称列表（按出现频率降序）

#### `extract_dialogues(text: str) -> List[Dict[str, str]]`

提取文本中的对话内容。

支持的引号格式：
- 中文双引号：""
- 中文单引号：''
- 英文双引号：""
- 英文单引号：''

**参数：**
- `text` (str): 输入文本

**返回：**
- `List[Dict[str, str]]`: 对话列表，每项包含：
  - `speaker` (str): 说话人（如果能识别）
  - `text` (str): 对话内容

#### `extract_actions(text: str) -> List[str]`

提取文本中的动作描述。

识别包含动作动词的句子或短语。

**参数：**
- `text` (str): 输入文本

**返回：**
- `List[str]`: 动作描述列表

#### `extract_scene_description(text: str) -> str`

提取场景描述（环境描写）。

识别描述性的句子，通常包含环境、外观、氛围等描述。

**参数：**
- `text` (str): 输入文本

**返回：**
- `str`: 场景描述文本

#### `analyze_emotion(text: str) -> str`

分析文本的情感倾向。

基于情感词典，统计积极和消极词汇的出现次数。

**参数：**
- `text` (str): 输入文本

**返回：**
- `str`: 情感类型 - 'positive'（积极）、'negative'（消极）或'neutral'（中性）

#### `get_emotion_intensity(text: str) -> float`

计算情感强度。

**参数：**
- `text` (str): 输入文本

**返回：**
- `float`: 情感强度值（0-1之间）

### ChapterParser 类

#### `__init__()`

初始化章节解析器。

```python
parser = ChapterParser()
```

#### `parse(text: str) -> List[Dict]`

解析小说章节。

**支持的章节格式：**
- 第X章（X可以是中文数字或阿拉伯数字）
- 第X回
- 第X节
- 第X卷
- Chapter X
- Part X

**参数：**
- `text` (str): 完整的小说文本

**返回：**
- `List[Dict]`: 章节列表，每个章节包含：
  - `title` (str): 章节标题
  - `content` (str): 章节内容
  - `paragraphs` (List[str]): 段落列表
  - `chapter_number` (int): 章节序号

#### `extract_chapter_number(title: str) -> Optional[int]`

从章节标题中提取章节号。

**参数：**
- `title` (str): 章节标题

**返回：**
- `Optional[int]`: 章节号，如果提取失败返回None

## 🧪 测试

### 运行测试

```bash
# 使用pytest运行
pytest test_text_processor.py -v

# 或直接运行测试文件
python3 test_text_processor.py
```

### 测试覆盖

测试文件 `test_text_processor.py` 包含40+个测试用例，覆盖：

- ✅ 所有公共方法的功能测试
- ✅ 边界条件测试（空文本、单句文本、超长文本等）
- ✅ 异常情况测试
- ✅ 集成测试（完整处理流程）

### 运行演示

```bash
python3 demo_text_processor.py
```

演示程序展示了：
1. TextProcessor的基本功能
2. ChapterParser的基本功能
3. 完整的处理流程和统计报告

## 🎯 使用场景

### 场景1：小说章节分析

```python
# 解析整部小说
parser = ChapterParser()
chapters = parser.parse(novel_text)

# 分析每个章节
for chapter in chapters:
    processor = TextProcessor()
    scenes = processor.process_novel(chapter['content'])
    
    print(f"{chapter['title']}:")
    print(f"  - {len(scenes)} 个场景")
    print(f"  - 主要角色: {set(char for s in scenes for char in s['characters'])}")
```

### 场景2：情感分析

```python
processor = TextProcessor()

# 分析多个场景的情感
texts = ["他非常高兴...", "她感到悲伤...", "天气很好..."]

for text in texts:
    emotion = processor.analyze_emotion(text)
    intensity = processor.get_emotion_intensity(text)
    print(f"情感: {emotion}, 强度: {intensity:.2f}")
```

### 场景3：对话提取

```python
processor = TextProcessor()

text = '''张三说："你好！"
李四回答："你好啊！"'''

dialogues = processor.extract_dialogues(text)

for dialogue in dialogues:
    print(f"{dialogue['speaker']}: {dialogue['text']}")
```

## 🔧 自定义扩展

### 添加自定义情感词汇

```python
processor = TextProcessor()

# 添加自定义积极词汇
processor.positive_words.update(['棒', '赞', '优秀'])

# 添加自定义消极词汇
processor.negative_words.update(['糟糕', '失败', '错误'])
```

### 添加自定义动作词汇

```python
processor = TextProcessor()

# 添加自定义动作词
processor.action_words.update(['飞翔', '跳跃', '奔跑'])
```

## 📊 性能考虑

- **文本长度**：适合处理中等长度的小说文本（几万到几十万字）
- **分词性能**：使用jieba分词，性能良好
- **内存占用**：场景数据会保存在内存中，超长文本建议分批处理

## ⚠️ 注意事项

1. **依赖jieba**：需要安装jieba分词库
2. **人名识别准确性**：依赖jieba的人名识别，可能不够精确
3. **对话识别**：仅支持引号格式的对话，其他格式可能无法识别
4. **情感分析**：基于词典的简单方法，适合初步分析

## 🔄 更新日志

### v1.0 (2024-10-24)

- ✅ 实现TextProcessor核心功能
- ✅ 实现ChapterParser功能
- ✅ 添加详细的中文注释
- ✅ 编写完整的单元测试（40+测试用例）
- ✅ 创建演示程序

## 📝 代码示例

完整的示例代码请参考：
- `demo_text_processor.py` - 演示程序
- `test_text_processor.py` - 单元测试
- `text_processor.py` - 源代码（含详细注释）

## 💡 后续改进方向

1. **使用更先进的NER模型** - 提高角色识别准确性
2. **集成LLM** - 使用大语言模型进行更精确的场景分析
3. **支持更多对话格式** - 识别非引号格式的对话
4. **情感分析增强** - 使用机器学习模型提升准确性
5. **性能优化** - 对超长文本的处理优化

## 📞 支持

如有问题或建议，请：
1. 查看代码中的详细注释
2. 运行演示程序了解使用方法
3. 查看测试用例了解预期行为
