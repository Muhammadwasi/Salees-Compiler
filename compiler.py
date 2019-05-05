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

        stmt :  (decl_var|decl_init_var|init_var|update_var
                |if_stmt|if_otif_stmt|if_other_stmt
                |loop_stmt|looptill_stmt) [stmt]
        
        init_var: identifier "=" data_val ";"
        decl_init_var: data_type identifier "=" data_val ";"
        decl_var : data_type identifier ";"
        update_var: identifier "=" (identifier|WHOLE|FRAC) BASIC_OP (identifier|WHOLE|FRAC) [";"]

        if_stmt: "if(" condition "){" stmt "}"
        if_otif_stmt: "if(" condition "){" stmt "}" otif_stmt
        if_other_stmt: "if(" condition "){" stmt "}" other_stmt
        otif_stmt: "otif(" condition "){" stmt "}" (otif_stmt |other_stmt)
        other_stmt: "other{" stmt "}"

        loop_stmt: "loop(" (init_var|decl_init_var) (condition";") (update_var) "){" stmt "}"
        looptill_stmt: "looptill(" condition "){" stmt "}"

        condition: (identifier|WHOLE|FRAC|LETTER)  CON_OP (identifier|WHOLE|FRAC|LETTER)
        bool_stmt: condition (bool_op) condition

        data_val : WORD | LETTER | WHOLE | FRAC
        identifier: IDENTIFIER
        data_type : DATA_TYPE
        bool_op: BOOL_OP

        BOOL_OP: "&&" | "||" 
        IDENTIFIER : /[a-zA-Z_][a-zA-Z0-9_]*/
        WORD : ESCAPED_STRING
        WHOLE: /-?\d+/
        FRAC: /-?\d.\d+/
        LETTER : "a".."z"

        BASIC_OP: "+" | "-" | "*" | "/"
        CON_OP : ">" | "<" | "<=" | ">=" | "==" | "!="
        DATA_TYPE : "WHOLE" | "frac" | "letter" | "word" | "bool"

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS 
        """,start=self.starter)

    def parserProgram(self):
        self.parseTree=self.grammar.parse(self.programText)

    def showParseTree(self):
        #print json.dumps(json.loads(self.parseTree),ident=4)
        print self.parseTree.pretty()

    def generateIC(self):
        return str(ICGenerator().transform(self.parseTree))

class ICGenerator(Transformer):
    pass


if __name__=='__main__':
    textInput1="""
    word my_string="Wasi gg";
    frac my_float;
    my_float=3.4;
    if(my_float == 7.4){
        WHOLE my_int=9;
    }other{
        my_int= my_int+4;
    }

    loop(WHOLE i =0; i<5; i=i+1){
        my_float=my_float+i;    
    }
    looptill(my_float<0){
        my_float=my_float-5;
    }
    """
    textInput="int a=b*c+b*d;"
    myParser=SaleesParser(textInput1,'stmt')
    myParser.parserProgram()
    myParser.showParseTree()