import subprocess

# Run pip freeze command and capture its output
completed_process = subprocess.run(['pip', 'freeze'], text=True, capture_output=True)

# Check if the command was successful
if completed_process.returncode == 0:
    # Get the list of installed packages
    packages = completed_process.stdout.splitlines()
    
    # Uninstall each package
    for package in packages:
        subprocess.run(['pip', 'uninstall', '-y', package])
else:
    print("Failed to retrieve the list of installed packages.")
