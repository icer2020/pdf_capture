#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-


"""
    File        utils
    Author      ICerDev
    Date        2021/9/7 16:03
    Describe    initial version: Common function
    Version     v0.1
    History     v0.1: 2021/9/7 16:03
"""

#############################################################
# local utilities function import and common header template
#############################################################

"""
# -*- coding: utf-8 -*-
import re
import datetime
import argparse
import sys
import os
import time

# local utils.py
sys.path.append("..\99_common")
import utils as ut


# RUN_STATUS:  CRITICAL > ERROR > WARNING > INFO > DEBUG
ut.RUN_STATUS = "DEBUG"

# Version history
ver = 'V0.1'
ver_date = 'August 18, 2021'
ver_des = 'initial version.'
ver_detail_des = 'initial version '
scr_des = "Library Analysis"
starttime = time.time()

ut.ver = ver
ut.ver_date = ver_date
ut.ver_des = ver_des
ut.ver_detail_des = ver_detail_des
ut.scr_des = scr_des
ut.starttime = starttime
"""

import time
import sys
# variable initial
D_CNT = 1
I_CNT = 1
E_CNT = 1
W_CNT = 1
C_CNT = 1
RUN_STATUS = None

scr_des = ''
ver = ''
ver_date = ''
line_width = ''

starttime = time.time()


# ------------------------------------------------------------
# basic function section
# ------------------------------------------------------------
# RUN_STATUS:  CRITICAL > ERROR > WARNING > INFO > DEBUG


def print_debug(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    global RUN_STATUS
    global D_CNT
    if RUN_STATUS == "DEBUG":
        print("D-{0:d} ".format(D_CNT), end="")
        print(*objects,sep=sep, end=end, file=file, flush=flush)
        D_CNT += 1


def print_info(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    global RUN_STATUS
    global I_CNT
    if RUN_STATUS == "DEBUG" or RUN_STATUS == "INFO" or RUN_STATUS == "RUN":
        print("I-{0:d} ".format(I_CNT), end="")
        print(*objects,sep=sep, end=end, file=file, flush=flush)
        I_CNT += 1


def print_warning(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    global RUN_STATUS
    global W_CNT
    if RUN_STATUS == "DEBUG" or RUN_STATUS == "INFO" or RUN_STATUS == "WARNING" or RUN_STATUS == "RUN":
        print("W-{0:d} ".format(W_CNT), end="")
        print(*objects,sep=sep, end=end, file=file, flush=flush)
        W_CNT += 1


def print_error(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    global RUN_STATUS
    global E_CNT
    if (RUN_STATUS == "DEBUG" or RUN_STATUS == "INFO" or RUN_STATUS == "WARNING" or RUN_STATUS == "ERROR"
            or RUN_STATUS == "RUN"):
        print("E-{0:d} ".format(E_CNT), end="")
        print(*objects,sep=sep, end=end, file=file, flush=flush)
        E_CNT += 1


def print_critical(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    global RUN_STATUS
    global C_CNT
    if RUN_STATUS == "DEBUG" or RUN_STATUS == "INFO" or RUN_STATUS == "WARNING" or RUN_STATUS == "ERROR" \
            or RUN_STATUS == "CRITICAL" or RUN_STATUS == "RUN":
        print("C-{0:d} ".format(C_CNT), end="")
        print(*objects,sep=sep, end=end, file=file, flush=flush)
        C_CNT += 1


def ifdef(v):
    try:
        type(eval(v))
    except():
        return 0
    else:
        return 1


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False


def welcome_msg():
    msg = """
/ ----------------------------------------------- /
/       __________             ____               /
/      /  _/ ____/__  _____   / __ \___ _   __    /
/      / // /   / _ \/ ___/  / / / / _ \ | / /    /
/    _/ // /___/  __/ /     / /_/ /  __/ |/ /     /
/   /___/\____/\___/_/     /_____/\___/|___/      /
/ ----------------------------------------------- /
    """
    print(msg)


def header(add_msg=None):
    # global unit
    # global total_time
    global scr_des
    global ver
    global ver_date
    global line_width

    welcome_msg()
    msg_0 = scr_des + " (" + ver + ") " + ver_date

    # additional message
    # msg_2 = "Time unit: " + str(unit)
    # msg_3 = "Time window: " + str(total_time) + str(unit)
    line_width = len(msg_0) + 15  # 计算星号所在行的宽度，作为其他行的对齐基准
    print("#" * (line_width + 8))
    print("### {:^{}} ###".format(msg_0, line_width))
    if add_msg:
        print("### {:^{}} ###".format(add_msg, line_width))
    # print("### {:^{}} ###".format(msg_3, line_width))
    print("#" * (line_width + 8))
    print()
    return 1


def footer():
    import time
    global scr_des
    global ver
    global ver_date

    elapsed_time = time.time() - starttime

    msg_0 = scr_des + " done. Elapase time " + '{:.3f}'.format(float(elapsed_time)) + "s"

    print()
    print("### {:^{}} ###".format(msg_0, line_width))
    return 1


#############################################################
# main example template
#############################################################

'''
# ------------------------------------------------------------
# Running  main
# ------------------------------------------------------------
if __name__ == '__main__':
    # print('start:', datetime.datetime.now())
    # run status:  "DEBUG" || "INFO" || "WARNING" || "ERROR" || "CRITICAL" || "RUN":
    ut.RUN_STATUS = "RUN"

    # additional meg in header for current scripts
    ut.header(add_msg='')

    args = parseargu()
    ut.print_debug('args', args)
    if args.status == "Debug":
        ut.RUN_STATUS = "DEBUG"
        ut.print_info('Run sripts in DEBUG mode')
    # please use main_run instead of main to split the main and __name__ == main (main scripts special variable)
    main_run(in_file=args.input_rtl, out_file=args.output_dump)
    ut.footer()
'''
