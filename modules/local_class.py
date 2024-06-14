#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Copyright (C) 2022 WayOn. All rights reserved.
# Filename      : local_class.py
# Description   :  
# Date          : 2024-03-22
# Author        : Li Guoqiang
# Email         : lgq@way-on.com
# Version       : v0.1
# History       : initial version
#--------------------------------------------------

from functools import reduce
import operator

# from modules import utils_wo as ut


def get_number(char):
    count = 0
    for item in char:
        if 0x4E00 <= ord(item) <= 0x9FA5 or 0xFF00 <= ord(item) <=0xFFEF or 0x3000 <= ord(item) <= 0x303F:
            count += 1
    return count


class ParseTable():
    def __init__(self, t):
        self.table = t
        self.length = len(l)
        if cal:
            self.getmin()
            self.getmax()
            self.getsum()
            self.getavg()
            self.getsd()
            self.getmaxlen(handle_chinese)
            self.getminlen(handle_chinese)
    def getmin(self):
        self.min = sorted(self.list)[0]
        return self.min



class ParseList():
    # handle_chinese == True: trace one Chinese char as 2 words length  
    def __init__(self, l, cal=True, handle_chinese=True):
        self.list = l
        self.length = len(l)
        if cal:
            self.getmin()
            self.getmax()
            self.getsum()
            self.getavg()
            self.getsd()
            self.getmaxlen(handle_chinese)
            self.getminlen(handle_chinese)
    def getmin(self):
        self.min = sorted(self.list)[0]
        return self.min
    def getmax(self):
        self.max = sorted(self.list)[-1]
        return self.max
    def getsum(self):
        try:
            self.sum = reduce(lambda x,y : x+y, self.list)
        except:
            self.sum = None
        return self.sum
    def getavg(self):
        try:
            self.avg = reduce(lambda x,y : x+y, self.list)/len(self.list)
        except:
            self.avg = None
        return self.avg
    def getsd(self):
        try: 
            self.avg
        except:
            self.getavg()
        try:
            self.sd = (reduce(operator.add , map (lambda x: (x-self.avg )**2, self.list))/len(self.list))**0.5
        except:
            self.sd = None
        return self.avg
    def getmaxlen(self, handle_chinese=True):
        self.maxlen = None
        for i in self.list:
            i = str(i)
            # print(f'handle_chinese: {handle_chinese}')
            if handle_chinese:
                try:
                    if not self.maxlen:
                        self.maxlen = len(i) + get_number(i) 
                    elif (len(i) + get_number(i)) > self.maxlen:
                        self.maxlen = len(i) + get_number(i)
                except:
                    self.maxlen = len(i) + get_number(i)
                # print(f'== {i}; {self.maxlen}; {get_number(i)} : {len(i)}')
            else:
                try:
                    if not self.maxlen:
                        self.maxlen = len(i)
                    elif len(i) > self.maxlen:
                        self.maxlen = len(i)
                except:
                    self.maxlen = len(i)
        return self.maxlen
    def getminlen(self, handle_chinese=True):
        self.minlen= None
        for i in self.list:
            i = str(i)
            if handle_chinese:
                try:
                    if not self.minlen:
                        self.minlen = len(i) + get_number(i) 
                    elif (len(i) + get_number(i)) < self.minlen:
                        self.minlen = len(i) + get_number(i)
                except:
                    self.minlen = len(i) + get_number(i)
                # print(f'== {i}; {self.minlen}; {get_number(i)} : {len(i)}')
            else:
                try:
                    if not self.minlen:
                        self.minlen = len(i)
                    elif len(i) < self.minlen:
                        self.minlen = len(i)
                except:
                    self.minlen = len(i)
        return self.minlen


class ParseTable():
    def __init__(self, d):
        self.table = d
        self.check_self()
    def check_self(self):
        if 'dict' not in str(type(self.table)):
            ut.print_error(f'target type is out of dict ({type(self)} vs dict). Initialize fail out')
            return -1
        else:
            for k in ["head", "con", "tail"]:
                if k not in self.table:
                    ut.print_error(f'{k} is not in dict. Need key are: head con tail')
                    return -2
        self.h = self.table['head']
        self.c = self.table['con']
        self.t = self.table['tail']
    def row2clm(self):
        c = 0
        clm = dict()
        str_len = []
        # get columx count
        for c in range(len(self.h[0])):
            k = "clm_" + str(c)
            clm[k] = []
            for i in range(len(self.h)):
                clm[k].append(self.h[i][c])
            for i in range(len(self.c)):
                clm[k].append(self.c[i][c])
            for i in range(len(self.t)):
                clm[k].append(self.t[i][c])
        sl_full = 0
        for i in clm:
            try:
                ut.print_debug(f'clm[{i}]: {clm[i]}')
            except:
                pass
            j = ParseList(clm[i], cal=False)
            j.getmaxlen()
            str_len.append(j.maxlen)
            sl_full +=  j.maxlen
        self.r = clm
        self.sl = str_len
        self.sl_full = sl_full
    def tbl_print(self, adj=3):
        self.row2clm()
        self.tbl = []
        cnt = 0
        for i in [self.h, self.c, self.t]:
            for j in i:
                line = []
                k = 0
                for m in j:
                    if k == 0:
                        line.append(f'{m:<{self.sl[k]+adj}}')
                    else:
                        line.append(f'{m:>{self.sl[k]+adj}}')
                    k += 1
                # print("".join(line)) if verbose else None
                line.append("\n")
                self.tbl.append(line)
            # print("-"*(self.sl_full+len(self.sl)*adj)) if cnt == 0 and verbose else None 
            self.tbl.append("-"*(self.sl_full+len(self.sl)*adj)+"\n") if cnt == 0 else None
            # print("="*(self.sl_full+len(self.sl)*adj)) if cnt == 1 and verbose else None
            self.tbl.append("="*(self.sl_full+len(self.sl)*adj)+"\n") if cnt == 1 else None
            cnt += 1
    def __str__(self):
        try:
            self.tbl
        except:
            self.tbl_print()
        t = ""
        for i in self.tbl:
            t = t + "".join(i)
        return t



# ------------------------------------------------------------
# module test section
# ------------------------------------------------------------
if __name__ == '__main__':
    
    print('-'*80)
    print(f'### {"CLASS TEST SECTION":^72} ###')
    print('-'*80)

    print(f'-I- testcase for ParseList')
    l = [1,533,65,-644,-9653,1266]
    l1 = ParseList(l)
    print(f'l1.length : {l1.length}')
    print(f'l1.max    : {l1.max}')
    print(f'l1.min    : {l1.min}')
    print(f'l1.sum    : {l1.sum}')
    print(f'l1.avg    : {l1.avg}')
    print(f'l1.sd     : {l1.sd}')
    
    print(f'')
    print(f'-I- testcase for ParseTable')
    d = dict()
    d['head'] = [["item", 'color', 'weight']]
    d['con'] = [
            ["apple", 'red', '100.9912'],
            ["peach", 'pink', '500.1'],
            ["orange", 'yellow', '300.656'],
            ]
    d['tail'] = [["Fruit", 'MISC', '901.7472']]
    t1 = ParseTable(d)
    t1.tbl_print(adj=4,verbose=True)
 


