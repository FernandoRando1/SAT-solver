
def load_clause(file_name):

    Clause_File = open(file_name, "r")

    clause_ls = []
    max_varible = 0

    while (1):
        clause_str = Clause_File.readline()
        if (clause_str == ""):
            break

        clause = []

        for word in clause_str.split():
            if (word == "0"):
                break
            number = int(word)

            if (abs(number) > max_varible):
                max_varible = abs(number)

            clause.append(number)

        clause = sorted(clause, key=lambda x:abs(x))

        if (clause == []):
            break

        clause_ls.append(clause)

    number_of_clauses = len(clause_ls)

    Clause_File.close()

    clause_ls = sorted(clause_ls, key = lambda x: -1 * abs(x[0]))

    return clause_ls,max_varible

#############################################

def gen_power_ls(max_var):
    ls = []
    for i in range(max_var+1):
        ls.append(2**i)
    return ls

#############################################

def binary_add(arr,index):
    #print(len(arr))
    if(index < len(arr)):
        if(arr[index] == 0):
            arr[index] = 1
        elif(arr[index] == 1):
            arr[index] = 0
            binary_add(arr, (index+1))
        else:
            print("error binary_add() sat_funct")
    else:
        print("edge reached high binary_add()")
        arr[30] += 1

def binary_sub(arr,index):
    #print(len(arr))
    b = False
    for a in arr:
        if a != 0:
            b = True
            break

    if(b):
        if (index < len(arr)):
            if (arr[index] == 1):
                arr[index] = 0
            elif (arr[index] == 0):
                arr[index] = 1
                binary_sub(arr, (index + 1))
            else:
                i = 1
                # print("error binary_sub() sat_funct")
        else:
            i = 1
            # print("edge reached low binary_sub()")

#############################################

def arr_to_num(arr):
    #if len(arr) != len(power_ls_): print("length miss match")
    value = 0
    for i in range(len(arr)):
        value += (2 ** i) * arr[i]
    return value


def arr_to_num_fast(arr,power_ls_):
    #if len(arr) != len(power_ls_): print("length miss match")
    value = 0
    for i in range(len(arr)):
        value += power_ls_[i] * arr[i]
    return value

def num_to_arr(num,max_var):
    ls = [int(i) for i in reversed(bin(num)[2:])]
    while(len(ls) < max_var + 1):
        ls.append(0)
    return ls

def num_to_arr_fast(num,max_var,power_ls_): # can make faster
    arr = []
    for i in range(max_var+1):
        bit = (num//power_ls_[i]) % 2
        arr.append(bit)
    return arr



############################################

def clause_add_(arr,clause,pos):   #test
    if(((pos+1) in clause) or (-(pos+1) in clause)):
        clause_add_(arr, clause, pos+1)
    else:
        if (arr[pos] == 0):
            arr[pos] = 1
        elif (arr[pos] == 1):
            arr[pos] = 0
            clause_add_(arr, clause, pos+1)
        else:
            print("error binary_add() sat_funct")

def clause_add(arr,clause):
    clause_add_(arr, clause,abs(clause[0])-1)

def set_bound(arr,clause):

    b = True
    first_clause_discrepency = abs(clause[0])-1
    for var1 in clause:
        if (arr[(abs(var1) - 1)] != (var1 < 0)):
            first_clause_discrepency = abs(var1) - 1
            break

    for var in clause:
        #print(abs(var)-1)
        if(arr[(abs(var)-1)] != (var < 0)):
            binary_add(arr, (abs(var)-1))
            first_clause_discrepency = abs(var)-1
            b = False

    for i in reversed(range(abs(first_clause_discrepency))):
        arr[i] = 0

    for var_ in clause:
        arr[abs(var_) - 1] = int(var_ < 0)

    #print("first_clause_discrepency ",first_clause_discrepency)
    return b

def gen_bound(arr,clause):
    upper_bound = arr.copy()
    lower_bound = arr.copy()
    for i in range(abs(clause[0])-1):
        upper_bound[i] = 1
        lower_bound[i] = 0
    return [lower_bound,upper_bound]

############################################

def is_bound_collision(bound,bound_):
    if(bound[0] < bound_[0]): #orders bound
        bound1 = bound
        bound2 = bound_
    elif(bound[0] > bound_[0]):
        bound2 = bound
        bound1 = bound_
    else: # ==
        return True
    return not(bound1[1]+1 < bound2[0])

############################################

def bisect_l(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        #print("llllll",a[mid],x)
        if a[mid][0] < x[0]:
            lo = mid+1
        else:
            hi = mid
    return lo

def bisect_r(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x[1] < a[mid][1]:
            hi = mid
        else:
            lo = mid+1
    return lo

############################################

def insert_bound(bound,bound_ls):  # can be optimized

    l = bisect_l(bound_ls,bound)
    r = bisect_r(bound_ls,bound)

    if (l == r):
        # test upper
        try:
            if(is_bound_collision(bound,bound_ls[r])):
                bound[1] = bound_ls[r][1]
                del bound_ls[r]
        except:
            print("oopsy")
        # test lower
        if (is_bound_collision(bound, bound_ls[l - 1])):
            bound[0] = bound_ls[l - 1][0]
            del bound_ls[l - 1]
            l -= 1
        bound_ls.insert(l,bound)
        return bound
    elif (l < r):
        # test upper
        try:
            if(is_bound_collision(bound,bound_ls[r])):
                bound[1] = bound_ls[r][1]
                del bound_ls[r]
        except:
            print("oopsy")
        # test lower
        if (is_bound_collision(bound, bound_ls[l - 1])):
            bound[0] = bound_ls[l - 1][0]
            del bound_ls[l - 1]
            l -= 1
        del bound_ls[l:r]
        bound_ls.insert(l, bound)
        return bound
    elif (l > r):
        return bound_ls[r]
    else:
        return [-10, -10]