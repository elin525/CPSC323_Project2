
# operators = ["==", "=", "!=", ">", "<", "<=", "=>", "+", "-", "*", "/"]

# keywords = ["function", "integer", "real", "boolean", "if", "else", "endif", 
#             "while", "return", "scan", "print", "endwhile","true", "false"]

# seperators = ["{", "}", ";", "(", ")", "$$", ",", ":"]

# def fsmId(curr_tok):
#     """
#         Finite State machine that handles Identifiers and keywords.
#         A token is an identifier if:
#             - It starts with a letter,
#             - It contains a "_", letter, or digit
#         A token is a keyword if it is contained within the keywords data 
#         structure defined above.
#     """

#     # Handle Keywords
#     if curr_tok in keywords:
#         return ("Keyword", curr_tok)
    
#     else:
#         for char in curr_tok:
#             if char.isalpha() or char.isdigit() or char == "_":
#                 continue
#             # Invalid identifier
#             else:
#                 return ("Unknown", curr_tok)
#         # Identifier
#         return ("Identifier", curr_tok)
    
# def fsmInt(curr_tok):
#     """
#         Finite State machine that handles Integers.
#         This FSM is called for any tokens that start with an integer
#         and returns "Not_Int" in the case that the the token does not just 
#         contain integers. If the token is a real it will be initially defined
#         as "Not_Int" and then will be passed to fsmReal to verify if it is
#         a Real.
#     """
#     for integer in curr_tok:
#         if integer.isdigit():
#             continue
#         else:
#             return ("Not_Int", curr_tok)
#     # Integer
#     return ("Integer", curr_tok)

# def fsmReal(curr_tok):
#     """
#         Finite State machine that handles Reals.
#         A token is defined as a Real if:
#         - It starts with an integer.
#         - It contains one decimal.
#         - It contains at least one integer after the decimal.
#     """
#     num_decimals = 0
#     index_of_last_digit = len(curr_tok) - 1
#     for index in range(1, len(curr_tok)):

#         if curr_tok[index].isdigit():
#             continue
#         elif curr_tok[index] == ".":

#             # If number of decimals exceeds one.
#             if num_decimals >= 1:
#                 return ("Unknown", curr_tok)
            
#             num_decimals += 1
#         else:
#             return ("Unknown", curr_tok)
    
#     # Token is a Real.
#     if curr_tok[index_of_last_digit].isdigit():
#         return ("Real", curr_tok)
    
#     # Cases where an integer does not occur after the decimal.
#     else:
#         return ("Unknown", curr_tok)
    
def lexer(fp):

    # read until whitespace, newline, or tab
    curr_tok = ""
    curr_tok_type = ""
    curr_string = ""

    is_comment = False

    first_char_seperators = ["{", "}", ";", "(", ")", "$", ",", ":"]
    seperators = ["{", "}", ";", "(", ")", "$$", ",", ":"]

    first_char_operators = ["=", "!", ">", "<", "+", "-", "*", "/"]
    operators = ["==", "=", "!=", ">", "<", "<=", "=>", "+", "-", "*", "/"]

    while (
            curr_string != ' ' and curr_string != '\t' and 
            curr_string != '\n' and not curr_string is None
    ):
        curr_string = fp.read(1)

        if curr_string == "":
            return ("EOF", "EOF")
        
        if (curr_string == '\n' or curr_string == '\t'):
            curr_string = ""
            continue
        
        # token is flushed
        if curr_tok == "":

            curr_tok = curr_string

            # now analyze the current token

            ######################## Token is a Comment ########################
            if curr_tok == "[":
                curr_tok_type = "Unknown"
                curr_string = ""
                continue

            ####################### Token is an Operator #######################
            if curr_tok in first_char_operators:
                curr_tok_type = "Operator"
                curr_string = "" # flush the current string
                continue

            ####################### Token is a Seperator #######################
            if curr_tok in first_char_seperators:
                curr_tok_type = "Seperator"
                curr_string = "" # flush the current string
                continue

            ###################### Token is a Identifier #######################
            if curr_tok.isalpha():
                curr_tok_type = "Identifier"
                curr_string = "" # flush the current string
                continue

            ####################### Token is a Int/Real ########################
            if curr_tok.isdigit():
                curr_tok_type = "Integer"
                curr_string = "" # flush the current string
                continue

            if curr_tok == " ":
                curr_string = ""
                curr_tok = ""
                continue
            
            # TODO: If current token is unknown, continue to concat to it until 
            # a string is read that is not unknown. Create a seperate if statement
            # in the else (that handles curr_tok != "" ) that will update curr_tok
            # with the known string type and return the Unknown token
            else:
                # print("BUG: " + curr_tok)
                curr_tok_type = "Unknown"
                curr_string = "" # flush the current string
                continue
        
        else:
            ######################## Token is a Comment ########################
            if is_comment:
                buf = curr_tok + curr_string
                len_of_buf = len(buf)
                if curr_string == "]" and buf[len_of_buf-2] == "*":
                    is_comment = False
                    curr_tok = ""
                    curr_string = ""
                    continue
                else:
                    curr_tok = curr_tok + curr_string
                    curr_string = ""
                    continue

            ####################### Token is an Operator #######################
            if curr_tok_type == "Operator":
                # if current operator is 2 char long then it should be returned
                buf = curr_tok + curr_string
                if buf in operators:
                    curr_tok = "" # flush the current token
                    curr_string = "" # flush the current string
                    return ("Operator", buf)
                # if the current operator is 1 char long return what is in the current token
                else:
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    if buf == "!":
                        return ("Unknown", buf)
                    return ("Operator", buf)
            
            ####################### Token is a Seperator #######################
            if curr_tok_type == "Seperator":
                # if current seperator is 2 char long then it should be returned
                buf = curr_tok + curr_string
                if buf in seperators:
                    curr_tok = "" # flush the current token
                    curr_string = "" # flush the current string
                    return ("Seperator", buf)
                # if the current operator is 1 char long return what is in the current token
                else:
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    if buf == "$":
                        return ("Unknown", buf)
                    return ("Seperator", buf)
            
            ######################## Token is a Keyword ########################
            keywords = ["function", "integer", "real", "boolean", "if", "else", "endif", 
            "while", "return", "scan", "print", "endwhile","true", "false"]
            potential_keyword = curr_tok + curr_string
            if potential_keyword in keywords:
                curr_tok = "" # flush the current token
                curr_string = ""
                return ("Keyword", potential_keyword)
            
            if curr_tok in keywords:
                buf = curr_tok # return the current token
                curr_tok = "" # flush the current token since the current char will be read again
                # send the file pointer back one
                if curr_string != " ":
                    current_fp_position = fp.tell()
                    fp.seek(current_fp_position - 1)
                curr_string = "" # flush the current string
                return ("Keyword", buf)
            
            ###################### Token is a Identifier #######################
            if curr_tok_type == "Identifier":
                if (curr_string.isalpha() or curr_string.isdigit()):
                    curr_tok = curr_tok + curr_string
                    curr_string = ""
                    continue
                else:
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    return ("Identifier", buf)
            
            ######################## Token is a Integer ########################
            if curr_tok_type == "Integer":
                if curr_string == ".":
                    curr_tok_type = "Real"
                    curr_tok = curr_tok + curr_string
                    curr_string = ""
                    continue
                elif curr_string.isdigit():
                    curr_tok = curr_tok + curr_string
                    curr_string = ""
                    continue
                else:
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    return ("Integer", buf)
                
            ######################### Token is a Real ##########################
            if curr_tok_type == "Real":
                if curr_string.isdigit():
                    curr_tok = curr_tok + curr_string
                    curr_string = ""
                    continue
                else:
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    return ("Real", buf)
            ####################### Token is a Unknown #########################
            if curr_tok_type == "Unknown":
                
                if curr_tok == "[":
                    if curr_string == "*":
                        is_comment = True
                        curr_tok = curr_tok + curr_string
                        curr_string = ""
                        continue

                if (curr_string in first_char_operators or
                    curr_string in first_char_seperators):
                    
                    buf = curr_tok # return the current token
                    curr_tok = "" # flush the current token since the current char will be read again
                    # send the file pointer back one
                    if curr_string != " ":
                        current_fp_position = fp.tell()
                        fp.seek(current_fp_position - 1)
                    curr_string = "" # flush the current string
                    # print("Tok Unknown: " + buf)
                    return ("Unknown", buf)
                else:
                    if (curr_string == " " or
                        curr_string == '\t' or
                        curr_string == '\n'):
                        buf = curr_tok
                        curr_tok = ""
                        curr_string = ""
                        return ("Unknown", buf)
                    else:
                    
                        curr_tok = curr_tok + curr_string
                        curr_string = ""
                        continue

def main():
    """
        Starting point for the lexical analyser.
        
        User may enter in a test file written in Rat_25s to be analyzed and an
        output file containing each token's type and lexeme will be produced.
    """
    import sys
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <input_file>")
        return

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as fp:    
            while True:
                token_type, lexeme = lexer(fp)
                print(f"{token_type:14} {lexeme}")
                if token_type == "EOF":
                    break
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")

if __name__ == "__main__":
    main()