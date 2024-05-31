def get_config(host):
    if host:
        from .utils import hosting
        return hosting
    else:
        from .utils import local
        return local
