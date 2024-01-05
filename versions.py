

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

VERSIONS= [
    Version(formal="14.0",      short="14",    ip="127.0.0.140"),     
    Version(formal="15.0",      short="15",    ip="127.0.0.150"),        
    Version(formal="saas-15.2", short="15.2",  ip="127.0.0.152"),       
    Version(formal="16.0",      short="16",    ip="127.0.0.160"),       
    Version(formal="saas-16.1", short="16.1",  ip="127.0.0.161"),       
    Version(formal="saas-16.2", short="16.2",  ip="127.0.0.162"),       
    Version(formal="saas-16.3", short="16.3",  ip="127.0.0.163"),       
    Version(formal="saas-16.4", short="16.4",  ip="127.0.0.164"),       
    Version(formal="17.0",      short="17",    ip="127.0.0.170"),       
    Version(formal="master",    short="master",ip="127.0.0.254"),       
]
