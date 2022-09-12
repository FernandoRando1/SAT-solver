from itertools import combinations
import random
import modulo_push_solver as mps
import DTD_solver as dtd


def gen_possible_clause_ls(max_var, clause_length):
    var_arr = list(range(1, max_var + 1)) + list(range(-1 * (max_var), 0))

    possible_clause_ls = list(combinations(var_arr, clause_length))

    for cl_i in reversed(range(len(possible_clause_ls))):
        possible_clause_ls[cl_i] = list(possible_clause_ls[cl_i])
        possible_clause_ls[cl_i].sort(key = lambda x : abs(x))
        cl = possible_clause_ls[cl_i]
        for var_i in range(clause_length):
            if ((cl[var_i] * -1) in cl):
                possible_clause_ls.pop(cl_i)

    return possible_clause_ls



def generate_sat_problem(max_var, min_ans, clause_length = 3, file_name = None, first_round_count = 50, possible_clause_ls = None):  # working solving function into paramiters later

    sat_problem = []

    if possible_clause_ls == None:
        possible_clause_ls = gen_possible_clause_ls(max_var, clause_length)

    for i in range(first_round_count):
        sat_problem.append(possible_clause_ls.pop(random.randint(0,len(possible_clause_ls)-1)))

    print("hi :)")

    round = 0

    while(1):
        #k = bfs.test_range_true(max_var, sat_problem, quite=True)
        k = dtd.num_of_sat_solutions(dtd.sat_sharp_dfd(sorted(sat_problem, key=lambda x: -1 * abs(x[0])), max_var, quite=True), max_var)
        #k = mps.mps_solution_count(sorted(sat_problem, key=lambda x: -1 * abs(x[0])), max_var)
        print("K: ",k)
        if(k == 0):
            print("number of solution: 0, Restarting")
            if(round == 0):
                return generate_sat_problem(max_var, min_ans, clause_length, file_name, first_round_count - 5, possible_clause_ls = possible_clause_ls)
            else:
                return generate_sat_problem(max_var, min_ans, clause_length, file_name, first_round_count + 5, possible_clause_ls = possible_clause_ls)
        if(k <= min_ans):
            print("number of solution: ", k)
            break
        sat_problem.append(possible_clause_ls.pop(random.randint(0, len(possible_clause_ls) - 1)))
        round += 1

    # load files onto files
    if file_name != None:
        with open(file_name, 'w') as f:
            for cl in sat_problem:
                str_ = ""
                for c in list(cl):
                    str_ += str(c) + " "
                f.write(str_ + "0")
                f.write("\n")

    return sorted(sat_problem, key = lambda x: -1 * abs(x[0]))
