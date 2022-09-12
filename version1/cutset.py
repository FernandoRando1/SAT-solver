import DTD_solver as dtd
import var_grouping as vg
import bit_finder as bf
import copy


class cutset:

    def __init__(self, start_clause_ls_, var_ls_, size_, starting_point_=None):
        start_clause_ls = copy.deepcopy(start_clause_ls_)
        var_ls = copy.deepcopy(var_ls_)
        if (len(var_ls) > size_): # remove later
            self.og_var_ls = vg.negative_var_ls_gen(start_clause_ls, var_ls, size_, starting_point_)
        else:
            self.og_var_ls = var_ls
        self.og_clause_ls = vg.get_clauses(start_clause_ls_, self.og_var_ls)
        self.remapped_dicts = vg.remap_var(self.og_var_ls, self.og_clause_ls)
        self.remapped_clause_ls = vg.remap_clause(self.og_clause_ls, self.remapped_dicts)
        self.remapped_max_var = len(self.og_var_ls)
        self.solutions = []
        self.implied_ls = []

        self.score = vg.find_score(self.remapped_clause_ls)
        #self.score = vg.find_score_(self.remapped_clause_ls, self.remapped_max_var, 5)

    def fix(self, start_clause_ls_, var_ls_, size_, starting_point_=None):
        start_clause_ls = copy.deepcopy(start_clause_ls_)
        var_ls = copy.deepcopy(var_ls_)
        if (len(var_ls) > size_): # remove later
            self.og_var_ls = cutset_gen_test.funct_(start_clause_ls_,size_=size_)
        else:
            self.og_var_ls = var_ls
        self.og_clause_ls = vg.get_clauses(start_clause_ls_, self.og_var_ls)
        self.remapped_dicts = vg.remap_var(self.og_var_ls, self.og_clause_ls)
        self.remapped_clause_ls = vg.remap_clause(self.og_clause_ls, self.remapped_dicts)
        self.remapped_max_var = len(self.og_var_ls)
        self.solutions = []
        self.implied_ls = []

        self.score = vg.find_score(self.remapped_clause_ls)
        #self.score = vg.find_score_(self.remapped_clause_ls, self.remapped_max_var, 5)

    def solve(self):
        db_ls = dtd.sat_sharp_dfd(self.remapped_clause_ls, self.remapped_max_var, quite=True)
        self.solutions = dtd.resurrection(db_ls, self.remapped_max_var)
        self.implied_ls = bf.find_implied_list(self.solutions, self.remapped_max_var, self.remapped_dicts)
        return len(self.implied_ls)

    def print_state(self):
        print("#" * 100)
