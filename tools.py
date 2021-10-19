
class Data:

    def __init__(self, args, res):
        self.args  = args
        self.res   = res

class Table:
    def __init__(self, names):
        self.names = list(names)
        self.data = list()
        self.vova = []

    def print_headers(self):

        self.max_ = len(sorted(self.names, key=len)[-1])
        def gen(s):
            return ' ' + str(' ' * (self.max_ - len(s) -1 )) + s + ' '
        tmp = '|' + f'|'.join([gen(s) for s in self.names]) + '| RES |'

        print(f'|{"=" * (len(tmp) - 2)}|')
        print(tmp)
        print(f'|{"=" * (len(tmp) - 2)}|')


    def print_row(self, args, res):

        def gen(args, res):
            p = '|'
            for i in args:
                p += ' ' + str(' ' * (self.max_ - len(str(i)))) +str(i) + ' |'
            p += f'  {res}  |'
            return p
        print(gen(args, res))
        self.data.append([args, res])
        #print(f'| {" | ".join([str(x) for x in args])} |  {res}  |')

    def recurser(self, lst : list):

        return_data = []
        for i in range(len(lst)):
            p = []
            for mat in range(0, len(lst)):
                bebra = []
                for ii in range(len(lst[i])):
                    if lst[i][ii] != lst[mat][ii]:

                        bebra.append(ii)
                if len(bebra) == 1:
                    tmp_bebra = list(lst[i])
                    tmp_bebra[bebra[0]] = 2
                    p.append(tmp_bebra)
            if not len(p):
                self.vova.append(lst[i])
            else:
                find = False
                for aue in p:
                    if aue not in return_data:
                        return_data.append(aue)

        if not len(return_data):
            return
        return self.recurser(return_data)


    def check_is_need(self, tests : list):  # tests = [Data, Data]

        l = 0
        for i in tests:
            l += i.res

        if l / len(tests) == 1:
            return "1"
        elif l / len(tests) == 0:
            return "0"

        tmp = []
        for i in self.data:
            if i[1] == 1:
                tmp.append(i[0])

        tmp_data = self.recurser(tmp)
        d = []

        for i in self.vova:
            Tmp_data = []
            for ii in range(len(i)):
                if not i[ii]:
                    Tmp_data.append(f'¬{self.names[ii]}')
                if i[ii] == 1:
                    Tmp_data.append(self.names[ii])

            d.append(Tmp_data)
        for i in range(len(self.data)):
            if type(self.data[i]) == list:
                if self.data[i][1]:

                    self.data[i] = list(self.data[i][0])
                    for x in range(len(self.data[i])):
                        if not self.data[i][x]:
                            self.data[i][x] = '¬' + self.names[x]
                        else:
                            self.data[i][x] = self.names[x]
        p = []
        for i in self.data:
            if type(i) == list:
                if type(i[0]) != tuple:
                    p.append(i)
        self.data = p
        step2 = [[False for _ in self.data] for _ in d]

        for i, impl in enumerate(d):
            for j, orig in enumerate(self.data):
                if all(arg in orig for arg in impl):
                    step2[i][j] = True

        sdnf, fucked = petric(d, step2)

        for item in fucked:
            sdnf.append(d[item])


        print(f'Штрих Шефера    : {sheffer(sdnf)}')
        return str('+'.join(['*'.join([str(x) for x in sdnf])]).replace('[', '(').replace(']', ')').replace("'", '').replace(',', '').replace(' ', '+'))

def sheffer(sdnf):
    sheffer_sdnf = [item.copy() for item in sdnf]

    for i in range(len(sheffer_sdnf)):
        item = sheffer_sdnf[i]
        for j in range(len(item)):
            if item[j][0] == '¬':
                s = item[j].replace('¬', '')
                item[j] = f'({s} {"↑"} {s})'

    res = []
    for i in range(len(sdnf)):
        while len(sheffer_sdnf[i]) > 1:
            sheffer_sdnf[i][
                0] = f'(({sheffer_sdnf[i][0]} {"↑"} {sheffer_sdnf[i][1]}) {"↑"} ({sheffer_sdnf[i][0]} {"↑"} {sheffer_sdnf[i][1]}))'
            del sheffer_sdnf[i][1]
        res.extend(sheffer_sdnf[i])

    if len(sheffer_sdnf) > 1:
        final = []

        for item in res:
            s = f'(({item}) {"↑"} ({item}))'
            final.append(s)

        final_res = f' {"↑"} '.join(final)
    else:
        final_res = f' {"↑"} '.join(sheffer_sdnf[0])

    return final_res


def multiply(first, second):
    res = []

    for left in first:
        for right in second:
            r = left
            if right not in r:
                r += right
            if r not in res:
                res.append(r)

    return res


def petric(vars, step2):
    from string import ascii_uppercase
    letters = {ascii_uppercase[i]: var for i, var in enumerate(vars)}

    fucked = []
    res = []
    for i in range(len(step2[0])):
        exp = []
        for j in range(len(step2)):
            if step2[j][i]:
                exp.append(ascii_uppercase[j])

        if len(exp) == 0:
            fucked.append(i)
        else:
            res.append(exp)

    while len(res) > 1:
        res[0] = multiply(res[0], res[1])
        del res[1]

    final = min(res[0], key=len)
    super_final = [letters[item] for item in final]

    return super_final, fucked

