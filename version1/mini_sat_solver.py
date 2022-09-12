import subprocess

def get_next(output_file_):
    with open(output_file_,'r') as f:
        lines = f.readlines()
    if(len(lines) == 1):
        return (False,[],[])
    sat_arr = []
    new_clause = []
    for var in lines[1].split(" "):
        sat_arr.append(int(int(var) > 0))
        new_clause.append(-1 * int(var))
    f.close()
    return (True,sat_arr,new_clause)

def add_clause_minisat(new_clause,input_file_):
    str_ = ""
    for var in new_clause:
        str_ += str(var) + " "
    #str_ = str_[:-1]
    with open(input_file_, 'a') as f:
        f.write('\n' + str_)
    f.close()
    #return str_

def remove_clause(num_of_removal_lines,input_file):

    with open(input_file, 'r') as fr:
        lines = fr.readlines()
    fr.close()

    with open(input_file, 'w') as fw:
        for i in range(len(lines) - num_of_removal_lines):
            fw.write(lines[i])
    fw.close()

def sat_sharp_minisat(input_file,output_file):
    ls = []

    counter = 0

    while (1):

        subprocess.run("minisat " + input_file + " " + output_file, shell=True)
        b, sat_arr, next_clause = get_next(output_file)
        #print(sat_arr,next_clause)
        if (b):
            # print("SAT\n", next_clause)
            ls.append(next_clause)
            add_clause_minisat(next_clause, input_file)
        else:
            # print("UNSAT")
            break
        counter += 1
    remove_clause(len(ls), input_file)
    print("couter: ",counter)

    if(len(ls) > 0):
        with open(output_file, 'a') as f:
            for ls_ in ls:
                f.write(', '.join([str(-1*e) for e in ls_])+"\n")
        f.close()
    return ls