import random
import jieba
from collections import Counter

# Pattern Based AI
# 怎么样生成语言（pattern）==（target）～～输出递归规律（模式）的～～str or formula（公式）
# sample func
hello_to_someone = """
say_hello = name hello
name = Jhon|Mike|老梁
hello = 你好|您来了|快请进
"""
def name():
    return random.choice('Jhon | Mike | 老梁'.split('|'))
def hello():
    return random.choice('你好 | 您来了 | 快请进'.split('|'))
def say_hello():
    return name() + ',' + hello()

print('[sample func]: %s'%say_hello())

# conplicated func
def get_generation_by_gram(grammar_str:str,target,stmt_split='=',or_split='|'):
    rules = dict() # key is the @statement,value is @expression
    for line in grammar_str.split('\n'):
        if not line:continue #skip the empty line
        stmt,expr = line.split(stmt_split)
        rules[stmt.strip()] = expr.split(or_split)
    generated = generate(rules,target=target)
    return generated

def generate(grammar_rule,target):
    if target in grammar_rule:
        condidates = grammar_rule[target]
        condidate = random.choice(condidates)
        return ''.join(generate(grammar_rule,target=c.strip()) for c in condidate.split())
    else:
        return target

simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => Adj | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的"""

print('[sentence]: %s'%get_generation_by_gram(simple_grammar,target='sentence',stmt_split='=>',or_split='|'))


simpel_programming = '''
if_stmt => if ( cond ) { stmt }
cond => var op var
op => > | == | < | >= | <= 
stmt => assign | if_stmt
assign => var = var
var =>  char var | char
char => a | b |  c | d | 0 | 1 | 2 | 3
'''

print('[if_stmt]: %s'%get_generation_by_gram(simpel_programming, target='if_stmt', stmt_split='=>'))

