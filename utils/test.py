import random

list = ['fnd17_oxlcxspebq', 'fnd17_shsoutbs', 'fnd28_value_05191q', 'fnd28_value_05301q', 'fnd28_value_05302q',
        'fnd17_pehigh',
        'fnd17_pelow', 'fnd17_priceavg150day', 'fnd17_priceavg200day', 'fnd17_priceavg50day', 'fnd17_pxedra',
        'fnd28_newa3_value_18191a', 'fnd28_value_02300a', 'mdl175_ebitda', 'mdl175_pain']

list2 = [1, 2, 3]


def ts_zscore(A, num=500):
    info = 'ts_zscore(' + A + ',' + str(num) + ')'
    return info


def ts_regresion(A, B, num=500):
    info = 'ts_regresion(' + A + ',' + B + ',' + str(num) + ')'
    return info


if __name__ == '__main__':
    num1 = random.randint(0, len(list) - 1)
    A = ts_zscore(list[num1])
    list2 = list.pop(num1)
    num2 = random.randint(0, len(list) - 1)
    B = ts_zscore(list[num2])
    res = ts_regresion(A, B, 500)
    print(res)
