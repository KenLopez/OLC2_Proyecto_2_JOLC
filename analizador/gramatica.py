reservadas = {
    'end'       :   'END',
    'Nothing'   :   'NOTHING',
    'Int64'     :   'INT64',
    'Float64'   :   'FLOAT64',
    'Bool'      :   'BOOL',
    'Char'      :   'CHAR',
    'String'    :   'STRING',
    'struct'    :   'STRUCT',
    'print'     :   'PRINT',
    'println'   :   'PRINTLN',
    'local'     :   'LOCAL',
    'global'    :   'GLOBAL',
    'function'  :   'FUNCTION',
    'parse'     :   'PARSE',
    'trunc'     :   'TRUNC',
    'float'     :   'FLOAT',
    'string'    :   'FSTRING',
    'length'    :   'LENGTH',
    'if'        :   'IF',
    'elseif'    :   'ELSEIF',
    'else'      :   'ELSE',
    'while'     :   'WHILE',
    'for'       :   'FOR',
    'in'        :   'IN',
    'break'     :   'BREAK',
    'continue'  :   'CONTINUE',
    'return'    :   'RETURN',
    'mutable'   :   'MUTABLE',
    'true'      :   'TRUE',
    'false'     :   'FALSE',
}

tokens = [
    'PTCOMA',
    'CORCHEA',
    'CORCHEC',
    'DDOSPT',
    'MAS',
    'POR',
    'ELEVADO',
    'MENOS',
    'DIVIDIDO',
    'MODULO',
    'PAREA',
    'PAREC',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUAL',
    'EQUALS',
    'DIFERENTE',
    'OR',
    'AND',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'ID',
    'CADENA',
    'CARACTER',
    'COMA',
    'DOSPT',
    'PT',
] + list(reservadas.values())

# Tokens
t_PTCOMA        = r';'
t_CORCHEA       = r'\['
t_CORCHEC       = r'\]'
t_DDOSPT        = r'::'
t_DOSPT         = r':'        
t_MAS           = r'\+'
t_POR           = r'\*'
t_ELEVADO       = r'\^'
t_MENOS         = r'\-'
t_DIVIDIDO      = r'/'
t_MODULO        = r'%'
t_PAREA         = r'\('
t_PAREC         = r'\)'
t_MENOR         = r'<'
t_MAYOR         = r'>'
t_MENORIGUAL    = r'<='
t_MAYORIGUAL    = r'>='
t_IGUAL         = r'='
t_EQUALS        = r'=='
t_DIFERENTE     = r'!='
t_OR            = r'\|\|'
t_AND           = r'&&'
t_NOT           = r'!'
t_COMA          = r','
t_PT            = r'\.'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor decimal es demasiado grande (%d)", t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor entero es demasiado grande (%d)", t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_CHAR(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter no reconocido '%s'" % t.value[0])

import ply.lex as lex
lexer = lex.lex()

def p_init(t):
    'init           : globales'

def p_globales_mult_1(t):
    'globales       : globales instruccion'

def p_globales_mult_2(t):
    '''globales     : globales funcion END sync
                    | globales struct END sync
    '''

def p_globales_1(t):
    '''globales     : funcion END sync
                    | struct END sync
    '''


def p_globales_3(t):
    'globales       : instruccion'

def p_struct(t):
    'struct         : STRUCT ID attributes'

def p_struct_mutable(t):
    'struct         : MUTABLE STRUCT ID attributes'

def p_attributes(t):
    'attributes     : attributes attribute'

def p_attributes_attribute(t):
    'attributes     : attribute'

def p_attribute(t):
    'attribute      : ID sync'

def p_attribute_type(t):
    'attribute      : ID DDOSPT typing sync'

def p_instrucciones_lista(t):
    'instrucciones  : instrucciones instruccion'

def p_instrucciones_instruccion(t):
    'instrucciones  :   instruccion'

def p_instruccion_while(t):
    'instruccion    : WHILE expl instrucciones END sync'

def p_instruccion_for(t):
    'instruccion    : FOR ID IN range instrucciones END sync'
def p_range_expl(t):
    'range          : expl'

def p_range_range(t):
    'range          : expl DOSPT expl'

def p_instruccion(t):
    '''instruccion  : PRINT args sync 
                    | PRINTLN args sync
    '''

def p_instruccion_asignacion(t):
    'instruccion    : asignacion sync'

def p_instruccion_if(t):
    'instruccion    : if END sync'

def p_instruccion_control(t):
    '''instruccion  : BREAK sync
                    | CONTINUE sync
                    | RETURN sync
    '''

def p_instruccion_return_value(t):
    'instruccion    : RETURN expl sync'

def p_instruccion_call(t):
    'instruccion    : call sync'

def p_if_solo(t):
    'if             : IF expl instrucciones'

def p_if_else(t):
    'if             : IF expl instrucciones ELSE instrucciones'

def p_if_elseif(t):
    'if             : IF expl instrucciones elseif'

def p_if_full(t):
    'if             : IF expl instrucciones elseif ELSE instrucciones'

def p_if_elseifs(t):
    'elseif         : elseif ELSEIF expl instrucciones'

def p_elseif(t):
    'elseif         : ELSEIF expl instrucciones'

def p_asignacion_any(t):
    'asignacion     : variable IGUAL expl'

def p_asignacion_tipo(t):
    'asignacion     : variable IGUAL expl DDOSPT typing'

def p_declaracion_none(t):
    'asignacion     : variable'

def p_funcion(t):
    'funcion        : FUNCTION ID params instrucciones'

def p_params(t):
    'params         : PAREA list_params PAREC'

def p_params_none(t):
    'params         : PAREA PAREC'

def p_call(t):
    'call           : ID args'

def p_list_params(t):
    'list_params    : list_params COMA param'

def p_list_param(t):
    'list_params    : param'

def p_param(t):
    'param          : ID'

def p_param_type(t):
    'param          : ID DDOSPT typing'

def p_variable_id(t):
    'variable       : id'

def p_variable_struct(t):
    'variable       : ID PT struct_access'

def p_variable_local(t):
    'variable       : LOCAL ID'

def p_variable_global(t):
    'variable       : GLOBAL ID'

def p_id_id(t):
    'id         : ID'

def p_id_array_access(t):
    'id         : ID array_access'

def p_expl(t):
    '''expl         : expl OR expl
                    | expl AND expl
    '''

def p_expl_expr(t):
    'expl           : expr'

def p_expr(t):
    '''expr         : expr EQUALS expr
                    | expr DIFERENTE expr
                    | expr MENOR expr
                    | expr MAYOR expr
                    | expr MAYORIGUAL expr
                    | expr MENORIGUAL expr
    
    '''

def p_expr_expm(t):
    'expr           : expm'

def p_expm(t):
    '''expm         : expm MAS expm
                    | expm MENOS expm
                    | expm POR expm
                    | expm DIVIDIDO expm
                    | expm MODULO expm
                    | expm ELEVADO expm
    '''

def p_expm_val(t):
    'expm           : expval'

def p_expval_not(t):
    'expval         : NOT expval'

def p_expval_neg(t):
    'expval         : MENOS expval'

def p_expval_string(t):
    'expval         : CADENA'

def p_expval_char(t):
    'expval         : CARACTER'

def p_expval_bool(t):
    'expval         : booleano'

def p_expval_int(t):
    'expval         : ENTERO'

def p_expval_float(t):
    'expval         : DECIMAL'

def p_expval_nativa(t):
    'expval         : nativa'

def p_expval_id(t):
    'expval         : ID'

def p_expval_call(t):
    'expval         : call'

def p_expval_paren(t):
    'expval         : PAREA expl PAREC'

def p_nativa(t):
    '''nativa       : PARSE args
                    | TRUNC args
                    | FLOAT args
                    | FSTRING args
                    | LENGTH args
    '''

def p_expval_array(t):
    'expval         : CORCHEA list_values CORCHEC'

def p_expval_empty_array(t):
    'expval         : CORCHEA CORCHEC'

def p_expval_array_access(t):
    'expval         : ID array_access'

def p_expval_nothing(t):
    'expval         : NOTHING'

def p_expval_struct_access(t):
    'expval         : ID PT struct_access'

def p_array_accesses(t):
    'array_access   : array_access CORCHEA expm CORCHEC'

def p_array_access(t):
    'array_access   : CORCHEA expm CORCHEC'

def p_struct_accesses(t):
    'struct_access   : struct_access PT ID'

def p_struct_access(t):
    'struct_access   : ID'

def p_list_values(t):
    'list_values    : list_values COMA expl'

def p_list_value(t):
    'list_values    : expl'

def p_args(t):
    'args           : PAREA list_values PAREC'

def p_args_none(t):
    'args           : PAREA PAREC'

# Valores Booleanos

def p_booleano_true(t):
    'booleano       : TRUE'

def p_booleano_false(t):
    'booleano       : FALSE'

# Tipado

def p_typing(t):
    '''typing       : INT64
                    | FLOAT64
                    | STRING
                    | BOOL
                    | CHAR
                    | ID
                    | NOTHING
    '''

def p_sync(t):
    'sync           : PTCOMA'

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    return parser.parse(input)