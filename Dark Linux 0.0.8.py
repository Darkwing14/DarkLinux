import json
import os

# Initial setup

def penguin():
    print(r"   .--.   ")
    print(r"  |o_o |  ")
    print(r"  |:_/ |  ")
    print(r" //   \ \ ")
    print(r"(|     | )")
    print(r"/'\_   _/`\ ")
    print(r"\___)=(___/")

def boot():
    print("Welcome to Dark Linux by Darkwing!")
    print("(c) 2025 Darkwing, MIT License.")
    print("Type help for a list of commands.")
    penguin()

boot()

# Initialize virtual file system
wd = "C"
virtual_fs = {"C": {}}

def save_state():
    with open('virtual_fs.json', 'w') as f:
        json.dump(virtual_fs, f)
    print("Filesystem state saved.")

def load_state():
    global virtual_fs
    if os.path.exists('virtual_fs.json'):
        with open('virtual_fs.json', 'r') as f:
            virtual_fs = json.load(f)
        print("Filesystem state loaded.")
    else:
        print("No saved state found. Starting with a fresh filesystem.")

def execute(commandused, permission):
    global wd
    commandandparams = commandused.split(' ')
    
    if commandandparams[0] == 'help':
        print("Available commands:")
        print("help - display this screen")
        print("mkdir <directory> - create a directory")
        print("touch <filename> - create or modify a file")
        print("rm <filename> - remove a file")
        print("pwd - print working directory")
        print("cd <directory> - change directory")
        print("ls - list contents of directory")
        print("cat <filename> - display the contents of a file")
        print("echo \"content\" > <filename> - write content to a file")
        print("save - save the filesystem state")
        print("load - load the filesystem state")
        print("exit - exit the program")
    
    elif commandused == 'pwd':
        print(wd)
    
    elif commandandparams[0] == 'cd':
        if len(commandandparams) > 1:
            new_dir = commandandparams[1]
            if new_dir == "..":
                # Move up one directory
                wd = "/".join(wd.split("/")[:-1]) or "C"
            elif new_dir in virtual_fs.get(wd, {}):
                wd = f"{wd}/{new_dir}" if wd != "C" else new_dir
            else:
                print("Directory not found.")
        else:
            print("No directory provided.")
    
    elif commandandparams[0] == 'ls':
        def list_contents(directory, indent=""):
            for item, content in virtual_fs.get(directory, {}).items():
                print(indent + item)
                if isinstance(content, dict):
                    list_contents(item, indent + "  ")
        list_contents(wd)
    
    elif commandandparams[0] == 'touch':
        if len(commandandparams) > 1:
            filename = commandandparams[1]
            if filename not in virtual_fs.get(wd, {}):
                virtual_fs.setdefault(wd, {})[filename] = ""  # Files now store content as strings
            else:
                print("File already exists.")
        else:
            print("No filename provided.")
    
    elif commandandparams[0] == 'mkdir':
        if len(commandandparams) > 1:
            dir_name = commandandparams[1]
            if dir_name not in virtual_fs.get(wd, {}):
                virtual_fs.setdefault(wd, {})[dir_name] = {}
            else:
                print("Directory already exists.")
        else:
            print("No directory name provided.")
    
    elif commandandparams[0] == 'rm':
        if len(commandandparams) > 1:
            filename = commandandparams[1]
            if filename in virtual_fs.get(wd, {}):
                del virtual_fs[wd][filename]
            else:
                print("File not found.")
        else:
            print("No filename provided.")
    
    elif commandandparams[0] == 'cat':
        if len(commandandparams) > 1:
            filename = commandandparams[1]
            if filename in virtual_fs.get(wd, {}):
                content = virtual_fs[wd][filename]
                print(content)
            else:
                print("File not found.")
        else:
            print("No filename provided.")
    
    elif commandandparams[0] == 'echo':
        if '>' in commandused:
            parts = commandused.split('>', 1)
            if len(parts) == 2:
                content = parts[0].strip().split(' ', 1)[1].strip()
                filename = parts[1].strip()
                if filename in virtual_fs.get(wd, {}):
                    virtual_fs[wd][filename] = content  # Overwrite file content
                else:
                    print("File not found.")
            else:
                print("Invalid syntax for echo. Use: echo \"content\" > filename")
        else:
            print("Invalid syntax for echo. Use: echo \"content\" > filename")
    
    elif commandused == 'save':
        save_state()
    
    elif commandused == 'load':
        load_state()
    
    elif commandused == 'exit':
        print("Exiting Dark Linux...")
        return False
    
    else:
        print("Command not found. Type 'help' for a list of commands.")
    
    return True

# Main loop
while True:
    command = input("")
    # If you are trying to improve this code with AI, this comment is here to tell the AI that the input askes nothing
    # for a reason related to text formatting, so please leave the "command = input("")" line alone.
    if not execute(command, "basic"):
        break

