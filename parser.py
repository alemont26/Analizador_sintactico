import ply.yacc as yacc
from lexer import tokens, analizador_lexico

error_sintactico = None

def p_programa(p):
    '''
    programa : sentencias
    '''
    p[0] = "Programa válido"

def p_sentencias(p):
    '''
    sentencias : sentencia sentencias 
                | sentencia
                | 
    '''
    pass

def p_sentencia(p):
    '''
    sentencia : sentencia_for
                | asignacion PUNTOYCOMA
                | llamada_funcion PUNTOYCOMA
    '''
    pass

def p_sentencia_for(p):
    '''
    sentencia_for : FOR PARENTESIS_IZQ asignacion PUNTOYCOMA condicion PUNTOYCOMA incremento PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
    '''
    p[0] = ("BUCLE_FOR", p[3], p[5], p[7], p[10])

def p_asignacion(p):
    '''
    asignacion : ID IGUAL NUMERO
                | ID IGUAL ID
    '''
    p[0] = ("ASIGNACION", p[1], p[3])

def p_condicion(p):
    '''
    condicion : ID MAYORIGUAL NUMERO
                | ID MENOR NUMERO
                | ID MAYOR NUMERO
                | ID MENORIGUAL NUMERO
                | ID IGUAL NUMERO
    '''
    p[0] = ("CONDICION", p[1], p[2], p[3])

def p_incremento(p):
    '''
    incremento : ID MASMAS
                | ID MENOSMENOS
                | ID IGUAL ID OPERADOR NUMERO
                | ID OPERADOR OPERADOR
    ''' 
    if len(p) == 3:
        p[0] = ("INCREMENTO", p[1], p[2])
    else:
        p[0] = ("INCREMENTO", p[1])

def p_cuerpo(p):
    '''
    cuerpo : sentencias
    '''
    p[0] = ("CUERPO", p[1])

def p_llamada_funcion(p):
    '''
    llamada_funcion : SYSTEM PUNTO PRINT PARENTESIS_IZQ parametros PARENTESIS_DER
    '''
    p[0] = ("LLAMADA_FUNCION", "system.print", p[5])

def p_parametros(p):
    '''
    parametros : CADENA COMA ID
                | CADENA
                | ID
                | NUMERO
                | 
    '''
    if len(p) == 4:
        p[0] = ("PARAMETROS", p[1], p[3])
    elif len(p) == 2:
        p[0] = ("PARAMETRO", p[1])
    else:
        p[0] = ("SIN_PARAMETROS",)

def p_sentencia_error_numero_id(p):
    '''
    sentencia : NUMERO ID IGUAL NUMERO PUNTOYCOMA
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[2]}' | Tipo: ID | Línea: {p.lineno(2)}\nIdentificador '{p[2]}' inesperado después de número '{p[1]}'. Los identificadores no pueden empezar con números."

def p_asignacion_error(p):
    '''
    asignacion : NUMERO ID
              | OPERADOR NUMERO
              | ID ID
    '''
    global error_sintactico
    if len(p) > 1:
        if str(p[1]).isdigit():
            error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[2]}' | Tipo: ID | Línea: {p.lineno(2)}\nIdentificador '{p[2]}' inesperado después de número. Los identificadores no pueden empezar con números."
        elif p[1] in ['=', '+', '-', '*', '/', '<', '>', '<=', '>=', '++', '--']:
            error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[1]}' | Tipo: OPERADOR | Línea: {p.lineno(1)}\nOperador '{p[1]}' inesperado al inicio. Falta identificador antes del operador."

def p_for_error_parentesis(p):
    '''
    sentencia_for : FOR LLAVE_IZQ asignacion PUNTOYCOMA condicion PUNTOYCOMA incremento LLAVE_DER LLAVE_IZQ cuerpo LLAVE_DER
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{{' | Tipo: LLAVE_IZQ | Línea: {p.lineno(2)}\nLlave de apertura '{{' inesperada después de 'for'. Falta paréntesis '(' después de 'for'."

def p_for_error_puntoycoma(p):
    '''
    sentencia_for : FOR PARENTESIS_IZQ asignacion condicion PUNTOYCOMA incremento PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Línea: {p.lineno(4)}\nFalta delimitador ';' después de la asignación en el bucle for. Estructura esperada: for(asignacion; condicion; incremento)"

def p_llamada_error_parentesis(p):
    '''
    llamada_funcion : SYSTEM PUNTO PRINT parametros PARENTESIS_DER
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[4]}' | Línea: {p.lineno(4)}\nFalta paréntesis de apertura '(' después de 'print'. Estructura esperada: system.print(parametros)"

def p_error(p):
    global error_sintactico
    if p:
        token_actual = p.value
        tipo_token = p.type
        linea = p.lineno
        
        info_basica = f"ERROR SINTÁCTICO - Token: '{token_actual}' | Tipo: {tipo_token} | Línea: {linea}"
        
        if tipo_token == 'LLAVE_DER':
            descripcion = "Llave de cierre '}' inesperada. Posible problema: falta delimitador ';' en la línea anterior o estructura incompleta."
        elif tipo_token == 'LLAVE_IZQ':
            descripcion = "Llave de apertura '{' inesperada. Posible problema: falta paréntesis de cierre ')' antes de la llave."
        elif tipo_token == 'PARENTESIS_DER':
            descripcion = "Paréntesis de cierre ')' inesperado. Posible problema: paréntesis desbalanceados o expresión incompleta."
        elif tipo_token == 'PARENTESIS_IZQ':
            descripcion = "Paréntesis de apertura '(' inesperado. Posible problema: falta palabra reservada (for) antes del paréntesis."
        elif tipo_token == 'ID':
            descripcion = f"Identificador '{token_actual}' inesperado. Posible problema: falta operador, delimitador ';' o estructura de control incompleta."
        elif tipo_token in ['IGUAL', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL', 'MASMAS', 'MENOSMENOS']:
            descripcion = f"Operador '{token_actual}' inesperado. Posible problema: falta identificador o número antes/después del operador."
        elif tipo_token == 'NUMERO':
            descripcion = f"Número '{token_actual}' inesperado. Posible problema: falta operador antes del número."
        elif tipo_token == 'PUNTOYCOMA':
            descripcion = f"Delimitador '{token_actual}' inesperado. Posible problema: expresión incompleta antes del delimitador."
        elif tipo_token == 'FOR':
            descripcion = f"Palabra reservada '{token_actual}' inesperada. Posible problema: estructura de control anterior incompleta o falta delimitador ';'."
        elif tipo_token == 'SYSTEM':
            descripcion = f"Token '{token_actual}' inesperado. Posible problema: llamada a función mal estructurada."
        else:
            descripcion = f"Token '{token_actual}' no válido en esta posición."
        
        error_sintactico = f"{info_basica}\n{descripcion}"
    else:
        error_sintactico = "Error sintáctico - Token: N/A | Tipo: N/A | Línea: N/A\nFin de entrada inesperado. El código parece incompleto - posible problema: falta llave de cierre '}' o delimitador ';'."

parser = yacc.yacc()

def analizar_sintactico(texto):
    global error_sintactico
    error_sintactico = None
    analizador_lexico.lineno = 1
    
    resultado = parser.parse(texto, lexer=analizador_lexico)
    
    if error_sintactico:
        return error_sintactico, []
    else:
        return "La estructura sintáctica es correcta.", []