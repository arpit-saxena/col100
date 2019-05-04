# Represents a one argument function
class Function:
    function_derivatives = {
        'log': lambda arg: Expression('1') / arg,
        'exp': lambda arg: Expression(Function('exp', arg)),
        'sin': lambda arg: Expression(Function('cos', arg)),
        'cos': lambda arg: Expression('(0-1)') * Expression(Function('sin', arg)),
        'tan': lambda arg: Expression(Function('sec', arg)) ** Expression('2'),
        'sec': lambda arg: Expression(Function('sec', arg)) * Expression(Function('tan', arg)),
        'cosec': lambda arg: Expression('(0-1)') * Expression(Function('cosec', arg)) * Expression(Function('cot', arg)),
        'cot': lambda arg: Expression('(0-1)') * Expression(Function('cosec', arg)) ** Expression('2')
    }

    def __init__(self, fname, arg):
        self.name = fname
        self.arg = arg

    def __str__(self):
        return '%s(%s)' % (self.name, self.arg)

    def __repr__(self):
        return str(self)

    def differentiate_wrt(self, x):
        if self.name in Function.function_derivatives:
            return self.function_derivatives[self.name](self.arg) * self.arg.differentiate_wrt(x)
        else:
            raise Exception("Function '%s' has no derivative defined" % (self.name))

class Expression:
    
    # Smallest part of an Expression
    # Can be a number, variable or a function
    class Atom:
        def __init__(self, data):
            self.data = data

        def _set_data(self, data):
            self.data = data

        def __str__(self):
            return str(self.data)
            
        def __repr__(self):
            return str(self)

        def __eq__(self, other):
            if isinstance(other, Expression.Atom) and isinstance(self.data, str) and isinstance(other.data, str):
                return self.data == other.data
            
            return False

        def differentiate_wrt(self, x):
            # https://www.geeksforgeeks.org/type-isinstance-python/
            if isinstance(self.data, Function):
                return self.data.differentiate_wrt(x)
            elif self.data == x:
                return Expression('1')
            else:
                return Expression('0')

    def __init__(self, s = None, expr1 = None, expr2 = None):
        if isinstance(s, str):
            self.data = None
            self.expr1 = None
            self.expr2 = None
            self._parse(s)
        elif isinstance(s, Expression.Atom):
            self.data = s
            self.expr1 = expr1
            self.expr2 = expr2
        elif isinstance(s, Function):
            self.data = Expression.Atom(s)
            self.expr1 = expr1
            self.expr2 = expr2
        else:
            raise Exception("Argument of type %s not supported by Expression's constructor" % type(s))

        self._simplify()

    def __add__(self, expr):
        expr = Expression(Expression.Atom('+'), self, expr)
        return expr

    def __sub__(self, expr):
        expr = Expression(Expression.Atom('-'), self, expr)
        return expr

    def __mul__(self, expr):
        expr = Expression(Expression.Atom('*'), self, expr)
        return expr

    def __truediv__(self, expr):
        # Checking for division by zero
        if expr._is_atomic() and str(expr.data) == '0':
            raise Exception("Division by zero!")
        
        expr = Expression(Expression.Atom('/'), self, expr)
        return expr

    def __pow__(self, expr):
        expr = Expression(Expression.Atom('^'), self, expr)
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

    # Finds a expression in s[begin..] and returns expr, end such that
    # s[begin..end-1] was the smallest complete expression found and
    # expr is an Expression object representing s[begin..end-1]
    def _find_sub_expr(self, s, begin):
        if self._valid_name_first_char(s[begin]):
            i = begin + 1
            #INV: a[begin..i-1] is a valid identifier, begin <= i <= len(s) - 1
            while i < len(s) and self._valid_name_char(s[i]):
                i += 1
            
            expr = Expression(Expression.Atom(s[begin:i]))

            if i != len(s) - 1 and s[i] == '(': # Function
                arg, i2 = self._find_sub_expr(s, i+1) #assert: s[i+1..i2-1] is an expression
                if s[i2] != ')':
                    raise Exception("Closing parentheses missing")
                expr = Expression(Function(str(expr.data), arg))
                i = i2 + 1

        elif s[begin].isdigit() or s[begin] == '.':
            i = begin + 1
            found_decimal = False
            #INV: a[begin..i-1] is a number, found_decimal <=> a[begin..i-1] has a decimal pt. begin <= i <= len(s) - 1
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.':
                    if found_decimal:
                        raise Exception("Illegal numeric part in %s" % s[begin:])
                    else:
                        found_decimal = True
                i += 1
            expr = Expression(Expression.Atom(s[begin:i]))

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
            expr = Expression(s[begin:i])
        else:
            raise Exception("Unable to parse: '" + s + "'")

        return expr, i

    # Expression is taken as:
    # 1. (expr1 op expr2)
    # 2. var_name
    def _parse(self, s):
        s = "".join(filter(lambda x : not x.isspace(), s))
        #assert: spaces from s have been removed
        #tokens = self._separate(s)

        self.data = Expression.Atom("")
        self.expr1 = None
        self.expr2 = None

        if s[0] != '(':
            i=0
        elif s[-1] != ')': #assert: s[0] == '('
            raise Exception("Matching right bracket not found in '" + s + "'")
        else:
            i = 1

        expr1, i1 = self._find_sub_expr(s, i) #assert: expr1 = parsed s[i..i1-1]
        
        if i1 == len(s) - i: # Atomic expression
            self._set(expr1)
            return

        if s[i1] == '(': # Must be a function
            arg, i2 = self._find_sub_expr(s, i1+1) #assert: arg = parsed s[i1+1..i2-1]
            if s[i2] != ')':
                raise Exception("Closing parentheses missing")
            expr1 = Function(expr1.data, arg)
            
            if i2 + 1 == len(s) - i: # Only one function in the expression
                self._set_data(Expression.Atom(expr1))
                return
        else:
            i2 = i1-1
        
        operator = Expression.Atom(s[i2 + 1]) #Only single character operators are supported

        expr2, i3 = self._find_sub_expr(s, i2+2) #assert: expr2 = parsed s[i2+2..i3-1]

        if i3 != len(s) - i:
            raise Exception("Malformed expression: '" + s + "'")
        
        self.data = operator
        self.expr1 = expr1
        self.expr2 = expr2

    def _is_atomic(self):
        return self.expr1 == None and self.expr2 == None
    
    #returns (expr1, operator, expr2)
    def _get_sub_exprs(self):
        return self.expr1, self.data, self.expr2

    def differentiate_wrt(self, x):
        if self._is_atomic(): # Expression can't be broken down into smaller expressions
            return self.data.differentiate_wrt(x)
        else:
            expr1, operator, expr2 = self._get_sub_exprs() #assert: self = expr1 operator expr2
            if operator.data == '+':
                return expr1.differentiate_wrt(x) + expr2.differentiate_wrt(x)
            elif operator.data == '-':
                return expr1.differentiate_wrt(x) - expr2.differentiate_wrt(x)
            elif operator.data == '*':
                return expr1 * expr2.differentiate_wrt(x) + expr1.differentiate_wrt(x) * expr2
            elif operator.data == '/':
                return (expr2 * expr1.differentiate_wrt(x) - expr1 * expr2.differentiate_wrt(x)) / (expr2 * expr2)
            elif operator.data == '^':
                return expr2 * expr1 ** (expr2 - Expression("1")) * expr1.differentiate_wrt(x) + \
                expr1 ** expr2 * Expression(Function("log", expr1)) * expr2.differentiate_wrt(x)
            else:
                raise Exception("Operator %s not supported!" % operator)

    def _set(self, expr):
        self.data = expr.data
        self.expr1 = expr.expr1
        self.expr2 = expr.expr2

    def _set_data(self, data):
        self.data = data

    def _simplify(self):
        if self.expr1 != None and self.expr2 != None:
            operator = str(self.data)
            expr1 = str(self.expr1.data)
            expr2 = str(self.expr2.data)

            if operator == '*':
                if expr1 == '0' or expr2 == '0':
                    self._set(Expression('0'))
                elif expr1 == '1':
                    self._set(self.expr2)
                elif expr2 == '1':
                    self._set(self.expr1)
            elif operator == '+':
                if expr1 == '0':
                    self._set(self.expr2)
                elif expr2 == '0':
                    self._set(self.expr1)
            elif operator == '-':
                if str(self.expr2.data) == '0':
                    self._set(self.expr1)
                elif self.expr1._is_atomic() and self.expr2._is_atomic() and self.expr1.data == self.expr2.data:
                    self._set(Expression('0'))
            elif operator == '/':
                if str(self.expr1.data) == '0':
                    self._set(Expression('0'))
                elif str(self.expr2.data) == '0':
                    raise Exception("Division by zero!")
            elif operator == '^':
                if str(self.expr1.data) == '1':
                    self._set(Expression('1'))
                elif str(self.expr1.data) == '0':
                    self._set(Expression('0'))
                elif str(self.expr2.data) == '0':
                    self._set(Expression('1'))
                elif str(self.expr2.data) == '1':
                    self._set(self.expr1)

s = input("Enter an expression: ")
e = Expression(s)
print(e)
e_diff = e.differentiate_wrt('x')
print(e_diff)