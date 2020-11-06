#!/usr/bin/env python
import sys
import re

def decimal_to_binary_string(num):
    return '{0:016b}'.format(num)

class Simbolos():
    simbolos_base = {
        'SP'  : 0,
        'LCL' : 1,
        'ARG' : 2,
        'THIS': 3,
        'THAT': 4,
        'R0'  : 0,
        'R1'  : 1,
        'R2'  : 2,
        'R3'  : 3,
        'R4'  : 4,
        'R5'  : 5,
        'R6'  : 6,
        'R7'  : 7,
        'R8'  : 8,
        'R9'  : 9,
        'R10' : 10,
        'R11' : 11,
        'R12' : 12,
        'R13' : 13,
        'R14' : 14,
        'R15' : 15,
        'SCREEN': 16384,
        'KBD'   : 24576
    }

    def __init__(self):
        self.symbols = self.simbolos_base
        self.siguiente_espacio_memoria = 16

    def add_entry(self, symbol=None, address=None):
        if address:
            self.symbols[symbol] = address
        else:
            self.symbols[symbol] = self.siguiente_espacio_memoria
            self.siguiente_espacio_memoria += 1

        return self.get_address(symbol)

    def contains(self, symbol):
        return symbol in self.symbols

    def get_address(self, symbol):
        return self.symbols[symbol]


class Assembler():
    def __init__(self, input_file):
        self.parser = AssemblerParser(input_file)
        self.symbol_table = Simbolos()
    # 1ra pasada
    def parsear_labels(self):
        instructiones_leidas = 0

        while self.parser.has_more_lineas_to_parse:
            self.parser.advance()

            if self.parser.tipo_de_comando == 'not_instruction':
                continue
            elif self.parser.tipo_de_comando == 'label':
                self.symbol_table.add_entry(symbol=self.parser.symbol(), address=instructiones_leidas)
            else:
                instructiones_leidas += 1

    # 2da pasada
    def traducir(self):
        hack_file_name = self.parser.input_file.name.split('.')[0] + '.hack'
        hack_file = open(hack_file_name, 'w+')

        char_only_matcher = re.compile('[a-zA-Z]+')

        while self.parser.has_more_lineas_to_parse:
            self.parser.advance()
            machine_code = ''

            if self.parser.tipo_de_comando == 'address':
                symbol = self.parser.symbol()
                not_number = char_only_matcher.match(symbol)

                if not_number:
                    if self.symbol_table.contains(symbol):
                        register_number = self.symbol_table.get_address(symbol)
                    else:
                        register_number = self.symbol_table.add_entry(symbol)
                else:
                    register_number = int(symbol)

                machine_code = decimal_to_binary_string(register_number)
            elif self.parser.tipo_de_comando == 'computation':
                # init_bits
                init_bits = AssemblerDecoder.c_inicio
                # Comp
                comp_mnemonic = self.parser.comp_mnemonic()
                comp_bits = AssemblerDecoder.comparar_dict[comp_mnemonic]
                # Dest
                dest_mnemonic = self.parser.dest_mnemonic()
                dest_bits = AssemblerDecoder.destino_dict[dest_mnemonic]
                # Jump
                jump_mnemonic = self.parser.jump_mnemonic()
                jump_bits = AssemblerDecoder.jump_dict[jump_mnemonic]

                machine_code = init_bits + comp_bits + dest_bits + jump_bits

            if len(machine_code) > 0:
                hack_file.write(machine_code + '\n')

        hack_file.close()

    def run(self):
        self.parsear_labels()
        self.parser.reset()
        self.traducir()



class AssemblerDecoder():
    c_inicio = '111'

    destino_dict = {
        None : '000',
        'M'  : '001',
        'D'  : '010',
        'MD' : '011',
        'A'  : '100',
        'AM' : '101',
        'AD' : '110',
        'AMD': '111'
    }

    comparar_dict = {
        None : '',
        '0'  : '0101010',
        '1'  : '0111111',
        '-1' : '0111010',
        'D'  : '0001100',
        'A'  : '0110000',
        'M'  : '1110000',
        '!D' : '0001101',
        '!A' : '0110001',
        '!M' : '1110001',
        '-D' : '0001111',
        '-A' : '0110011',
        '-M' : '1110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'M-1': '1110010',
        'D+A': '0000010',
        'D+M': '1000010',
        'D-A': '0010011',
        'D-M': '1010011',
        'A-D': '0000111',
        'M-D': '1000111',
        'D&A': '0000000',
        'D&M': '1000000',
        'D|A': '0010101',
        'D|M': '1010101'
    }

    jump_dict = {
        None : '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }


class AssemblerParser():
    DEST_DELIMITER = '='
    JUMP_DELIMITER = ';'

    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.current_command = None
        self.next_linea = None
        self.has_more_lineas_to_parse = True

    def reset(self):
        self.input_file.seek(0)
        self.current_command = None
        self.next_linea = None
        self.has_more_lineas_to_parse = True

    def dest_mnemonic(self):
        if self.current_command.find(self.DEST_DELIMITER) != -1:
            return self.current_command.split(self.DEST_DELIMITER)[0]

    def comp_mnemonic(self):
        if self.current_command.find(self.DEST_DELIMITER) != -1:
            return self.current_command.split(self.DEST_DELIMITER)[1]
        elif self.current_command.find(self.JUMP_DELIMITER) != -1:
            return self.current_command.split(self.JUMP_DELIMITER)[0]

    def jump_mnemonic(self):
        if self.current_command.find(self.JUMP_DELIMITER) != -1:
            return self.current_command.split(self.JUMP_DELIMITER)[1]

    def symbol(self):
        return ''.join(c for c in self.current_command if c not in '()@/')

    def advance(self):
        # initial state
        if self.current_command == None:
            self.current_command = self.input_file.readline()
        else:
            self.current_command = self.next_linea

        # remove whitespace and comments
        self.current_command = self.limpiar_linea_linea(self.current_command)

        self.next_linea = self.input_file.readline()
        # empty lines return \n
        if self.next_linea == '':
            self.has_more_lineas_to_parse = False

        self.encontrar_tipo_de_comando()

    def limpiar_linea_linea(self, line):
        # remove leading and trailing whitespace
        line = line.strip()
        # remove comments
        line = line.split('//')[0]
        # strip again in case space after, i.e., D=M+1 // comments
        line = line.strip(' ')

        return line

    def encontrar_tipo_de_comando(self):
        if self.current_command == '':
            self.tipo_de_comando = 'not_instruction'
        elif self.current_command[0] == '@':
            self.tipo_de_comando = 'address'
        elif self.current_command[0] == '(':
            self.tipo_de_comando = 'label'
        else:
            self.tipo_de_comando = 'computation'

asm_input_file = sys.argv[1]
assembler = Assembler(asm_input_file)
assembler.run()
