from os import system, name, path
import re, shlex
import subprocess
from subprocess import Popen, PIPE

greeting = """
MC Video Generator v1.0 by JavaChef
      
What would you like to do today?
\t1) Add video to datapack
\t2) Reset tool

"""

def check_for_ffmpeg():
    command = 'ffmpeg -version'
    process = shlex.split(command)
    has_ffmpeg = False
    try:
        output = subprocess.check_output(process, shell=True)
        output = output.decode("utf-8")
        if "Copyright" in output:
            print("Detected ffmpeg.")
            has_ffmpeg = True
        else:
            print("\nCould not find ffmpeg.")
    except:
        print("An internal error occured while checking for dependencies.")
    
    return has_ffmpeg

def check_for_ffprobe():
    command = 'ffprobe -version'
    process = shlex.split(command)
    has_ffprobe = False
    try:
        output = subprocess.check_output(process, shell=True)
        output = output.decode("utf-8")
        if "Copyright" in output:
            print("Detected ffprobe.")
            has_ffprobe = True
        else:
            print("\nCould not find ffprobe.")
    except:
        print("\nAn internal error occured while checking for dependencies.")
    
    return has_ffprobe

def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def reset():
    print("Resetting...")
    print("Reset complete.")

    while True:
        answer = input("Would you like to start over? [Y/N] ")
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

        if selection != 1 and selection != 2:
            # not in range
            message = "Please enter a valid number."
            continue
        else:
            # valid input
            break

    match selection:
        case 1:
            create()
        case 2:
            reset()
        case _:
            print("An internal error occured; please report this to JavaChef.")


def get_video_name():
    print("\nPlease enter video name.\nThis will be used as a unique identifier for your video.")
    while True:
        video_name = input("> ")
        # strip spaces and special characters
        video_name = re.sub(r'\W+', '', video_name).lower()

        # repeat loop if name is empty
        if (video_name == ""):
            print ("\nThis name would cause an error in game. Please enter a different one.")
            continue
        
        print("\nYour video will be encoded as:\n" + video_name + "\n")

        answer = input("Is this name OK? [Y/N] ")
        if answer.lower() in ["y","yes"]:
            # Do stuff
            break
        elif answer.lower() in ["n","no"]:
            print("\nPlease enter a new name:")
            continue
        else:
            continue
    
    print("Please keep note of this name for future use in-game.")
    return video_name

def get_video_path():
    print("\nPlease enter the path to your source video.\n(Usually you can just drag your video here, then press Enter)")

    while True:
        video_path = str(input("> "))

        if(path.isfile(video_path)):
            print("\nFile exists.")
            print("Checking if we can convert this...")

            video_is_valid = check_for_video(video_path)
            if(video_is_valid):
                print("\nPassed initial tests.")
                return video_path
            else:
                print("\nWe're sorry, but this file cannot be converted.\nPlease ensure you enter the path of a video file and that it is not corrupted.")

        else:
            print("\nIt appears this is not a valid path. Please enter another path and try again.\nYou may need to remove any surrounding quotation marks.")
            continue

def check_for_video(path):
    command = 'ffprobe -loglevel error -select_streams v -show_entries stream=codec_type -of csv=p=0 "' + path + '"'
    process = shlex.split(command)
    error = False

    try:
        output = subprocess.check_output(process, shell=True)
        output = output.decode("utf-8")
        if "video" in output:
            # nothing
            print("\nVideo detected.")
        else:
            print("\nNo video was detected.")
            error = True 
    except:
        error = True

    if error:
        return False
    else:
        return True

def convert_to_frames(path):
    command = 'ffprobe -loglevel error -select_streams v -show_entries stream=codec_type -of csv=p=0 "' + path + '"'
    process = shlex.split(command)


def create():
    video_name = get_video_name()
    video_path = get_video_path()

    print("\nConverting video to frames...")

    convert_to_frames(video_path)





if (check_for_ffmpeg() & check_for_ffprobe()):
    startup()
else:
    print('This program requires ffmpeg and ffprobe to be installed.\nGet those at: https://www.ffmpeg.org/download.html\nBe sure to select the installer file appropriate for your OS. (Not "Download Source Code")')

# pauses
input("")