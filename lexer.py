import ply.lex as lex

palabras_reservadas = {
    'for': 'FOR',
    'system': 'SYSTEM',
    'print': 'PRINT'
}

tokens = [
    'ID', 'NUMERO', 'CADENA',
    'IGUAL', 'PUNTOYCOMA', 'MAYOR', 'MAYORIGUAL', 'MENOR', 'MENORIGUAL',
    'PARENTESIS_IZQ', 'PARENTESIS_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'MASMAS', 'MENOSMENOS', 'PUNTO', 'COMA', 'OPERADOR'
] + list(palabras_reservadas.values())

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ      = r'\{'
t_LLAVE_DER      = r'\}'
t_IGUAL          = r'='
t_PUNTOYCOMA     = r';'
t_MASMAS         = r'\+\+'
t_MENOSMENOS     = r'--'
t_MAYORIGUAL     = r'>='
t_MENORIGUAL     = r'<='
t_MAYOR          = r'>'
t_MENOR          = r'<'
t_OPERADOR       = r'[+\-*/]'
t_PUNTO          = r'\.'
t_COMA           = r','
t_CADENA         = r'\"(.*?)\"'

def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = palabras_reservadas.get(token.value, 'ID')
    return token

def t_NUMERO(token):
    r'\d+'
    token.value = int(token.value)
    return token

def t_newline(token):
    r'\n+'
    token.lexer.lineno += len(token.value)

t_ignore = ' \t'

def t_error(token):
    print(f"Caracter no reconocido '{token.value[0]}' en la línea {token.lineno}")
    token.lexer.skip(1)

analizador_lexico = lex.lex()

def analizar_lexico(texto):
    analizador_lexico.input(texto)
    lista_de_tokens = []
    while True:
        token = analizador_lexico.token()
        if not token:
            break
        lista_de_tokens.append(token)
    return lista_de_tokens