'''
MIT License

Copyright (c) 2022 Marcel Guinhos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


__author__ = 'Marcel Guinhos'
__version__ = '1.0.0'

__contact__ = 'github: https://github.com/RazyRabbit; gmail: mguinhos@gmail.com'


from argparse import ArgumentParser
from subprocess import run, getstatusoutput
from os import path, name


def compress(string: str):
    def sanitize(string: str):
        return ''.join(char for char in string if char in '+-<.>[,]')

    oldchar = None
    count = 0
    
    for char in sanitize(string):
        if oldchar is None:
            oldchar = char
            count = 1

        elif char != oldchar:
            yield (oldchar, count)

            oldchar = char
            count = 1

        else:
            count += 1
    
    yield oldchar, count


c_head = '''
#include "base.c"

int main()
{
C_CODE_HERE
}
'''

def transpile_string(program: str):
    def _():
        ioupdated = False
        level = 1

        for opcode, repeat in compress(program):
            if opcode == '+':
                yield 'T[P]++;' if repeat == 1 else f'T[P] += {repeat};', level
            elif opcode == '-':
                yield 'T[P]--;' if repeat == 1 else f'T[P] -= {repeat};', level
            elif opcode == '>':
                yield 'P++;' if repeat == 1 else f'P += {repeat};', level
            elif opcode == '<':
                yield 'P--;' if repeat == 1 else f'P -= {repeat};', level
                
            elif opcode == '[':
                yield 'U();', level
                for _ in range(repeat):
                    yield 'while (T[P] != 0) {', level
                    level += 1
                    
            elif opcode == ']':
                yield 'U();', level
                for _ in range(repeat):
                    level -= 1
                    yield '}', level

                if ioupdated:
                    ioupdated = False
                    
                    yield 'F();', level
                
            elif opcode == '.':
                ioupdated = True

                for _ in range(repeat):
                    yield 'O();', level
            
            elif opcode == ',':
                ioupdated = True

                for _ in range(repeat):
                    yield 'I();', level
                
        return
    
    return c_head.replace('C_CODE_HERE', '\n'.join(('\t' * level) + line for line, level in _()))


def transpile_file(filepath: str, compiler_name: str):
    if not path.isfile(filepath):
        return False

    basename = path.basename(filepath)

    with open(f'src/{basename}.c', 'w') as fout:
        fout.write(transpile_string(open(filepath).read()))

    print(basename, 'transpiled!')
    print('now you must compile it and run!')

    if name.lower() == 'nt':
        print(f'to compile: {compiler_name} src/{basename}.c -o bin/{basename}.exe')
        print(f'to run: bin\\{basename}.exe')
    else:
        print(f'to compile: {compiler_name} src/{basename}.c -o bin/{basename}')
        print(f'to run: ./bin/{basename}')
    
    print()
    
    return True


argparser = ArgumentParser(description='A simple BF to C transpiler')
argparser.add_argument('files', type=str, default=None, nargs='*')

def main(args):
    def get_avaliable_compilers():
        return sorted(name for name in 'gcc clang tcc cc'.split() if getstatusoutput(f'{name} --version')[0] == 0)

    if args.files:
        avaliable_compilers = get_avaliable_compilers()
        compiler_name = avaliable_compilers[0] if avaliable_compilers else 'cc'

        if avaliable_compilers:
            print("Your avaliable C compilers: ", *avaliable_compilers)
        else:
            print("You don't have any supported C compiler installed, please install clang or gcc")

        for filepath in args.files:
            if not transpile_file(filepath, compiler_name):
                argparser.error(f"file {filepath!r} is not a file")
        
    else:
        argparser.error("you must provide a file!")
    
    return

if __name__ == '__main__':
    main(argparser.parse_args())