# 软件工程实验
20211060240 赵钰芳

## 目录
- [一、项目描述](#一项目描述)
- [二、项目结构文件说明](#二项目结构文件说明)
  - [2.1 process_single_corpus.py文件](#process_single_corpuspy文件)
  - [2.2 word_dict.py文件](#word_dictpy文件)
  - [2.3 python_structured.py文件](#python_structuredpy文件)
  - [2.4 sqlang_structured.py文件](#sqlang_structuredpy文件)
  - [2.5 getStru2Vec.py文件](#getStru2Vecpy文件)
  - [2.6 embddings_process.py文件](#embddings_processpy文件)
- [三、总结](#三总结)

## 一、项目描述
  此项目的python文件是对文本数据进行预测处理。通过给出python文件，对文件进行代码代码规范调试。
## 二、项目结构文件说明
### 结构说明：
```
├── hnn_preprocessing  
│   └── embddings_process.py  
│   └── getStru2Vec.py
│   └── process_single_corpus.py
│   └── python_structured.py
│   └── sqlang_structured.py
│   └── word_dict.py
```
### 文件说明

### process_single_corpus.py文件

#### 2.1.1. 概述
  把语料中的单候选和多候选分隔开
#### 2.1.2. 导入依赖库
该文件导入了以下依赖库：
 - `pickle`：用于读取和写入 pickle 文件
 - `Counter`：用于计数数据中元素的频率

#### 2.1.3. 类和方法说明
- `load_pickle(filename)`：以二进制读模式打开文件,加载pickle格式的数据。
- `split_data(total_data, qids)`：统计数据出现的次数,根据数据出现的次数将其将分为单候选或多候选问题并存入对应列表。
- `data_staqc_processing(filepath, save_single_path, save_multiple_path)`: 针对staqc数据,读取文件内容,然后使用eval函数将字符串转换为Python数据结构。根据问题ID判断单候选和多候选问题,将数据以文本形式分别保存到对应的文件中。
- `data_large_processing(filepath, save_single_path, save_multiple_path)`: 针对large数据,将pickle文件内容反序列化为Python数据结构。根据问题ID判断单候选和多候选问题,将数据序列化为pickle格式并分别保存到不同的文件中。
- `def single_unlabeled_to_labeled(input_path, output_path)`: 加载未标记的数据并为每个数据项添加标签1,表示它们是单候选问题,然后按照问题ID和标签对数据进行排序并保存。

---
### word_dict.py文件
#### 2.2.1. 概述
  构建语料词典
#### 2.2.2. 导入依赖库
该文件导入了以下依赖库：
 - `pickle`：用于读取和写入 pickle 文件

#### 2.2.3. 类和方法说明
- `load_pickle(filename)`：以二进制读模式打开文件,返回加载的pickle格式的数据。
- `get_vocab(corpus1, corpus2)`：遍历输入的两个语料库中的所有数据，将所有单词存储到一个词汇表集合中，返回词汇表。
- `vocab_prpcessing(filepath1,filepath2,save_path)`：调用load_pickle()函数加载语料库数据并调用get_vocab()函数获取词汇表,将仅存在于第二个语料库的词汇保存在词汇表中并保存到指定的文件路径。

---
### python_structured.py文件
#### 2.3.1. 概述
  解析 Python 代码，修复代码中的变量命名问题；代码重构，添加变量名的注释。
#### 2.3.2. 导入依赖库
该文件导入了以下依赖库：
 - `re`：Python的正则表达式模块，它允许进行有效的字符串匹配和操作。
 - `ast`: 代表抽象语法树，它允许以非文本方式处理Python代码。
 - `sys`: 提供访问Python解释器使用或维护的一些变量以及与解释器交互的函数。
 - `token`: 与tokenize模块一起工作，将Python代码分解为其各个组成部分。
 - `tokenize`：用于将文本分解为tokens，这是语言的基本构建块。
 - `io.StringIO`：一个内存中的类似文件的对象。这个对象可以被用作输入或输出到大多数期望标准文件对象的函数。
 - `inflection`：用于进行单词的单复数转换
 - `nltk`：自然语言处理工具包，用于词性标注、分词和词形还原

#### 2.3.3. 类和方法说明
- `repair_program_io(code)`: 通过正则表达式匹配和文本处理来删除不必要的I/O格式符号。
- `get_vars(ast_root)`：从给定的 AST 中提取并返回所有非加载（non-load）上下文的变量名，并且这些变量名会被排序后返回。
- `get_vars_heuristics(code)`: 从给定的代码字符串中提取变量名，使用启发式方法处理不完整的代码片段。
- `PythonParser(code)`: 将代码字符串解析为Token 序列，并且执行变量解析。
 └──`first_trial(_code)`: 对输入的 _code 进行词法分析，并检查是否能够成功生成至少一个词法单元。
- `revert_abbrev(line)`: 缩略词处理，将常见的英语缩写还原为它们的原始形式。
- `get_wordpos(tag)`:获取词性。
- `process_nl_line(line)`: 对传入的一行文本进行处理预处理,包括空格，还原缩写，下划线命名，去括号，去除开头末尾空格。
- `process_sent_word(line)`: 对一个句子进行分词、词性标注、还原和提取词干的功能。
- `filter_all_invachar(line)`：过滤掉Python代码中不常用的字符，以减少解析时的错误。
- `filter_part_invachar(line)`: 过滤掉Python代码中部分不常用的字符，以减少解析时的错误。
- `python_code_parse(line)`: 对 Python 代码行进行预处理，并尝试解析它，最终返回一个由单词（或标识符）组成的列表。
- `python_query_parse(line)`: 解析 python 查询语句，进行文本预处理,并返回一个处理过的单词列表。
- `python_context_parse(line)`: 对输入的文本进行预处理，并返回一个处理过的单词列表。


---
### sqlang_structured.py文件
#### 2.4.1. 概述
  解析 SQL 代码，修复代码中的变量命名问题；
  代码重构，添加变量名的注释。
#### 2.4.2. 导入依赖库
该文件导入了以下依赖库:
 - `re`：Python的正则表达式模块，它允许进行有效的字符串匹配和操作。
 - `ast`: 代表抽象语法树，它允许以非文本方式处理Python代码。
 - `sys`: 提供访问Python解释器使用或维护的一些变量以及与解释器交互的函数。
 - `sqlparse`：sql解析
 - `inflection`：用于进行单词的单复数转换
 - `nltk`：自然语言处理工具包，用于词性标注、分词和词形还原
  
#### 2.4.3. 类和方法说明
- `string_scanner(s)`: 定义了一个正则表达式扫描器，扫描字符串。
- `tokenizeRegex(s)`: 用正则表达式分词处理输入的字符串s，并返回处理后的结果。
- `SqlParser()`: SQL语句处理。  
   └──`sanitizeSql(sql)`: 对输入的SQL语句进行清理和标准化。  
   └──`parseStrings(self, tok)`: 可以根据配置对SQL语句中的字符串选择使用正则表达式分词处理或直接将字符串值设置为"CODSTR"。
   └──`renameIdentifiers(self, tok)`: 使用两个字典idMap和idMapInv以及一个计数器idCount来实现对SQL语句中的表名和列名的重命名,并对其他类型的token进行处理。
   └──` _hash_(self)`: 用于计算并返回对象的哈希值。  
   └──`_init__(self, sql, regex=False, rename=True)`: 定义了初始化方法,并对输入的SQL语句进行一系列的处理。
   └──`getTokens(parse)`: 从解析的SQL语句中提取tokens,对于类型为STRING的token使用空格进行分割,对于其他类型的token直接转换为字符串。  
   └──` removeWhitespaces(self, tok)`: 从SQL语句中移除所有的空白字符。  
   └──`identifySubQueries(self, tokenList)`: 在SQL语句中识别子查询，并将识别到的子查询的类型设置为SUBQUERY。
   └──`identifyLiterals(self, tokenList)`: 识别关键字、整数、十六进制数、浮点数、字符串、通配符和列名等各种类型的字面量,并将这些字面量的类型设置为相应的值。
   └──`identifyFunctions(self, tokenList)`: 从给定的token列表中识别SQL语句中的函数并设置ttype类型。  
   └──`identifyTables(self, tokenList)`: 在SQL语句中识别函数,并将识别到的函数的类型设置为FUNCTION。
   └──`__str__(self)`: 将SQL语句的tokens列表中的所有token连接成一个字符串。  
   └──`parseSql(self)`: 返回SQL语句中所有token的字符串列表。
- `revert_abbrev(line)`: 缩略词处理，使用正则表达式对字符串进行匹配和替换,将文本中的缩写还原为完整的词。
- `get_word_pos(tag)`:获取词性。
- `process_nl_line(line)`: 对传入的一行文本进行处理预处理：空格，还原缩写，去除冗余字符、下划线命名，去括号，去除开头末尾空格。
- `process_sent_word(line)`: 对一个句子进行分词、词性标注、还原和提取词干的功能。
- `filter_all_invachar(line)`：过滤掉SQL代码中不常用的字符，以减少解析时的错误。
- `filter_part_invachar(line)`: 过滤掉SQL代码中部分不常用的字符，以减少解析时的错误。
- `sqlang_code_parse(line)`: 对输入的代码行进行文本预处理和解析。
- `sqlang_query_parse(line)`: 对输入的SQL语句调用函数进行过滤无效字符、预处理、分词处理、替换字符。
- `sqlang_context_parse(line)`: 对输入的文本调用函数进行过滤无效字符、预处理、分词处理、替换字符

---
### getStru2Vec.py文件
#### 2.5.1. 概述
  获取最终的python解析文本和SQL解析文本。
#### 2.5.2. 导入依赖库
该文件导入了以下依赖库：
 - `pickle`：用于读取和写入 pickle 文件
 - `python_structured.py`文件中的所有函数
 - `sql_structured.py`文件中的所有函数
 - `multiprocessing.Pool`：用于多进程处理

#### 2.5.3. 类和方法说明
- `multipro_python_query(data_list)`: 对Python语料中的查询文本进行解析和分词处理。
- `multipro_python_code(data_list)`: 对Python语料中的代码文本进行解析和分词处理。
- `multipro_python_context(data_list)`: 对Python语料中的上下文文本进行解析和分词处理。
- `multipro_sqlang_query(data_list)`: 对SQL语料中的查询文本进行解析和分词处理。
- `multipro_sqlang_code(data_list)`: 对SQL语料中的代码文本进行解析和分词处理。
- `multipro_sqlang_context(data_list)`: 对SQL语料中的代码文本进行解析和分词处理。
- `parse(data_list, split_num, context_func, query_func, code_func))`: 并行处理数据。首先创建一个进程池并将数据列表分割成多个子列表。接着并行地对每一个数据子列表应用处理函数，并收集结果。
- `main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func)`: 读取源数据,调用parse函数处理数据,将所有数据组合成一个新的列表并保存结果。

---
### embddings_process.py文件
#### 2.6.1. 概述
  从大词典中获取特定于于语料的词典；将数据处理成待打标签的形式
#### 2.6.2. 导入依赖库
该文件导入了以下依赖库：
 - `pickle`：用于读取和写入 pickle 文件
 - `numpy`：用于处理数组和矩阵的库
 - `gensim.models.KeyedVectors`：用于加载和保存词向量模型

#### 2.6.3. 类和方法说明
- `trans_bin(path1, path2)`:将词向量文件从文本格式转换为二进制格式,同时释放原始词向量,节省内存空间,以提高加载速度。
- `get_new_dict(type_vec_path, type_word_path, final_vec_path, final_word_path)`: 根据给定的词向量文件和词典文件，构建新的词典和词向量矩阵，并保存至指定路径。
- `get_index(type,text,word_dict)`:获取给定文本中每个词在词典中的索引。
- `serialization(word_dict_path, type_path, final_type_path)`: 将原始的文本数据替换为词典中对应的索引(模型可以处理的数字序列)，即语料序列化。

---

## 三、总结  
在本次实验中，学习并掌握了规范化代码。并且初步了解了自然语言处理项目如何进行文本数据的预处理与分析。
