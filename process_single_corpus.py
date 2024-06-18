import pickle
from collections import Counter

def load_pickle(filename):
    '''
    以二进制读模式打开文件,加载pickle格式的数据。(指定了在反序列化字符串时使用的编码形式为iso-8859-1)
    filename:pickle文件路径
    '''   
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='iso-8859-1')
    return data

def split_data(total_data, qids):
    """
    遍历总数据,统计数据出现的次数,根据数据出现的次数将其将分为单候选或多候选问题。
    并将单候选问题存入total_data_single列表中,多候选问题存入total_data_multiple列表中。
    total_data: 要分割的总数据。
    qids: 总数据中每个问题的ID列表。
    """
    result = Counter(qids)
    total_data_single = []
    total_data_multiple = []
    for data in total_data:
        if result[data[0][0]] == 1:
            total_data_single.append(data)
        else:
            total_data_multiple.append(data)
    return total_data_single, total_data_multiple

def data_staqc_processing(filepath, save_single_path, save_multiple_path):
    '''
    针对staqc数据(以文本形式存储在文本文件中),首先读取文件内容,然后使用eval函数将字符串转换为Python数据结构。
    根据问题ID判断单候选和多候选问题,将数据转换为字符串并以文本形式分别保存到不同的文件中。
    filepath: 总数据的文件路径。
    save_single_path: 保存单候选数据文件的路径。
    save_multiple_path: 保存多候选数据文件的路径。
    '''
    with open(filepath, 'r') as f:
        total_data = eval(f.read())
    qids = [data[0][0] for data in total_data]
    total_data_single, total_data_multiple = split_data(total_data, qids)

    with open(save_single_path, "w") as f:
        f.write(str(total_data_single))
    with open(save_multiple_path, "w") as f:
        f.write(str(total_data_multiple))

def data_large_processing(filepath, save_single_path, save_multiple_path):
    '''
    针对large数据(以pickle格式存储在.pickle文件中),将pickle文件内容反序列化为Python数据结构。
    根据问题ID判断单候选和多候选问题,将数据序列化为pickle格式并分别保存到不同的文件中。
    filepath: 总数据的文件路径。
    save_single_path: 保存单候选数据文件的路径。
    save_multiple_path: 保存多候选数据文件的路径。
    '''
    total_data = load_pickle(filepath)
    qids = [data[0][0] for data in total_data]
    total_data_single, total_data_multiple = split_data(total_data, qids)

    with open(save_single_path, 'wb') as f:
        pickle.dump(total_data_single, f)
    with open(save_multiple_path, 'wb') as f:
        pickle.dump(total_data_multiple, f)

def single_unlabeled_to_labeled(input_path, output_path):
    '''
    加载未标记的数据并为每个数据项添加标签1,表示它们是单候选问题,然后按照问题ID和标签对数据进行排序并保存。
    input_path: 输入文件路径,该文件应包含pickle格式的未标记数据。
    output_path: 输出文件路径,函数会将标记后的数据以文本形式写入该文件。
    '''
    total_data = load_pickle(input_path)
    labels = [[data[0], 1] for data in total_data]
    total_data_sort = sorted(labels, key=lambda x: (x[0], x[1]))
    with open(output_path, "w") as f:
        f.write(str(total_data_sort))

if __name__ == "__main__":
    staqc_python_path = './ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_single_save = './ulabel_data/staqc/single/python_staqc_single.txt'
    staqc_python_multiple_save = './ulabel_data/staqc/multiple/python_staqc_multiple.txt'
    data_staqc_processing(staqc_python_path, staqc_python_single_save, staqc_python_multiple_save)

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_single_save = './ulabel_data/staqc/single/sql_staqc_single.txt'
    staqc_sql_multiple_save = './ulabel_data/staqc/multiple/sql_staqc_multiple.txt'
    data_staqc_processing(staqc_sql_path, staqc_sql_single_save, staqc_sql_multiple_save)

    large_python_path = './ulabel_data/python_codedb_qid2index_blocks_unlabeled.pickle'
    large_python_single_save = './ulabel_data/large_corpus/single/python_large_single.pickle'
    large_python_multiple_save = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    data_large_processing(large_python_path, large_python_single_save, large_python_multiple_save)

    large_sql_path = './ulabel_data/sql_codedb_qid2index_blocks_unlabeled.pickle'
    large_sql_single_save = './ulabel_data/large_corpus/single/sql_large_single.pickle'
    large_sql_multiple_save = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    data_large_processing(large_sql_path, large_sql_single_save, large_sql_multiple_save)

    large_sql_single_label_save = './ulabel_data/large_corpus/single/sql_large_single_label.txt'
    large_python_single_label_save = './ulabel_data/large_corpus/single/python_large_single_label.txt'
    single_unlabeled_to_labeled(large_sql_single_save, large_sql_single_label_save)
    single_unlabeled_to_labeled(large_python_single_save, large_python_single_label_save)
