import funct as f

def get_var_value(num,var):
    return (num // (2 ** (var-1)) ) % 2


def find_set_var_bound(lb,max_var_):
    arr = f.num_to_arr(lb[0],max_var_)
    pos = ( ( lb[1] - lb[0] + 1 ).bit_length() - 1 )
    #print(pos)
    if( get_var_value(lb[0],pos + 1) != get_var_value(lb[1],pos + 1)):
        pos += 1
    return arr[pos:-1]


def find_implied_list(lb_ls_, max_var_, dict_):
    big_ls = []
    for lb in lb_ls_:
        ls = find_set_var_bound(lb, max_var_)
        ls_num = []
        index = max_var_
        for bit in reversed(ls):
            ls_num.append(((bit * 2) - 1) * dict_[0][index])
            index -= 1
        big_ls.append(ls_num)
    return big_ls