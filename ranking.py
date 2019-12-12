import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
    r_i = np.sum(r, axis=1) / (model_nums-1)
    # aggressive and resistent matrix ...
    a_show = a - np.transpose(a)
    r_show = r - np.transpose(r)
    print(a_show)
    print(r_show)

    # make the color by myself
    cmap_name = 'my_color'
    colors = [(0, 0, 1), (0.06, 0.29, 0.99), (0.15, 0.88, 0.98), 
                (0.52, 1, 0.52), (0.98, 0.86, 0.25), (0.99, 0.25, 0.12), (1, 0, 0)] # R -> G -> B
    n_bin = 1000
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    alpha = ['MSE', 'SSIM', 'VGG-Gram']

    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    cax1 = ax.matshow(a_show, interpolation='nearest', cmap=cm, vmin=-0.65, vmax=0.65)
    fig1.colorbar(cax1)
    fig1.suptitle('Aggressive matrix', fontsize=16)
    ax.set_xticklabels(['']+alpha, verticalalignment='baseline')
    ax.set_yticklabels(['']+alpha)
    plt.show()

    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    cax2 = ax.matshow(r_show, interpolation='nearest', cmap=cm, vmin=-0.65, vmax=0.65)
    fig2.colorbar(cax2)
    fig2.suptitle('Resistance matrix', fontsize=16)
    ax.set_xticklabels(['']+alpha, verticalalignment='baseline')
    ax.set_yticklabels(['']+alpha)
    plt.show()

    # global ranking
    size = 3
    a_array = np.random.random(size)
    r_array = np.random.random(size)
    fig, ax = plt.subplots()
    index = np.arange(size)
    bar_width = 0.35

    for i in range(0, model_nums):
        print('a_' + str(i) + ': ' + str(a_i[i]))
        print('r_' + str(i) + ': ' + str(r_i[i]))
        a_array[i] = a_i[i] - 0.5
        r_array[i] = r_i[i] - 0.5

    rects1 = ax.bar(index, a_array, bar_width, color=(0.15, 0.98, 0.95),
                    label='Aggressive')
    rects2 = ax.bar(index + bar_width, r_array, bar_width, color=(0.05, 0.05, 0.9),
                    label='Resistence')

    # ax.set_xlabel('Group')
    ax.set_ylabel('Global ranking score')
    ax.set_title('Global ranking')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('MSE', 'SSIM', 'VGG-Gram'), rotation=25)
    ax.legend()

    fig.tight_layout()
    plt.show()