from ConfigParser import SafeConfigParser


def _build_conf():
    parser = SafeConfigParser()
    parser.read('resources/parameters.ini')
    typed_dict = {}

    param_type = 'ints'
    for name in parser.options(param_type):
        typed_dict[name] = parser.getint(param_type, name)
    param_type = 'floats'
    for name in parser.options(param_type):
        typed_dict[name] = parser.getfloat(param_type, name)

    return typed_dict

conf = _build_conf()
