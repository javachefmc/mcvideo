#!/usr/bin/env python3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def error(str):
    print(bcolors.FAIL + str + bcolors.ENDC)

def warning(str):
    print(bcolors.WARNING + str + bcolors.ENDC)

def success(str):
    print(bcolors.OKGREEN + str + bcolors.ENDC)

# Initial check for python version. Sometimes errors due to version mismatch happen anyway and this code is unreachable.
# TODO: remove this code or handle version checking better
import sys
version_number = str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
try:
    assert sys.version_info >= (3, 10)
except:
    error("Please update python to version 3.10 or later.\nDetected version: " + version_number)
    quit()

# Main program intro
from os import system, name, path
import re, shlex
import subprocess
from subprocess import Popen, PIPE

greeting = """
MC Video Generator v1.0 by JavaChef
      
What would you like to do today?
\t1) Create resoucepack and datapack from video
\t2) Create datapack only (you have frames)
\t3) Reset tool

"""

def check_for_ffmpeg():
    # Runs an ffmpeg version check and reads result

    shell_output = get_shell_output("ffmpeg -version")

    if "Copyright" in shell_output[1] or shell_output[0] == 1:
        success("Detected ffmpeg")
        return 1
    elif shell_output[0] == -1:
        error("\nError: ffprobe is not installed or is inaccessible.")
        return 0
    else:
        return -1

def check_for_ffprobe():
    # Runs an ffprobe version check and reads result

    shell_output = get_shell_output("ffprobe -version")

    if "Copyright" in shell_output[1] or shell_output[0] == 1:
        success("Detected ffprobe")
        return 1
    elif shell_output[0] == -1:
        error("\nError: ffprobe is not installed or is inaccessible.")
        return 0
    else:
        return -1

def get_shell_output(command):
    process = shlex.split(command)
    try:
        result = subprocess.run(process, capture_output=True)
        return [result.returncode, str(result.stdout)]
    except FileNotFoundError:
        return [-1, ""]

def clear():
    # Clears console window

    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac and linux (os.name is 'posix')
    else:
        _ = system('clear')

def is_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        if int(s) < 1:
            return False
        else:
            return True

def reset():
    # Delete generated files and recreate folder structure

    print("Resetting...")

    # TODO: main code
    print("Reset complete.")

    while True:
        answer = input("Would you like to start over? [Y/N] > ")
        if answer.lower() in ["y","yes"]:
            # Do stuff
            break
        elif answer.lower() in ["n","no"]:
            exit()
        else:
            continue
    
    # unreachable unless user enters "yes"
    startup()

def startup():
    # Main function
    message = "Type number then press enter."

    while True:
        clear()
        print(greeting + message)
        try:
            selection = int(input("> "))
        except ValueError:
            # error parsing int
            message = "Please enter a valid number."
            continue

        if selection != 1 and selection != 2 and selection != 3:
            # not in range
            message = "Please enter a valid number."
            continue
        else:
            # valid input
            break

    # if selection == 1:
    #     create_full()
    # elif selection == 2:
    #     create_datapack_only()
    # elif selection == 3:
    #     reset()
    # else:
    #     error("An internal error occured; please report this to the developer.")

    match selection:
        case 1:
            create_full()
        case 2:
            create_datapack_only()
        case 3:
            reset()
        case _:
            error("An internal error occured; please report this to the developer.")


def get_video_name():
    # Prompts user to enter a video name. Exits only when input has been validated

    print("\nPlease enter video name.\nThis will be used as a unique identifier for your video.")
    while True:
        video_name = input("> ")
        # strip spaces and special characters
        video_name = re.sub(r'\W+', '', video_name).lower()

        # repeat loop if name is empty
        if (video_name == ""):
            print ("\nThis name would cause an error in game. Please enter a different one.")
            continue
        
        print("\nYour video will be encoded as:")
        warning(video_name)

        answer = input("\nIs this name OK? [Y/N] > ")
        if answer.lower() in ["y","yes"]:
            # Do stuff
            break
        elif answer.lower() in ["n","no"]:
            print("\nPlease enter a new name:")
            continue
        else:
            continue
    
    warning("Please keep note of this name for future use in-game.")
    return video_name

def get_video_path():
    # Prompts user to enter a video path. Exits only when input has been validated

    print("\nPlease enter the path to your source video.\n(Usually you can just drag your video here, then press Enter)")

    while True:
        video_path = str(input("> "))

        if(path.isfile(video_path)):
            print("\nFile exists.")
            print("Checking if we can convert this...")

            video_is_valid = check_for_video(video_path)

            if(video_is_valid):
                success("\nPassed initial tests.")
                return video_path
            else:
                print("\nWe're sorry, but this file cannot be converted.\nPlease ensure you enter the path of a video file and that it is not corrupted.")

        else:
            print("\nIt appears this is not a valid path. Please enter another path and try again.\nYou may need to remove any surrounding quotation marks.")
            continue

def get_frame_count_from_user():
    # Prompts user for the number of frames in video. Exits only when input has been validated

    # TODO: untested code

    print("\nHow many frames is your video?")

    while True:
        video_length = input("> ")
        if (is_int(video_length)):
            return int(video_length)
        else:
            print("\nThat does not appear to be valid.\nPlease enter a whole number for the number of frames in your video:")
            continue

def check_for_video(path):
    # Runs ffprobe command to check if file contains a video stream. Fails gracefully if video is not detected

    command = 'ffprobe -loglevel error -select_streams v -show_entries stream=codec_type -of csv=p=0 "' + path + '"'
    process = shlex.split(command)
    error = False

    try:
        output = subprocess.check_output(process, shell=True)
        output = output.decode("utf-8")
        if "video" in output:
            # nothing
            success("\nVideo detected.")
        else:
            print("\nNo video was detected.")
            error = True 
    except:
        error = True

    if error:
        return False
    else:
        return True

def get_frame_count_from_video(path):
    # Runs ffprobe command to read the number of frames from the supplied video path. No input validation

    command = 'ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -print_format default=nokey=1:noprint_wrappers=1 "' + path + '"'
    process = shlex.split(command)

    frame_count = -1

    # TODO: UNTESTED CODE

    try:
        output = subprocess.check_output(process, shell=True)
        output = output.decode("utf-8")
        if output.is_integer():
            frame_count = output
        else:
            error("\nAn internal error occurred. Please report this to the developer.")
    except:
        error("\nAn internal error occurred. Please report this to the developer.")
    
    return frame_count


def convert_video_to_frames(path):
    # Runs ffmpeg command to convert video path to frames

    # TODO: main code
    command = 'ffprobe -loglevel error -select_streams v -show_entries stream=codec_type -of csv=p=0 "' + path + '"'
    process = shlex.split(command)

def create_full():
    # High level program tasks: generates resourcepack and datapack from video

    # TODO: finish main code

    video_name = get_video_name()
    video_path = get_video_path()

    print("\nConverting video to frames...")

    frame_count = get_frame_count_from_video(video_path)

    convert_video_to_frames(video_path)


def create_datapack_only():
    # High level program tasks: generates datapack based on information supplied by user

    # TODO: finish main code

    video_name = get_video_name()
    frame_count = get_frame_count_from_user()


# Initiates startup process
ffmpeg_status = check_for_ffmpeg()
ffprobe_status = check_for_ffprobe()

if (ffmpeg_status == 1 & ffprobe_status == 1):
    startup()
elif (ffmpeg_status == -1 | ffprobe_status == -1):
    error('\nAn internal error occurred while checking for the following dependencies:')
    if (ffmpeg_status == -1): error("- ffmpeg")
    if (ffprobe_status == -1): error("- ffprobe")
    error('Please report this to the developer.')
else:
    warning('This program requires ffmpeg and ffprobe to be installed.\nGet those at: https://www.ffmpeg.org/download.html\nBe sure to select the installer file appropriate for your OS. (Not "Download Source Code")')

# pauses
# input("")