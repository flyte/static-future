import __future__
import ast


def future_imports(code):
    """
    Return the names of all features imported from __future__.
    """
    tree = compile(code, "<string>", "exec", ast.PyCF_ONLY_AST)
    import_froms = [x for x in tree.body if isinstance(x, ast.ImportFrom)]
    for imp in [x for x in import_froms if x.module == "__future__"]:
        for name in imp.names:
            yield name.name


def features(code):
    """
    Take the output from future_imports() and resolve the feature names to
    _Feature objects.
    """
    for imp in future_imports(code):
        if imp in __future__.all_feature_names:
            yield getattr(__future__, imp)


def compiler_flags(code):
    """
    Return an integer for use in compile()'s flags parameter based on which
    features have been imported from __future__.
    """
    flags = 0
    for feature in features(code):
        flags |= feature.compiler_flag
    return flags
