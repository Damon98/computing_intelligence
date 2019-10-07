import random
from collections import Counter
import jieba

# 如何判断一段语言是对的 简化为 Probability Based（判断一句话出现的概率的高低）
# N-gram Models :N-gram模型是一种语言模型（language Model），是一个基于概率的判别模型，它的输入是一句话，输出是这句话的概率，即这些单词的联合概率（joint probability）。
####### 参考资料（来自web）（https://blog.csdn.net/songbinxu/article/details/80209197）
# N-Gram是基于一个假设：第n个词出现与前n-1个词相关，而与其他任何词不相关（这也是隐马尔可夫当中的假设）
# P(T)=P(w1)*p(w2)*p(w3)***p(wn)=p(w1)*p(w2|w1)*p(w3|w1w2)** *p(wn|w1w2w3...wn-1)~~~p(T) 就是语言模型，即用来计算一个句子 T 概率的模型。~~~~
# 上面这个公式很难实际应用：参数空间过大（有n个）；对数据量要求大，组合阶数高时尤其明显。
# 马尔科夫假设（Markov Assumption）：一个词的出现仅与它之前的若干个词有关。==》 P(w1)P(w2|w1)P(w3|w1w2)…P(wn|w1w2…wn-1)≈P(w1)P(w2|w1)P(w3|w2)…P(wn|wn-1)
# 简化 ⬇️ w1出现时w2出现的概率关系较大(与Wn对比)，因此简化为只计算与w1距离较近的单词出现的概率。
# P(T)=p(w1|begin)*p(w2|w1)*p(w3|w2)***p(wn|wn-1) ～～～2-gram～～～Bi-gram
# P(T)=p(w1|begin1,begin2)*p(w2|w1,begin1)*p(w3|w2w1)***p(wn| wn-1,wn-2) ～～～3-gram～～～Tri-gram
# 如何计算其中每一项的条件概率p(wn|wn-1,wn-2),~~~~~极大似然估计（maximum likelihood Estimation，MLE）~~~~~ 也就是说：数频数
# P(w1|begin)=以w1为开头的所有句子/句子总数；p(w2|w1)=w1,w2同时出现的次数/w1出现的次数
######## 高民权老师视频中对N-gram计算对解释
# gmq公式：P(T)=P(w1)*p(w2)*p(w3)***p(wn)=p(w1|w2w3...wn)*p(w2w3...wn)=p(w1|w2w3...wn)*p(w2|w3...wn)*p(w3w4...wn)=.....
# 极大似然估计 >>>>>p(w1|w2)*p(w2|w3)*p(w3|w4)...p(wn-1|wn)<<<<<～～～2-gram～～～Bi-gram count(w1w2)/count(w2)*count(w2w3)/count(w3)...count(wn-1wn)/count(wn)
# 极大似然估计 >>>>>p(w1|w2w3)*p(w2|w3w4)*p(w3|w4w5)...p(wn-2|wn-1wn)<<<<<～～～3-gram～～～Tri-gram count(w1w2w3)/count(w2w3)
# 设计思路：导入语料库 - 清洗（切割，统计）- 生成n-gram模型

# 导入
STR_PATH = '/Users/damon/文档/kkb/source/article_9k.txt'
with open (STR_PATH,'r',encoding='utf-8') as f:
    corpus = f.read()

# 清洗 ？？jieba分词效果并不理想，如何提高分词准确率？？
def cut_jieba(string):
    return list(jieba.cut(string))
TOKENS = cut_jieba(corpus) ## list like ['我'，'的'，'电脑'....]

words_count = Counter(TOKENS) #字典 key @word， value @count

_2_gram_words = [TOKENS[i] + TOKENS[i + 1] for i in range(len(TOKENS) - 1)]
_2_gram_word_counts = Counter(_2_gram_words)

_3_gram_words = [TOKENS[i] + TOKENS[i+1] + TOKENS[i+2] for i in range(len(TOKENS)-2)]
_3_gram_word_counts =Counter(_3_gram_words)

# 2-gram & 3-gram model
def get_gram_count(word,gram_word_counts):
    if word in gram_word_counts: return gram_word_counts[word]
    else: return gram_word_counts.most_common()[-1][-1] ## list sort like[('的'，241885）....]


def two_gram_model(sentence):
    # 2-gram langauge model
    tokens = cut_jieba(sentence)

    probability = 1

    for i in range(len(tokens) - 1):
        word = tokens[i]
        next_word = tokens[i + 1]

        _two_gram_c = get_gram_count(word + next_word, _2_gram_word_counts)
        _one_gram_c = get_gram_count(next_word, words_count)
        pro = _two_gram_c / _one_gram_c

        probability *= pro

    return probability

def tri_gram_model(sentence):
    # 3-gram langauge model
    tokens = cut_jieba(sentence)

    probability = 1

    for i in range(len(tokens)-2):
        word = tokens[i]
        next_word = tokens[i + 1]
        tri_word = tokens[i + 2]

        _tri_gram_c = get_gram_count(word + next_word + tri_word,_3_gram_word_counts)
        _two_gram_c = get_gram_count(next_word + tri_word,_2_gram_word_counts)
        pro = _tri_gram_c / _two_gram_c

        probability *= pro

    return probability




print("two_gram: %s"%two_gram_model('这个人来自清华大学'))
print("tri_gram: %s"%tri_gram_model('这个人来自清华大学'))

