#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
V ： 置換規則（後述の P ）により順次置き換えられてゆく変数の集合。
S ： 計算が進んでも変化しない定数の集合。
ω ： システムの初期状態を示すV の要素からなる文字列。
P ： V を変化させてゆく置換規則の集合。
"""
def attributesFromDict(d):
        self = d.pop("self")
        for n, v in d.iteritems():
            setattr(self, n, v)

import re
def multiple_replace(text, adict):
    rx = re.compile("|".join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

class Lsystem():
    def __init__(self, Variavles=None, Constants=None, Start=None, Rules=None):
        attributesFromDict(locals())
        try:
            self.replacementRules = dict(zip([k for k, v in self.Rules], [v for k, v in self.Rules]))
        except TypeError:
            self.replacementRules = None
    def Algae(self):
        return Lsystem(["A", "B"], None, "A", [("A", "AB"), ("B", "A")])
    def Tree(self):
        return Lsystem(["0", "1"], ["[", "]"], "0", [("1", "11"), ("0", "1[0]0")])
    def Fibonacci_number(self):
        return Lsystem(["A", "B"], None, "A", [("A", "B"), ("B", "AB")])
    def Koch(self):
        return Lsystem(["F"], ["+", "-"], "F", [("F", "F+F-F-F+F")])
    def Cantor(self):
        return Lsystem(["A", "B"], None, "A", [("A", "ABA"), ("B", "BBB")])
    def Sierpinski(self):
        return Lsystem(["A", "B"], ["+", "-"], "A", [("A", "B-A-B"), ("B", "A+B+A")])
    def generate(self, n=1, mute=False):
        strings = self.Start
        if not mute:
            print "0:"+strings
            for num, i in enumerate(range(n)):
                strings = multiple_replace(strings, self.replacementRules)
                print str(num+1)+":"+strings
        else:
            for num, i in enumerate(range(n)):
                strings = multiple_replace(strings, self.replacementRules)
        return strings

if __name__ == "__main__":
    import turtle
    turtle.speed(0)

    test = Lsystem().Sierpinski()
    test_out = test.generate(10)
    for s in test_out:
        if s == "A" or s == "B":
            turtle.fd(1)
        elif s == "-":
            turtle.lt(60)
        elif s == "+":
            turtle.rt(60)
