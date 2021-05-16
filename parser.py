from rules import keywords_priority


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_stack = []
        self.tree_node_stack = []
        self.__parse_tokens()

    def __parse_tokens(self):
        for token in self.tokens:
            self.__process_token(token)
        self.root_token = self.tree_node_stack[0]

    def __process_token(self, token):
        if token.type in ['BLOCK_START', 'KEYWORD']:
            self.token_stack.append(token)
            if token.type == 'KEYWORD':
                while len(self.token_stack) >= 2 \
                        and self.token_stack[-2].type == 'KEYWORD' \
                        and keywords_priority[self.token_stack[-2].value] < keywords_priority[token.value]:
                    prev_token = self.token_stack[-2]
                    prev_token.left = self.tree_node_stack[-2]
                    prev_token.right = self.tree_node_stack[-1]
                    del self.tree_node_stack[-2:]
                    self.tree_node_stack.append(prev_token)
                    del self.token_stack[-2:-1]
        elif token.type == 'STRING':
            self.tree_node_stack.append(token)
        elif token.type == 'BLOCK_END' or token.type == 'END':
            while len(self.token_stack) > 0 and self.token_stack[-1].type == 'KEYWORD':
                prev_token = self.token_stack[-1]
                prev_token.left = self.tree_node_stack[-2]
                prev_token.right = self.tree_node_stack[-1]
                del self.tree_node_stack[-2:]
                self.tree_node_stack.append(prev_token)
                del self.token_stack[-1]
            if len(self.token_stack) > 0:
                del self.token_stack[-1]
