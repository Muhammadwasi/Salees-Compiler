from lark import Lark,Transformer
class IntermediateCodeGenerator(Transformer):

    def __init__(self):
        self.reg_count=0
        self.sym_table={}
        self.intermediate_code=""
        self.line_count=0

    def top_level(self,items):
        self.intermediate_code+=(items[0])

    def get_new_line(self):
        lc="L"+str(self.line_count)
        self.line_count+=1
        return lc

    def get_new_reg(self):
        reg= "t"+str(self.reg_count)
        self.reg_count+=1
        return reg

    def immutable(self,items):
        return items[0]

    def mutable(self,items):
        if items[0] not in self.sym_table:
            raise Exception("Variable {} is not declared".format(items[0]))
        elif items[0] in self.sym_table and "value" not in self.sym_table[items[0]]:
            raise Exception("Variable {} is not initialzed".format(items[0]))
        return items[0]
    
    def mul_expression(self,items):
        if len(items)>2:
            reg=self.get_new_reg()
            if len(items[0])==2:
                code=items[0][1]+"\n"+reg+"=" +items[0][0] +items[1] +items[2]
            else:
                code= "\n"+reg+"=" +items[0] +items[1] +items[2]
            return [reg,code]
        else:
            return items[0]

    def sum_expression(self,items):
        if len(items)>2:
            reg=self.get_new_reg()
            if len(items[0])==2 and len(items[2])==2:
                code=items[0][1]+items[2][1]+"\n"+reg+"=" +items[0][0] +items[1] +items[2][0]

            elif len(items[2])==2:
                code=items[2][1]+"\n"+reg+"=" +items[0] +items[1] +items[2][0]
            elif len(items[0])==2:
                code=items[0][1]+"\n"+reg+"=" +items[0][0] +items[1] +items[2]
            else:
                code="\n"+reg+"=" +items[0] +items[1] +items[2]
            return [reg,code]
        else:
            return items[0]

    def relop(self,items):
        return items[0]

    def rel_expression(self,items):
        if len(items)>2:
            reg=self.get_new_reg()
            if len(items[0])==2 and len(items[2])==2:
                code=items[0][1]+items[2][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2][0]
            elif len(items[0])==2:
                code=items[0][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2]
            elif len(items[2])==2:
                code=items[2][1]+"\n"+reg+"="+items[0]+items[1]+items[2][0]
            else:
                code="\n"+reg+"="+items[0]+items[1]+items[2]

            return [reg,code]
        else:
            return items[0]

    def unary_rel_expression(self,items):
        if len(items)==2:
            reg=self.get_new_reg()
            if(len(items[1])==2):
                code=items[1][1]+"\n"+reg+"="+items[0]+items[1][0]
            else:
                code="\n"+reg+"="+items[0]+items[1]
            return [reg,code]
        else: 
            return items[0]

    def and_expression(self,items):
        if len(items)>2:
            reg=self.get_new_reg()
            if len(items[0])==2 and len(items[2])==2:
                code=items[0][1]+items[2][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2][0]
            elif len(items[0])==2:
                code=items[0][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2]
            elif len(items[2])==2:
                code=items[2][1]+"\n"+reg+"="+items[0]+items[1]+items[2][0]
            else:
                code="\n"+reg+"="+items[0]+items[1]+items[2]

            return [reg,code]
        else:
            return items[0]

    def simple_expression(self,items):
        if len(items)>2:
            reg=self.get_new_reg()
            if len(items[0])==2 and len(items[2])==2:
                code=items[0][1]+items[2][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2][0]
            elif len(items[0])==2:
                code=items[0][1]+"\n"+reg+"="+items[0][0]+items[1]+items[2]
            elif len(items[2])==2:
                code=items[2][1]+"\n"+reg+"="+items[0]+items[1]+items[2][0]
            else:
                code="\n"+reg+"="+items[0]+items[1]+items[2]

            return [reg,code]
        else:
            return items[0]

    def expression(self, items):
        return items[0]
    
    def factor(self,items):
        return items[0]
   
    def statement(self,items):
        return items[0]

    def declaration(self,items):
        return items[0]

    def declare_init(self,items):
        if items[1] in self.sym_table:
            raise Exception("Variable {} is already declared of type {}".format(items[1],self.sym_table[items[1]]["type"]))
        
        if len(items[2])==2:            
            code=items[2][1]+"\n"+items[1]+"="+items[2][0]
            self.sym_table[items[1]]={"type":items[0],"value":items[2][0]}
        else:
            code="\n"+items[1]+"="+items[2]
            self.sym_table[items[1]]={"type":items[0],"value":items[2]}

        return code

    def type_specifier(self,items):
        return items[0]

    def init(self,items):
        if items[0] not in self.sym_table:
            raise Exception("Variable {} is not declared".format(items[0]))
        if len(items[1])==2:
            code=items[1][1]+"\n"+items[0]+"="+items[1][0]

        else:
            code="\n"+items[0]+"="+items[1]
        return code

    def declare(self, items):
        if items[1] in self.sym_table:
            raise Exception("Variable {} is already declared of type {}".format(items[1],self.sym_table[items[1]]["type"]))
        self.sym_table[items[1]]={"type":items[0]}
        return ""

    def statement(self,items):
        if len(items)==2:
            return items[0]+items[1]
        else:
            return items[0]
    
    def selection_statement(self,items):
        lc=self.get_new_line()

        if len(items)==3:
            if items[0]=="if":
                code=items[1][1]+"\n"+"IFZ " +items[1][0]+ " GOTO "+lc+items[2]+"\n"+lc+":"
        elif len(items)==5:
            lc1=self.get_new_line()
            code=items[1][1]+"\n"+"IFZ " +items[1][0]+ " GOTO "+lc+items[2]+"\nGoto "+lc1+"\n"+lc+":"+items[4]+"\n"+lc1+":"

        return code

    def iteration_statement(self,items):
        lc=self.get_new_line()
        lc1=self.get_new_line()
        if len(items)==3:
            code="\n"+lc+":"+items[1][1]+"\nIFZ "+items[1][0]+" Goto "+lc1+items[2]+"\nGoto "+lc+"\n"+lc1+":"
        return code

    def compound_statement(self,items):
        if len(items)==1:
            return items[0]
