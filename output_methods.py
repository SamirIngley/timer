import subprocess

def time_format(current_time):
    # Converts seconds grand total --> HH:MM:SS
    curr_time = int(current_time)
    hours, hours_rem = divmod(curr_time, 3600)
    minutes, minutes_rem = divmod(hours_rem, 60) 
    seconds = minutes_rem 
 
    times = [hours, minutes, seconds]
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_time

def output_handler(timerDone_flag, userInput_flag):

    notify_title = "Timer in Terminal"
    message = None
    if timerDone_flag.is_set():
        message = "timer completed"
    elif userInput_flag.is_set():
        message = "user input - ending timer"
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
