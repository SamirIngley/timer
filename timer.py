
from concurrent.futures import ThreadPoolExecutor
import threading
import time

'''
TODO: Allow user input to end timer
TODO: Allow input to determine end time (don't hardcoat end time)
TODO: simplify clock logic 

'''

ZEROES = "00:00:00"
TEN_SECONDS = "00:00:10"

def background_timer(stop_event): 
    print()
    print()

    time_value = ZEROES # start time / or current time
    end_time = TEN_SECONDS

    while not stop_event.is_set(): 
        time_value, end_flag = clock_logic(time_value, end_time)
        if end_flag: 
            return end_flag

def clock_logic(current_time, end_time="12:59:59"):
    h_tens, h_ones, m_tens, m_ones, s_tens, s_ones = time_split(current_time)
    print(f"\r  {current_time}  \033[K", end="", flush=True)
    # print(current_time)
    end_flag = False
    if current_time == end_time:
        end_flag = True
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

    return current_time, end_flag

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

def timer(current_time=0):

    stop_flag = threading.Event()

    executor = ThreadPoolExecutor(max_workers=1) 
    future = executor.submit(background_timer, stop_flag)

    while not future.done():
        if future.running():
            input()
            stop_flag.set()
            print()
            return print(" user input - ending timer\n")
            

    result = future.result()
    print('result: ', result)

    if result:
        return print("\n\n timer ended\n")

    
if __name__ == "__main__":
    timer()
