import funct as f

############################################

def test_state_clause(arr_,clause_):
    for var in clause_:
        if(arr_[abs(var)-1] != int(var < 0)):
            return True
    return False

def test_state(arr_,clause_arr_):
    for cl_ in clause_arr_:
        if(not test_state_clause(arr_,cl_)):
            return False
    return True

def test_range(max_var_,clause_arr_):
    arr = [0] * (max_var_ + 1)
    while(arr[max_var_] == 0):
        print("arr:",arr[:-1]," num:",f.arr_to_num(arr)," = ",test_state(arr,clause_arr_))
        f. binary_add(arr,0)

def test_range_true(max_var_,clause_arr_,quite = False):
    v = 0
    arr = [0] * (max_var_ + 1)
    ans_ls = []
    while(arr[-1] == 0):
        if(test_state(arr, clause_arr_)):
            if not quite: print(arr[:-1]," = ",f.arr_to_num(arr[:-1]))
            ans_ls.append(f.arr_to_num(arr[:-1]))
            v += 1
        f.binary_add(arr,0)
    return v
