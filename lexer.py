import re
from rules import rules, keywords
from Token import Token


class Lexer:
    def __init__(self, query):
        self.query = query
        self.tokens = self.__run_lexer()

    def __read_spaces(self, i):
        break_word = re.search(r"[^[\s\t]", self.query[i: len(self.query)])
        if break_word:
            ei = break_word.span()[0] + i
        else:
            ei = len(self.query)
        return ei

    def __read_keyword(self, i):
        keyword = self.query[i:len(self.query)].split()[0]
        if keyword in keywords:
            return keyword, len(keyword) + i
        else:
            raise SyntaxError("Unexpected Keyword '" + keyword + "'")

    def __is_block_start(self, i):
        return self.query[i] == "("

    def __is_block_end(self, i):
        return self.query[i] == ")"

    def __read_string(self, i):
        if self.query[i] == '"' or self.query[i] == "'":
            ei = self.query.find(self.query[i], i + 1, len(self.query))
            if ei == -1:
                raise SyntaxError("Unexpected end of query.")
            return self.query[i + 1: ei], ei + 1
        else:
            break_word = re.search(r"\s|\(|\)|\"|'", self.query[i: len(self.query)])
            if break_word:
                ei = break_word.span()[0] + i
            else:
                ei = len(self.query)
            return self.query[i: ei], ei

    def __is_end(self, i):
        return len(self.query) == i

    def __exec_rules(self, i, mode):
        i = self.__read_spaces(i)
        if mode == 'END':
            if self.__is_end(i):
                return True, None, i + 1
            else:
                return False, None, None
        elif mode != 'END' and i >= len(self.query):
            raise SyntaxError("Unexpected end of query.")
        elif mode == 'BLOCK_START':
            if self.__is_block_start(i):
                return True, '(', i + 1
            else:
                return False, None, None
        elif mode == 'BLOCK_END':
            if self.__is_block_end(i):
                return True, ')', i + 1
            else:
                return False, None, None
        elif mode == 'STRING':
            s, ni = self.__read_string(i)
            return True, s, ni
        elif mode == 'KEYWORD':
            s, ni = self.__read_keyword(i)
            return True, s, ni

    def __run_lexer(self):
        tokens = []
        block_count = 0
        ci = 0
        read_mode = 'START'

        while read_mode != 'END':
            if read_mode == 'BLOCK_START':
                block_count += 1
            elif read_mode == 'BLOCK_END':
                block_count -= 1
            if block_count < 0:
                raise SyntaxError("Unexpected '" + self.query[ci - 1:] + "'")
            for mode in rules[read_mode]:
                is_success, token, i = self.__exec_rules(ci, mode)
                if is_success:
                    ci = i
                    read_mode = mode
                    tokens.append(Token(mode, token))
                    break
        if block_count > 0:
            raise SyntaxError("Unexpected end of query.")
        return tokens

    def get_tokens(self):
        return self.tokens
