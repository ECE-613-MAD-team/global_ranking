import numpy as np

read_path = './test/a_'

def read_datas(model1=0, model2=1):
    # we do not save the judgement for every subject, just mean ..
    n1 = n2 = n3 = 0
    file_name = read_path + str(model1) + '_' + str(model2) + '.txt'
    with open(file_name, 'rt') as f:
        ff = f.read().split('\n')
        for line in ff[:-1]:
            # every line is a texture with unknown subjects ..
            user_choose = line.split(' ')
            for res in user_choose:
                res = int(res)
                if res == 0:
                    n1 += 1
                elif res == 1:
                    n2 += 1
                else:
                    n3 += 1
    print(n1+n2+n3, n2, n3)

    return n3 / (n1+n2+n3), n2 / (n1+n2+n3)

if __name__ == "__main__":
    model_nums = 3
    a = np.zeros((model_nums, model_nums), dtype=float)
    r = np.zeros((model_nums, model_nums), dtype=float)
    for i in range(0, model_nums):
        for j in range(0, model_nums):
            if i == j:
                continue
            # do model i attack j
            a[i][j], r[j][i] = read_datas(i, j)

    a_i = np.sum(a, axis=1) / (model_nums-1)
    r_i = np.sum(r, axis=0) / (model_nums-1)

    # aggressive and resistent matrix ...
    a_show = a - np.transpose(a)
    r_show = r - np.transpose(r)
    print(a_show)
    print(r_show)

    # global ranking
    for i in range(0, model_nums):
        print('a_' + str(i) + ': ' + str(a_i[i]))
        print('r_' + str(i) + ': ' + str(r_i[i]))
