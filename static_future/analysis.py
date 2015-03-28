import __future__
import tokenize

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def compiler_flags(unformatted_source):
    """
    Establish which features have been imported from __future__
    and return an integer value suitable for use in the compile()
    'flags' parameter.
    """
    def get_all_imports(tokens, last_was_name=False):
        """
        Pop tokens until we get to a NAME type, then if it's an import
        return it and recurse. If it's a newline or endmarker, end the
        recursion. last_was_name makes sure that NAME tokens adjacent to
        one another don't get returned, such as the 'as' and 'print2' tokens
        in "print_function as print2".
        """
        while True:
            t = next(tokens)
            if t[0] == tokenize.NAME:
                if not last_was_name:
                    return [t[1]] + get_all_imports(tokens, True)
            elif t[0] in (tokenize.NEWLINE, tokenize.ENDMARKER):
                return []
            else:
                last_was_name = False

    flags = 0
    tokens = tokenize.generate_tokens(
        StringIO(unformatted_source).readline)
    imports = []
    try:
        while True:
            # from __future__ import has to be the first statement in a file
            # https://docs.python.org/2/reference/simple_stmts.html#future
            first_three_tokens = " ".join(
                (next(tokens)[1], next(tokens)[1], next(tokens)[1]))
            if first_three_tokens == "from __future__ import":
                imports += get_all_imports(tokens)
            else:
                # Keep popping tokens until the end of the _logical_ line
                # https://docs.python.org/2/library/tokenize.html#tokenize.NL
                while True:
                    t = next(tokens)
                    if t[0] in (tokenize.NEWLINE, tokenize.ENDMARKER):
                        break
    except StopIteration:
        # We reached the end of the file
        pass

    for imp in imports:
        if imp in __future__.all_feature_names:
            flags |= getattr(__future__, imp).compiler_flag
    return flags
