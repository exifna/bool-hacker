from itertools import product
import tests
from tools import Data, Table
import inspect

def hack(func):

    print(f'\n> Program start')

    print(f'> Function: {func.__name__}\n> Table\n')
    args = [i.name for i in  inspect.signature(func).parameters.values()]
    Class = Table(args)
    Class.print_headers()

    Datas = []

    arg_list = list(product([0, 1], repeat=len(args)))

    for i in range(len(arg_list)):

        Datas.append(Data(arg_list[i], int(func(*arg_list[i]))))

    # ∧ - и, +
    # ∨ - или, *

    lst = []
    for i in Datas:
        Class.print_row(i.args, i.res)
        if i.res:
            res = ''
            for ii in range(len(i.args)):
                iii = i.args[ii]

                if not iii:
                    if ii != 0:
                        res += f'∧¬{Class.names[ii]}'
                    else:
                        res += f'¬{Class.names[ii]}'
                else:
                    if ii != 0:
                        res += f'∧{Class.names[ii]}'
                    else:
                        res += f'{Class.names[ii]}'
            lst.append(res)


    Class.print_headers()
    x = '∨'.join(f'({res})' for res in lst)
    if not x:
        x = "0"
    print(f'\nСДНФ : {x}')
    print(f'СДНФ2: {x.replace("∧", "+").replace("∨", "*")}\n\n{"#" * 40}\n')

    print(f'Сокращенное ДНФ : {Class.check_is_need(Datas)}')

def func1(x,y,z):
    return x or y and z

def func2(a,b,c,d,e):
    return False

def func3(a,b,c,f,g):
    return (a or b) and c and f or g

hack(func3)
