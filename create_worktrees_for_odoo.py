#!/usr/bin/env python 
import argparse
from pathlib import Path
import subprocess
import re

doc=""" Create worktrees for community enterprise in separate folders. 
    
    Example:
            ./create_worktrees_for_odoo.py --wt /home/wt --c /odoo_community_repo --e /odoo_enterprise_repo

        This command will use source folders:
        -  /odoo_community_repo            
        -  /odoo_enterprise_repo

        And create the following folder structure filled with worktrees:
        /home/wt:
            ├── 15.0
            │   ├── enterprise
            │   └── odoo
            ├── saas-15.2
            │   ├── enterprise
            │   └── odoo
            ├── 16.0
            │   ├── enterprise
            │   └── odoo
            ├── saas-16.1
            │   ├── enterprise
            .   └── odoo
            .
            .

            └── master
                ├── enterprise
                └── odoo
    """

MAIN_ODOO_BRANCHES=[
    "15.0",
    "16.0",
    "17.0",
    "saas-17.1",
    "saas-17.2",
    "saas-17.3",
    "saas-17.4",
    "master",
]

doc+="\nList of odoo branches used by this script:\n"
for branch in MAIN_ODOO_BRANCHES:
    doc+=f"\t{branch}\n"

def parse_arguments():
    parser = argparse.ArgumentParser(description=f"{doc}", formatter_class=argparse.RawDescriptionHelpFormatter
)
    parser.add_argument("--wt", required=True, help="work-trees:  dir to create worktrees in")
    parser.add_argument("--c", required=True, help="directory with odoo community repo cloned  (source to create worktrees from)")
    parser.add_argument("--e", required=True, help="directory with odoo enterprise repo cloned (source to create worktrees from)")
    return parser.parse_args()

def create_wt_dir_if_doesnt_exist(dir_path:Path):
    dir_path.mkdir(parents=True, exist_ok=True)

def fetch_branch_from_repo(branch_name, repo_path):
    """
    Args:
        branch_name (_type_): branch to fetch from
        repo_path (_type_): Path to the repository that branch you want to fetch.
    """
    cmd = ['git', '-C', repo_path, 'fetch', 'origin', branch_name]
    res= subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )

def create_worktree_from_repo(branch_name:str, repo_path:str, worktrees_root_dir:str):
    """ Creates a worktree from a repository for a given branch in a given directory.
            Example: create_worktree_from_repo(branch_name='15', repo_path='/enterprise', worktrees_root_dir='wt/15')
            will create a worktree of branch '15' in directory 'wt/15' 
            as if command would be executed in the '/enterprise' directory
    Args:
        branch_name (str): Branch name to create worktree OF.
        repo_path (str):  Path to repo to source worktree creation FROM. Allows to specify whether to use community or enterprise.
        worktrees_root_dir (str): Path to a dir where worktree (for branch_name) will be placed. 
    """
    cmd= ['git', '-C', repo_path, 'worktree', 'add', worktrees_root_dir, branch_name]
    res= subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )
    return res

def is_worktree_already_created(branch_name:str, repo_path:str, worktrees_root_dir):
    # limitation worktree dir path has to contain branch_name as a folder! Otherwise it won't get recognized.
    # So branch 15.0 worktree has to be in a directory **/15.0/**

    worktree_list_str = subprocess.check_output(['git', '-C', repo_path ,'worktree', 'list'], universal_newlines=True)
    # worktree_list_str have the following form
    # /home/odoo/Repos/Odoo/wt/saas-15.2/odoo  f036ea6dfd1f [saas-15.2]
    # /home/odoo/Repos/Odoo/wt/saas-16.1/odoo  73e0e2b6233a [saas-16.1]
    # ... 
    pattern = re.compile(worktrees_root_dir + r'\/.*\/')
    existing_wt_paths = pattern.findall(worktree_list_str) # returns list with elements like '/home/odoo/Repos/Odoo/wt/14.0/'
    existing_wt_branch_names = [ path.split(worktrees_root_dir)[1].strip('/') for path in existing_wt_paths ] # returns list with elements like '/14.0/'
    return branch_name in existing_wt_branch_names 

def setup(args):
    """ Switch both community and enterprise repositories to tmp_branch (which gets created if needed). this is needed because you can't create a worktree from a branch you are currently on."""
    res= subprocess.run(['git', '-C', args.c, 'checkout', '-b', 'tmp_branch'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res= subprocess.run(['git', '-C', args.c, 'switch', 'tmp_branch'],         stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    res= subprocess.run(['git', '-C', args.e, 'checkout', '-b', 'tmp_branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res= subprocess.run(['git', '-C', args.c, 'switch', 'tmp_branch'],         stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def main():
    args = parse_arguments()
    msg=f"\nSUMMARY:\ncommunity ({args.c}):"
    
    setup(args)
    
    print("Running: ", end=' '); progressbar_msg= (x for x in list("probably."+'.'*99))
    for branch_name in MAIN_ODOO_BRANCHES:
        msg+=f"\n\t{branch_name:<11}"
        if is_worktree_already_created(branch_name, repo_path=args.c, worktrees_root_dir=args.wt):
            msg+=" already exists" 
        else:
            create_wt_dir_if_doesnt_exist(Path(args.wt)/branch_name)
            fetch_branch_from_repo(branch_name, repo_path=args.c)
            create_worktree_from_repo(branch_name, repo_path=args.c, worktrees_root_dir=Path(args.wt)/branch_name/"odoo")
            msg+=f" probably added ;)"
        print(next(progressbar_msg), end='')


    msg+=f"\n\nenterprise ({args.e}):"
    for branch_name in MAIN_ODOO_BRANCHES:
        msg+=f"\n\t{branch_name:<11}"
        if is_worktree_already_created(branch_name, repo_path=args.e, worktrees_root_dir=args.wt):
            msg+=" already exists"
        else:
            create_wt_dir_if_doesnt_exist(Path(args.wt)/branch_name)
            fetch_branch_from_repo(branch_name, repo_path=args.e)
            create_worktree_from_repo(branch_name, repo_path=args.e, worktrees_root_dir=Path(args.wt)/branch_name/"enterprise")
            msg+=f" probably added ;)"
        print(next(progressbar_msg), end='')


    print('\n'+msg)


if __name__ == "__main__":
    main()
