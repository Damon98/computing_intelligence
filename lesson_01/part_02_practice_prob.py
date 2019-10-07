from collections import Counter

import jieba
import pandas as pd

from part_02_practice_sentence_builder import *

fields=['comment']
source_path = '/Users/damon/文档/kkb/source/movie_comments.csv'
df = pd.read_csv(source_path,skipinitialspace=True, usecols=fields)

# print(len(df[fields[0]]))
# print(type(df[fields[0]][0]))
corpus = ",".join(df[fields[0]][i].replace(' ','').replace('，',',') if type(df[fields[0]][i]) == str else '' for i in range(len(df[fields[0]])-1))

def cut_jieba(string):
    return list(jieba.cut(string))

TOKENS = list(jieba.cut(corpus))
words_count = Counter(TOKENS)

_2_gram_words = [TOKENS[i] + TOKENS[i + 1] for i in range(len(TOKENS) - 1)]
_2_gram_word_counts = Counter(_2_gram_words)

_3_gram_words = [TOKENS[i] + TOKENS[i+1] + TOKENS[i+2] for i in range(len(TOKENS)-2)]
_3_gram_word_counts =Counter(_3_gram_words)

def get_gram_count(word,gram_word_counts):
    if word in gram_word_counts: return gram_word_counts[word]
    else: return gram_word_counts.most_common()[-1][-1]

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



if __name__ == '__main__':
    # n = input('生成多少个句子:')
    n_result = generator_n(n=10)
    new_result = []
    for item in n_result:
        scr = two_gram_model(item)
        new_result.append((scr,item))
    result = sorted(new_result, key=lambda x: x[0])
    print(result)
    print(result[-1][1])