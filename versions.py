from sync import create_worktrees, PATH_TO_DIR_WITH_WORKTREES, create_hosts, add_odoo_change_shortcut

class Version():
    all_tags = set()
    def __init__(self, formal:str, short:str, ip:str ,tags:set=set()) -> None:
        self.formal=formal # official branch name used in git, conda
        self.short=short   # shorter identifier
        self.ip=ip         # ip to serve this version at
        self.tags=self._validate_tags({formal} | {short} | tags)  # all strings used
    def _validate_tags(self, tags):
        if self.all_tags.intersection(tags):
            raise ValueError(f"Tags {tags} have already been used.")
        self.all_tags |= tags
        return tags
    def __eq__(self, other:str):
        return other in self.tags
    def __repr__(self) -> str:
        return f"<V_{self.formal}>"

# Formal is the official branch name
VERSIONS= [
    Version(formal="15.0",      short="15",    ip="127.0.0.150", tags={"150"}),
    Version(formal="16.0",      short="16",    ip="127.0.0.160", tags={"160"}),
    Version(formal="17.0",      short="17",    ip="127.0.0.170", tags={"170"}),
    Version(formal="saas-17.2", short="17.2",  ip="127.0.0.172", tags={"172"}),
    Version(formal="saas-17.4", short="17.4",  ip="127.0.0.174", tags={"174"}),
    Version(formal="18.0",      short="18",    ip="127.0.0.180", tags={"18"}),
    Version(formal="saas-18.1", short="18.1",  ip="127.0.0.181", tags={"181"}),
    Version(formal="saas-18.2", short="18.2",  ip="127.0.0.182", tags={"182"}),
    Version(formal="master",    short="master",ip="127.0.0.254", tags={"ms"}),
]


def sync_versions(versions):
    for version in versions:
        print(f"\n\nSynchronizing {version}")
        create_worktrees(version.formal)
        create_hosts(version.ip, version.short)
        add_odoo_change_shortcut(version_short_num=version.short)

if __name__ == "__main__":
    sync_versions(VERSIONS)
 