from commands import help_cmd, notify_flag

DEFAULT_ENDTIME = "99:59:59"

BUILTIN_CMDS = {

    "-h": help_cmd,
    "-n": notify_flag,

    }


def input_parser(user_input):  

    # check number of arguments
    # if cmd, call its function
    # if it's an end time, return that endtime

    end_time = DEFAULT_ENDTIME
    flags = []

    if len(user_input) > 1: # check if more input than just program name
        for item in user_input[1:]: # gather flags and set end time
            
            if item[0] == "-": 
                flags.append(item)
                if item in BUILTIN_CMDS.keys():
                    BUILTIN_CMDS[item]()
        
            elif end_time_check(item): 
                end_time = item 

    return end_time

def input_listener(timerDone_flag, userInput_flag):

    while not timerDone_flag.is_set():
        input() # input() blocks this thread until some input is received, only then moves to next step
        userInput_flag.set()
        return 

def end_time_check(text): 
    # True if value is an end_time
    parts = text.split(":")
    if len(parts) != 3:
        return False
    if not all(p.isdigit() and len(p) == 2 for p in parts):
        return False
    return True