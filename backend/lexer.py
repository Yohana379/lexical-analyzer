import re
import bisect

# Token Specifications - ORDER MATTERS!
TOKEN_SPEC = [
    # Literals
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"([^"\\\\]|\\.)*"'),
    ('BOOLEAN', r'\b(true|false|True|False)\b'),
    ('NULL', r'\b(null|None|nil|NULL)\b'),
    
    # Keywords
    ('KEYWORD', r'\b(if|else|while|for|do|switch|case|break|continue|return|int|float|double|char|boolean|string|void|class|struct|def|import|from|try|catch|except|new|delete|public|private|protected|static|const|final)\b'),
    
    # Identifiers
    ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
    
    # Comments
    ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
    ('COMMENT_SINGLE', r'//[^\n]*'),
    ('HASH_COMMENT', r'#[^\n]*'),
    
    # Comparison Operators
    ('EQ_OP', r'=='),
    ('NE_OP', r'!='),
    ('LE_OP', r'<='),
    ('GE_OP', r'>='),
    ('LT_OP', r'<'),
    ('GT_OP', r'>'),
    
    # Logical Operators
    ('AND_OP', r'&&'),
    ('OR_OP', r'\|\|'),
    ('NOT_OP', r'!'),
    
    # Arithmetic Operators
    ('POWER_OP', r'\*\*'),
    ('ADD_OP', r'\+'),
    ('SUB_OP', r'-'),
    ('MUL_OP', r'\*'),
    ('DIV_OP', r'/'),
    ('FLOOR_DIV', r'//'),
    ('MOD_OP', r'%'),
    
    # Assignment Operators
    ('ASSIGN_OP', r'='),
    ('ADD_ASSIGN', r'\+='),
    ('SUB_ASSIGN', r'-='),
    ('MUL_ASSIGN', r'\*='),
    ('DIV_ASSIGN', r'/='),
    ('MOD_ASSIGN', r'%='),
    
    # Bitwise Operators
    ('BIT_AND', r'&'),
    ('BIT_OR', r'\|'),
    ('BIT_XOR', r'\^'),
    ('BIT_NOT', r'~'),
    ('LSHIFT', r'<<'),
    ('RSHIFT', r'>>'),
    
    # Increment/Decrement
    ('INC_OP', r'\+\+'),
    ('DEC_OP', r'--'),
    
    # Special Operators
    ('ARROW', r'->'),
    ('SCOPE_RES', r'::'),
    ('SAFE_NAV', r'\?\.'),
    ('SPREAD', r'\.\.\.'),
    ('AT', r'@'),
    
    # Delimiters - SPECIFIC NAMES
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('COLON', r':'),
    ('QUESTION', r'\?'),
    
    # Whitespace
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    
    # Error
    ('MISMATCH', r'.'),
]

# Compile master regex
master_pat = re.compile('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC))

def tokenize_source_code(code: str):
    tokens = []
    line_starts = [0] + [m.end() for m in re.finditer(r'\n', code)]
    
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        start_pos = mo.start()
        
        if kind in ('NEWLINE', 'SKIP'):
            continue
            
        if kind == 'MISMATCH':
            kind = 'ERROR'
            
        line_num = bisect.bisect_right(line_starts, start_pos)
        col_num = start_pos - line_starts[line_num - 1] + 1
        
        tokens.append({
            'lexeme': value,
            'token_type': kind,
            'line': line_num,
            'column': col_num
        })
        
    return tokens

if __name__ == "__main__":
    sample_code = """
int x = (5 + 3) * 2;
if (x == 16) {
    return x;
}
"""
    results = tokenize_source_code(sample_code)
    for r in results:
        print(f"{r['token_type']:15} | {r['lexeme']:10} | L{r['line']:2} C{r['column']:2}")
