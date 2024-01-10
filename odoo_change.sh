#!/usr/bin/env bash
#   ___   __| | ___   ___        ___| |__   __ _ _ __   __ _  ___      / /   __| (_)_ __  \ \ 
#  / _ \ / _` |/ _ \ / _ \      / __| '_ \ / _` | '_ \ / _` |/ _ \    | |   / _` | | '__|  | |
# | (_) | (_| | (_) | (_) |    | (__| | | | (_| | | | | (_| |  __/    | |  | (_| | | |     | |
#  \___/ \__,_|\___/ \___/      \___|_| |_|\__,_|_| |_|\__, |\___|    | |   \__,_|_|_|     | |
#                                                      |___/           \_\                /_/ 

# Link in your bashrc

# Set of Odoo change dir scripts,


_base_odoo_change(){
    # Paths
    prefix="/home/odoo/Repos/Odoo/wt"

# Declare an associative array
    declare -A all_versions=(
        ["14.0"]="${prefix}/14.0" ["14"]="${prefix}/14.0"
        ["15.0"]="${prefix}/15.0" ["15"]="${prefix}/15.0"
        ["saas-15.2"]="${prefix}/saas-15.2" ["15.2"]="${prefix}/saas-15.2" ["152"]="${prefix}/saas-15.2"
        ["16.0"]="${prefix}/16.0" ["16"]="${prefix}/16.0"
        ["saas-16.1"]="${prefix}/saas-16.1" ["16.1"]="${prefix}/saas-16.1" ["161"]="${prefix}/saas-16.1"
        ["saas-16.2"]="${prefix}/saas-16.2" ["16.2"]="${prefix}/saas-16.2" ["162"]="${prefix}/saas-16.2"
        ["saas-16.3"]="${prefix}/saas-16.3" ["16.3"]="${prefix}/saas-16.3" ["163"]="${prefix}/saas-16.3"
        ["saas-16.4"]="${prefix}/saas-16.4" ["16.4"]="${prefix}/saas-16.4" ["164"]="${prefix}/saas-16.4"
        ["17.0"]="${prefix}/17.0" ["17"]="${prefix}/17.0"
        ["master"]="${prefix}/master"
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
