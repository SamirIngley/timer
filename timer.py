#!/usr/bin/env python3
# above makes it executable from cli 

from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys
import subprocess


'''
TODO: add notification (via flag) for end time
TODO: help flag
TODO: be able to schedule several end times
'''

ZERO = "0"
THREE_SECONDS = "3"
TEN_SECONDS = "10"

def background_timer(timeComplete_flag, userInput_flag, end_time): 
    # time_value keeps track of the current time 
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


# -----------------------------------------------------------------------------
#           HELPER FUNCTIONS

def time_format(current_time):
    # seconds grand total --> HH:MM:SS
    curr_time = int(current_time)
    hours, hours_rem = divmod(curr_time, 3600)
    minutes, minutes_rem = divmod(hours_rem, 60) 
    seconds = minutes_rem 
 
    times = [hours, minutes, seconds]

    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_time

def input_listener(timerDone_flag, userInput_flag):

    while not timerDone_flag.is_set():
        input() # input() blocks this thread until some input is received, only then moves to next step
        userInput_flag.set()
        return 

def output_handler(timerDone_flag, userInput_flag):

    notify_title = "Terminal Timer"
    message = None
    if timerDone_flag.is_set():
        message = "timer completed"
        notify_mac(notify_title, message)
    elif userInput_flag.is_set():
        message = "user input - ending timer"
        notify_mac(notify_title, message)
        return print(f"\n {message} \n")
    else: 
        message = "unexepcted error"
        notify_mac(notify_title, message)

    return print(f"\n\n {message} \n")

def notify_mac(title, text):
    # Using safe list-based arguments instead of a raw string shell execution
    subprocess.run([
        "osascript", 
        "-e", 
        f'display notification "{text}" with title "{title}"'
    ])

# -----------------------------------------------------------------------------

def main_timer(current_time=0):

    # program_name = sys.argv[0]
    end_time = "99:59:59"
    if len(sys.argv) > 1:
        end_time = sys.argv[1]

    timeComplete_flag = threading.Event()
    userInput_flag = threading.Event()

    executor = ThreadPoolExecutor(max_workers=1) 
    timer = executor.submit(background_timer, timeComplete_flag, userInput_flag, end_time)
    # Daemon thread, so it won't keep the program alive
    threading.Thread(target=input_listener, args=(timeComplete_flag, userInput_flag), daemon=True).start()
            
    result = timer.result()

    return output_handler(timeComplete_flag, userInput_flag)

    
if __name__ == "__main__":

    main_timer()
