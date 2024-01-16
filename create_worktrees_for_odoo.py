#!/usr/bin/env python 
import argparse
from pathlib import Path
import subprocess

doc=""" Create worktrees for community enterprise in separate folders. Example:
            ./create_worktrees_for_odoo.py --wt /home/worktrees --c /odoo_community_repo --e /odoo_enterprise_repo

    This command will use source folders:
    -  /home/odoo_community_repo            
    -  /odoo_enterprise_repo

    And create the following folder structure filled with worktrees:
    /home/worktrees:
    ├── 14.0
    │   ├── enterprise
    │   └── odoo
    ├── 15.0
    │   ├── enterprise
    │   └── odoo
    ├── 16.0
    │   ├── enterprise
    │   └── odoo
    ├── 17.0
    │   ├── enterprise
    │   └── odoo
    ├── master
    │   ├── enterprise
    │   └── odoo
    ├── saas-15.2
    │   ├── enterprise
    │   └── odoo
    ├── saas-16.1
    │   ├── enterprise
    │   └── odoo
    ├── saas-16.2
    │   ├── enterprise
    │   └── odoo
    ├── saas-16.3
    │   ├── enterprise
    │   └── odoo
    ├── saas-17.1
    │   ├── enterprise
    │   └── odoo
    └── saas-16.4
        ├── enterprise
        └── odoo
    """

MAIN_ODOO_BRANCHES=[
  "15.0",
  "saas-15.2",
  "16.0",
  "saas-16.1",
  "saas-16.2",
  "saas-16.3",
  "saas-16.4",
  "17.0",
  "saas-17.1",
  "master",
]

def parse_arguments():
    parser = argparse.ArgumentParser(description=f"{doc}", formatter_class=argparse.RawDescriptionHelpFormatter
)
    parser.add_argument("--wt", required=True, help="work-trees:  dir to create worktrees in")
    parser.add_argument("--c", required=True, help="directory with odoo community repo cloned  (source to create worktrees from)")
    parser.add_argument("--e", required=True, help="directory with odoo enterprise repo cloned (source to create worktrees from)")
    return parser.parse_args()

def create_version_dir_if_doesnt_exist(dir_path:Path):
    dir_path.mkdir(parents=True, exist_ok=True)

    c

def main():
    args = parse_arguments()
    msg=f"\nSUMMARY:\ncommunity ({args.c}):"
    res= subprocess.run(['git', '-C', args.c, 'checkout', '-b', 'to_delete'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res= subprocess.run(['git', '-C', args.c, 'switch', 'to_delete'],         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print("running: ", end=' '); probably= (x for x in list("probably."+'.'*30))
    for branch_name in MAIN_ODOO_BRANCHES:
        msg+=f"\n\t{branch_name:<11}"
        create_version_dir_if_doesnt_exist(Path(args.wt)/branch_name)

        cmd = ['git', '-C', args.c, 'fetch', 'origin', branch_name]
        res= subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )

        cmd= ['git', '-C', args.c, 'worktree', 'add', Path(args.wt)/branch_name/"odoo", branch_name]
        res= subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )
        if res.stderr and "already exists" in res.stderr:
            msg+=" already exists" 
        else:
            msg+=f" probably added xD"
        print(next(probably), end='')

    res= subprocess.run(['git', '-C', args.e, 'checkout', '-b', 'to_delete'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg+=f"\n\nenterprise ({args.e}):"
    for branch_name in MAIN_ODOO_BRANCHES:
        msg+=f"\n\t{branch_name:<11}"

        cmd = ['git', '-C', args.e, 'fetch', 'origin', branch_name]
        res= subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )

        cmd= ['git', '-C', args.e, 'worktree', 'add', Path(args.wt)/branch_name/"enterprise", branch_name]
        res= subprocess.run(cmd,            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        if res.stderr and "already exists" in res.stderr:
            msg+=" already exists" 
        else:
            msg+=f" added"
        print(next(probably), end='')

    
    print('\n'+msg)
    res= subprocess.run(['git', '-C', args.c, 'checkout', '-b', 'to_delete'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

if __name__ == "__main__":
    main()
