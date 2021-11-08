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
        self.functions = {'main': FuncionC3D('main', [])}
        self.input = ""
        self.output = ""

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
            self.functions["main"].c3d += instruccion.translate(self, self.symbols)
        self.buildTranslation()
    
    def buildTranslation(self):
        self.output = f'''package main;
import ('''
        for i in self.imports:
            self.output += f'\n    "{i}"'
        self.output += f'''
);

var '''
        for var in range(0, self.temp):
            self.output += f'T{var}'
            if(var!=self.temp-1): self.output += ', '
        self.output += f''' float64;
var P, H float64;
var stack[30101999] float64;
var heap[30101999] float64;

/* NATIVES */
'''

        for key in self.functions:
            if(key != 'main'): 
                self.output += self.functions[key].translate()
        self.output += '\n' + self.functions['main'].translate()


    
    def addPrint(self):
        temps = [self.getTemp(), self.getTemp(), self.getTemp()]
        labels = [self.getLabel(), self.getLabel()]
        self.functions["printString"] = FuncionC3D("printString", [
            InstruccionC3D(temps[0], None, 'P', None, 0, TYPE.ADDITION),
            InstruccionC3D(temps[1], None, 'stack', temps[0], None, TYPE.ASSIGN),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[2], None, 'heap', temps[1], None, TYPE.ASSIGN),
            InstruccionC3D(labels[0], None, temps[2], None, -1, TYPE.EQUAL),
            InstruccionC3D(None, None, temps[2], None, TYPE.CHAR, TYPE.PRINT),
            InstruccionC3D(temps[1], None, temps[1], None, 1, TYPE.ADDITION),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL)
        ])
    
    def addJoinStrings(self):
        temps = [self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp()]
        labels = [self.getLabel(), self.getLabel(), self.getLabel(), self.getLabel()]
        self.functions['joinStrings'] = FuncionC3D('joinStrings',[
            InstruccionC3D(temps[0], None, 'H', None, None, TYPE.ASSIGN),
            InstruccionC3D(temps[1], None, 0, None, None, TYPE.ASSIGN),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(labels[0], None, temps[1], None, 1, TYPE.GREATER),
            InstruccionC3D(temps[2], None, 'P', None, temps[1], TYPE.ADDITION),
            InstruccionC3D(temps[3], None, 'stack', temps[2], None, TYPE.ASSIGN),
            InstruccionC3D(labels[3], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[4], None, 'heap', temps[3], None, TYPE.ASSIGN),
            InstruccionC3D(labels[2], None, temps[4], None, -1, TYPE.EQUAL),
            InstruccionC3D('heap', 'H', temps[4], None, None, TYPE.ASSIGN),
            InstruccionC3D(temps[3], None, temps[3], None, 1, TYPE.ADDITION),
            InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
            InstruccionC3D(labels[3], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[2], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[1], None, temps[1], None, 1, TYPE.ADDITION),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
            InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN),
            InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
            InstruccionC3D(temps[6], None, 'P', None, 2, TYPE.ADDITION),
            InstruccionC3D('stack', temps[6], temps[0], None, None, TYPE.ASSIGN),
        ])

    def addRepeatStrings(self):
        temps = [self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp()]
        labels = [self.getLabel(), self.getLabel(), self.getLabel(), self.getLabel()]
        self.functions['repeatStrings'] = FuncionC3D('repeatStrings',[
            InstruccionC3D(temps[0], None, 'H', None, None, TYPE.ASSIGN),
            InstruccionC3D(temps[1], None, 'P', None, 0, TYPE.ADDITION),
            InstruccionC3D(temps[2], None, 'stack', temps[1], None, TYPE.ASSIGN),
            InstruccionC3D(temps[3], None, 'P', None, 1, TYPE.ADDITION),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(labels[0], None, temps[2], None, 0, TYPE.LOWEREQUAL),
            InstruccionC3D(temps[4], None, 'stack', temps[3], None, TYPE.ASSIGN),
            InstruccionC3D(labels[3], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[5], None, 'heap', temps[4], None, TYPE.ASSIGN),
            InstruccionC3D(labels[2], None, temps[5], None, -1, TYPE.EQUAL),
            InstruccionC3D('heap', 'H', temps[5], None, None, TYPE.ASSIGN),
            InstruccionC3D(temps[4], None, temps[4], None, 1, TYPE.ADDITION),
            InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
            InstruccionC3D(labels[3], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[2], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[2], None, temps[2], None, 1, TYPE.SUBSTRACTION),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
            InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN),
            InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
            InstruccionC3D(temps[6], None, 'P', None, 2, TYPE.ADDITION),
            InstruccionC3D('stack', temps[6], temps[0], None, None, TYPE.ASSIGN),
        ])
    
    def addNumberPower(self):
        temps = [self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp(), self.getTemp()]
        labels = [self.getLabel(), self.getLabel(), self.getLabel(), self.getLabel()]
        self.functions['numberPower'] = FuncionC3D('numberPower',[
            InstruccionC3D(temps[0], None, 'P', None, 0, TYPE.ADDITION),
            InstruccionC3D(temps[1], None, 'stack', temps[0], None, TYPE.ASSIGN),
            InstruccionC3D(temps[2], None, 'P', None, 1, TYPE.ADDITION),
            InstruccionC3D(temps[3], None, 'stack', temps[2], None, TYPE.ASSIGN),
            InstruccionC3D(temps[4], None, 1, None, None, TYPE.ASSIGN),
            InstruccionC3D(labels[0], None, temps[3], None, 0, TYPE.GREATEREQUAL),
            InstruccionC3D(temps[5], None, temps[3], None, -1, TYPE.MULTIPLICATION),
            InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[5], None, temps[3], None, None, TYPE.ASSIGN),
            InstruccionC3D(labels[2], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(labels[1], None, temps[5], None, 0, TYPE.EQUAL),
            InstruccionC3D(temps[4], None, temps[4], None, temps[1], TYPE.MULTIPLICATION),
            InstruccionC3D(temps[5], None, temps[5], None, 1, TYPE.SUBSTRACTION),
            InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
            InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(labels[3], None, temps[3], None, 0, TYPE.GREATEREQUAL),
            InstruccionC3D(temps[4], None, 1, None, temps[4], TYPE.DIVISION),
            InstruccionC3D(labels[3], None, None, None, None, TYPE.LABEL),
            InstruccionC3D(temps[6], None, 'P', None, 2, TYPE.ADDITION),
            InstruccionC3D('stack', temps[6], temps[4], None, None, TYPE.ASSIGN),
        ])

        