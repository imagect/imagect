

def init_global(klass) :
    import imagect.api.util as u
    klass.app = u.app
    klass.mainwin = u.mainwin
    klass.actmgr = u.actmgr
    klass.recent = u.recent
    klass.console = u.console
    klass.datamgr = u.datamgr
    klass.viewmgr = u.viewmgr
    return klass