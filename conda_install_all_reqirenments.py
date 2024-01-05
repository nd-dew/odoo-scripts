import os
import subprocess
from colorama import Fore, Style, Back

branch_names = [
    "16.0",
    "15.0", 
    "14.0", 
    "master",
    "saas-16.1",
    "saas-16.2",
    "saas-16.3",
    "saas-16.4",
]


# Define the directory you want to navigate to
directory_path = "/home/odoo/Repos/Odoo/community"

# Check if the specified directory exists
if not os.path.exists(directory_path):
    print(f"The directory '{directory_path}' does not exist.")
    exit(1)

for branch_name in branch_names:
    command=f"git switch {branch_name}"
    print(f"{Back.WHITE}Branch: {branch_name} git switch{Style.RESET_ALL}\n{command}")
    try:
        # Run the 'git switch' command
       
        subprocess.run(command, check=True, shell=True, cwd=directory_path, )#stdout=subprocess.PIPE)
        print(f"Switched to branch '{branch_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while switching to branch '{branch_name}':")
        raise(e)
    
    command+=" && git pull"
    print(f"{Back.WHITE}Branch: {branch_name} git pull{Style.RESET_ALL}\n{command}")
    try:
        # Run the 'git pull' command
        subprocess.run(command, check=True, shell=True, cwd=directory_path, )#stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error while pulling branch '{branch_name}':")
        raise(e)

    command+=f" && /home/odoo/miniconda3/envs/{branch_name}/bin/python3 -m pip install -r requirements.txt"
    print(f"{Back.WHITE}Branch: {branch_name} pip3 install requirenments{Style.RESET_ALL}\n{command}")
    try:
        # Run the 'git pull' command
        subprocess.run(command, check=True, shell=True, cwd=directory_path, )#stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error while installing requirenments '{branch_name}':")
        raise(e)


    # break
    print("\n")
