import random


def get_clauses(clause_ls_, var_ls_, remove=False):  # edits the clause ls using pop
    new_clauses_ls_ = []
    for cl_i in range(len(clause_ls_)):
        cl = clause_ls_[cl_i]
        b = True
        for cl_var in cl:
            if (not abs(cl_var) in var_ls_):
                b = False
                break
        if (b):
            new_clauses_ls_.append(cl)
            if (remove):
                clause_ls_.pop(cl_i)

    return new_clauses_ls_


###########################################################################
###########################################################################


def freq_score(var, clause_ls):
    score = 0
    for cl in clause_ls:
        if((var in cl) or (-1 * var in cl)):
            score += 1
    return score


def gen_freq_score(cl_ls_,var_ls_):
    freq_score = {}
    for var in var_ls_:
        freq_score[var] = 0
    for cl in cl_ls_:
        for var in cl:
            freq_score[abs(var)] += 1
    return sorted(freq_score.keys(),key = lambda x : 1*freq_score[x])


def remap_var(var_ls_, clause_ls_):  # returns dict
    var_ls_ = gen_freq_score(clause_ls_, var_ls_)
    var_dict_new_to_old = {}
    var_dict_old_to_new = {}
    k = 1
    for var in var_ls_:
        var_dict_new_to_old[k] = abs(var)
        var_dict_old_to_new[abs(var)] = k
        k += 1
    return (var_dict_new_to_old, var_dict_old_to_new)


def find_score_(clause_ls,max_var,range_):
    score = 0
    for var in range((max_var-range_),max_var):
        score += freq_score(var, clause_ls)
    return score


def find_score(clause_ls):
    score = 0
    for cl in clause_ls:
        score += abs(cl[0])
        #for var in cl:
            #score += freq_score(var, clause_ls) * abs(var)
    return score / len(clause_ls)


def remap_clause(old_clause_ls_, dict_tuple_):
    new_clause_ls_ = []
    for cl in old_clause_ls_:
        new_clause = []
        for var in cl:
            if (var > 0):
                new_clause.append(dict_tuple_[1][abs(var)])
            else:
                new_clause.append(-1 * dict_tuple_[1][abs(var)])
        new_clause_ls_.append(sorted(new_clause, key=lambda x: abs(x)))
    return sorted(new_clause_ls_, key = lambda x: (-1 * abs(x[0]), -1 * abs(x[1])))


###########################################################################
###########################################################################


def add_cl(cl,var_ls):
    for var in cl:
        if abs(var) not in var_ls:
            var_ls.append(abs(var))


def collision_scoring(clause_1, clause_2):
    count_vars = len(clause_1) + len(clause_2)
    for var in clause_1:
        if(var in clause_2):
            count_vars -= 1
        elif (-1 * var in clause_2):
            #count_vars = 0
            return 0
    return count_vars


def score_alt_5(scoring_clause_ls, clause, var_ls):
    score = 0
    for scoring_cl in scoring_clause_ls:
        count_vars = collision_scoring(clause, scoring_cl)
        score += 1 / (2 ** count_vars)
    score = (1 / (2 ** len(clause))) - score
    any_new_var = False
    for var in clause:
        if abs(var) not in var_ls:
            #print("new_var: ",var)
            any_new_var = True
            score = score / 2
    if not any_new_var:
        return 10000
    return score


def score_6(clause, var_ls):
    score = 0
    for var in clause:
        if var in var_ls:
            score -= 1
    any_new_var = False
    for var in clause:
        if abs(var) not in var_ls:
            any_new_var = True
            score = score / 2
    if not any_new_var:
        return 10000
    return score


##################################################################
##################################################################


def clean_list(cl_ls_,var_ls):
    for cl_i in reversed(range(len(cl_ls_))):
        remove = True
        for var in cl_ls_[cl_i]:
            if var not in var_ls:
                remove = False
                break
        if remove:
            cl_ls_.pop(cl_i)


def negative_var_ls_gen(cl_ls_, remaining_var_ls, size, starting_point_ = None):  # try only starting_point_ == clause that are top 10 connected!!!!!!!!!!!!!!!!!!!

    var_ls = []
    new_cl_ls = []

    if starting_point_ == None:
        starting_point_ = random.randint(0,len(cl_ls_)-1)

    add_cl(cl_ls_[starting_point_], var_ls)
    new_cl_ls.append(cl_ls_[starting_point_])
    cl_ls_.pop(starting_point_)

    while(len(var_ls) < size):
        #adding_clause = min(cl_ls_,key = lambda cl : score_alt_5(new_cl_ls, cl, var_ls))
        adding_clause = min(cl_ls_, key=lambda cl: score_6(cl, var_ls))
        add_cl(adding_clause, var_ls)
        new_cl_ls.append(adding_clause)
        clean_list(cl_ls_, var_ls)

    return var_ls
