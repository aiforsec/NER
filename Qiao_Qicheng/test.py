import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as linear
import random
import math

text1 = "Identity transformation"
text2 = "Tahn transformation"


def problem1():
    w_1 = [0.25, 0.25, 0.25]
    w_0 = [w_1, w_1]
    x_1 = np.array([1.0, 1.0, 1.0])
    x_2 = np.insert(np.tanh(np.dot(w_0, x_1)), 0, 1.0)
    hid = np.tanh(np.dot(w_1, x_2))
    print("=======================")
    print("(a)")
    print(text1)
    m = 2
    wt = 0.25
    d_2 = wt * m * (hid - 1)
    dif_2 = np.dot(d_2, x_2)
    d_1 = cal_d1(d_2, w_1, x_2)
    dif_1 = np.outer(x_1, d_1)
    print('dif 1: \n', dif_1)
    print('dif 2: \n', dif_2)
    print(text2)
    d_2_t = wt * m * (hid - 1) * (1 - pow(hid, 2))
    d_1_t = cal_d1(d_2_t, w_1, x_2)
    dif_1_t = np.outer(x_1, d_1_t)
    dif_2_t = np.dot(d_2, x_2)
    print('dif 1: \n', dif_1_t)
    print('dif 2: \n', dif_2_t)

    print("====================")
    print("(b)")
    print(text1)
    new_dif_2 = []
    new_dif_1 = []
    i = 0
    while (i < 3):
        p_w_1 = [0.25, 0.25, 0.25]
        p_w_1[i] += 0.0001
        m_w_1 = w_1
        m_w_1[i] -= 0.0001
        p_hid = np.dot(p_w_1, x_2)
        m_hid = np.dot(m_w_1, x_2)
        w_2_ = cam_num(m_hid, p_hid)
        new_dif_2.append(w_2_)
        i += 1
    i = 0
    while (i < 2):
        j = 0
        sub_dif = []
        while (j < 3):
            #
            p_w_0 = [[0.25, 0.25, 0.25], [0.25, 0.25, 0.25]]
            p_w_0[i][j] += 0.0001
            p_x_2 = np.insert(np.tanh(np.dot(p_w_0, x_1)), 0, 1.0)
            p_hid = np.dot(w_1, p_x_2)
            # p_hid = np.tanh(np.dot(w_1, p_x_2))
            m_w_0 = [[0.25, 0.25, 0.25], [0.25, 0.25, 0.25]]
            m_w_0[i][j] += 0.0001
            m_x_2 = np.insert(np.tanh(np.dot(m_w_0, x_1)), 0, 1.0)
            m_hid = np.dot(w_1, m_x_2)
            # m_hid = np.tanh(np.dot(w_1, m_x_2))
            w_1_ = cam_num(m_hid, p_hid)
            sub_dif.append(w_1_)
            j += 1
        new_dif_1.append(sub_dif)
        i += 1
    print(text1)
    print(new_dif_1)
    print(text2)
    print(new_dif_2)


def cam_num(m_hid, p_hid):
    temp = (2 * 0.0001 * 4)
    return ((1 - p_hid) ** 2 - (1 - m_hid) ** 2) / temp


def cal_d1(d_2, w_1, x_2):
    temp = np.dot(d_2, w_1[1:])
    d_1 = (1 - x_2[1:] * x_2[1:]) * temp
    return d_1


def horiSym(array):
    matrix = []
    i = 0
    count = 0
    while i < 16:
        line = []
        j = 0
        while j < 16:
            line.append(array[count])
            j += 1
            count += 1
        matrix.append(line)
        i += 1
    result = 0
    i = 0
    while i < 16:
        j = 0
        while j < 8:
            result += abs(float(matrix[i][j]) - float(matrix[i][15 - j]))
            j += 1
        i += 1
    return result / 256


def vertiSym(array):
    matrix = []
    i = 0
    count = 0
    while i < 16:
        line = []
        j = 0
        while j < 16:
            line.append(array[count])
            j += 1
            count += 1
        matrix.append(line)
        i += 1
    result = 0
    i = 0
    while i < 16:
        j = 0
        while j < 8:
            result += abs(float(matrix[i][j]) - float(matrix[15 - i][j]))
            j += 1
        i += 1
    return result / 256


def problem2():
    one = []
    notone = []
    xmin = 100
    ymin = 100
    xmax = -100
    ymax = -100
    ori_train_data = []
    test_data = []
    f = open("ZipDigits.train.txt")
    while True:
        line = f.readline()
        if line == "":
            break
        line = str.split(line)
        arr = [float(num) for num in line[:]]
        x = horiSym(arr[1:])
        y = vertiSym(arr[1:])
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
        if arr[0] == 1:
            ori_train_data.append([[x, y], 1])
        else:
            ori_train_data.append([[x, y], -1])
    f.close()
    f = open("ZipDigits.test.txt")
    while True:
        line = f.readline()
        if line == "":
            break
        line = str.split(line)
        arr = [float(num) for num in line[:]]
        x = horiSym(arr[1:])
        y = vertiSym(arr[1:])
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
        if arr[0] == 1:
            test_data.append([[x, y], 1])
        else:
            test_data.append([[x, y], -1])
    f.close()
    test_data = test_data + ori_train_data
    train_data = []
    np.random.seed(0)
    for i in range(300):
        idx = random.randint(0, len(test_data) - 1)
        temp = test_data[idx]
        train_data.append(temp)
        del test_data[idx]
    edgeset = [xmax, xmin, ymax, ymin]
    train_data = normalize(train_data, edgeset)
    test_data = normalize(test_data, edgeset)
    for temp in train_data:
        if temp[1] == 1:
            one.append(temp[0])
        else:
            notone.append(temp[0])

    in_error = []
    vali_error = []
    iteration = []
    ev_min = 1
    iter_min = 0

    # X = [p for [p, y] in train_data]
    # Y = [[y] for [p, y] in train_data]

    early_train = train_data[:250]
    early_vali = train_data[250:300]
    X = [p for [p, y] in early_train]
    Y = [[y] for [p, y] in early_train]
    Xv = [p for [p, y] in early_vali]
    Yv = [[y] for [p, y] in early_vali]

    X = np.array(X)
    Y = np.array(Y)
    Xv = np.array(Xv)
    Yv = np.array(Yv)




    w_1, w_2 = randomgenelize(10)
    i = 1
    while i <= 2000000:
        iteration.append(i)
        # w_1, w_2 = training(X, Y, 0.00001, w_1, w_2)
        lamb = 0.01/len(train_data)
        w_1, w_2 = training(X, Y, lamb/math.sqrt(i), w_1, w_2)
        e = calerr(X, Y, w_1, w_2)
        in_error.append(e)
        ev = calerr(Xv, Yv, w_1, w_2)
        vali_error.append(ev)
        if ev < ev_min:
            ev_min = ev
            iter_min = i
        i += 1
        if (i % 10000 == 0):
            print(i, e)

    print("iter_min:", iter_min)
    print("ev_min: ", ev_min)
    test_X = [p for [p, y] in test_data]
    test_Y = [[y] for [p, y] in test_data]
    test_err = calerr(test_X, test_Y, w_1, w_2)


    X, Y = np.meshgrid(np.linspace(-1, 1, 1000), np.linspace(-1, 1, 1000))
    Z = predictZ(X, Y)
    plotpoints(one, notone)
    plt.contourf(X, Y, Z)
    plt.xlabel("Horizontal")
    plt.ylabel("Vertical")
    plt.title("Decision Boudary")
    plt.show()


    a, = plt.plot(iteration, in_error, 'r.')
    b, = plt.plot(iteration, vali_error, 'b.')
    plt.legend([a, b], ["Ein", "Ev"])
    plt.xlabel("Iteration")
    plt.ylabel("Ein")
    plt.title("Iteration vs Ein")
    plt.show()

    print(test_err)


def normalize(whole, e):
    xptp = float(2) / (e[0] - e[1])
    xshift = float(e[0] + e[1]) / 2
    yptp = float(2) / (e[2] - e[3])
    yshift = float(e[2] + e[3]) / 2

    for i in range(len(whole)):
        whole[i] = [[(whole[i][0][0] - xshift) * xptp, (whole[i][0][1] - yshift) * yptp], whole[i][1]]
    return whole


def plotpoints(one, notone):
    pxone = [x for [x, y] in one]
    pyone = [y for [x, y] in one]
    pxnotone = [x for [x, y] in notone]
    pynotone = [y for [x, y] in notone]
    plt.plot(pxone, pyone, 'b.')
    plt.plot(pxnotone, pynotone, 'rx')
    # plt.show()


def training(X, Y, epsilon, w_1, w_2):
    # Forward
    v_1 = np.insert(X, 0, 1, axis=1).dot(w_1)
    x_1 = np.tanh(v_1)
    v_2 = np.insert(x_1, 0, 1, axis=1).dot(w_2)
    # Back
    d_2 = (v_2 - Y) * 2
    d_1 = (1 - np.power(x_1, 2)) * (d_2.dot(w_2[1:].T))
    dif_1 = np.insert(X, 0, 1, axis=1).T.dot(d_1)
    dif_2 = np.insert(x_1, 0, 1, axis=1).T.dot(d_2)
    w_1 -= dif_1 * epsilon
    w_2 -= dif_2 * epsilon
    return w_1, w_2


def calerr(X, Y, w_1, w_2):
    v_1 = np.insert(X, 0, 1, axis=1).dot(w_1)
    x_1 = np.tanh(v_1)
    v_2 = np.insert(x_1, 0, 1, axis=1).dot(w_2)
    e_norm = linear.norm((np.sign(v_2) - Y), ord=2)
    error = float(e_norm) / len(Y)
    return error


def predictZ(X, Y):
    # Go Office Hour
    # can i mimic svm?
    return np.sign(X + 2 * Y + 2.23)


def randomgenelize(m):
    np.random.seed(1)
    w_1 = np.random.randn(3, m)
    w_2 = np.random.randn(m + 1, 1)
    return w_1, w_2

def problem3():
    x = np.linspace(-1, 1, 1000)
    plt.plot(x, x**3, 'g')
    plt.plot([0]*len(x), x, 'r')
    plt.show()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # problem1()
    # problem2()
    # problem3()

    X, Y = np.meshgrid(np.linspace(-1, 1, 1000), np.linspace(-1, 1, 1000))
    Z = predictZ(X, Y)
    print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
