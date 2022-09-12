import flash_solver
#import minisat_solver as mss
import cProfile
import pstats

import subprocess

print("Start!!!!!!!!!!!!!!!!!!!!!")

filename_0 = "sat_problem_5.txt"
filename_1 = "uf250-01.txt"
filename_2 = "uf20-01.txt"
filename_3 = "uf50-01.txt"

#mss.sat_sharp_minisat(filename_3,"out2.txt")
with cProfile.Profile() as pr:
    flash_solver.flash(filename_1, "test_out.txt",BFS=True,intial_round_count=1000).run()

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()

