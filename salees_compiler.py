from lark import Lark,Transformer 
from code_generator import IntermediateCodeGenerator
class SaleesCompiler:
    def __init__(self, programText,starter="top_level"):
        self.programText=programText
        self.starter=starter
        self.grammar=None
        self.parseTree=None
        self.initialize_grammar()
        self.fileExtension=".sl"

    def initialize_grammar(self):
        self.grammar=Lark(r"""
        
    top_level: statement

    statement : (compound_statement
        | selection_statement
        | iteration_statement
        | jump_statement
        | declaration) [statement]

    declaration: declare_init | declare | init
    declare_init: type_specifier IDENTIFIER "=" expression ";"
    declare : type_specifier IDENTIFIER ";"     
    init : IDENTIFIER "=" expression ";"

    compound_statement: "{" "}" 
        | "{" statement "}"

    selection_statement : IF "(" expression ")" compound_statement
        | IF "(" expression ")" compound_statement OTHER compound_statement
        
    iteration_statement : LOOPTILL "(" expression ")" compound_statement
        | DO compound_statement LOOPTILL "(" expression ")" ";"
        
    jump_statement : CONTINUE ";"
        | BREAK ";"
        | RETURN ";"
        | RETURN expression ";"


    expression: simple_expression
    simple_expression: simple_expression OR_OP and_expression | and_expression
    and_expression: and_expression AND_OP unary_rel_expression | unary_rel_expression
    unary_rel_expression: NOT_OP unary_rel_expression | rel_expression
    rel_expression : sum_expression relop sum_expression | sum_expression
    sum_expression: sum_expression SUM_OP mul_expression | mul_expression
    mul_expression : mul_expression MUL_OP factor | factor
    factor : mutable | immutable
    immutable:  WORD_CONST | WHOLE_CONST | FRAC_CONST | LETTER_CONST | BOOL_CONST 
    mutable: IDENTIFIER

    relop : LE_OP | GE_OP | EQ_OP | NE_OP | L_OP | G_OP
    
    type_specifier:LETTER
        | FRAC
        | WHOLE
        | WORD
        | BOOL
        
        L_OP: "<"
        G_OP: ">"
        SUM_OP: "+" | "-"
        MUL_OP: "*" | "/" | "%"
        NOT_OP: "~"

        LOOP: "loop"
        LOOPTILL: "looptill"
        DO: "do"
        IF: "if"
        OTHER: "other"
        CONTINUE: "continue"
        BREAK: "break"

        
        IDENTIFIER : /[a-zA-Z_][a-zA-Z0-9_]*/

        WORD_CONST : ESCAPED_STRING 
        WHOLE_CONST: /-?\d+/
        FRAC_CONST: /-?\d.\d+/
        LETTER_CONST : "\'" "a".."z" "\'"
        BOOL_CONST: "true" | "false"

        AND_OP : "&&"
        OR_OP : "||"
        LE_OP : "<="
        GE_OP : ">="
        EQ_OP : "=="
        NE_OP : "!="

        LETTER : "letter"
        FRAC : "frac"
        WHOLE : "whole"
        WORD : "word"
        BOOL : "bool"
        RETURN : "return"

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS 
        """,start=self.starter)

    def parse_program(self):
        self.parseTree=self.grammar.parse(self.programText)
    
    def show_parse_tree(self,isPretty):
        if isPretty:
            print self.parseTree.pretty()
        else:
            print self.parseTree
    
    def generate_intermediate_code(self,fileName=None):
        icg=IntermediateCodeGenerator()
        icg.transform(self.parseTree)
        if fileName:
            with open(fileName+self.fileExtension,"w+") as f:
                f.write(icg.ic)
        return icg.ic
    