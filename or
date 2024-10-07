#!/usr/bin/env python3
# run selected odoo MAIN version , so one of the ones for which worktres are created

import multiprocessing as mp
import argparse
import subprocess
# from fuzzywuzzy import fuzz, process
import psutil
from pathlib import Path
import time
from versions import Version, VERSIONS

ODOO='odoo'
ENTERPRISE='enterprise'
WT_DIR=Path("/home/odoo/Repos/Odoo/wt")  # path to directory with:
# .
# ├── cwt            <- dir with all community worktree branches: 14.0, 15.0, saas-15.2 ...
# ├── enterprise     <- primary repo with enterprise
# ├── ewt            <- dir with all enterprise worktree branches: 14.0, 15.0, saas-15.2 ...
# └── odoo           <- primary repo with community


def match_version(s:str):
    """Returns [] if no match, returns [Version, Version...] on matches
    """
    matches = []
    for v in VERSIONS:
        if s == v:
            matches.append(v)
    return matches

def parse_arguments():
    description=''' or i.e. Odoo Run
        Usage examples:
            or 15       <- switches git branches to 15.0, next runs odoo version 15
            or -s 15    <- opens interactive shell with db 15 (db called "15" gotta exist)
            '''
    parser = argparse.ArgumentParser(description='or i.e "Odoo run" [version]')
    parser.add_argument("version", nargs="?", default=None, help="Which version do you want to run? ")  
    parser.add_argument('--force', '-f', action='store_true', help='run even if it is already running, (duplicate)')
    parser.add_argument('--shell', '-s', action='store_true', help='run interactive shell')
    parser.add_argument('--community', '-c', action='store_true', help='run only community addons')
    parser.add_argument('--preserve', '-p', action='store_true', help='Do NOT switch branches, nor pull. Run odoo as it is.')
    parser.add_argument('extra_args', nargs='*', help='kwargs to pass to odoo-bin, pass after double dash --, like -- -i crm')
    return parser.parse_args()

def _switch_branch(repo_path, version_formal):
    subprocess.run(['git', '-C', repo_path, 'switch', version_formal])

def ensure_correct_git_branch(version:Version):
    """It may happen that wt is on a different branch, this will restore required one"""
    print("Switching...", end="")
    p1 = mp.Process(target=_switch_branch, args=(WT_DIR/version.formal/'odoo', version.formal))
    p2 = mp.Process(target=_switch_branch, args=(WT_DIR/version.formal/'enterprise', version.formal))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(" done")

def _pull_worktree(path):
    subprocess.run(['git', '-C', path, 'pull'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def pull(version:Version):
    print("Pulling...", end="")
    p1 = mp.Process(target=_pull_worktree, args=(WT_DIR/version.formal/'odoo', ))
    p2 = mp.Process(target=_pull_worktree, args=(WT_DIR/version.formal/'enterprise', ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(" done")

def _append_histfile(cmd):
    timestamp = int(time.time())
    cmd_str=' \\\\\n'.join(cmd)
    history_entry = f": {timestamp}:0;{cmd_str}\n"
    with open("/home/odoo/.zsh_history", "a") as history_file:
        history_file.write(history_entry)


def run_odoo(version:Version, shell:bool=False, community:bool=False, extra_args:list=[]):
    conda_python=f'/home/odoo/miniconda3/envs/{version.formal}/bin/python3'
    dir_odoo=WT_DIR/version.formal/'odoo'
    odoo_bin=str(dir_odoo/'odoo-bin')
    addons=         f"--addons-path={dir_odoo}/addons/"
    if not community:
        addons+=f",{dir_odoo.parent/'enterprise'}"
    db_host =        "--db_host=127.0.0.1"
    db_port =        "--db_port=5433" # TODO infer that
    db_name =       f"--database={version.short}"
    db_user =        "--db_user=odoo"
    db_password =    "--db_password=odoo"
    http_interface= f"--http-interface={version.ip}"
    cmd=[conda_python, odoo_bin, 'shell', addons, db_host, db_port, db_name, db_user, db_password, http_interface] + extra_args
    if not shell:
        cmd.pop(2)
    print("Running command:\n", ' \\\n'.join(cmd), '\n')
    _append_histfile(cmd)
    res= subprocess.run(cmd)

def is_already_running(version:Version):
    processes=[]
    for process in psutil.process_iter(['pid', 'name', 'cpu_times', 'create_time', 'cmdline']):
        # if 'python' in str(process.info.get('cmdline', "")):
        if 'odoo-bin' in str(process.info.get('cmdline', "")):
            pass
            processes.append({
                'pid':           process.pid,
                'cmdline':       process.info['cmdline'],
                'create_time':   process.info['create_time'],
                'cpu_time':      process.info['cpu_times'],
            })
    for p in processes:
        if f"/{version.formal}/" in str(p['cmdline']):
            print("detected", str(p['cmdline']))
            return True
    return False

def fuzzy_selector(given_version_str:str)-> str:
    raise NotImplementedError("fuzzy_selector still to be implemented")
    # return versions_map["14"]

def change_tmux_window_name(new_name):
    subprocess.run(["tmux", "rename-window", new_name])

def main():
    # select version
    args = parse_arguments()
    if len((v := match_version(args.version))) != 1:
        v= fuzzy_selector(args.version)
    v=v[0]
    # check if already running
    if not args.force and is_already_running(v):
        print(f"odoo {v.short} is already running (add --force for duplicates)")
    else:
        if not args.preserve:
            ensure_correct_git_branch(v)
            pull(v)
        change_tmux_window_name(v.short)
        run_odoo(v, args.shell, args.community, args.extra_args)


if __name__ == "__main__":
    main()
