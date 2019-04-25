class Expression:
    def __init__(self, s):
        self._parse(s)

    # Source: https://stavshamir.github.io/python/2018/05/26/overloading-constructors-in-python.html
    @classmethod
    def from_sub_exprs(cls, expr1, operator, expr2): #Make an expression from operator and sub-expressions
        expr = Expression('0')
        expr.expr1 = expr1
        expr.data = operator
        expr.expr2 = expr2
        return expr

    def __add__(self, expr):
        expr = Expression.from_sub_exprs(self, '+', expr)
        expr._simplify()
        return expr

    def __sub__(self, expr):
        expr = Expression.from_sub_exprs(self, '-', expr)
        expr._simplify()
        return expr

    def __mul__(self, expr):
        expr = Expression.from_sub_exprs(self, '*', expr)
        expr._simplify()
        return expr

    def __truediv__(self, expr):
        # Checking foir division by zero
        expr._simplify()
        if expr._is_atomic() and expr.data == '0':
            raise Exception("Division by zero!")
        
        expr = Expression.from_sub_exprs(self, '/', expr)
        expr._simplify()
        return expr

    # https://www.journaldev.com/22460/python-str-repr-functions
    def __str__(self):
        if self.expr1 == None and self.expr2 == None:
            return '%s' % (self.data)
        else:
            return '(%s %s %s)' % (
                self.expr1,
                self.data,
                self.expr2
            )

    def __repr__(self):
        return str(self)

    def _valid_name_first_char(self, c):
        return c.isalpha() or c == '_'

    def _valid_name_char(self, c):
        return self._valid_name_first_char(c) or c.isdigit()

    # Finds a expression in s[begin..] and returns end such that
    # s[begin..end-1] was the smallest complete expression found 
    def _find_sub_expr(self, s, begin):
        if self._valid_name_first_char(s[begin]):
            i = begin + 1
            #INV: a[begin..i-1] is a valid identifier, begin <= i <= len(s) - 1
            while i < len(s) and self._valid_name_char(s[i]):
                i += 1
        elif s[begin].isdigit():
            i = begin + 1
            #INV: a[begin..i-1] is a number, begin <= i <= len(s) - 1
            while i < len(s) and s[i].isdigit():
                i += 1
        elif s[begin] == '(':
            i = begin + 1
            num_unmatched_parens = 1
            #INV: a[begin..i-1] is part of a sub-expression with num_unmatched_parens unmatched brackets
            # begin + 1 <= i <= len(s) - 1
            while i < len(s) and num_unmatched_parens > 0:
                if s[i] == '(':
                    num_unmatched_parens += 1
                elif s[i] == ')':
                    num_unmatched_parens -= 1
                i += 1
        else:
            raise Exception("Unable to parse: '" + s + "'")
        
        return i

    # Breaks s into parts. s should not have spaces
    # The parts would be sub-expressions and operators.
    # Raises an expection if parens are not added / mismatched
    # E.g. ((2*x)+y) would give [(2*x), +, y]
    def _separate(self, s):
        if s[0] != '(':
            i=0
        elif s[-1] != ')': #assert: s[0] == '('
            return Exception("Matching right bracket not found in '" + s + "'")
        else:
            i = 1

        i1 = self._find_sub_expr(s, i) #assert: s[i..i1-1] is a expression 
        
        if i1 == len(s) - i: # Atomic expression
            return [s[i:i1-i]]
        
        operator = s[i1] #TODO: Add support for multi-character operators

        i2 = self._find_sub_expr(s, i1+1) #assert: s[i1+1..i2-1] is an expression

        if i2 != len(s) - i:
            raise Exception("Malformed expression: '" + s + "'")
        
        return s[1:i1],
        operator,
        s[i1+1:i2]

    # Expression is taken as:
    # 1. (expr1 op expr2)
    # 2. var_name
    def _parse(self, s):
        s = "".join(filter(lambda x : not x.isspace(), s))
        #assert: spaces from s have been removed
        tokens = self._separate(s)

        if len(tokens) == 1: # atomic expression
            self.data = tokens[0]
            self.expr1 = None
            self.expr2 = None
        elif len(tokens) == 3: # Has a binary operator and sub-expressions
            self.data = tokens[1]
            self.expr1 = Expression(tokens[0])
            self.expr2 = Expression(tokens[2])
        else:
            raise Exception("Only binary operators allowed!")

    def _is_atomic(self):
        return self.expr1 == None and self.expr2 == None

    def _is_const_wrt(self, var):
        return self.data != var
    
    #returns (expr1, operator, expr2)
    def _get_sub_exprs(self):
        return self.expr1, self.data, self.expr2

    def differentiate_wrt(self, x):
        if self._is_atomic(): # Expression can't be broken down into smaller expressions
            if self._is_const_wrt(x):
                return Expression("0")
            else:
                return Expression("1") # An expression which is atomic and is not const wrt x is x
        else:
            expr1, operator, expr2 = self._get_sub_exprs() #assert: self = expr1 operator expr2
            if operator == '+':
                return expr1.differentiate_wrt(x) + expr2.differentiate_wrt(x)
            elif operator == '-':
                return expr1.differentiate_wrt(x) - expr2.differentiate_wrt(x)
            elif operator == '*':
                return expr1 * expr2.differentiate_wrt(x) + expr1.differentiate_wrt(x) * expr2
            elif operator == '/':
                return (expr2 * expr1.differentiate_wrt(x) - expr1 * expr2.differentiate_wrt(x)) / (expr2 * expr2)
            else:
                raise Exception("Operator %s not supported!" % operator)

    def _set(self, expr):
        self.data = expr.data
        self.expr1 = expr.expr1
        self.expr2 = expr.expr2

    def _simplify(self):
        if self.expr1 != None and self.expr2 != None:
            self.expr1._simplify()
            self.expr2._simplify()

            if self.data == '*':
                if self.expr1.data == '0' or self.expr2.data == '0':
                    self._set(Expression('0'))
                elif self.expr1.data == '1':
                    self._set(self.expr2)
                elif self.expr2.data == '1':
                    self._set(self.expr1)
            elif self.data == '+':
                if self.expr1.data == '0':
                    self._set(self.expr2)
                elif self.expr2.data == '0':
                    self._set(self.expr1)
            elif self.data == '-':
                if self.expr2.data == '0':
                    self._set(self.expr1)
                elif self.expr1._is_atomic() and self.expr2._is_atomic() and self.expr1.data == self.expr2.data:
                    self._set(Expression('0'))
            elif self.data == '/':
                if self.expr1.data == '0':
                    self._set(Expression('0'))
                elif self.expr2.data == '0':
                    raise Exception("Division by zero!")

s = input("Enter an expression: ")
e = Expression(s)
print(e)
e_diff = e.differentiate_wrt('x')
e_diff._simplify()
print(e_diff)