#import jieba.analyse
import collections
import re

import jieba
from jieba import analyse
def extract_tags_method1():
    stop = "stopword.txt"
    jieba.analyse.set_stop_words(stop)
    file="comment.txt"
    lines = open(file, encoding='utf8').read()
    new = "output.txt"
    newfile = open(new, "w", encoding='utf8')
    num = 10
    res =  analyse.extract_tags(lines, topK=num, withWeight=False, allowPOS=())
    print(res)
    newfile.write("  ".join(res))
    newfile.close()

#extract_tags_method1()
#方案2

# 读取文件
def extract_tags_method2():
    fn = open('comment.txt', 'rt', encoding='utf-8')  # 打开文件
    string_data = fn.read()  # 读出整个文件
    fn.close()  # 关闭文件

    # 文本预处理  洗

    #pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
    pattern = re.compile(u'\t|\n"')  # 定义正则表达式匹配模式

    string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除
    #print(string_data)
    # 文本分词
    seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
    print(seg_list_exact)

    object_list = []

    # 分词并去除停用词
    remove_words = set()
    fr = open('stopword.txt', encoding = 'UTF-8')
    for word in fr:
        remove_words.add(str(word).strip())
    fr.close()


    for word in seg_list_exact:  # 循环读出每个分词
        if word not in remove_words:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表

    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(100)  # 获取前100最高频的词
    print(word_counts_top10)  # 输出检查

extract_tags_method2()
