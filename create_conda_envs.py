import subprocess

# Define Python version
python_version = "3.10"

# Define a list of environment names
env_names = [
    "14.0", 
    "15.0", 
    "16.0",
    "master",
    "saas-16.1",
    "saas-16.2",
    "saas-16.3",
    "saas-16.4",
    "saas-17.1",
    "saas-17.2",
]


# Iterate through the lists and create the environments
for env_name in env_names:
    # Check if the environment already exists
    output = subprocess.check_output("conda env list", text=True, shell=True)
    if any(env_name in line for line in output.splitlines()):
        print(f"Environment {env_name} already exists. Skipping...")
    
    else: # Environment does not exist; create it
        print(f"Creating environment {env_name} with Python {python_version}...")
        subprocess.run(f"conda create -n {env_name} python={python_version} -y", shell=True)
        subprocess.run(f"conda create -n {env_name} python={python_version} -y", shell=True)
