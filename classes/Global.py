import base64
from classes.Declaracion import Declaracion
from classes.FuncionC3D import FuncionC3D
from classes.InstruccionC3D import InstruccionC3D
from classes.SymbolTable import SymbolTable
from classes.Tipo import TYPE
import graphviz

class Global:
    def __init__(self):
        self.instrucciones = []
        self.symbols = SymbolTable()
        self.errors = []
        self.ast = None
        self.label = 0
        self.temp = 0
        self.imports = []
        self.functions = {'main': FuncionC3D('main')}
        self.input = ""
        self.output = f'''package main;
        
import (
    "fmt"
)
        
var P, H float64;
var stack[100000000] float64;
var heap[100000000] float64;

func main(){{
    fmt.Println("Hello World!");   
}}
'''

    def getLabel(self):
        newLabel = f'L{self.label}'
        self.label = self.label + 1
        return newLabel
    
    def getTemp(self):
        newTemp = f'T{self.temp}'
        self.temp = self.temp + 1
        return newTemp
    
    def translate(self):
        for instruccion in self.instrucciones:
            res = instruccion.translate(self)
    
    def addPrint(self):
        temps = [self.getTemp(), self.getTemp(), self.getTemp()]
        labels = [self.getLabel(), self.getLabel()]
        self.functions["printString"] = FuncionC3D("printString", [
            InstruccionC3D(temps[0], 'P', 1, TYPE.ADDITION),
            InstruccionC3D(temps[1], 'stack', temps[0], TYPE.LIST),
            InstruccionC3D(labels[1], None, None, TYPE.LABEL),
            InstruccionC3D(temps[2], 'heap', temps[1], TYPE.LIST),
            InstruccionC3D(labels[0], temps[2], -1, TYPE.EQUAL),
            InstruccionC3D(None, temps[2], TYPE.CHAR, TYPE.PRINT),
            InstruccionC3D(temps[1], temps[1], 1, TYPE.ADDITION),
            InstruccionC3D(labels[1], None, None, TYPE.GOTO),
            InstruccionC3D(labels[0], None, None, TYPE.LABEL)
        ])

        