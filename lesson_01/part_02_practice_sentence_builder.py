import random
import time

navigate_service_step_1 = """
host = 寒暄 ， 询问
寒暄 = 称谓 招呼|招呼|称谓
称谓 = 帅哥|美女|先生|女士
招呼 = 你好|您好|很高兴为您服务
询问 = 简单|复杂
简单 = 告诉我目的地?|我们去哪里?
复杂 = 疑问 具体业务 结尾词
疑问 = 需要我为您
具体业务 = 探索周边|推荐酒店|推荐美食
结尾词 = 吗？
"""
navigate_service_step_2 = """
host = 结果 数字 条线路。 提示
结果 = 已经为你查询到|这里有
数字 = 2|3|4
提示 = 开始 安全|安全
开始 = 准备出发，|导航开始，
安全 = 请系好安全带
"""

def run(pre_str,target,stmt_split='=',or_split='|'):
    rules = dict()
    for line in pre_str.split('\n'):
        if not line:continue
        stmt,expr = line.split(stmt_split)
        rules[stmt.strip()] = expr.split(or_split)
    return sentence_generator(rules,target)


def sentence_generator(rules,target):
    if target in rules:
        condidates = rules[target]
        condidate = random.choice(condidates)
        return ''.join(sentence_generator(rules, target=c.strip()) for c in condidate.split())
    else:
        return target


def generator_n(n):
    n_result = []
    for i in range (1,int(n)+1):
        sent = run(navigate_service_step_1,target='host') + run(navigate_service_step_2,target='host')
        n_result.append(sent)
    return n_result

if __name__ == '__main__':
    n = input('生成多少个句子:')
    generator_n(n)