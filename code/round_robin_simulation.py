# Load Libraries

from timeit import default_timer as timer
from collections import defaultdict
from collections import deque
from typing import Dict
from typing import List
import pandas as pd
import numpy as np

# Plotting
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 250

# Round Robin Simulation
def round_robin_scheduling_sim(p1: List[int], p2: List[int], p3: List[int], time_slice: List[float]) -> Dict[str, List[int]]:
    """ 
    Given three programs (p), where each program has a different program length (t),
    quantize or time-slice some fixed amount (q) to simulate a round-robin scheduler.
    ---------------------
    Params:
    p1,p2,p3: arrays of form [program, program_length, iteration count, response time]

    time_slice: length of to run program before continuing in queue
    ---------
    Returns:
    
    program_dictionary: dictionary of program keys and number of iterations given time-slices
    
    """
    
    # create a list to collect results
    time_slice_results = []

    # for each time slice (q), loop through the round-robin scheduler
    for time_slice in time_slice_list:
        
        # record time program entered in queue...
        parent_arrival_time = timer()
        
        # ...into response time position in each list
        p1[3] += parent_arrival_time
        p2[3] += parent_arrival_time
        p3[3] += parent_arrival_time
        
        # create tuple of structure: program, program_length, iteration count, response time
        program_tuple = [p1, p2, p3]
        
        # program tuple enters queue 
        program_queue = deque(program_tuple)

        # create list to collect short-term results
        result_list = []

        # begin round-robin scheduler: loop while a program is in queue
        while len(program_queue) != 0:
 
            # access program and unpack tuple
            program, program_length, iteration, arrival_time = program_queue.popleft()
            
            # if response time has not been calculated, calculate it
            if parent_arrival_time == arrival_time:
                # response time: first-run - arrival time
                arrival_time = timer() - arrival_time
            
            # run program for length of time-slice, and record results
            program_length = program_length - time_slice
            
            # if program still has positive value, it is incomplete
            if program_length > 0:
                # record that an iteration has been run
                iteration += 1
                # place unfinished program back into end of queue
                program_queue.append([program, program_length, iteration, arrival_time])
                
            # if program is zero or negative, it has completed its run-time 
            else:
                # record last iteration
                iteration += 1
                # record which program has finished, and iteration count
                result_list.append((program, iteration, arrival_time))
                
        #after all programs have left queue, record results
        time_slice_results.append(result_list)
        
        # reset iteration count, arrival time for next run
        p1[2], p1[3] = (0,0)
        p2[2], p2[3] = (0,0)
        p3[2], p3[3] = (0,0)
    
    
    # unpack results into single list of tuples
    time_slice_results_single_list = [x for y in time_slice_results for x in y]
    
    # organize single list into dictionary
    program_dictionary = defaultdict(list) 
    for program, iteration, arrival_time in time_slice_results_single_list: 
        program_dictionary[program].append([iteration, arrival_time])
    
    # return dictionary of results
    return program_dictionary


def response_time_simulation(x: int)->plt.Figure:
    """
    Loop x amount of times through round-robin scheduler,
    track response times, and plot average of all x response times,
    where average response times:

    average response time = sigma {i,n} first-run_i - queue-time_i / n
    for each program p
    ----------------------
    Parameters:
    
    x: number of simulations to run
    ----------------------
    Returns: 

    plt.Figure: plot of simulations
    """

    # generate 100 different slices (q) between 10 and .5 seconds
    time_slice_list = [round(q,2) for q in np.linspace(10, .5, num = 110)]
    average_response_list = []
    for i in range(1000):
        program_dictionary = round_robin_scheduling_sim(p1=['p1',10,0,0],
                                                    p2=['p2',35,0,0],
                                                    p3=['p3',100,0,0],
                                                    time_slice=time_slice_list)
        
        average_response = [(x[1] + y[1] + z[1])/3 for x,y,z in zip(program_dictionary['p1'],
                                                                    program_dictionary['p2'],
                                                                    program_dictionary['p3'])]
        average_response_list.append(average_response)

    fig, ax = plt.subplots(figsize = [7,3])
    ax.plot([x[0] for x in program_dictionary['p1']][::-1], label = 'Program 1')
    ax.plot([x[0] for x in program_dictionary['p2']][::-1], label = 'Program 2')
    ax.plot([x[0] for x in program_dictionary['p3']][::-1], label = 'Program 3')


    custom_lines = [Line2D([0], [0], color='green'),
                    Line2D([0], [0], color='orange'),
                    Line2D([0], [0], color='blue')]

    ax.legend(custom_lines, ['p3: 100 seconds',
                            'p2: 35 seconds',
                            'p1: 10 seconds',])


    plt.xticks(np.arange(0, 110, 10), labels=time_slice_list[::10][::-1])

    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # set labels
    ax.set_xlabel("Slice Length (seconds)")
    ax.set_ylabel("# Iterations")

    # alter axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # title
    ax.set_title("Round-Robin Scheduling")
    ttl = ax.title
    ttl.set_weight('bold')

    fig.savefig('/Users/blabaschin/Documents/Technical/GitHub/EconoBen-Blog/assets/2020-08-22-automating-tasks/round_robin.png')

if __name__ == "__main__":
    response_time_simulation(1000)