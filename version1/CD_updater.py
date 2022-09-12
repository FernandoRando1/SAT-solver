import var_grouping as vg

def minimize_clause(clause_, set_var_ls_):
    for var in reversed(clause_):
        if(-1 * var in set_var_ls_):
            clause_.remove(var)

###########################################################################

def is_clause_true(clause_, set_var_ls_):
    for var in clause_:
        if(var in set_var_ls_):
            return True
    return False

def final_verify(clause_ls_, set_var_ls_):
    for cl in clause_ls_:
        if not is_clause_true(cl, set_var_ls_):
            #print("Error Clause: ", cl)
            #input("pause")
            return False
    return True

def verify(clause_ls_, set_var_ls_):
    set_var_ls_clean = []
    for var in set_var_ls_:
        set_var_ls_clean.append(abs(var))
    return final_verify(vg.get_clauses(clause_ls_, set_var_ls_clean), set_var_ls_)

###########################################################################

def update_clause_ls_(clause_ls_, set_var_ls_, available_vat_ls_):
    for cl_i in reversed(range(len(clause_ls_))):
        if is_clause_true(clause_ls_[cl_i], set_var_ls_):
            clause_ls_.pop(cl_i)
        else:
            minimize_clause(clause_ls_[cl_i], set_var_ls_)
            if(len(clause_ls_[cl_i]) == 0):
                return True
            elif(len(clause_ls_[cl_i]) == 1):
                var = clause_ls_[cl_i][0]
                if(-1 * var in set_var_ls_):
                    return True
                else:
                    set_var_ls_.append(var)
                    available_vat_ls_.remove(abs(var))
                    clause_ls_.pop(cl_i)
    return False

