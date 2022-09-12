import CD_updater as cd
import cutset as cs
import funct as f

import random
import copy

import math

class var_set:

    def __init__(self, master_clause_ls_, start_clause_ls_, start_var_ls_, set_var_ls_ = None, level = 0, round_count = 4000):
        self.master_clause_ls = master_clause_ls_

        # deciders
        self.available_clause_ls = start_clause_ls_
        self.available_var_ls = start_var_ls_
        self.set_vars_ls = set_var_ls_
        self.level = level

        # changables # this are the starting values tho
        self.batch_size = 10
        self.round_count = round_count
        self.sat_sharp_funct = "dtd"                # 3 options "dtd" (default), "modulo push", "minisat"
        self.var_search_funct = "shared var"        # 2 options "shared var" (default), "neg var"
        self.gen_cd_cutset_search = False           # True or False


    def gen_cutset(self, batch_size_ = 10, rounds_ = 100): #returns big implication ls  # rewrite
        min_cutset = cs.cutset(self.available_clause_ls,self.available_var_ls,batch_size_,starting_point_ = 0)
        min_value = min_cutset.solve()
        for i in range(1, rounds_):
            if (i % 100 == 0):
                print("round: ", i)
            if (i % len(self.available_clause_ls) == 0):
                random.shuffle(self.available_clause_ls)
            comp_cutset = cs.cutset(self.available_clause_ls, self.available_var_ls, batch_size_, i%len(self.available_clause_ls))
            comp_value = comp_cutset.solve()
            if comp_value == 0:
                return comp_cutset
            if (comp_value < min_value):
                min_value = comp_value
                min_cutset, comp_cutset = comp_cutset, min_cutset
            # print(min_value)
            del comp_cutset
        #print("Intial branch value: ", min_value)
        return min_cutset


    def gen_cutset_(self, batch_size_ = 10, rounds_ = 100): # old version !!!!!!!!!! keep

        random.shuffle(self.available_clause_ls)

        if(rounds_ >= len(self.available_clause_ls)):
            rounds_ = len(self.available_clause_ls)
            print("var_set: gen_cutset: rounds reset to ",rounds_)

        min_cutset = cs.cutset(self.available_clause_ls,self.available_var_ls,batch_size_,starting_point_ = 0)
        min_value = min_cutset.solve()
        for i in range(1, rounds_):

            if (i % 100 == 0):
                print("round: ", i)

            comp_cutset = cs.cutset(self.available_clause_ls, self.available_var_ls, batch_size_, i)
            comp_value = comp_cutset.solve()
            if comp_value == 0:
                return comp_cutset
            if (comp_value < min_value):
                min_value = comp_value
                min_cutset, comp_cutset = comp_cutset, min_cutset
            # print(min_value)
            del comp_cutset
        #print("Intial branch value: ", min_value)
        return min_cutset


    def CD_update(self):  # returns true is still sat # returns false if it completes problem
        if (len(self.set_vars_ls) == 0):
            print("error: CD_update: len(set_vars_ls) == 0")
            return True
        old_len = 0
        new_len = len(self.set_vars_ls)
        while (new_len > old_len):
            if cd.update_clause_ls_(self.available_clause_ls, self.set_vars_ls, self.available_var_ls):
                #print("early catch0000")
                return False
            old_len = new_len
            new_len = len(self.set_vars_ls)
        return True

    def tune_parameters(self,parent_var_set): #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4$$
        self.round_count = self.round_count // 2
        #self.batch_size += 2
        #self.sat_sharp_funct = None
        #self.var_search_funct = None
        #self.gen_cd_cutset_search = None
        return 0

    def hard_search(self):  # only at end
        out_ls = []
        arr = [0] * (len(self.available_var_ls) + 1)
        while (arr[-1] == 0):
            add_ls = []
            for i in range(len(self.available_var_ls)):
                add_ls.append(self.available_var_ls[i] * ((arr[i] * 2) - 1))
            new_var_list = add_ls
            if (self.set_vars_ls != None):
                new_var_list += self.set_vars_ls
            if cd.final_verify(self.master_clause_ls, new_var_list):
                out_ls.append(var_set(self.master_clause_ls, [], [], new_var_list))  # empty list cause only runs at end
            f.binary_add(arr, 0)
        return out_ls


    def cutset_cd_search(self):
        out_ls = []
        cutset_ = self.gen_cutset_(self.batch_size,self.round_count)
        for ls in cutset_.implied_ls:
            available_var_ls, set_vars_ls, available_clause_ls = copy.deepcopy(self.available_var_ls), copy.deepcopy(self.set_vars_ls), copy.deepcopy(self.available_clause_ls)
            for var in ls:
                available_var_ls.remove(abs(var))
            if (set_vars_ls == None):
                set_vars_ls = ls
            else:
                set_vars_ls += ls
            a = var_set(self.master_clause_ls, available_clause_ls, available_var_ls, set_vars_ls, level = self.level + 1)
            if a.CD_update():
                a.set_vars_ls.sort(key=lambda x: abs(x))
                a.tune_parameters(self)
                out_ls.append(a)
            else:
                del a
        return out_ls
        #return sorted(out_ls,key=lambda x: len(x.set_vars_ls))


    def next(self):
        if len(self.available_var_ls) < self.batch_size:
            return self.hard_search()
        else:
            return self.cutset_cd_search()


    def print_state(self):
        print("#" * 50)
        print("self.available_clause_ls: ", len(self.available_clause_ls), self.available_clause_ls)
        print("self.available_var_ls: ", len(self.available_var_ls), self.available_var_ls)
        if self.set_vars_ls != None:
            print("self.set_vars_ls: ", len(self.set_vars_ls), self.set_vars_ls)

    ####################################################################################################
    ####################################################################################################

    def test(self, batch_size = 10):
        the_ls = []

        #for i in range(len(self.available_clause_ls)):

        for i in range(10000):
            if (i % 100 == 0):
                print("round: ", i)
            if (i % len(self.available_clause_ls) == 0):
                random.shuffle(self.available_clause_ls)

            cutset_ = cs.cutset(self.available_clause_ls, self.available_var_ls, batch_size, i % len(self.available_clause_ls))
            value_ = cutset_.solve()

            avg = 0
            for ls in cutset_.implied_ls:
                avg += len(ls)
            avg = avg/len(cutset_.implied_ls)
            avg = int(avg * 100)/100
            score = avg - math.log2(value_)
            score = int(score*100)/100
            the_ls.append(['value_: ', value_, ' score: ', score, ' avg: ', avg, cutset_.og_clause_ls])

        the_ls.sort(key = lambda x : x[1])

        for i in range(100):
            print(the_ls[i])