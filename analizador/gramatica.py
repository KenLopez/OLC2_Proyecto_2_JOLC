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
    'uppercase' :   'UPPERCASE',
    'lowercase' :   'LOWERCASE',
    'true'      :   'TRUE',
    'false'     :   'FALSE',
    'Vector'    :   'VECTOR',
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
    'LLAVEA',
    'LLAVEC',
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
t_LLAVEA        = r'\{'
t_LLAVEC        = r'\}'

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

def t_CARACTER(t):
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

from classes.Aritmetica import Aritmetica
from classes.Array import Array
from classes.Global import Global
from classes.Logica import Logica
from classes.Print import Print
from classes.Relacional import Relacional
from classes.Tipo import TYPE
from classes.Variable import Variable
from classes.Value import Value
from classes.Nativa import Nativa
from classes.Call import Call
from classes.ArrayAccess import ArrayAccess
from classes.While import While
from classes.StructAccess import StructAccess
from classes.Param import Param
from classes.Funcion import Funcion
from classes.Declaracion import Declaracion
from classes.Asignacion import Asignacion
from classes.If import If
from classes.Control import Control
from classes.For import For
from classes.Struct import Struct
import ply.lex as lex

lexer = lex.lex()

precedence = (
    ('right', 'IGUAL'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQUALS', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'ELEVADO'),
)

def p_init(t):
    'init           : globales'
    t[0] = Global()
    t[0].instrucciones = t[1]

def p_globales_list(t):
    'globales       : globales global'
    t[1].append(t[2])
    t[0] = t[1]

def p_globales(t):
    'globales       : global'
    t[0] = [t[1]]

def p_global_func_struct(t):
    '''global       : funcion END sync
                    | struct END sync
    '''
    t[0] = t[1]

def p_global_instruccion(t):
    'global       : instruccion'
    t[0] = t[1]

# Definición de struct

def p_struct(t):
    'struct         : STRUCT ID attributes'
    t[0] = Declaracion(t[2], Struct(t[3], False, TYPE.STRUCTDEF), t.lexer.lineno, t.lexer.lexpos)

def p_struct_mutable(t):
    'struct         : MUTABLE STRUCT ID attributes'
    t[0] = Declaracion(t[3], Struct(t[4], True, TYPE.STRUCTDEF), t.lexer.lineno, t.lexer.lexpos)

# Atributos de struct

def p_attributes(t):
    'attributes     : attributes attribute'
    t[1].append(t[2])
    t[0] = t[1]

def p_attributes_attribute(t):
    'attributes     : attribute'
    t[0] = [t[1]]

# Definición de atributo

def p_attribute(t):
    'attribute      : ID sync'
    t[0] = Param(t[1], Value(TYPE.ANY, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos))

def p_attribute_type(t):
    'attribute      : ID DDOSPT typing sync'
    t[0] = Param(t[1], t[3])

# Lista de instrucciones locales

def p_instrucciones_lista(t):
    'instrucciones  : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    'instrucciones  :   instruccion'
    t[0] = [t[1]]

# Instrucción while

def p_instruccion_while(t):
    'instruccion    : WHILE expl instrucciones END sync'
    t[0] = While(t[2], t[3], t.lexer.lineno, t.lexer.lexpos)

# Instrucción for

def p_instruccion_for(t):
    'instruccion    : FOR ID IN range instrucciones END sync'
    t[0] = For(t[2], t[4], t[5], t.lexer.lineno, t.lexer.lexpos)

# Tipos de range

def p_range_expl(t):
    'range          : expl'
    t[0] = t[1]

def p_range_range(t):
    'range          : expl DOSPT expl'
    t[0] = Value([t[1], t[3]], TYPE.RANGE, t.lexer.lineno, t.lexer.lexpos)

# Instrucciones locales

def p_instruccion(t):
    '''instruccion  : PRINT args sync 
                    | PRINTLN args sync
    '''
    if t[1]=='print': t[0] = Print(t[2], TYPE.PRINT, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='println': t[0] = Print(t[2], TYPE.PRINTLN, t.lexer.lineno, t.lexer.lexpos)

def p_instruccion_asignacion(t):
    'instruccion    : asignacion sync'
    t[0] = t[1]

def p_instruccion_if(t):
    'instruccion    : if END sync'
    t[0] = t[1]

def p_instruccion_control(t):
    '''instruccion  : BREAK sync
                    | CONTINUE sync
                    | RETURN sync
    '''
    if t[1] == 'break': t[0] = Control(None, TYPE.BREAK, t.lexer.lineno, t.lexer.lexpos)
    elif t[1] == 'return': t[0] = Control(Value(None, TYPE.NOTHING, t.lexer.lineno, t.lexer.lexpos), TYPE.RETURN, t.lexer.lineno, t.lexer.lexpos)
    elif t[1] == 'continue': t[0] = Control(None, TYPE.CONTINUE, t.lexer.lineno, t.lexer.lexpos)

def p_instruccion_return_value(t):
    'instruccion    : RETURN expl sync'
    t[0] = Control(t[1], TYPE.RETURN, t.lexer.lineno, t.lexer.lexpos)

def p_instruccion_call(t):
    'instruccion    : call sync'
    t[0] = t[1]

# Sentencia if

def p_if_solo(t):
    'if             : IF expl instrucciones'
    t[0] = If([t[2]], [t[3]], [], t.lexer.lineno, t.lexer.lexpos)


def p_if_else(t):
    'if             : IF expl instrucciones ELSE instrucciones'
    t[0] = If([t[2]], [t[3]], t[5], t.lexer.lineno, t.lexer.lexpos)

def p_if_elseif(t):
    'if             : IF expl instrucciones elseif'
    con = [t[2]]
    con.extend(t[4][0])
    ins = [t[3]]
    ins.extend(t[4][1])
    t[0] = If(con, ins, [], t.lexer.lineno, t.lexer.lexpos)

def p_if_full(t):
    'if             : IF expl instrucciones elseif ELSE instrucciones'
    con = [t[2]]
    con.extend(t[4][0])
    ins = [t[3]]
    ins.extend(t[4][1])
    t[0] = If(con, ins, t[6], t.lexer.lineno, t.lexer.lexpos)

def p_if_elseifs(t):
    'elseif         : elseif ELSEIF expl instrucciones'
    t[1][0].append(t[3])
    t[1][1].append(t[4])
    t[0] = [t[1][0], t[1][1]]

def p_elseif(t):
    'elseif         : ELSEIF expl instrucciones'
    t[0] = [[t[2]], [t[3]]]

# Asinaciones y definición de variables

def p_asignacion_any(t):
    'asignacion     : variable IGUAL expl'
    t[0] = Asignacion(
        t[1][0], 
        t[3], 
        Value(TYPE.ANY, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos), 
        t[1][1], 
        t.lexer.lineno, 
        t.lexer.lexpos
    )

def p_asignacion_tipo(t):
    'asignacion     : variable IGUAL expl DDOSPT typing'
    t[0] = Asignacion(
        t[1][0], 
        t[3], 
        t[5], 
        t[1][1], 
        t.lexer.lineno, 
        t.lexer.lexpos
    )
def p_declaracion_none(t):
    'asignacion     : variable'
    t[0] = Asignacion(
        t[1][0], 
        Value(None, TYPE.NOTHING, t.lexer.lineno, t.lexer.lexpos), 
        Value(TYPE.ANY, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos), 
        t[1][1], 
        t.lexer.lineno, 
        t.lexer.lexpos
    )

# Definición de función

def p_funcion(t):
    'funcion        : FUNCTION ID params instrucciones'
    t[0] = Declaracion(t[2], Funcion(t[3], t[4], TYPE.NOTHING), t.lexer.lineno, t.lexer.lexpos)

def p_funcion_2(t):
    'funcion        : FUNCTION ID params DDOSPT typing instrucciones'
    t[0] = Declaracion(t[2], Funcion(t[3], t[5], t[4]), t.lexer.lineno, t.lexer.lexpos) 

# Parámetros

def p_params(t):
    'params         : PAREA list_params PAREC'
    t[0] = t[2]

def p_params_none(t):
    'params         : PAREA PAREC'
    t[0] = []

# Llamada a método

def p_call(t):
    'call           : ID args'
    Call(t[1], t[2], t.lexer.lineno, t.lexer.lexpos)

# Lista de parámetros

def p_list_params(t):
    'list_params    : list_params COMA param'
    t[1].append(t[3])
    t[0] = t[1]

def p_list_param(t):
    'list_params    : param'
    t[0] = [t[1]]

# Definición de parámetros

def p_param(t):
    'param          : ID'
    t[0] = Param(t[1], Value(TYPE.ANY, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos))

def p_param_type(t):
    'param          : ID DDOSPT typing'
    t[0] = Param(t[1], t[3])

# Formas de definir una variable

def p_variable_id(t):
    'variable       : id'
    if(isinstance(t[1], ArrayAccess)):
        t[0] = [t[1], TYPE.ANY]
    else:
        t[0] = [Variable(t[1], t.lexer.lineno, t.lexer.lexpos), TYPE.ANY]

def p_variable_local(t):
    'variable       : LOCAL id'
    if(isinstance(t[2], ArrayAccess)):
        t[0] = [t[2], TYPE.LOCAL]
    else:
        t[0] = [Variable(t[2], t.lexer.lineno, t.lexer.lexpos), TYPE.LOCAL]

def p_variable_global(t):
    'variable       : GLOBAL id'
    if(isinstance(t[2], ArrayAccess)):
        t[0] = [t[2], TYPE.GLOBAL]
    else:
        t[0] = [Variable(t[2], t.lexer.lineno, t.lexer.lexpos), TYPE.GLOBAL]

# Identificadores de asignación

def p_id_id(t):
    'id         : ID'
    t[0] = t[1]

def p_id_array_access(t):
    'id         : array_value'
    t[0] = t[1]

def p_id_struct_access(t):
    'id         : struct_value'
    t[0] = t[1]

# Expresiones lógivas

def p_expl(t):
    '''expl         : expl OR expl
                    | expl AND expl
    '''
    if t[2]=='||': t[0] = Logica(t[1], t[3], TYPE.OR, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='&&': t[0] = Logica(t[1], t[3], TYPE.AND, t.lexer.lineno, t.lexer.lexpos)

def p_expl_expr(t):
    'expl           : expr'
    t[0] = t[1]

# Expresiones relacionales

def p_expr(t):
    '''expr         : expr EQUALS expr
                    | expr DIFERENTE expr
                    | expr MENOR expr
                    | expr MAYOR expr
                    | expr MAYORIGUAL expr
                    | expr MENORIGUAL expr
    
    '''
    if t[2]=='==': t[0] = Relacional(t[1], t[3], TYPE.EQUAL, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='!=': t[0] = Relacional(t[1], t[3], TYPE.DIFFERENT, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='<': t[0] = Relacional(t[1], t[3], TYPE.LOWER, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='>': t[0] = Relacional(t[1], t[3], TYPE.GREATER, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='<=': t[0] = Relacional(t[1], t[3], TYPE.LOWEREQUAL, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='>=': t[0] = Relacional(t[1], t[3], TYPE.GREATEREQUAL, t.lexer.lineno, t.lexer.lexpos)

def p_expr_expm(t):
    'expr           : expm'
    t[0] = t[1]

# Expresiones matemáticas

def p_expm(t):
    '''expm         : expm MAS expm
                    | expm MENOS expm
                    | expm POR expm
                    | expm DIVIDIDO expm
                    | expm MODULO expm
                    | expm ELEVADO expm
    '''
    if t[2]=='+': t[0] = Aritmetica(t[1], t[3], TYPE.ADDITION, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='-': t[0] = Aritmetica(t[1], t[3], TYPE.SUBSTRACTION, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='*': t[0] = Aritmetica(t[1], t[3], TYPE.MULTIPLICATION, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='/': t[0] = Aritmetica(t[1], t[3], TYPE.DIVISION, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='%': t[0] = Aritmetica(t[1], t[3], TYPE.MODULUS, t.lexer.lineno, t.lexer.lexpos)
    elif t[2]=='^': t[0] = Aritmetica(t[1], t[3], TYPE.POWER, t.lexer.lineno, t.lexer.lexpos)

def p_expm_val(t):
    'expm           : expval'
    t[0] = t[1]

# Expresiones de valores

def p_expval_not(t):
    'expval         : NOT expval'
    t[0] = Logica(t[2], None, TYPE.NOT, t.lexer.lineno, t.lexer.lexpos)

def p_expval_neg(t):
    'expval         : MENOS expval'
    t[0] = Aritmetica(t[2], None, TYPE.NEGATIVE, t.lexer.lineno, t.lexer.lexpos)


def p_expval_string(t):
    'expval         : CADENA'
    t[0] = Value(t[1], TYPE.STRING, t.lexer.lineno, t.lexer.lexpos)

def p_expval_char(t):
    'expval         : CARACTER'
    t[0] = Value(t[1], TYPE.CHAR, t.lexer.lineno, t.lexer.lexpos)

def p_expval_bool(t):
    'expval         : booleano'
    t[0] = t[1]

def p_expval_int(t):
    'expval         : ENTERO'
    t[0] = Value(t[1], TYPE.INT64, t.lexer.lineno, t.lexer.lexpos)

def p_expval_float(t):
    'expval         : DECIMAL'
    t[0] = Value(t[1], TYPE.FLOAT64, t.lexer.lineno, t.lexer.lexpos)

def p_expval_nativa(t):
    'expval         : nativa'
    t[0] = t[1]

def p_expval_id(t):
    'expval         : ID'
    t[0] = Variable(t[1], t.lexer.lineno, t.lexer.lexpos)

def p_expval_call(t):
    'expval         : call'
    t[0] = t[1]

def p_expval_paren(t):
    'expval         : PAREA expl PAREC'
    t[0] = t[2]

def p_expval_array(t):
    'expval         : CORCHEA list_values CORCHEC'
    t[0] = Value(t[2], TYPE.LIST, t.lexer.lineno, t.lexer.lexpos)

def p_expval_empty_array(t):
    'expval         : CORCHEA CORCHEC'
    t[0] = Value([], TYPE.LIST, t.lexer.lineno, t.lexer.lexpos)

def p_expval_array_access(t):
    'expval         : array_value'
    t[0] = t[1]

def p_expval_struct_access(t):
    'expval         : struct_value'
    t[0] = t[1]

def p_expval_type(t):
    'expval         : typing'
    t[0] = t[1]

# Nativas

def p_nativa(t):
    '''nativa       : PARSE args
                    | TRUNC args
                    | FLOAT args
                    | FSTRING args
                    | LENGTH args
                    | LOWERCASE args
                    | UPPERCASE args 
    '''
    if t[1]=='parse': t[0] = Nativa(t[2], TYPE.PARSE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='trunc': t[0] = Nativa(t[2], TYPE.TRUNCATE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='float': t[0] = Nativa(t[2], TYPE.FFLOAT, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='string': t[0] = Nativa(t[2], TYPE.FSTRING, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='length': t[0] = Nativa(t[2], TYPE.LENGTH, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='uppercase': t[0] = Nativa(t[2], TYPE.UPPERCASE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='lowercase': t[0] = Nativa(t[2], TYPE.LOWERCASE, t.lexer.lineno, t.lexer.lexpos)

# Acceso a array

def p_array(t):
    'array_value    : ID array_access'
    t[0] = ArrayAccess(Variable(t[1], t.lexer.lineno, t.lexer.lexpos), t[2], t.lexer.lineno, t.lexer.lexpos)

def p_array_accesses(t):
    'array_access   : array_access CORCHEA expl CORCHEC'
    t[1].append(t[3])
    t[0] = t[1]

def p_array_access(t):
    'array_access   : CORCHEA expl CORCHEC'
    t[0] = [t[2]]

# Acceso a struct

def p_struct_value(t):
    'struct_value   : ID PT struct_access'
    t[0] = StructAccess(t[1], t[3], t.lexer.lineno, t.lexer.lexpos)

def p_struct_accesses(t):
    'struct_access   : struct_access PT ID'
    t[1].append(t[3])
    t[0] = t[1]

def p_struct_access(t):
    'struct_access   : ID'
    t[0] = [t[1]]

# Lista de valores

def p_list_values(t):
    'list_values    : list_values COMA expl'
    t[1].append(t[3])
    t[0] = t[1]

def p_list_value(t):
    'list_values    : expl'
    t[0] = [t[1]]

# Valores de parámetros

def p_args(t):
    'args           : PAREA list_values PAREC'
    t[0] = t[2]

def p_args_none(t):
    'args           : PAREA PAREC'
    t[0] = []

# Valores Booleanos

def p_booleano_true(t):
    'booleano       : TRUE'
    t[0] = Value(True, TYPE.BOOL, t.lexer.lineno, t.lexer.lexpos)

def p_booleano_false(t):
    'booleano       : FALSE'
    t[0] = Value(False, TYPE.BOOL, t.lexer.lineno, t.lexer.lexpos)

# Tipado

def p_typing(t):
    '''typing       : INT64
                    | FLOAT64
                    | STRING
                    | BOOL
                    | CHAR
                    | NOTHING
    '''
    if t[1]=='Int64': t[0] = Value(TYPE.INT64, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='Float64': t[0] = Value(TYPE.FLOAT64, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='String': t[0] = Value(TYPE.STRING, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='Bool': t[0] = Value(TYPE.BOOL, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='Char': t[0] = Value(TYPE.CHAR, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)
    elif t[1]=='Nothing': t[0] = Value(TYPE.STRING, TYPE.TYPE, t.lexer.lineno, t.lexer.lexpos)

def p_typing_id(t):
    'typing         : ID'
    t[0] = Value(t[1], TYPE.TYPESTRUCT, t.lexer.lineno, t.lexer.lexpos)

def p_typing_vector(t):
    'typing         : VECTOR LLAVEA typing LLAVEC'
    if(isinstance(t[3].type, Array)):
        t[0] = Value(TYPE.LIST, Array(0, TYPE.LIST, t[3].type), t.lexer.lineno, t.lexer.lexpos)
    else:
        t[0] = Value(TYPE.LIST, Array(0, t[3].val, None), t.lexer.lineno, t.lexer.lexpos)

def p_sync(t):
    'sync           : PTCOMA'

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    return parser.parse(input)