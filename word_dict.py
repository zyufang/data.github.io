import pickle

def get_vocab(corpus1, corpus2):
    '''
    遍历输入的两个语料库中的所有数据，将所有单词存储到一个词汇表集合中，返回词汇表。
    corpus1, corpus2: 输入的两个语料库，它们是包含单词的列表。
    '''
    word_vocab = set()
    for corpus in [corpus1, corpus2]:
        for i in range(len(corpus)):
            word_vocab.update(corpus[i][1][0])
            word_vocab.update(corpus[i][1][1])
            word_vocab.update(corpus[i][2][0])
            word_vocab.update(corpus[i][3])
    print(len(word_vocab))
    return word_vocab


def load_pickle(filename):
    '''
    以二进制读模式打开文件,返回加载的pickle格式的数据。
    filename: 要加载的pickle文件的路径。
    '''
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def vocab_processing(filepath1, filepath2, save_path):
    '''
    调用load_pickle()函数加载语料库数据并调用get_vocab()函数获取词汇表,
    将仅存在于第二个语料库的词汇保存在词汇表中并保存到指定的文件路径。
    filepath1, filepath2: 两个语料库文件的路径。
    save_path: 保存词汇表的文件路径。
    '''
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())

    word_set = get_vocab(total_data1, total_data2)

    excluded_words = total_data1.intersection(word_set)
    word_set = word_set - excluded_words
    
    print(len(total_data1))
    print(len(word_set))

    with open(save_path, 'w') as f:
        f.write(str(word_set))


if __name__ == "__main__":
    
    python_hnn = './data/python_hnn_data_teacher.txt'
    python_staqc = './data/staqc/python_staqc_data.txt'
    python_word_dict = './data/word_dict/python_word_vocab_dict.txt'
    
    sql_hnn = './data/sql_hnn_data_teacher.txt'
    sql_staqc = './data/staqc/sql_staqc_data.txt'
    sql_word_dict = './data/word_dict/sql_word_vocab_dict.txt'

    new_sql_staqc = './ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = './ulabel_data/sql_word_dict.txt'

    final_vocab_processing(sql_word_dict, new_sql_large, large_word_dict_sql)
