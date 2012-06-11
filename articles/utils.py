from django import template


def parse_tokens(parser, bits):
    """
    Parse a tag bits (split tokens) and return a list on kwargs (from bits of the  fu=bar) and a list of arguments.
    """

    kwargs = {}
    args = []
    for bit in bits[1:]:
        try:
            try:
                pair = bit.split('=')
                kwargs[str(pair[0])] = parser.compile_filter(pair[1])
            except IndexError:
                args.append(parser.compile_filter(bit))
        except TypeError:
            raise template.TemplateSyntaxError('Bad argument "%s" for tag "%s"' % (bit, bits[0]))

    return args, kwargs
