#!/usr/bin/env bash
#   ___   __| | ___   ___        ___| |__   __ _ _ __   __ _  ___      / /   __| (_)_ __  \ \ 
#  / _ \ / _` |/ _ \ / _ \      / __| '_ \ / _` | '_ \ / _` |/ _ \    | |   / _` | | '__|  | |
# | (_) | (_| | (_) | (_) |    | (__| | | | (_| | | | | (_| |  __/    | |  | (_| | | |     | |
#  \___/ \__,_|\___/ \___/      \___|_| |_|\__,_|_| |_|\__, |\___|    | |   \__,_|_|_|     | |
#                                                      |___/           \_\                /_/ 

# Link in your bashrc

# Set of Odoo change dir scripts,

# AKA occ

_base_odoo_change(){
    # This function, '_base_odoo_change', sets paths for various Odoo versions
    # within the specified directory structure. The associative array 'all_versions'
    # provides convenient aliases for different versions, allowing for easy
    # switching between Odoo releases during development. The 'prefix' variable
    # defines the base directory where Odoo versions are stored.

    # Associative array mapping Odoo version aliases to their corresponding worktree locations.
    # orgaznided as: [yr_shortcut_1]=path_to_worktree [yr_shortcut_2]=path_to_worktree ...
    # usage: "oc yr_shortcut_1"  -> changes dir to path_to_worktree
    prefix="/home/odoo/Repos/Odoo/wt"
    declare -A all_versions=(
        ["saas-15.2"]="${prefix}/saas-15.2" ["15.2"]="${prefix}/saas-15.2" ["152"]="${prefix}/saas-15.2"
        ["16.0"]="${prefix}/16.0" ["16"]="${prefix}/16.0"
        ["saas-16.1"]="${prefix}/saas-16.1" ["16.1"]="${prefix}/saas-16.1" ["161"]="${prefix}/saas-16.1"
        ["saas-16.2"]="${prefix}/saas-16.2" ["16.2"]="${prefix}/saas-16.2" ["162"]="${prefix}/saas-16.2"
        ["saas-16.3"]="${prefix}/saas-16.3" ["16.3"]="${prefix}/saas-16.3" ["163"]="${prefix}/saas-16.3"
        ["saas-16.4"]="${prefix}/saas-16.4" ["16.4"]="${prefix}/saas-16.4" ["164"]="${prefix}/saas-16.4"
        ["17.0"]="${prefix}/17.0" ["17"]="${prefix}/17.0"
        ["saas-17.1"]="${prefix}/saas-17.1" ["17.1"]="${prefix}/saas-17.1" ["171"]="${prefix}/saas-17.1"
        ["saas-17.2"]="${prefix}/saas-17.2" ["17.2"]="${prefix}/saas-17.2" ["172"]="${prefix}/saas-17.2"
        ["saas-17.3"]="${prefix}/saas-17.3" ["17.3"]="${prefix}/saas-17.3" ["173"]="${prefix}/saas-17.3"
        ["saas-17.4"]="${prefix}/saas-17.4" ["17.4"]="${prefix}/saas-17.4" ["174"]="${prefix}/saas-17.4"
        ["18.0"]="${prefix}/18.0" ["18"]="${prefix}/18.0"
        ["saas-18.1"]="${prefix}/saas-18.1" ["18.1"]="${prefix}/saas-18.1" ["181"]="${prefix}/saas-18.1"
        ["master"]="${prefix}/master" ["ms"]="${prefix}/master"
        ["182"]="/home/odoo/Repos/Odoo/wt/saas-182"
)


    if [ -n "${all_versions[$1]}" ]; then
        target_path="${all_versions[$1]}"
        cd "$target_path" || return 1
        echo "$target_path"
    else
        echo "Error: Unknown Odoo version '$1'"
        return 1
    fi
}

oc(){
    echo -ne "\033[A\033[K"  # Move up one line and clear the line
    echo "$0 $@  -> Odoo Change into '$1'"
    _base_odoo_change "$1"
}

occ(){
    echo -ne "\033[A\033[K"  # Move up one line and clear the line
    echo "$0 $@  -> Odoo Change into '$1' and open Code"
    target_path=$(_base_odoo_change "$1") && code "$target_path"
    _base_odoo_change "$1"
}

occr(){
    echo -ne "\033[A\033[K"  # Move up one line and clear the line
    echo "$0 $@  -> Odoo Change into '$1' and open Code and Run"
    target_path=$(_base_odoo_change "$1") && code "$target_path" && or "$1"
    _base_odoo_change "$1"
}
