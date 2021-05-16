class Token:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return "{} -> left -> {}\n{} -> right -> {}\n\n{}{}".format(self.value, self.left.value if self.left else None,
                                                                 self.value, self.right.value if self.right else None,
                                                                 self.left.__str__() if self.left else "",
                                                                 self.right.__str__() if self.right else "")
