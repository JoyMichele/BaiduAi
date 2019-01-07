import jieba
import gensim
from gensim import corpora
from gensim import models
from gensim import similarities
from settings import MONGO_DB

# 查询所有歌曲
content = MONGO_DB.content.find({})
l1 = [con.get("title") for con in content]  # 构建曲名列表
all_doc_list = []  # 存储歌曲名分词列表
for doc in l1:
    # 使用jieba分词处理每个曲名
    doc_list = [word for word in jieba.cut_for_search(doc)]
    # jieba分词后的曲名列表
    all_doc_list.append(doc_list)


def gensim_nlp(text):
    """
    使用gensim 和 jieba配合进行NLP
    :param text:与语料库进行匹配的文本内容
    :return:匹配到的语料库中的文本内容
    """
    # 将待匹配的文本text进行jieba分词
    doc_text_list = [word for word in jieba.cut_for_search(text)]

    # 1. 制作语料库
    # 1.1 制作词袋
    dictionary = corpora.Dictionary(all_doc_list)
    '''
    词袋:
    以两句话为例['你叫什么名字', '你的名字是什么']
    进行jieba分词 --> [ ['你', '叫', '什么', '名字'], ['你', '的', '名字', '是', '什么'] ]
    词袋 -- > {'你':0, '的':1, '是':2, '叫':3, '名字':4, '什么':5}
    将这些词排列形成一个词(key)与一个标志位(value)的字典,也就是词袋
    '''
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]  # 初始语料库
    '''
    语料库:
    将 all_doc_list 中的每个列表中的词语与 dictionary中的key进行匹配
    以这句话为例['你', '的', '爱好', '是', '什么']
    匹配结果 [(0:1), (1:1), (2:1), (5:1)]
    你(标志位0)出现1次--> (0:1)
    的(标志位1)出现1次--> (1:1)
    ...只返回匹配到的词语的元组
    
    '''
    # 1.2 将待匹配的文本text做成语料库
    doc_text_vec = dictionary.doc2bow(doc_text_list)

    # 2.0 将corpus语料库(初始语料库) 使用Lsi模型进行训练
    lsi = models.LsiModel(corpus)
    print('lsi[corpus]', lsi[corpus])  # 语料库corpus训练结果
    print("lsi[doc_test_vec]", lsi[doc_text_vec])  # doc_text_vec在语料库corpus的训练结果中的向量表示

    # 3 文本相似度
    # 3.1 稀疏矩阵相似度将主语料库corpus的训练结果作为初始值
    index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))
    # 3.2 将语料库doc_text_vec在语料库corpus的训练结果中的向量表示与语料库corpus的向量表示做矩阵相似度计算
    sim = index[lsi[doc_text_vec]]
    # 3.3 对下标和相似度结果进行一个排序,拿出相似度最高的结果
    # cc = sorted(enumerate(sim), key=lambda item: item[1],reverse=True)
    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    print(cc)

    content = l1[cc[0][0]]
    if cc[0][1] > 0:
        print(text, content)
        music = MONGO_DB.content.find_one({'title': text})
        return music
