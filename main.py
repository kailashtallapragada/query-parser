from lexer import Lexer
from parser import Parser
from codegen.sql import to_query_string as to_sql
from codegen.mongo import to_query_string as to_mongo


if __name__ == '__main__':
    query = input("Enter your search query: ")
    output_format = None
    while output_format not in [1, 2]:
        try:
            output_format = int(input("[1] sql\n[2] mongodb\nEnter output format option number:"))
        except ValueError:
            output_format = None
    try:
        tokens = Lexer(query).get_tokens()
        syntax_tree = Parser(tokens).root_token
        if output_format == 1:
            print(to_sql(syntax_tree))
        elif output_format == 2:
            print(to_mongo(syntax_tree))
    except SyntaxError:
        print("Error - Please check input")
