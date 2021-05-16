import json
import re


keyword_mapping = {
    "AND": "$and",
    "OR": "$or",
}


def _escape_query(token):
    return re.escape(token)


def _query_string_former(token):
    return {"$text": {"$search": token}}


def _to_where_query(syntax_tree, parent_keyword):
    if syntax_tree.type == 'KEYWORD':
        same_parent_operation = parent_keyword is not None and \
                       syntax_tree.value == parent_keyword
        left_children = _to_where_query(syntax_tree.left, syntax_tree.value)
        right_children = _to_where_query(syntax_tree.right, syntax_tree.value)
        children = []
        if isinstance(left_children, list):
            children.extend(left_children)
        else:
            children.append(left_children)
        if isinstance(right_children, list):
            children.extend(right_children)
        else:
            children.append(right_children)
        if same_parent_operation:
            return children
        else:
            return {keyword_mapping[syntax_tree.value]: children}
    else:
        return _query_string_former(syntax_tree.value)


def to_query_string(syntax_tree):
    query = _to_where_query(syntax_tree, None)
    return json.dumps(query)
