import funct as f

import math

def sat_sharp_dfd(clause_ls,max_var,  quite = False):
    power_ls = f.gen_power_ls(max_var)
    jk = 2** max_var + 1
    dead_bound_ls = [[-2, -2], [jk, jk]]
    couter = 0
    for clause_ in clause_ls:
        arr = [0] * (max_var + 1)
        bool_ = f.set_bound(arr, clause_)
        while (arr[-1] == 0):
            bound_arr = f.gen_bound(arr, clause_)
            bound = [f.arr_to_num_fast(bound_arr[0],power_ls), f.arr_to_num_fast(bound_arr[1],power_ls)]
            arr = f.num_to_arr(f.insert_bound(bound, dead_bound_ls)[1], max_var)
            if (f.set_bound(arr, clause_)):  # set_bound changed nothing
                f.clause_add(arr, clause_)
            for i in range(abs(clause_[0]) - 1):
                arr[i] = 0
        if not quite:
            print("clause: ",clause_,math.log2(len(dead_bound_ls)), " - couter: ",couter)
        couter += 1
    return dead_bound_ls[1:-1]

def num_of_sat_solutions(dead_bound_ls_,max_var):
    val = dead_bound_ls_[0][0] + ((2**max_var - 1) - dead_bound_ls_[-1][1])
    for db_i in range(len(dead_bound_ls_)-1):
        val += dead_bound_ls_[db_i+1][0] - dead_bound_ls_[db_i][1] - 1
    return val

def resurrection(dead_bound_ls_,max_var):
    living_bound_ls = []

    if(dead_bound_ls_[0][0] != 0):
          living_bound_ls.append([0, dead_bound_ls_[0][0] - 1])

    for db_i in range(len(dead_bound_ls_) - 1):
        living_bound_ls.append( [dead_bound_ls_[db_i][1] + 1, dead_bound_ls_[db_i + 1][0] - 1] )

    if(dead_bound_ls_[-1][1] != 2**max_var - 1):
          living_bound_ls.append([dead_bound_ls_[-1][1] + 1,  2**max_var - 1])

    return living_bound_ls
