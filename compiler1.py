from lark import Lark,Transformer 
import re, json


class SaleesParser:
    def __init__(self, programText,starter):
        self.programText=programText
        self.starter=starter
        self.grammar=None
        self.parseTree=None
        self.initializeGrammar()

    def initializeGrammar(self):
        self.grammar=Lark(r"""
        

    relop : LE_OP | GE_OP | EQ_OP | NE_OP | L_OP | G_OP

    immutable: "(" expression ")" | WORD_CONST | WHOLE_CONST | FRAC_CONST | LETTER_CONST | BOOL_CONST 
    mutable: IDENTIFIER | IDENTIFIER "[" expression "]"

    factor : mutable | immutable

    unary_expression: UNARY_OP unary_expression | factor
    
    mul_expression : mul_expression MUL_OP unary_expression | unary_expression

    sum_expression: sum_expression SUM_OP mul_expression | mul_expression

    rel_expression : sum_expression relop sum_expression | sum_expression

    unary_rel_expression: NOT_OP unary_rel_expression 
        | rel_expression
        
    and_expression: and_expression AND_OP unary_rel_expression | unary_rel_expression

    simple_expression: simple_expression OR_OP and_expression | and_expression

    expression : mutable "=" expression
            | mutable ADD_ASSIGN expression
            | mutable SUB_ASSIGN expression
            | mutable DIV_ASSIGN expression
            | mutable MUL_ASSIGN expression
            | mutable MOD_ASSIGN expression
            | mutable INC_OP
            | mutable DEC_OP
            | simple_expression
    

    declaration: type_specifier IDENTIFIER ";"
        | init_declarator ";"
        |type_specifier IDENTIFIER ";" statement
        | init_declarator ";" statement

        
        
    init_declarator:  type_specifier IDENTIFIER "=" initializer
        | IDENTIFIER "=" initializer
    type_specifier: VOID
        | LETTER
        | FRAC
        | WHOLE
        | WORD
        | BOOL
  
    initializer : expression
    
    statement : labeled_statement
        | compound_statement
        | expression_statement
        | selection_statement
        | iteration_statement
        | jump_statement
        | declaration
        

    labeled_statement : IDENTIFIER ":" statement
        | CASE expression ":" statement
        | DEFAULT ":" statement
        

    compound_statement: "{" "}" 
        | "{" statement "}"
        | "{" statement "}" statement


    expression_statement : ";"
        | expression ";"
        

    selection_statement : IF "(" expression ")" statement
        | IF "(" expression ")" statement OTHER statement
        | SWITCH "(" expression ")" statement
        

    iteration_statement : LOOPTILL "(" expression ")" statement
        | DO statement LOOPTILL "(" expression ")" ";"
        | LOOP "(" declaration expression_statement expression ")" statement
        

    jump_statement : CONTINUE ";"
        | BREAK ";"
        | RETURN ";"
        | RETURN expression ";"
        

        MUL_ASSIGN :"*="
        DIV_ASSIGN :"/="
        MOD_ASSIGN :"%="
        ADD_ASSIGN :"+="
        SUB_ASSIGN :"-="
        AND_ASSIGN :"&="
        XOR_ASSIGN :"^="
        OR_ASSIGN :"|="

        L_OP: "<"
        G_OP: ">"
        SUM_OP: "+" | "-"
        MUL_OP: "*" | "/" | "%"
        UNARY_OP: "*" | "-" | "?"
        NOT_OP: "~"

        LOOP: "loop"
        LOOPTILL: "looptill"
        DO: "do"
        IF: "if"
        OTHER: "other"
        SWITCH: "switch"
        CASE: "case"
        DEFAULT: "default"
        CONTINUE: "continue"
        BREAK: "break"
        RETURN: "return"

        
        IDENTIFIER : /[a-zA-Z_][a-zA-Z0-9_]*/

        WORD_CONST : ESCAPED_STRING
        WHOLE_CONST: /-?\d+/
        FRAC_CONST: /-?\d.\d+/
        LETTER_CONST : "a".."z"
        BOOL_CONST: "true" | "false"

        INC_OP : "++"
        DEC_OP : "--"
        AND_OP : "&&"
        OR_OP : "||"
        LE_OP : "<="
        GE_OP : ">="
        EQ_OP : "=="
        NE_OP : "!="
        LEFT_OP : "<<"
        RIGHT_OP : ">>"


        VOID : "void"
        LETTER : "letter"
        FRAC : "frac"
        WHOLE : "whole"
        WORD : "word"
        BOOL : "bool"
        

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS 
        """,start=self.starter)

    def parserProgram(self):
        self.parseTree=self.grammar.parse(self.programText)

    def showParseTree(self,isPretty):
        #print json.dumps(json.loads(self.parseTree),ident=4)
        if isPretty:
            print self.parseTree.pretty()
        else:
            print self.parseTree

    def generateIC(self):
        icg=ICGenerator()
        icg.transform(self.parseTree)
        return icg.ic

class ICGenerator(Transformer):
    def __init__(self):
        self.scope=10000
        self.regCount=0
        self.sym_table=[]
        self.not_declared=[]
        self.ic=""
        self.line_count=0

    def immutable(self,items):
        return items[0]
    def mutable(self,items):
        return items[0]
    def factor(self,items):
        return items[0]
    def unary_expression(self,items):
        return items[0]
    def mul_expression(self,items):
        if len(items)>2:
            reg="t"+str(self.regCount)
            self.regCount+=1
            self.ic+= "\n"+reg+"=" +items[0] +items[1] +items[2]
            return reg
        else:
            return items[0]
    def sum_expression(self,items):
        if len(items)>2:
            reg="t"+str(self.regCount)
            self.regCount+=1

            self.ic+="\n"+reg+"=" +items[0] +items[1] +items[2]
            return reg
        else:
            return items[0]
    def relop(self,items):
        return items[0]
    def rel_expression(self,items):
        if len(items)>2:
            reg="t"+str(self.regCount)
            self.regCount+=1
            self.ic+="\n"+reg+"="+items[0]+items[1]+items[2]
            return reg
        else:
            return items[0]
    def unary_rel_expression(self,items):
        return items[0]
    
    def and_expression(self,items):
        return items[0]
    def simple_expression(self,items):
        return items[0]
    def expression(self, items):
        print items[0]
        if len(items)==1:
            return items[0]
        elif len(items)==2:
            code="\n"+items[0]+"="+items[1]
            return code

    def mutable(self,items):
        return items[0]
    def factor(self,items):
        return items[0]
    def immutable(self,items):
        return items[0]
    def type_specifier(self,items):
        return items[0]
    def initializer(self,items):
        return items[0]
    def statement(self,items):
        return items[0]
    def init_declarator(self,items):
        if len(items)==2:
            self.ic+="\n"+items[0]+"="+str(items[1])
            return ""
    def expression_statement(self,items):
        return items[0]
    def selection_statement(self,items):
        if len(items)==3:
            if items[0]=="if":
                self.ic+="\n"+"IFZ " +items[1]+ " GOTO L"+str(self.line_count)+(items[2])+"\nL"+str(self.line_count)+":"
                self.line_count+=1

    def compound_statement(self,items):
        return items[0]

if __name__=='__main__':
    textInput1="""
    word my_string="Wasi gg";
    frac my_float;
    my_float=3.4;
    if(my_float == 7.4){
        frac my_int=9;
    }
    other{
        my_int= my_int+4;
    }

    loop(whole id =0; i<5; i=i+1){
        my_float=my_float+i;    
    }
    looptill(my_float<0){
        my_float=my_float-5;
    }
    """
    textInput="""
    whole a;
    a=b*c+b*d;
    if(d>b+c){
        e=f;
    }
    m=g-h-d;
    """
    myParser=SaleesParser(textInput,'statement')
    myParser.parserProgram()
    myParser.showParseTree(isPretty=True)
    print myParser.generateIC()