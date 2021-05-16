from rules import keywords_priority

_escape_char = '\\'


def _escape_query(token):
    return token.replace(_escape_char, '{}{}'.format(_escape_char, _escape_char)) \
        .replace('\'', '\\\'') \
        .replace('_', '{}_'.format(_escape_char))\
        .replace('%', '{}%'.format(_escape_char)) \
        .replace('[', '{}['.format(_escape_char))


def _query_string_former(token):
    return "text LIKE '%{}%' ESCAPE '{}'".format(_escape_query(token), _escape_char.replace('\'', '\\\''))


def _to_where_query(syntax_tree, parent_keyword):
    if syntax_tree.type == 'KEYWORD':
        use_brackets = parent_keyword is not None and \
                       keywords_priority[syntax_tree.value] > keywords_priority[parent_keyword]
        return "{}{} {} {}{}".format('(' if use_brackets else "",
                                     _to_where_query(syntax_tree.left, syntax_tree.value),
                                     syntax_tree.value,
                                     _to_where_query(syntax_tree.right, syntax_tree.value),
                                     ')' if use_brackets else "")
    else:
        return _query_string_former(syntax_tree.value)


def to_query_string(syntax_tree):
    return "SELECT name FROM Resume WHERE " + _to_where_query(syntax_tree, None)
