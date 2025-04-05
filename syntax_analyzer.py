from lexer import lexer

# control whether to print the parsing rules
print_rules = True

# global variables for tracking current token and file pointers
current_token = None
current_lexeme = None
output_file = None
fp = None  # file pointer for lexer

def next_token():
    """Get next token from lexer and write to output file"""
    global current_token, current_lexeme
    current_token, current_lexeme = lexer(fp)
    
    # write token info to output file
    if output_file:
        output_file.write(f"Token: {current_token:14} Lexeme: {current_lexeme}\n")
    if print_rules:
        print(f"Token: {current_token:14} Lexeme: {current_lexeme}")

def syntax_error(expected):
    """Handle syntax errors with meaningful messages"""
    err_msg = f"[Syntax Error] Expected {expected}, but got '{current_lexeme}' ({current_token})"
    if output_file:
        output_file.write(err_msg + "\n")
    print(err_msg)
    exit(1)

# R1. <Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$
def Rat25S():
    if print_rules: 
        if output_file: output_file.write("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$\n")
        print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    OptFunctionDefinitions()
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    OptDeclarationList()
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    StatementList()
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()

# R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
def OptFunctionDefinitions():
    if print_rules: 
        if output_file: output_file.write("<Opt Function Definitions> -> <Function Definitions> | <Empty>\n")
        print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    
    if current_token == "Keyword" and current_lexeme == "function":
        FunctionDefinitions()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R3. <Function Definitions> ::= <Function> <Function Definitions>
def FunctionDefinitions():
    if print_rules: 
        if output_file: output_file.write("<Function Definitions> -> <Function> <Function Definitions>\n")
        print("<Function Definitions> -> <Function> <Function Definitions>")
    Function()
    FunctionDefinitions()

# R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
def Function():
    if print_rules: 
        if output_file: output_file.write("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>\n")
        print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    
    if current_lexeme != "function":
        syntax_error("function")
    next_token()
    
    if current_token != "Identifier":
        syntax_error("Identifier")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    OptParameterList()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    OptDeclarationList()
    Body()

# R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
def OptParameterList():
    if print_rules: 
        if output_file: output_file.write("<Opt Parameter List> -> <Parameter List> | <Empty>\n")
        print("<Opt Parameter List> -> <Parameter List> | <Empty>")
    
    if current_token == "Identifier":
        ParameterList()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R6. <Parameter List> ::= <Parameter> , <Parameter List> | <Parameter>
def ParameterList():
    if print_rules: 
        if output_file: output_file.write("<Parameter List> -> <Parameter> , <Parameter List> | <Parameter>\n")
        print("<Parameter List> -> <Parameter> , <Parameter List> | <Parameter>")
    
    Parameter()
    if current_lexeme == ",":
        next_token()
        ParameterList()

# R7. <Parameter> ::= <IDs> : <Qualifier>
def Parameter():
    if print_rules: 
        if output_file: output_file.write("<Parameter> -> <IDs> : <Qualifier>\n")
        print("<Parameter> -> <IDs> : <Qualifier>")
    
    IDs()
    if current_lexeme != ":":
        syntax_error(":")
    next_token()
    Qualifier()

# R8. <Qualifier> ::= integer | boolean | real
def Qualifier():
    if print_rules: 
        if output_file: output_file.write("<Qualifier> -> integer | boolean | real\n")
        print("<Qualifier> -> integer | boolean | real")
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean", "real"}:
        next_token()
    else:
        syntax_error("Qualifier (integer|boolean|real)")

# R9. <Body> ::= { <Statement List> }
def Body():
    if print_rules: 
        if output_file: output_file.write("<Body> -> { <Statement List> }\n")
        print("<Body> -> { <Statement List> }")
    
    if current_lexeme != "{":
        syntax_error("{")
    next_token()
    
    StatementList()
    
    if current_lexeme != "}":
        syntax_error("}")
    next_token()

# R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
def OptDeclarationList():
    if print_rules: 
        if output_file: output_file.write("<Opt Declaration List> -> <Declaration List> | <Empty>\n")
        print("<Opt Declaration List> -> <Declaration List> | <Empty>")
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean", "real"}:
        DeclarationList()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R11. <Declaration List> ::= <Declaration> ; <Declaration List>
def DeclarationList():
    if print_rules: 
        if output_file: output_file.write("<Declaration List> -> <Declaration> ; <Declaration List>\n")
        print("<Declaration List> -> <Declaration> ; <Declaration List>")
    
    Declaration()
    if current_lexeme != ";":
        syntax_error(";")
    next_token()
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean", "real"}:
        DeclarationList()

# R12. <Declaration> ::= <Qualifier> <IDs>
def Declaration():
    if print_rules: 
        if output_file: output_file.write("<Declaration> -> <Qualifier> <IDs>\n")
        print("<Declaration> -> <Qualifier> <IDs>")
    
    Qualifier()
    IDs()

# R13. <IDs> ::= <Identifier> , <IDs> | <Identifier>
def IDs():
    if print_rules: 
        if output_file: output_file.write("<IDs> -> <Identifier> , <IDs> | <Identifier>\n")
        print("<IDs> -> <Identifier> , <IDs> | <Identifier>")
    
    if current_token != "Identifier":
        syntax_error("Identifier")
    next_token()
    
    if current_lexeme == ",":
        next_token()
        IDs()

# R14. <Statement List> ::= <Statement> <Statement List> | <Statement>
def StatementList():
    if print_rules: 
        if output_file: output_file.write("<Statement List> -> <Statement> <Statement List> | <Statement>\n")
        print("<Statement List> -> <Statement> <Statement List> | <Statement>")
    
    Statement()
    
    # Look ahead for next possible statement
    if (current_lexeme in {"{", "if", "while", "return", "scan", "print"} or 
        current_token == "Identifier"):
        StatementList()

# R15. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
def Statement():
    if print_rules: 
        if output_file: output_file.write("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>\n")
        print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    
    if current_lexeme == "{":
        Compound()
    elif current_token == "Identifier":
        Assign()
    elif current_lexeme == "if":
        If()
    elif current_lexeme == "return":
        Return()
    elif current_lexeme == "print":
        Print()
    elif current_lexeme == "scan":
        Scan()
    elif current_lexeme == "while":
        While()
    else:
        syntax_error("Statement start")

# R16. <Compound> ::= { <Statement List> }
def Compound():
    if print_rules: 
        if output_file: output_file.write("<Compound> -> { <Statement List> }\n")
        print("<Compound> -> { <Statement List> }")
    
    if current_lexeme != "{":
        syntax_error("{")
    next_token()
    
    StatementList()
    
    if current_lexeme != "}":
        syntax_error("}")
    next_token()

# R17. <Assign> ::= <Identifier> = <Expression> ;
def Assign():
    if print_rules: 
        if output_file: output_file.write("<Assign> -> <Identifier> = <Expression> ;\n")
        print("<Assign> -> <Identifier> = <Expression> ;")
    
    if current_token != "Identifier":
        syntax_error("Identifier")
    next_token()
    
    if current_lexeme != "=":
        syntax_error("=")
    next_token()
    
    Expression()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R18. <If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi
def If():
    if print_rules: 
        if output_file: output_file.write("<If> -> if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi\n")
        print("<If> -> if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi")
    
    if current_lexeme != "if":
        syntax_error("if")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Condition()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    Statement()
    
    if current_lexeme == "else":
        next_token()
        Statement()
    
    if current_lexeme != "fi":
        syntax_error("fi")
    next_token()

# R19. <Return> ::= return <Expression> ;
def Return():
    if print_rules: 
        if output_file: output_file.write("<Return> -> return <Expression> ;\n")
        print("<Return> -> return <Expression> ;")
    
    if current_lexeme != "return":
        syntax_error("return")
    next_token()
    
    Expression()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R20. <Print> ::= print ( <Expression> );
def Print():
    if print_rules: 
        if output_file: output_file.write("<Print> -> print ( <Expression> );\n")
        print("<Print> -> print ( <Expression> );")
    
    if current_lexeme != "print":
        syntax_error("print")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Expression()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R21. <Scan> ::= scan ( <IDs> );
def Scan():
    if print_rules: 
        if output_file: output_file.write("<Scan> -> scan ( <IDs> );\n")
        print("<Scan> -> scan ( <IDs> );")
    
    if current_lexeme != "scan":
        syntax_error("scan")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    IDs()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R22. <While> ::= while ( <Condition> ) <Statement>
def While():
    if print_rules: 
        if output_file: output_file.write("<While> -> while ( <Condition> ) <Statement>\n")
        print("<While> -> while ( <Condition> ) <Statement>")
    
    if current_lexeme != "while":
        syntax_error("while")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Condition()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    Statement()

# R23. <Condition> ::= <Expression> <Relop> <Expression>
def Condition():
    if print_rules: 
        if output_file: output_file.write("<Condition> -> <Expression> <Relop> <Expression>\n")
        print("<Condition> -> <Expression> <Relop> <Expression>")
    
    Expression()
    Relop()
    Expression()

# R24. <Relop> ::= == | != | > | < | <= | >=
def Relop():
    if print_rules: 
        if output_file: output_file.write("<Relop> -> == | != | > | < | <= | >=\n")
        print("<Relop> -> == | != | > | < | <= | >=")
    
    if current_token == "Operator" and current_lexeme in {"==", "!=", ">", "<", "<=", ">="}:
        next_token()
    else:
        syntax_error("relational operator (==|!=|>|<|<=|>=)")

# R25. <Expression> ::= <Term> <ExpressionPrime>
def Expression():
    if print_rules: 
        if output_file: output_file.write("<Expression> -> <Term> <ExpressionPrime>\n")
        print("<Expression> -> <Term> <ExpressionPrime>")
    Term()
    ExpressionPrime()

# R26. <ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | ε
def ExpressionPrime():
    if current_token == "Operator" and current_lexeme in {"+", "-"}:
        if print_rules: 
            if output_file: output_file.write(f"<ExpressionPrime> -> {current_lexeme} <Term> <ExpressionPrime>\n")
            print(f"<ExpressionPrime> -> {current_lexeme} <Term> <ExpressionPrime>")
        next_token()
        Term()
        ExpressionPrime()
    else:
        if print_rules: 
            if output_file: output_file.write("<ExpressionPrime> -> ε\n")
            print("<ExpressionPrime> -> ε")

# R27. <Term> ::= <Factor> <TermPrime>
def Term():
    if print_rules: 
        if output_file: output_file.write("<Term> -> <Factor> <TermPrime>\n")
        print("<Term> -> <Factor> <TermPrime>")
    Factor()
    TermPrime()

# R28. <TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | ε
def TermPrime():
    if current_token == "Operator" and current_lexeme in {"*", "/"}:
        if print_rules: 
            if output_file: output_file.write(f"<TermPrime> -> {current_lexeme} <Factor> <TermPrime>\n")
            print(f"<TermPrime> -> {current_lexeme} <Factor> <TermPrime>")
        next_token()
        Factor()
        TermPrime()
    else:
        if print_rules: 
            if output_file: output_file.write("<TermPrime> -> ε\n")
            print("<TermPrime> -> ε")

# R29. <Factor> ::= - <Primary> | <Primary>
def Factor():
    if print_rules: 
        if output_file: output_file.write("<Factor> -> - <Primary> | <Primary>\n")
        print("<Factor> -> - <Primary> | <Primary>")
    
    if current_token == "Operator" and current_lexeme == "-":
        next_token()
        Primary()
    else:
        Primary()

# Helper: <Primary> ::= Identifier | Integer | Real | ( <Expression> )
def Primary():
    if print_rules: 
        if output_file: output_file.write("<Primary> -> Identifier | Integer | Real | ( <Expression> )\n")
        print("<Primary> -> Identifier | Integer | Real | ( <Expression> )")
    
    if current_token in {"Identifier", "Integer", "Real"}:
        if output_file:
            output_file.write(f"Token: {current_token}   Lexeme: {current_lexeme}\n")
        print(f"Token: {current_token}   Lexeme: {current_lexeme}")
        next_token()
    elif current_lexeme == "(":
        next_token()
        Expression()
        if current_lexeme != ")":
            syntax_error(")")
        next_token()
    else:
        syntax_error("Identifier | Integer | Real | (Expression)")

def syntax_analyzer(input_filename, output_filename):
    """Main analyzer function that processes input file"""
    global output_file, fp
    
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            output_file = outfile
            fp = infile  # make file pointer available globally
            
            # initialize first token
            next_token()
            
            # begin parsing
            Rat25S()
            
            # verify we reached EOF
            if current_token != "EOF":
                syntax_error("EOF")
                
            if output_file:
                output_file.write("Parsing completed successfully!\n")
            print("Parsing completed successfully!")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found")
    except Exception as e:
        print(f"Error during parsing: {str(e)}")

if __name__ == "__main__":
    input_file = input("Enter input file name: ")
    output_file_name = input("Enter output file name: ")
    syntax_analyzer(input_file, output_file_name)