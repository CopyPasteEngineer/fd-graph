_config = {}


def set(**params):
    _config.update(params)


def get(name):
    tokens = name.split('.')

    r = _config
    for token in tokens:
        r = r.get(token, None)

    return r
