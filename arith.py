#!/usr/bin/env python3
class AST:
    pass

class BinOp(AST):
    
    def __init__(self, left, op, right):
        self.__left = left
        self.__op = op
        self.__right = right
    
    
    def Evaluate(self):
        x = self.__left.Evaluate()
        y = self.__right.Evaluate()
        
        if self.__op == '+':
            return x + y
        if self.__op == '-':
            return x - y
        if self.__op == '*':
            return x * y
        if self.__op == '/':
            return x / y
        raise Exception('Unknown operator!')

class Num(AST):

    def __init__(self, value):
        self.__value = value

    def Evaluate(self):
        return self.__value

class Parser:
    
    def parse(self, tokens):
        self.tokens = tokens
        self.nextToken()
        return self.parseAddition()
    
    def nextToken(self):
        if len(self.tokens) != 0:
            self.current = self.tokens.pop(0)
        else:
            self.current = None
        
    def parseAddition(self):
        result = self.parseMultiplication()
        while self.current in ['+', '-']:
            if self.current == '+':
                self.nextToken()
                add1 = result
                add2 = self.parseMultiplication()
                result = BinOp(add1, '+', add2)
            if self.current == '-':
                self.nextToken()
                sub1 = result
                sub2 = self.parseMultiplication()
                result = BinOp(sub1, '-', sub2)
        return result
    
    def parseMultiplication(self):
        result = self.parseNegative()
        while self.current in ['*', '/']:
            if self.current == '*':
                self.nextToken()
                mul1 = result
                mul2 = self.parseMultiplication()
                result = BinOp(mul1, '*', mul2)
            if self.current == '/':
                self.nextToken()
                div1 = result
                div2 = self.parseMultiplication()
                result = BinOp(div1, '/', div2)
        return result
    
    def parseNegative(self):
        if self.current == '-':
            self.nextToken()
            result = Num(-self.parseNumber().Evaluate())
        else:
            result = self.parseNumber()
        return result

    def parseNumber(self):
        result = None
        if type(self.current) is int:
            result = Num(self.current)
            self.nextToken()
        else:
            raise Exception("Unexpected character!")
        return result

class Interpreter:

    OPERATORS = ['+', '-', '*', '/']

    def __init__(self):
        self.parser = Parser()
    
    def eval(self, string):
        chars = list(string)
        tokens = self.tokenizer(chars)
        ast = self.parser.parse(tokens)
        return ast.Evaluate()
        
    def tokenizer(self, chars):
        tokens = []
        index = 0
        while index < len(chars):
            if chars[index] in " \t\n\r":
                index += 1
            elif chars[index] in self.OPERATORS:
                tokens.append(chars[index])
                index += 1
            elif chars[index] in '0123456789':
                num = int(chars[index])
                while index + 1 < len(chars) and chars[index + 1] in '0123456789':
                    index += 1
                    num = num * 10 + int(chars[index])
                index += 1
                tokens.append(num)
            else:
                raise Exception("Illegal input!")
        if len(tokens) == 0:
            raise Exception("Invalid input!")
        return tokens

def test(string):
    try:
        value = Interpreter().eval(string)
    except Exception as e:
        print(e)
        value = 0
    return int(value)

if __name__ == '__main__':
    string = input()
    print(test(string))