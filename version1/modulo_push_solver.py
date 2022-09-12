import funct as f
import brute_force_solver as bfs


def find_next_true(arr_,clause_ls_):
    while(arr_[-1] == 0):
        b = True
        for cl in clause_ls_:
            if not bfs.test_state_clause(arr_, cl):
                f.binary_add(arr_, abs(cl[0])-1)
                b = False
                break
        if(b):
            break


def make_bound(arr_,clause_ls_):
    bound = [f.arr_to_num(arr_)]
    while bfs.test_state(arr_, clause_ls_):
        f.binary_add(arr_, 0)
        if (arr_[-1] != 0):
            f.binary_sub(arr_, 0)
            break
    f.binary_sub(arr_, 0)
    bound.append(f.arr_to_num(arr_))
    f.binary_add(arr_, 0)
    return bound


def sat_sharp_mps(clause_ls_,max_var_):
    living_bound = []
    arr = [0] * (max_var_ + 1)
    while (1):
        find_next_true(arr,clause_ls_)
        if(arr[-1] == 0):
            living_bound.append(make_bound(arr,clause_ls_))
        else:
            break
    return living_bound

def mps_solution_count(clause_ls_,max_var_):
    num_of_solutions = 0
    for lb in sat_sharp_mps(clause_ls_, max_var_):
        num_of_solutions += (lb[1] - lb[0] + 1)
    return num_of_solutions
