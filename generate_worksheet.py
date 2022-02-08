#!/usr/bin/env python3

import txt_mixin, os, shutil, copy
from numpy.random import rand
import numpy as np
from IPython.core.debugger import Pdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lpr", action="store_true", \
                    help="send math sheets to lpr", \
                    default=False)
parser.add_argument("-w", "--web", action="store_true", \
                    help="open math sheets using python web browser", \
                    default=False)
parser.add_argument("-o", "--okular", action="store_true", \
                    help="open math sheets using okular", \
                    default=False)
parser.add_argument("-j", "--joshua", action="store_true", \
                    help="make math sheets for joshua", \
                    default=False)
parser.add_argument("-s", "--siah", action="store_true", \
                    help="make math sheets for joshua", \
                    default=False)
parser.add_argument("-c", "--cayden", action="store_true", \
                    help="make math sheets for joshua", \
                    default=False)

args = parser.parse_args()

header_list = ['\\documentclass{article}', \
               '\\usepackage[letterpaper, margin=1in]{geometry}', \
               '\\usepackage{tabu,mathtools}', \
               '\\usepackage{tabularx}', \
               '\\setlength\\parindent{10pt}', \
               '\\tabulinesep=_30pt', \
               '\\begin{document}', \
               '\\thispagestyle{empty}', \
               '\\begin{center}', \
               "\\LARGE %TITLE%", \
               '\\end{center}', \
               '\\vspace{-0.3in}', \
               '%%%INSTRUCTIONS%%%', \
               '%\\begin{tabu} to \\linewidth {XXXXX}', \
               '%\\vspace{0.4in}', \
               '\\def \\myspace {0.6in}', \
               '\\def \\mybigspace {0.9in}', \
               '\\Large', \
               '\\begin{tabularx}{\\textwidth}{XXXXX}', \
               '% first line', \
               ]
               
tail_list = ['\\end{tabularx}', \
             '\\end{document}', \
             ]

##########################################################
#
# Recent work on large and small floats to strings:
# (Jan. 2021)
#
##########################################################
def check_fstr(float_in, fstr):
    f2 = float(fstr)
    diff = abs(float_in-f2)
    pdiff = abs(diff/float_in)*100
    if pdiff < 0.01:
        return True
    else:
        return False

def small_float_to_str(float_in, start_exp=6):
    i = int(start_exp)
    fmt = "%0." + str(i) + "f"
    out_str = fmt % float_in
    #print("i = %i, out_str = %s" % (i, out_str))
    while not check_fstr(float_in, out_str):
        i += 1
        fmt = "%0." + str(i) + "f"
        out_str = fmt % float_in
        #print("i = %i, out_str = %s", (i, out_str))
    return out_str



def large_float_to_str(float_in):
    fmt1 = "%0.4g"
    str1 = fmt1 % float_in
    if "e" in str1:
        out_str = "%i" % float_in
    else:
        out_str = str1
    return out_str


def my_float_to_str(float_in):
    fmt0 = "%0.4g"
    str0 = fmt0 % float_in
    if "e" in str0:
        if float_in < 1:
            return small_float_to_str(float_in)
        else:
            return large_float_to_str(float_in)
    else:
        return str0


##########################################################
#
# End of float to string stuff
#
##########################################################

def one_problem(part1, part2, extra_space=True, \
                symbol='+'):
    outlist = []
    out = outlist.append
    
    if extra_space:
        out('\\vspace{\\myspace}')

    out('$\\begin{array}{r}')
    out('%i \\\\' % part1)
    out('%s %i \\\\' % (symbol, part2))
    out('\\hline')
    out('\\end{array}$')

    return outlist


def myrand(mymax=10.0, mymin=1):
    myspan = mymax - mymin
    out = mymin + int(rand()*myspan+0.5)
    return out


def rand_A_for_mul(mymax=10, mymin=0):
    return myrand(mymin, mymin)


def get_two_numbers(mymax=10):
    A = myrand()
    B = myrand()
    while A+B > mymax:
        B = myrand()

    return A, B


def gen_numbers(mymax=10, prev_A=-1, prev_B=-1):
    """Make sure we don't have duplicate problems right after one
    another"""

    A, B = get_two_numbers(mymax)

    while (A==prev_A) and (B==prev_B):
        A, B = get_two_numbers(mymax)

    return A, B


def get_two_numbers_subtract():
    A = myrand()
    B = myrand()
    while A-B < 0:
        B = myrand()

    return A, B


def gen_numbers_subtract(prev_A=-1, prev_B=-1):
    A, B = get_two_numbers_subtract()

    while (A==prev_A) and (B==prev_B):
        A, B = get_two_numbers_subtract()

    return A, B
    
    
def gen_row(N, extra_space=True, symbol='+', mymax=12):
    outlist = []

    first = True
    prev_A = -1
    prev_B = -1
    
    for i in range(N):
        if symbol == '+':
            A, B = gen_numbers(mymax, prev_A=prev_A, prev_B=prev_B)
        elif symbol == '-':
            A, B = gen_numbers_subtract(prev_A=prev_A, prev_B=prev_B)
        if not first:
            outlist.append('&')
            
        curlist = one_problem(A, B, extra_space=extra_space, \
                              symbol=symbol)
        outlist.extend(curlist)
        first = False
        prev_A = A
        prev_B = B
    return outlist


def generate_worksheet(filename, M=5, N=5, case=1, mymax=12):
    if case == 1:
        symbol = '+'
    elif case == 2:
        symbol = '-'

    biglist = []

    extra_space = False
    
    for j in range(M):
        rowlist = gen_row(N, extra_space=extra_space, symbol=symbol, \
                          mymax=mymax)
        biglist.extend(rowlist)
        biglist.extend(['','\\\\',''])
        extra_space = True

    header_list = self.get_header_list()
    body_list = header_list + biglist + tail_list

    txt_mixin.dump(filename, body_list)

    return body_list


class worksheet_generator(object):
    def __init__(self, filename, M=6, N=5, mymax=20, max_A=10, \
                 symbol='+', title="Math Sheet", **kwargs):
        # should worksheet_generator use max_A and max_B to be the
        # base class?
        self.filename = filename
        self.M = M
        self.N = N
        self.mymax = mymax
        self.max_A = max_A
        self.symbol = symbol
        print("self.N = %i" % self.N)
        self.title = title


    def run_latex(self):
        cmd = 'pdflatex %s' % self.filename
        os.system(cmd)

        
    def get_two_numbers(self):
        A = myrand()
        B = myrand()
        
        while A+B > self.mymax:
            B = myrand()

        return A, B


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        A, B = self.get_two_numbers()

        while (A==prev_A) and (B==prev_B):
            A, B = self.get_two_numbers()

        return A, B


    def one_problem(self, part1, part2, extra_space=True, \
                    symbol=None):
        if symbol is None:
            symbol = self.symbol
            
        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{\\myspace}')

        out('$\\begin{array}{r}')
        out('%i \\\\' % part1)
        out('%s %i \\\\' % (symbol, part2))
        out('\\hline')
        out('\\end{array}$')

        return outlist


    def get_header_list(self):
        hl_list = copy.copy(header_list)

        flist = ['%TITLE%']
        replist = [self.title]

        for f, r in zip(flist, replist):
            hl_list = [line.replace(f, r) for line in hl_list]
            
            
        if self.N != 5:
            findstr = "XXXXX"
            repstr = "X"*self.N
            hl_list = [line.replace(findstr, repstr) for line in hl_list]

        return hl_list
        

    def generate_worksheet(self):
        biglist = []

        for j in range(self.M):
            rowlist = self.gen_row()
            biglist.extend(rowlist)
            biglist.extend(['','\\\\',''])


        hl_list = self.get_header_list()
        body_list = hl_list + biglist + tail_list
        
        txt_mixin.dump(self.filename, body_list)

        return body_list


    def gen_row(self):
        outlist = []

        first = True
        prev_A = -1
        prev_B = -1
    
        for i in range(self.N):
            A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)

            if not first:
                outlist.append('&')
            
            curlist = self.one_problem(A, B)
            outlist.extend(curlist)
            first = False
            prev_A = A
            prev_B = B
            
        return outlist


class single_digit_addition(worksheet_generator):
    def get_two_numbers(self):
        A = myrand(mymax=9)
        B = myrand(mymax=9)

        while A+B > self.mymax:
            B = myrand(mymax=9)

        return A, B


class subtraction_generator(worksheet_generator):
    def __init__(self, filename, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '-'
        

    def get_two_numbers(self):
        C = myrand(self.mymax)

        while C == 0:
            C = myrand(self.mymax)
            
        A = myrand(C)

        return C, A


class one_more_generator(worksheet_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = 1
        A = myrand()

        while (A==prev_A):
            A = myrand()
        
        return A, B


class two_more_generator(worksheet_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = 2
        A = myrand()

        while (A==prev_A):
            A = myrand()

        return A, B



class one_less_generator(one_more_generator, subtraction_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = 1
        A = myrand()

        while (A==prev_A) or (A == 0):
            A = myrand()

        return A, B


class two_less_generator(one_less_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = 2
        A = myrand()

        while (A==prev_A) or (A < 2):
            A = myrand()

        return A, B


class one_or_two_less_generator(one_less_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        num = myrand()
        if num > 5.5:
            B = 2
        else:
            B = 1
        A = myrand()

        while (A==prev_A) or (A < B):
            A = myrand()

        return A, B




class multiplication_generator(worksheet_generator):
    def __init__(self, filename, max_B=3, max_A=9, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '\\times '
        self.max_B = max_B
        self.max_A = max_A


    def rand_B(self):
        #def myrand(mymax=10.0, mymin=1):
        return myrand(self.max_B, mymin=0)


    def rand_A(self):
        #def myrand(mymax=10.0, mymin=1):
        return myrand(self.max_A, mymin=0)


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = self.rand_B()
        A = self.rand_A()
            
        while (A==prev_A):
            A = self.rand_A()

        while (B==prev_B):
            B = self.rand_B()

            
        return A, B


class multiply_by_3(multiplication_generator):
    def __init__(self, filename, max_A=9, **kwargs):
        worksheet_generator.__init__(self, filename, max_A=max_A, **kwargs)
        self.symbol = '\\times '
        #self.max_A = max_A


    def rand_A(self):
        #def myrand(mymax=10.0, mymin=1):
        return myrand(self.max_A, mymin=0)


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = 3
        A = self.rand_A()

        while (A==prev_A):
            A = self.rand_A()

        return A, B


class multiply_by_B(multiply_by_3):
    def __init__(self, filename, B=4, max_A=9, N=6, **kwargs):
        worksheet_generator.__init__(self, filename, N=N, max_A=max_A, **kwargs)
        self.symbol = '\\times '
        #self.max_A = max_A
        self.B = B


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = self.B
        A = self.rand_A()

        while (A==prev_A):
            A = self.rand_A()

        return A, B



class multiply_range(multiply_by_B):
    def __init__(self, filename, B_list=[5,6,7], max_A=9, N=6, **kwargs):
        worksheet_generator.__init__(self, filename, N=N, **kwargs)
        self.symbol = '\\times '
        self.max_A = max_A
        self.B_list = B_list
        self.N_B = len(self.B_list)



    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B_ind = int(self.N_B*rand())
        B = self.B_list[B_ind]
        A = self.rand_A()
        
        while (A==prev_A):
            A = self.rand_A()

        return A, B
        


class multiply_fraction_by_powers_of_ten(multiply_range):
    def __init__(self, filename, B_list=[10,100,1000], max_A=30, \
                 M=3, N=2, **kwargs):
        multiply_range.__init__(self, filename, B_list=B_list, max_A=max_A, \
                                M=M, N=N, **kwargs)
        f1 = '\\def \\myspace {0.6in}'
        r1 = '\\def \\myspace {1.2in}'
        f2 = '\\Large'
        r2 = '\\huge'
        self.header_find_list = [f1,f2]
        self.header_replace_list = [r1,r2]


    def get_header_list(self):
        hl_list = multiply_range.get_header_list(self)
        outlist = copy.copy(hl_list)
        for f,r in zip(self.header_find_list, self.header_replace_list):
            outlist = [line.replace(f,r) for line in outlist]
        return outlist


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B_ind = int(self.N_B*rand())
        B = self.B_list[B_ind]
        A = self.max_A*rand()

        while (A==prev_A):
            A = self.rand_A()

        return A, B



    def one_problem(self, part1, part2, extra_space=True, \
                    symbol=None):
        if symbol is None:
            symbol = self.symbol

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{\\myspace}')

        out('$\\begin{array}{r}')
        out('%0.4g \\\\' % part1)
        out('%s %i \\\\' % (symbol, part2))
        out('\\hline')
        out('\\end{array}$')

        return outlist


class vertical_math_problem(object):# mix in class with no other methods to avoid inheritance problems
    def get_symbol(self):
        symbol_rand = rand()

        if symbol_rand < 0.5:
            symbol = '\\times '
            divide = False
        else:
            symbol = ' \\div '
            divide = True
        return symbol, divide



    def one_problem(self, part1, part2, extra_space=True, \
                    symbol=None):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{\\myspace}')

        out('$\\begin{array}{r}')
        out('%0.4g \\\\' % part1)
        out('%s %i \\\\' % (symbol, part2))
        out('\\hline')
        out('\\end{array}$')

        return outlist


class multiply_or_divide_decimal_by_powers_of_ten_vertical(vertical_math_problem):
    pass


class vertical_mul_only(vertical_math_problem):# mix in class with minimal methods to avoid inheritance problems
    def get_symbol(self):
        symbol = '\\times '
        divide = False
        return symbol, divide


class problem_with_random_A_and_B(worksheet_generator):
    def __init__(self, filename, max_A=10, max_B=10, \
                 M=3, N=2, **kwargs):
        worksheet_generator.__init__(self, filename, M=M, N=N, \
                                     **kwargs)
        self.max_A = max_A
        self.max_B = max_B

        
    def rand_B(self):
        return myrand(self.max_B, mymin=0)


    def rand_A(self):
        return myrand(self.max_A, mymin=0)


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = self.rand_B()
        A = self.rand_A()

        while (A==prev_A):
            A = self.rand_A()

        while (B==prev_B):
            B = self.rand_B()
        return A, B


class mul_3_digits_by_1_digit_vertical(vertical_mul_only, problem_with_random_A_and_B):
    def __init__(self, filename, max_A=1000, max_B=10, \
                 M=5, N=4, **kwargs):
        problem_with_random_A_and_B.__init__(self, filename, max_A=max_A, max_B=max_B, \
                                             M=M, N=N, **kwargs)
    
                                       
class multiply_fraction_horizontal(multiply_fraction_by_powers_of_ten):
    def __init__(self, filename, B_list=[10,100,1000], max_A=30, \
                 M=7, N=1, **kwargs):
        multiply_fraction_by_powers_of_ten.__init__(self, filename, B_list=B_list, max_A=max_A, \
                                                    M=M, N=N, **kwargs)
        self.header_find_list.append('\\vspace{-0.3in}')
        self.header_replace_list.append('%%%%')

    
    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        if symbol is None:
            symbol = self.symbol

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')


        pat = '$%0.4g \\; %s \\; %s \\; = \;$  \\rule{5EM}{1pt}'
        lineout = pat % (part1, symbol, part2)
        out(lineout)

        return outlist

    

class multiply_fraction_horizontal_with_blanks(multiply_fraction_horizontal):
    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        if symbol is None:
            symbol = self.symbol

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')


        blank_rand = rand()
        if blank_rand < 0.5:
            has_blank = True
        else:
            has_blank = False

        if has_blank:
            p1str ="%0.4g" % float(part1)
            p1f = float(p1str)
            p2 = float(part2)
            ans = p1f*p2
            pat = '$%0.4g \\; %s \\; \\rule{5EM}{1pt} \\; = \; %0.4g$'
            lineout = pat % (part1, symbol, ans)
        else:
            pat = '$%0.4g \\; %s \\; %s \\; = \;$  \\rule{5EM}{1pt}'
            lineout = pat % (part1, symbol, part2)
            
        out(lineout)

        return outlist


class multiply_or_divide_decimal_horizontal_with_blanks(multiply_fraction_horizontal_with_blanks):
    def one_problem(self, part1, part2, extra_space=True, **kwargs):
        symbol_rand = rand()

        if symbol_rand < 0.5:
            symbol = '\\times '
            divide = False
        else:
            symbol = ' \\div '
            divide = True
            

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')


        blank_rand = rand()
        if blank_rand < 0.5:
            has_blank = True
        else:
            has_blank = False

        if has_blank:
            p1str ="%0.4g" % float(part1)
            p1f = float(p1str)
            p2 = float(part2)
            if divide:
                ans = p1f/p2
            else:
                ans = p1f*p2
            pat = '$%0.4g \\; %s \\; \\rule{5EM}{1pt} \\; = \; %0.4g$'
            lineout = pat % (part1, symbol, ans)
        else:
            pat = '$%0.4g \\; %s \\; %s \\; = \;$  \\rule{5EM}{1pt}'
            lineout = pat % (part1, symbol, part2)

        out(lineout)

        return outlist



class multiply_or_divide_horiz_large_exponents_blanks(multiply_or_divide_decimal_horizontal_with_blanks):
    """Note that in this class, B is an exponent of ten"""
    def __init__(self, filename, B_list=[1,2,3,4,5,6,7], max_A=3000, \
             M=7, N=1, **kwargs):
        multiply_or_divide_decimal_horizontal_with_blanks.__init__(self, filename, B_list=B_list, max_A=max_A,
                                                                  M=M, N=N, **kwargs)


    def get_ans_str(self, part1, part2, divide=False):
        p1str ="%0.4g" % float(part1)# These two lines are a form of rounding
        p1f = float(p1str)
        #print("part2 = %s" % part2)
        p2 = 10**(float(part2))
        if divide:
            ans = p1f/p2
        else:
            ans = p1f*p2
        ans_str = my_float_to_str(ans)
        return ans_str
        

    def get_symbol(self):
        symbol_rand = rand()

        if symbol_rand < 0.5:
            symbol = '\\times '
            divide = False
        else:
            symbol = ' \\div '
            divide = True
        return symbol, divide


    def get_blank(self):
        blank_rand = rand()
        if blank_rand < 0.5:
            has_blank = True
        else:
            has_blank = False
        return has_blank
    

    def one_problem(self, part1, part2, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')

        has_blank = self.get_blank()

        
        if has_blank:
            ans_str = self.get_ans_str(part1, part2, divide=divide)
            pat = '$%0.4g \\; %s \\; \\rule{5EM}{1pt} \\; = \; %s$'
            lineout = pat % (part1, symbol, ans_str)
        else:
            if float(part2) > 1.5:
                pat = '$%0.4g \\; %s \\; 10^{%s} \\; = \;$  \\rule{5EM}{1pt}'
                lineout = pat % (part1, symbol, part2)
            else:
                pat = '$%0.4g \\; %s \\; 10 \\; = \;$  \\rule{5EM}{1pt}'
                lineout = pat % (part1, symbol)

        out(lineout)

        return outlist


class word_problem_multiply_version_1(multiply_or_divide_horiz_large_exponents_blanks):
    def get_symbol(self):
        symbol = ' times '
        divide = 0
        return symbol, divide


    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')


        p1str = my_float_to_str(part1)

        if float(part2) > 1.5:
            part2str = '10^{%s}' % part2
        else:
            part2str = '10'

        pat = '$%s \\textrm{%s}  %s \\textrm{ is }  \\rule{10EM}{1pt}$.'
        lineout = pat % (p1str, symbol, part2str)
        out(lineout)

        return outlist

    

class word_problem_multiply_version_1_with_blanks(word_problem_multiply_version_1):
    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')

        has_blank = self.get_blank()
            
        p1str = my_float_to_str(part1)


        if has_blank:
            p1str ="%0.4g" % float(part1)# These two lines are a form of rounding
            p1f = float(p1str)
            #print("part2 = %s" % part2)
            p2 = 10**(float(part2))
            if divide:
                ans = p1f/p2
            else:
                ans = p1f*p2
            ans_str = my_float_to_str(ans)
            pat = '$%s \\textrm{%s} \\rule{7EM}{1pt} \\textrm{ is } %s$.'
            lineout = pat % (p1str, symbol, ans_str)
        else:
            if float(part2) > 1.5:
                part2str = '10^{%s}' % part2
            else:
                part2str = '10'
                
            pat = '$%s \\textrm{%s}  %s \\textrm{ is }  \\rule{10EM}{1pt}$.'
            lineout = pat % (p1str, symbol, part2str)

        out(lineout)

        return outlist


class word_problem_multiply_version_2_ans_on_left(word_problem_multiply_version_1):
    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')

        p1str = my_float_to_str(part1)

        if float(part2) > 1.5:
            part2str = '10^{%s}' % part2
        else:
            part2str = '10'

        has_blank = self.get_blank()

        if has_blank:
            ans_str = self.get_ans_str(part1, part2, divide=divide)
            pat = '$%s \\textrm{ is } \\rule{7EM}{1pt} \\textrm{%s}  %s$.'
            lineout = pat % (ans_str, symbol, p1str)
        else:
            pat = '$\\rule{10EM}{1pt} \\textrm{ is } %s \\textrm{%s}  %s$.'
            lineout = pat % (part2str, symbol, p1str)
        out(lineout)

        return outlist



class word_problem_multiply_version_2_ans_on_left_with_blanks(word_problem_multiply_version_2_ans_on_left):
    def one_problem(self, part1, part2, symbol=None, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')


        p1str = my_float_to_str(part1)

        if float(part2) > 1.5:
            part2str = '10^{%s}' % part2
        else:
            part2str = '10'

            ans_str = self.get_ans_str(part1, part2, divide=divide)

        pat = '$\\rule{10EM}{1pt} \\textrm{ is } %s \\textrm{%s}  %s$.'
        lineout = pat % (part2str, symbol, p1str)
        out(lineout)

        return outlist



class round_to_tens_three_digit(multiply_or_divide_horiz_large_exponents_blanks):
    def __init__(self, filename, B_list=[1,2,3,4,5,6,7], max_A=1000, \
                 min_A=10, M=7, N=2, **kwargs):
        multiply_or_divide_horiz_large_exponents_blanks.__init__(self, filename, B_list=B_list, \
                                                                 max_A=max_A,
                                                                 M=M, N=N, **kwargs)
        self.min_A = min_A


    def get_header_list(self):
        hl_list = multiply_or_divide_horiz_large_exponents_blanks.get_header_list(self)
        mylist = ["{\\Large Round the numbers below to the tens place:\\\\}", \
                  ]
        ind = hl_list.index('%%%INSTRUCTIONS%%%')
        hl_list[ind:ind] = mylist
        return hl_list

    
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        #B_ind = int(self.N_B*rand())
        #B = self.B_list[B_ind]
        B = 7# don't care and won't use it for now
        A = int(self.max_A*rand())

        while (A==prev_A) or (A < self.min_A):
            A = self.rand_A()
        return A, B


    def one_problem(self, part1, part2, extra_space=True, **kwargs):
        symbol, divide = self.get_symbol()

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{1EM}')

        has_blank = self.get_blank()

        pat = '$%i \\; \\rightarrow \\; \\rule{5EM}{1pt}$'
        lineout = pat % (part1)
        out(lineout)

        return outlist
    


class divide_fraction_horizontal(multiply_fraction_horizontal):
    def __init__(self, filename, B_list=[10,100,1000], max_A=100, \
                 M=7, N=1, **kwargs):
        multiply_fraction_horizontal.__init__(self, filename, B_list=[10,100,1000], max_A=max_A, \
                                                    M=M, N=N, **kwargs)
        self.symbol = ' \\div '
    
    
class add_big_to_little(multiply_by_B):
    def __init__(self, filename, B_list=[1,2,3], max_A=1000, min_A=99, N=6, **kwargs):
        worksheet_generator.__init__(self, filename, N=N, **kwargs)
        self.symbol = '+'
        self.max_A = max_A
        self.min_A = min_A
        self.B_list = B_list
        self.N_B = len(self.B_list)
        self.delta_A = self.max_A - self.min_A


    def rand_A(self):
        return myrand(self.max_A, self.min_A)
    

    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""
        
        B_ind = int(self.N_B*rand())
        B = self.B_list[B_ind]
        A = self.rand_A()
            
        while (A==prev_A):
            A = self.rand_A()
            
        return A, B


class multiply_by_2_or_3(multiplication_generator):
    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        nB = rand()
        if nB < 0.5:
            B = 2
        else:
            B = 3
            
        A = self.rand_A()

        while (A==prev_A):
            A = self.rand_A()

        return A, B


class multiplication_intro_generator(multiply_by_3):
    def __init__(self, filename, B=3, max_A=9, **kwargs):
        worksheet_generator.__init__(self, filename, max_A=max_A, **kwargs)
        self.symbol = '\\times '
        #self.max_A = max_A
        self.B = B



    def gen_numbers(self, prev_A=-1, prev_B=-1):
        """Make sure we don't have duplicate problems right after one
        another"""

        B = self.B
        A = self.rand_A()

        while (A==prev_A):
            A = self.rand_A()

        return A, B


    def gen_specified_row(self, A_list):
        outlist = []

        first = True
        prev_A = -1
        prev_B = -1
    
        for A in A_list:
            if not first:
                outlist.append('&')
            
            curlist = self.one_problem(A, self.B)
            outlist.extend(curlist)
            first = False
            prev_A = A
            prev_B = self.B
            
        return outlist


    def generate_worksheet(self):
        # generate x0 - x4 as first row
        # and x5 - x9 as the second row
        # then generate random rows
        biglist = []

        row0 = self.gen_specified_row([0,1,2,3,4])
        biglist.extend(row0)
        biglist.extend(['','\\\\',''])
        row1 = self.gen_specified_row([5,6,7,8,9])
        biglist.extend(row1)
        biglist.extend(['','\\\\',''])
        
        
        for j in range(self.M-2):
            rowlist = self.gen_row()
            biglist.extend(rowlist)
            biglist.extend(['','\\\\',''])


        header_list = self.get_header_list()
        body_list = header_list + biglist + tail_list

        txt_mixin.dump(self.filename, body_list)

        return body_list



class mixed_add_subtract(worksheet_generator):
    def __init__(self, filename, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '\\times '
        self.max_B = 10
        self.max_A = 10


    def get_two_numbers(self):
        #def myrand(mymax=10.0, mymin=1):
        A = myrand(self.max_A)
        B = myrand(self.max_B)

        #while A+B > self.mymax:
        #    B = myrand()
        return A, B

    
    def gen_row(self):
        outlist = []

        first = True
        prev_A = -1
        prev_B = -1

        for i in range(self.N):
            A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)

            if not first:
                outlist.append('&')

            sym_num = rand()
            if sym_num > 0.5:
                symbol = '-'
            else:
                symbol = '+'

            curlist = self.one_problem(A, B, symbol=symbol)
            outlist.extend(curlist)
            first = False
            prev_A = A
            prev_B = B

        return outlist



class variable_add_subtract(worksheet_generator):
    def __init__(self, filename, add_thresh=0.9, allow_neg=False, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '\\times '
        self.max_B = 10
        self.max_A = 10
        self.add_thresh = add_thresh
        self.allow_neg = allow_neg


    def gen_row(self):
        outlist = []

        first = True
        prev_A = -1
        prev_B = -1
        
        for i in range(self.N):
            A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)

            if not first:
                outlist.append('&')

            sym_num = rand()
            if sym_num > self.add_thresh:
                symbol = '-'
                while (not self.allow_neg and B > A):
                    A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)
            else:
                symbol = '+'

            curlist = self.one_problem(A, B, symbol=symbol)
            outlist.extend(curlist)
            first = False
            prev_A = A
            prev_B = B

        return outlist



class subtraction_force_negative(variable_add_subtract):
    def gen_row(self):
        outlist = []

        first = True
        prev_A = -1
        prev_B = -1

        for i in range(self.N):
            A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)

            if not first:
                outlist.append('&')

            symbol = '-'
            while (B < A):
                    A, B = self.gen_numbers(prev_A=prev_A, prev_B=prev_B)

            curlist = self.one_problem(A, B, symbol=symbol)
            outlist.extend(curlist)
            first = False
            prev_A = A
            prev_B = B

        return outlist





class addition_level_2(worksheet_generator):
    def __init__(self, filename, max_A=20, max_B=10, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '+'
        self.max_B = max_B
        self.max_A = max_A


    def get_two_numbers(self):
        #def myrand(mymax=10.0, mymin=1):
        A = myrand(self.max_A)
        B = myrand(self.max_B)

        #while A+B > self.mymax:
        #    B = myrand()
        return A, B


class addition_within_20(worksheet_generator):
    def __init__(self, filename, max_A=20, max_B=10, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '+'
        self.max_B = max_B
        self.max_A = max_A


    def get_two_numbers(self):
        #def myrand(mymax=10.0, mymin=1):
        ans = myrand(20)
        A = myrand(ans-1)
        B = ans-A

        #while A+B > self.mymax:
        #    B = myrand()
        return A, B




class addition_two_digit_plus_single_digit(worksheet_generator):
    def __init__(self, filename, max_A=20, min_A=10, max_B=10, **kwargs):
        worksheet_generator.__init__(self, filename, **kwargs)
        self.symbol = '+'
        self.max_B = max_B
        self.max_A = max_A
        self.min_A = min_A


    def get_two_numbers(self):
        #def myrand(mymax=10.0, mymin=1):
        span_A = self.max_A - self.min_A
        A = myrand(span_A) + self.min_A
        B = myrand(self.max_B)

        #while A+B > self.mymax:
        #    B = myrand()
        return A, B



class addition_easy_to_medium(worksheet_generator):
    def get_two_numbers(self):
        #def myrand(mymax=10.0, mymin=1):
        difficulty = rand()

        if difficulty < 0.5:
            # easy
            A = myrand(7)
            B = myrand(5)
        elif difficulty < 0.75:
            A = myrand(10)
            B = myrand(9)
        else:
            A = myrand(20)
            B = myrand(9)
            
        return A, B


def get_rand_list_entry(listin):
    N = len(listin)
    ind = int(np.floor(np.random.random()*N))
    ent = listin[ind]
    return ent


class improper_fractions_gen(worksheet_generator):
    def __init__(self, filename, M=5, N=3, mymax=20, \
                 den_list=[2,3,4], whole_list=[1,2,3,4], **kwargs):
        worksheet_generator.__init__(self, filename, M=M, N=N, **kwargs)
        self.den_list = den_list
        self.whole_list = whole_list


    def gen_numbers(self, prev_A=-1, prev_B=-1):
        ### B is the num, A is the den
        den = get_rand_list_entry(self.den_list)
        whole = get_rand_list_entry(self.whole_list)
        extra_num = int(np.floor(np.random.random()*den))
        num = whole*den + extra_num
        return num, den
    
        
    def one_problem(self, part1, part2, extra_space=True, \
                        symbol=None):
        ###A, B = gen_numbers(mymax, prev_A=prev_A, prev_B=prev_B)
        #elif symbol == '-':
        #    A, B = gen_numbers_subtract(prev_A=prev_A, prev_B=prev_B)
        #if not first:
        #    outlist.append('&')

        #curlist = one_problem(A, B, extra_space=extra_space, \
        #                      symbol=symbol)
        
        if symbol is None:
            symbol = self.symbol

        outlist = []
        out = outlist.append

        if extra_space:
            out('\\vspace{\\mybigspace}')

        #out('$\\displaystyle \\frac{%s}{%s} = $ \\hspace{2EM}\\rule{3EM}{1pt}' % (part1, part2))
        out('$\\displaystyle \\frac{%s}{%s} = $' % (part1, part2))
        return outlist

    
def generate_number_bonds(save_num=1):
    nb_dir = 'number_bonds'
    os.chdir(nb_dir)
    cmd3 = 'generate_number_bonds.py'
    os.system(cmd3)
    out3 = 'number_bonds_auto_1.pdf'
    name_top = '../number_bonds_%i.pdf' % save_num
    shutil.copy(out3, name_top)

    os.chdir('..')

    return name_top



import datetime
now = datetime.datetime.now()
datestr = now.strftime('%m_%d_%y')
import time

def process_one_batch(mylist, title, lpr=False, web=False, okular=False):
    for row in mylist:
        myclass = row[0]
        fn = row[1]
        if len(row) == 2:
            kwargs = {}
        else:
            kwargs = row[2]
        myworksheet = myclass(fn, title=title, **kwargs)
        myworksheet.generate_worksheet()
        myworksheet.run_latex()

        fno, ext = os.path.splitext(fn)
        pdf_name = fno + '.pdf'

        if web:
            pcmd = "python3 -m webbrowser %s &" % pdf_name
            #pcmd = "okular %s" % pdf_name
            os.system(pcmd)
            time.sleep(0.5)

        if okular:
            #pcmd = "python3 -m webbrowser %s &" % pdf_name
            pcmd = "okular %s &" % pdf_name
            os.system(pcmd)
            time.sleep(0.2)
            
        if lpr:
            pcmd = "lpr %s &" % pdf_name
            os.system(pcmd)


siah_list = [(multiplication_intro_generator, 'multiply_by_3_intro.tex'), \
             #(multiplication_intro_generator, 'multiply_by_2_intro.tex', {'B':2}), \
             (multiplication_intro_generator, 'multiply_by_4_intro.tex', {'B':4}), \
             (multiplication_intro_generator, 'multiply_by_5_intro.tex', {'B':5}), \
             #(multiplication_intro_generator, 'multiply_by_4_intro.tex', {'B':4}), \
             #(multiply_range, 'multiply_by_2_thru_4_%s.tex' % datestr, {'B_list':[2,3,4]}), \
             #(subtraction_force_negative, 'neg_subtract_1.tex', {}), \
             #(add_big_to_little, 'add_big_to_little.tex', {}), \
             #(addition_within_20, "addition_within_20_siah_1.tex",{}), \
             #(subtraction_generator,'subtraction_within_20_siah_1.tex',{'mymax':20}), \
             #(addition_level_2,'addition_new_2_siah.tex',{'max_A':30, 'max_B':20}), \
            ]

cayden_list = [(addition_level_2,'addition_new_2.tex',{'max_A':30, 'max_B':20}), \
               (addition_within_20, "addition_within_20_p_1.tex",{}), \
               (addition_within_20, "addition_within_20_p_2.tex",{}), \
               (subtraction_generator,'subtraction_within_20_p_1.tex',{'mymax':20}), \
               (subtraction_generator,'subtraction_within_20_p_2.tex',{'mymax':20}), \
              ]


joshua_list = [(multiply_by_B, 'multiply_by_8_%s.tex' % datestr, {'B':8}), \
               (multiply_by_B, 'multiply_by_9_%s.tex' % datestr, {'B':9}), \
               (multiply_range, 'multiply_by_5_thru_9_%s.tex' % datestr, {'B_list':[5,6,7,8,9]}), \
               (improper_fractions_gen, "imp_frac_1_%s.tex" % datestr), \
               (multiply_fraction_horizontal, "decimal_powers_h.tex", {}), \
              ]

Jlist2 = [#(multiply_fraction_horizontal, "decimal_powers_h.tex", {}), \
          #(divide_fraction_horizontal, "decimal_divide_powers_h.tex", {}), \
          #(multiply_fraction_horizontal_with_blanks, "decimal_mult_w_blanks.tex", {}), \
          #(multiply_range, 'multiply_by_5_thru_9_%s.tex' % datestr, {'B_list':[5,6,7,8,9]}), \
          #(improper_fractions_gen, "imp_frac_1_%s.tex" % datestr), \
          #(multiply_or_divide_decimal_horizontal_with_blanks, "decimal_mult_or_div_with_blanks.tex"), \
          #(multiply_or_divide_horiz_large_exponents_blanks, "decimal_mult_or_div_large_exp_with_blanks.tex"), \
          #(multiply_or_divide_decimal_by_powers_of_ten_vertical, "decimal_mult_or_div_vert.tex"), \
          (word_problem_multiply_version_1, "word_problems_mult_v1.tex"), \
          (word_problem_multiply_version_1_with_blanks, "word_problems_mult_v1_with_blanks.tex"), \
          (word_problem_multiply_version_2_ans_on_left, "word_problems_mult_v2_ans_left_no_blanks.tex"), \
          (word_problem_multiply_version_2_ans_on_left_with_blanks, "word_problems_mult_v2_ans_left_with_blanks.tex"), \
          ]

Jlist3 = [#(round_to_tens_three_digit, 'rouding_to_tens.tex'), \
          (mul_3_digits_by_1_digit_vertical, "mul_3_digits_by_1_vert.tex"), \
          (mul_3_digits_by_1_digit_vertical, "mul_2_digits_by_1_vert.tex", {"max_A":100}), \
          ]

web = args.web
lpr = args.lpr
okular = args.okular

if args.siah:
    nums = [4,6,7,8]
    mylist = []
    for num in nums:
        for i in range(1):
            j = i+1
            fn = 'multiply_by_%i_intro_%i.tex' % (num, j)
            cur_tup = (multiplication_intro_generator, fn, {'B':num})
            mylist.append(cur_tup)

    process_one_batch(mylist, title="Josiah's Math Sheets", lpr=lpr, web=web, okular=okular)
    
#    process_one_batch(siah_list, title="Josiah's Math Sheets", lpr=lpr, web=web, okular=okular)
    
if args.cayden:
    process_one_batch(cayden_list, title="Cayden's Math Sheets", lpr=lpr, web=web, okular=okular)

if args.joshua:
    #process_one_batch(Jlist3, title="Joshua's Math Sheets", lpr=lpr, web=web, okular=okular)
    process_one_batch(joshua_list, title="Joshua's Math Sheets", lpr=lpr, web=web, okular=okular)
