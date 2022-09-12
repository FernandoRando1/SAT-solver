import var_set as vs
import funct as f
import CD_updater as cd

import copy

class flash:

    def __init__(self, input_filename_, output_filename_ = None, BFS = False, intial_round_count = None):
        self.input_filename = input_filename_
        self.var_set_stack = []  # the back is the front!!!!!!!!!!!!!!!
        if output_filename_ == None:
            self.output_filename = "out_.txt"
        else:
            self.output_filename = output_filename_
        self.master_clause_ls, self.max_var = f.load_clause(self.input_filename)
        self.backup_master_clause_ls = copy.deepcopy(self.master_clause_ls)
        self.master_var_ls = list(range(1, 1 + self.max_var))
        self.answers = []
        self.BFS = BFS
        if intial_round_count == None:
            self.round_count = len(self.master_var_ls)
        else:
            self.round_count = intial_round_count



    def clear_file(self):
        file = open(self.output_filename, "w")
        file.close()


    def start(self):
        self.var_set_stack.append(vs.var_set(self.master_clause_ls,self.master_clause_ls, self.master_var_ls, set_var_ls_ = None, round_count=self.round_count))
        #print("ahh: ",self.var_set_stack[0].available_var_ls)


    def update(self): # adds to var_set_stack (note: end at front)
        if self.BFS:
            var_set_ = self.var_set_stack.pop(0)
        else:
            var_set_ = self.var_set_stack.pop()
        if len(var_set_.available_var_ls) == 0:
            var_set_.set_vars_ls.sort(key=lambda x: abs(x))
            self.answers.append(var_set_.set_vars_ls)
        else:
            ls = sorted(var_set_.next(), key = lambda x : (2*int(not self.BFS)-1) * len(x.set_vars_ls))
            self.var_set_stack += ls
            if(var_set_.set_vars_ls != None):
                print("level: ", var_set_.level, " Branching Factor: ", len(ls), " Number of Variables Set: ", len(var_set_.set_vars_ls))
            else:
                print("level: ", var_set_.level, " Branching Factor: ", len(ls), " Number of Variables Set: ", 0)
                del var_set_


    def run(self):
        self.clear_file()
        self.start()
        while len(self.var_set_stack) > 0:
            self.update()
            #input("pause")
        self.output_answers()
        #self.print_answers()
        print("All done :) !!!!!!!!!!!!")
        print("verified: ",self.verify_answers())

    def test(self):
        print("boo")
        self.start()
        self.var_set_stack[0].test()

    def verify_answers(self):
        for answer in self.answers:
            if not cd.final_verify(self.backup_master_clause_ls, answer):
                return False
        return True


    def output_answers(self):
        with open(self.output_filename, 'a') as file:
            for answer in self.answers:
                file.write(', '.join([str(e) for e in answer]) + "\n")
        file.close()


    def print_answers(self):
        for answer in self.answers:
            print(answer,len(answer))


    def print_state(self):
        len_ls = []
        for thing in self.var_set_stack:
            len_ls.append(len(thing.set_vars_ls))
        print(len_ls)


    def print_state_full(self):
        print("&"*50)
        for thing in self.var_set_stack:
            thing.print_state()
        #print("&" * 50)
