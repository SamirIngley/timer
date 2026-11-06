#!/usr/bin/env python3
# above makes it executable from cli 

from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys

from input_handler import input_listener, input_parser 
from output_methods import time_format, output_handler

'''
TODO: add notification (via flag) for end time 
to be able to toggle notification, need to be able to distinguish between flag and endtime from argument
-h doesn't have end time and it independently ends the program
-n does have endtime

TODO: be able to schedule several end times
TODO: user input end time should be valid time. 
TODO: be able to name timers
TODO: add tests
TODO: convert to countdown if end time given?
'''

ZERO = "0"
THREE_SECONDS = "3"
TEN_SECONDS = "10"

def background_timer(timeComplete_flag, userInput_flag, end_time): 
    # time_value keeps track of the time in seconds and is updated constantly by clock_logic
    # time_format converts to HH:MM:SS when displaying the time

    time_value = ZERO # start time / or current time

    print()
    while time_value is not None and not timeComplete_flag.is_set() and not userInput_flag.is_set(): 
        time_value = clock_logic(time_value, end_time, timeComplete_flag)

def clock_logic(current_time, end_time, timeComplete_flag): 
    # CURRENT TIME, END TIME, COMPLETE_FLAG --> NONE or NEW TIME
    # Checks for end time

    formatted_time = time_format(current_time)
    print(f"\r  {formatted_time}  \033[K", end="", flush=True)

    if formatted_time == end_time: 
        timeComplete_flag.set()
        return
    else: 
        time.sleep(1)
        new_time = int(current_time) +  1
        return new_time


def main_timer(current_time=0):

    end_time = "99:59:59"
    end_time = input_parser(sys.argv) # Checks for cmd, returns output of Built-In Cmd 

    timeComplete_flag = threading.Event()
    userInput_flag = threading.Event()

    notify_flag = threading.Event()

    with ThreadPoolExecutor(max_workers=1)  as executor: 
        timer = executor.submit(background_timer, timeComplete_flag, userInput_flag, end_time)
        # Daemon thread, so it won't keep the program alive
        threading.Thread(target=input_listener, args=(timeComplete_flag, userInput_flag), daemon=True).start() 
            
    result = timer.result() # forces function to wait til threads are done before moving to return

    return output_handler(timeComplete_flag, userInput_flag)

    
if __name__ == "__main__":

    main_timer()
