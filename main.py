from salees_parser import SaleesParser

if __name__=='__main__':
    textInput1="""
    whole my_float=4;
    if(my_float == 7.4){
        frac my_int=9;
    }
    looptill(my_float<0){
        my_float=my_float-5;
    }
    """
    textInput="""
    frac x=4;
    whole y=5;
    whole z=5;
    whole a=9;
    whole b=6;
    looptill(x<y){
        x=x*2;
        if(x<y){
        z=x;
        }other{
        z=y;
        }
        z=z*z;
    }
    y=x;
    a=b*a+b*x;
    if(a>b+y){
        a=b+x;
    }
    y=b*x*y*y||b&&x;
    """
    myParser=SaleesParser(textInput,'top_level')
    myParser.parserProgram()
    #myParser.showParseTree(isPretty=True)
    myParser.generateIC(fileName="three_addr_code")
    