import os
from pathlib import Path
import subprocess
from colorama import Fore, Style, Back

branch_names = [
    "15.0",
    "16.0",
    "17.0",
    "saas-17.1",
    "saas-17.2",
    "saas-17.3",
    "saas-17.4",
    "master",
]


# Define the directory you want to navigate to
directory_path = Path("/home/odoo/Repos/Odoo/wt")

# Check if the specified directory exists
if not os.path.exists(directory_path):
    print(f"The directory '{directory_path}' does not exist.")
    exit(1)

for branch_name in branch_names:
    command=f"git switch {branch_name}"
    print(f"{Back.WHITE}Branch: {branch_name} git switch{Style.RESET_ALL}\n{command}")
    cwd = directory_path/branch_name/'odoo'
    try:
        # Run the 'git switch' command
       
        subprocess.run(command, check=True, shell=True, cwd=cwd )#stdout=subprocess.PIPE)
        print(f"Switched to branch '{branch_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while switching to branch '{branch_name}':")
        raise(e)
    
    command+=" && git pull"
    print(f"{Back.WHITE}Branch: {branch_name} git pull{Style.RESET_ALL}\n{command}")
    try:
        # Run the 'git pull' command
        subprocess.run(command, check=True, shell=True, cwd=cwd, )#stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error while pulling branch '{branch_name}':")
        raise(e)

    command+=f" && /home/odoo/miniconda3/envs/{branch_name}/bin/python3 -m pip install -r requirements.txt"
    print(f"{Back.WHITE}Branch: {branch_name} pip3 install requirenments{Style.RESET_ALL}\n{command}")
    try:
        # Run the 'git pull' command
        subprocess.run(command, check=True, shell=True, cwd=cwd, )#stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error while installing requirenments '{branch_name}':")
        raise(e)


    # break
    print("\n")
