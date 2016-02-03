from ConfigParser import SafeConfigParser

_MAX_UNCOVERED_SMART_METER = 'max_uncovered_smart_meters'
_MAX_ACCUMULATIVE_PROBABILITY = 'max_accumulative_probability'


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


_conf = _build_conf()
max_uncovered_smart_meters = _conf[_MAX_UNCOVERED_SMART_METER]
max_accumulative_probability = _conf[_MAX_ACCUMULATIVE_PROBABILITY]
