import jieba.analyse


# 分析文本并提取关键词
def extract_keywords(text, top_k=5):
    keywords = jieba.analyse.extract_tags(text, topK=top_k)
    return keywords

# 统计关键词出现的次数
def count_keyword_occurrences(text, keywords):
    keyword_counts = {}
    for keyword in keywords:
        keyword_counts[keyword] = text.count(keyword)
    return keyword_counts

# 示例文本
#text = "在这里，我们将使用Python的结巴分词库来展示如何提取关键词并统计它们的出现次数。"
#file = "unpackingComment.txt" #unpacking
file = "Comment.txt"
fn = open(file, 'rt', encoding='utf-8')  # 打开文件
text = fn.read()
stop = "stopword.txt"
jieba.analyse.set_stop_words(stop)

# 提取关键词
keywords = extract_keywords(text,200)
print("关键词:", keywords)

# 统计关键词出现次数
keyword_counts = count_keyword_occurrences(text, keywords)
print("关键词出现次数:", keyword_counts)
