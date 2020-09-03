# Title: N Queens solver
# Course: CISC 352
# Date: Feb-21-2020
# Authors: Aubrey McLeod, Duncan Clarke, Lianne Orlowski, Pheobe Liu, Taylor Jones
#
# a python implementation of Sosic-Gu QS4 algorithm to solve the N-Queens Problem
# This algorithm is based around the min conflict heuristic and iterative repair.

from collections import defaultdict
import math
import random


# global variables used for generating solutions
SIZE = 0

pieces = None
x_conflicts = None
y_conflicts = None
neg_conflicts = None
pos_conflicts = None

# swaps two pieces in the pieces array
def swap(i, j):
    storage = pieces[i]
    pieces[i] = pieces[j]
    pieces[j] = storage

# determines the current angular collision for a given piece
def partial_collisions(i):
    neg = neg_conflicts[pieces[i] - i]
    pos = pos_conflicts[pieces[i] + i]
    return neg + pos

# uses the min-conflict heuristic to place at least N-c queens without conflict, and at most c queens with
# with conflict.
def initial_search():
    global pieces
    pieces = list(range(SIZE))
    j = 0 # The index of our first element that has not been placed safely
    for i in range(math.floor(3.08*SIZE)):  # per the article 3.08 is a sufficiently good number
        m = random.randint(j, SIZE-1)   # pick a random row that has not been placed yet
        swap(m, j)                      # first element that has not been placed swaps position,
        # add conflicts to the new location
        neg_conflicts[pieces[j]-j] += 1
        pos_conflicts[pieces[j]+j] += 1

        # if there exists no other conflicts at this placement location:
        if partial_collisions(j)-2 == 0:
            # update the vertical/horizontal conflicts
            x_conflicts[j] += 1
            y_conflicts[pieces[j]] += 1
            j += 1 #move on to the next piece, since this has been placed safely
        else:
            # if it was not a safe location, return j to its starting position, undo conflict changes
            neg_conflicts[pieces[j] - j] -= 1
            pos_conflicts[pieces[j] + j] -= 1
            swap(m, j)

        if j == SIZE: #if we placed all the pieces here, break out of this loop
            break

    #here we will place our conflicting queens
    for i in range(j, SIZE):
        m = random.randint(i, SIZE-1)
        swap(m, i)  #swap pieces at random, in the unplaced region
        add_conflict(i)

    return SIZE - j #return the number of conflicting pieces


#returns the total number of conflicts at a given queen
def total_collisions(i):
    x = x_conflicts[i]
    y = y_conflicts[pieces[i]]
    neg = neg_conflicts[pieces[i] - i]
    pos = pos_conflicts[pieces[i] + i]
    return x+y+neg+pos


# here we perform a version of iterative repair, in which we go through our region of conflicting queens,
# select each one, and attempt to swap it with any other queen on the board; only accepting the swap when
# there exists zero conflicts for either piece; once this swap has been made, we shrink our unsorted space
# if we are unable to complete our solution (too many swaps) within a given number of steps, stop attempting to
# solve this board as we have hit a local optima.
def final_search(k, steps):
    s = 0
    for i in range(SIZE-k, SIZE):
        if total_collisions(i)-4 > 0:
            b = True
            while b:
                if s == steps:
                    return None
                j = random.randint(0, SIZE-1)
                swap_with_conflict(i, j)

                b = (total_collisions(i)-4 > 0) or (total_collisions(j)-4 > 0)
                if b:
                    swap_with_conflict(i, j)
                s += 1
    return pieces

#This macro function clears the conflict of two pieces, swaps them, then applies their new conflicts
def swap_with_conflict(i, j):
    remove_conflict(i)
    remove_conflict(j)
    swap(i, j)
    add_conflict(i)
    add_conflict(j)

# increments the row, column, left diagonal and right diagonal conflicts at the given index
def add_conflict(i):
    neg_conflicts[pieces[i] - i] += 1
    pos_conflicts[pieces[i] + i] += 1
    x_conflicts[i] += 1
    y_conflicts[pieces[i]] += 1

# decrements the row, column, left diagonal and right diagonal conflicts at the given index
def remove_conflict(i):
    neg_conflicts[pieces[i] - i] -= 1
    pos_conflicts[pieces[i] + i] -= 1
    x_conflicts[i] -= 1
    y_conflicts[pieces[i]] -= 1

#resets all global variables to their default state.
def init_all():
    global x_conflicts, y_conflicts, neg_conflicts, pos_conflicts, pieces
    x_conflicts = defaultdict(int)
    y_conflicts = defaultdict(int)
    neg_conflicts = defaultdict(int)
    pos_conflicts = defaultdict(int)
    pieces = []

#runs the QS4 algorithm
def solver(size):
    global SIZE
    SIZE = size
    solution = None
    while solution is None:
        init_all()
        solution = final_search(initial_search(), math.ceil(2 * SIZE / math.log2(SIZE)))
    return solution

#takes a solution and generates a string representation of the given solution.
def generate_output_string(solution):
    output_string = "["+str(solution[0]+1)
    for i in range(1,len(solution)):
        output_string += ","+str(solution[i]+1)
    output_string += "]"
    return output_string


def main():
    random.seed()
    solutions = []
    input_file = open("nqueens.txt", "r")
    for line in input_file:
        solutions.append(solver(int(line)))
    input_file.close()
    output_file = open("nqueens_out.txt", "w")
    for solution in solutions:
        output_file.write(generate_output_string(solution)+"\n")
    output_file.close()

    # for solution in solutions:
    #     solution_checker(solution)

# a debug function, that takes a solution and determines its correctness in linear time.
def solution_checker(solution):
    x_conflicts = defaultdict(int)
    y_conflicts = defaultdict(int)
    neg_conflicts = defaultdict(int)
    pos_conflicts = defaultdict(int)
    for x in range(len(solution)):
        x_conflicts[x] += 1
        y_conflicts[solution[x]] += 1
        neg_conflicts[solution[x]-x] += 1
        pos_conflicts[solution[x]+x] += 1
    for x in range(len(solution)):
        conflicts = x_conflicts[x]+y_conflicts[solution[x]]+neg_conflicts[solution[x]-x]+pos_conflicts[solution[x]+x]
        if conflicts != 4:
            print("failed...." + str(x))
            break
    print("test complete")






main()