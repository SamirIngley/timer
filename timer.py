
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys

'''
TODO: simplify clock logic 
'''

ZEROES = "00:00:00"
THREE_SECONDS = "00:00:03"
TEN_SECONDS = "00:00:10"

def background_timer(timerDone_flag, userInput_flag, end_time): 
    time_value = ZEROES # start time / or current time

    print()
    while not timerDone_flag.is_set() and not userInput_flag.is_set(): 
        time_value, endTimer_flag = clock_logic(time_value, end_time)

        if endTimer_flag:
            timerDone_flag.set()
            return endTimer_flag

def clock_logic(current_time, end_time):
    h_tens, h_ones, m_tens, m_ones, s_tens, s_ones = time_split(current_time)
    print(f"\r  {current_time}  \033[K", end="", flush=True)
    # print(current_time)
    timerEnd_flag = False
    if current_time == end_time:
        timerEnd_flag = True
    else: 
        time.sleep(1)

        if s_ones == 9: 

            if s_tens == 5: 

                if m_ones == 9: 

                    if m_tens == 5: 

                        if h_ones == 9: 

                            if h_tens == 1: 

                                print("out of bounds")
                            else: 
                                h_tens += 1
                                h_ones = 0
                                m_tens = 0
                                m_ones = 0
                                s_tens = 0
                                s_ones = 0
                        else: 
                            h_ones += 1
                            m_tens = 0
                            m_ones = 0
                            s_tens = 0
                            s_ones = 0
                    else: 
                        m_tens += 1
                        m_ones = 0
                        s_tens = 0
                        s_ones = 0
                else: 
                    m_ones += 1
                    s_tens = 0
                    s_ones = 0
            else:
                s_tens += 1
                s_ones = 0

        else: 
            s_ones += 1

    new_seconds = str(s_tens) + str(s_ones)
    new_minutes = str(m_tens) + str(m_ones)
    new_hours = str(h_tens) + str(h_ones)
    current_time = new_hours + ":" + new_minutes + ":" + new_seconds

    return current_time, timerEnd_flag

def time_split(time_string): 

    # Strings
    time_list = time_string.split(":")
    hours = time_list[0]
    minutes = time_list[1]
    seconds = time_list[2]

    hours_ones = int(hours[1])
    hours_tens = int(hours[0])

    minutes_ones = int(minutes[1])
    minutes_tens = int(minutes[0])

    seconds_ones = int(seconds[1])
    seconds_tens = int(seconds[0])

    return hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones

def input_reader(timerDone_flag, userInput_flag):

    while not timerDone_flag.is_set():
        input() # input() blocks this thread until some input is received, only then moves to next step
        userInput_flag.set()
        return 

def message(timerDone_flag, userInput_flag):
    message = None
    if timerDone_flag.is_set():
        message = "timer completed"
    elif userInput_flag.is_set():
        message = "user input - ending timer"
        return print(f"\n {message} \n")
    else: 
        message = "unexepcted error"

    return print(f"\n\n {message} \n")

def main_timer(current_time=0):

    # program_name = sys.argv[0]
    end_time = None
    if len(sys.argv) > 1:
        end_time = sys.argv[1]

    timerDone_flag = threading.Event()
    userInput_flag = threading.Event()

    executor = ThreadPoolExecutor(max_workers=1) 
    timer = executor.submit(background_timer, timerDone_flag, userInput_flag, end_time)
    # Daemon thread, so it won't keep the program alive
    threading.Thread(target=input_reader, args=(timerDone_flag, userInput_flag), daemon=True).start()
            
    result = timer.result()

    return message(timerDone_flag, userInput_flag)
    

    
if __name__ == "__main__":

    main_timer()
