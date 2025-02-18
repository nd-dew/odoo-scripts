import os
import subprocess
from versions import VERSIONS
import re

ODOO_COMMUNITY_CWD = '/home/odoo/Repos/Odoo/odoo'
ODOO_ENTERPRISE_CWD = '/home/odoo/Repos/Odoo/enterprise'

BRANCHES = [version.formal for version in VERSIONS]


def run_git_command(command, cwd):
    """Run a Git command in the specified directory and return the output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\n{e.stderr}")
        return None


def is_working_directory_clean(cwd):
    """Check if the Git working directory is clean."""
    status = run_git_command(["git", "status", "--porcelain"], cwd)
    return status == ""


def fetch_branches(cwd, origin_name='odoo', branches=BRANCHES):
    """Fetch updates for the specified branches without checking them out."""
    for branch in branches:
        print(f"\nFetching updates for branch: {branch}")
        fetch_output = run_git_command(["git", "fetch", origin_name, branch], cwd)
        if fetch_output is None:
            print(f"Failed to fetch branch {branch}.")
        else:
            print(f"Successfully fetched updates for branch {branch}.")


# def get_worktrees(cwd):
#     """Get a list of all worktree directories."""
#     worktree_output = run_git_command(["git", "worktree", "list", "--porcelain"], cwd)
#     if not worktree_output:
#         print("Failed to retrieve worktrees.")
#         return []
#     # Parse the output to extract directories
#     worktrees = []
#     for line in worktree_output.splitlines():
#         if line.startswith("worktree "):
#             worktrees.append(line.split(" ", 1)[1])
#     return worktrees



def extract_branch_name(path):
    """Extract branch name from a worktree path."""
    match = re.search(r'wt/?([^/]+)/', path)
    return match.group(1) if match else None


def get_worktrees(cwd):
    """Get a mapping of branches to their worktree directories."""
    worktree_output = run_git_command(["git", "worktree", "list", "--porcelain"], cwd)
    if not worktree_output:
        print("Failed to retrieve worktrees.")
        return {}

    branch_name_2_worktree_dir_mapping = {}
    current_worktree = None
    branch_or_ref = None

    for wortree_triline in worktree_output.split("\n\n"):
        if wortree_triline.startswith("worktree "):
            wortree_triline = wortree_triline.replace("worktree ", "")
            path_head_branch = wortree_triline.split("\n")
            path = path_head_branch[0]
            branch = extract_branch_name(path)
            if not branch:
                continue
            else:
                branch_name_2_worktree_dir_mapping[branch] = path

    return branch_name_2_worktree_dir_mapping


def update_worktrees(cwd, origin_name='origin', branches=BRANCHES):
    """Update each branch by locating its corresponding worktree and performing a fast-forward merge."""
    worktree_mapping = get_worktrees(cwd)
    if not worktree_mapping:
        print("No worktrees found.")
        return

    for branch in branches:
        if branch not in worktree_mapping:
            print(f"No worktree found for branch '{branch}'. Skipping...")
            continue

        worktree_dir = worktree_mapping[branch]
        print(f"\nUpdating branch: {branch} in worktree: {worktree_dir}")

        # Ensure the branch is checked out in the worktree
        switch_output = run_git_command(["git", "switch", branch], worktree_dir)
        if switch_output is None:
            print(f"Failed to switch to branch '{branch}' in worktree '{worktree_dir}'. Skipping...")
            continue

        # Perform a fast-forward merge
        print(f"Attempting fast-forward merge for branch '{branch}' in worktree {worktree_dir}...")
        merge_output = run_git_command(["git", "merge", "--ff-only", f"{origin_name}/{branch}"], worktree_dir)
        if merge_output is None:
            print(f"Failed to fast-forward branch '{branch}' in worktree {worktree_dir}.")
            # Log additional information
            log_local_branch = run_git_command(["git", "log", f"{branch}..{origin_name}/{branch}", "--oneline"], worktree_dir)
            log_remote_branch = run_git_command(["git", "log", f"{origin_name}/{branch}..{branch}", "--oneline"], worktree_dir)
            print(f"Commits on remote but not on local:\n{log_local_branch}")
            print(f"Commits on local but not on remote:\n{log_remote_branch}")
        else:
            print(f"Successfully fast-forwarded branch '{branch}' in worktree {worktree_dir}.")



if __name__ == "__main__":
    # if not os.path.isdir(ODOO_COMMUNITY_CWD):
    #     print(f"Error: The specified path {ODOO_COMMUNITY_CWD} is not a valid directory.")
    # else:
    #     # Fetch and update community branches
    #     fetch_branches(ODOO_COMMUNITY_CWD, branches=BRANCHES)

    # if not os.path.isdir(ODOO_ENTERPRISE_CWD):
    #     print(f"Error: The specified path {ODOO_ENTERPRISE_CWD} is not a valid directory.")
    # else:
    #     # Fetch and update enterprise branches
    #     fetch_branches(ODOO_ENTERPRISE_CWD, origin_name='origin', branches=BRANCHES)

    # get_worktrees(ODOO_COMMUNITY_CWD)
    update_worktrees(ODOO_COMMUNITY_CWD, branches=BRANCHES)
