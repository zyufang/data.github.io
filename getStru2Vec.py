import pickle
import multiprocessing
from python_structured import *
from sqlang_structured import *

def multipro_python_query(data_list):
    #对Python语料中的查询文本进行解析和分词处理。
    return [python_query_parse(line) for line in data_list]

def multipro_python_code(data_list):
    #对Python语料中的代码文本进行解析和分词处理。
    return [python_code_parse(line) for line in data_list]

def multipro_python_context(data_list):
    #对Python语料中的上下文文本进行解析和分词处理。
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(python_context_parse(line))
    return result

def multipro_sqlang_query(data_list):
    #对SQL语料中的查询文本进行解析和分词处理。
    return [sqlang_query_parse(line) for line in data_list]

def multipro_sqlang_code(data_list):
    #对SQL语料中的代码文本进行解析和分词处理。
    return [sqlang_code_parse(line) for line in data_list]

def multipro_sqlang_context(data_list):
    #对SQL语料中的代码文本进行解析和分词处理。
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(sqlang_context_parse(line))
    return result

def parse(data_list, split_num, context_func, query_func, code_func):
    '''
    并行处理数据。首先创建一个进程池并将数据列表分割成多个子列表。接着并行地对每一个数据子列表应用处理函数，并收集结果。
    data_list: 输入的数据列表，这个列表包含了所有需要处理的数据。
    split_num: 输入的分割数,函数会将数据列表分割成多个子列表,每个子列表包含split_num个数据。
    context_func: 用来处理context数据的处理函数。
    query_func: 用来处理query数据的处理函数。
    code_func: 用来处理code数据的处理函数。
    '''
    #创建进程池
    pool = multiprocessing.Pool()
    #将data_list分割成多个子列表，每个子列表包含split_num个元素。
    split_list = [data_list[i:i + split_num] for i in range(0, len(data_list), split_num)]
    #使用进程池并行地将context_func函数应用到split_list中的每个子列表上。
    results = pool.map(context_func, split_list)
    context_data = [item for sublist in results for item in sublist]
    print(f'context条数:{len(context_data)}')
    #使用进程池并行地将query_func函数应用到split_list中的每个子列表上。
    results = pool.map(query_func, split_list)
    query_data = [item for sublist in results for item in sublist]
    print(f'query条数:{len(query_data)}')
    #使用进程池并行地将code_func函数应用到split_list中的每个子列表上。
    results = pool.map(code_func, split_list)
    code_data = [item for sublist in results for item in sublist]
    print(f'code条数:{len(code_data)}')

    pool.close()
    pool.join()

    return context_data, query_data, code_data

def main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func):
    '''
    读取源数据,调用parse函数处理数据,将所有数据组合成一个新的列表并保存结果。
    lang_type:语言类型。
    split_num:分割数。
    source_path:源数据路径。
    save_path:保存路径。
    context_func: 用来处理context数据的处理函数。
    query_func: 用来处理query数据的处理函数。
    code_func: 用来处理code数据的处理函数。
    '''
    with open(source_path, 'rb') as f:
        corpus_lis = pickle.load(f)

    context_data, query_data, code_data = parse(corpus_lis, split_num, context_func, query_func, code_func)
    qids = [item[0] for item in corpus_lis]

    total_data = [[qids[i], context_data[i], code_data[i], query_data[i]] for i in range(len(qids))]

    with open(save_path, 'wb') as f:
        pickle.dump(total_data, f)

if __name__ == '__main__':
    staqc_python_path = '.ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_save = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.pkl'

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_save = './ulabel_data/staqc/sql_staqc_unlabled_data.pkl'
    #处理STAQC Python数据
    main(python_type, split_num, staqc_python_path, staqc_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    #处理STAQC SQL数据
    main(sqlang_type, split_num, staqc_sql_path, staqc_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)

    large_python_path = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    large_python_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.pkl'

    large_sql_path = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    large_sql_save = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.pkl'
    #处理大规模Python数据
    main(python_type, split_num, large_python_path, large_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    #处理大规模SQL数据
    main(sqlang_type, split_num, large_sql_path, large_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)
