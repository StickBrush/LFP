from math import pow, sin, log, asin, pi

def functions():
    declared_y = [100, 33, 50, 66]
    for y in declared_y:
        def fi(delta_t: int, t:int) -> float:
            if type(delta_t) != int:
                delta_t = int(delta_t)
            if type(t) != int:
                t = int(t)
            try:
                if delta_t > t:
                    slope = y/(delta_t-1)
                    return (slope*t)/100
                else:
                    return 1
            except ZeroDivisionError:
                return 1
        yield fi

def constants():
    const_vals = [0, 0.3, 0.5, 0.75]
    for y in const_vals:
        def fi(delta_t: int, t: int) -> float:
            if type(delta_t) != int:
                delta_t = int(delta_t)
            if type(t) != int:
                t = int(t)
            if delta_t > t:
                return y
            else:
                return 1
        yield fi


def marco_functions_a():
    declared_pairs = [(576, 40), (576, 33), (576, 29),
                      (576, 27), (576, 26), (576, 24),
                      (96, 50), (144, 34), (192, 3), 
                      (240, 26), (288, 23), (336, 21)]
    for delta_t, y in declared_pairs:
        def fi(t: int) -> float:
            if type(t) != int:
                t = int(t)
            try:
                if delta_t > t:
                    slope = y/(delta_t-1)
                    return (slope*t)/100, delta_t
                else:
                    return 1, delta_t
            except ZeroDivisionError:
                return 1, delta_t
        yield fi


def marco_functions_b():
    declared_ternaries = [(96, 0.395, 0.405), (144, 0.275, 0.285),
                          (192, 0.215, 0.225), (240, 0.185, 0.195), 
                          (288, 0.165, 0.175)]
    for delta_t, y0, y in declared_ternaries:
        def fi(t: int) -> float:
            if type(t) != int:
                t = int(t)
            try:
                if delta_t > t:
                    slope = y/(delta_t-1)
                    val = (slope*t) + y0
                    if val <= 1:
                        return val, delta_t
                    else:
                        return 1, delta_t
                else:
                    return 1, delta_t
            except ZeroDivisionError:
                return 1, delta_t
        yield fi


def marco_constants():
    const_tuples = [(96, 0.4), (144, 0.28), (192, 0.22),
                    (240, 0.19), (288, 0.17)]
    for delta_t, y in const_tuples:
        def fi(t: int) -> float:
            if type(t) != int:
                t = int(t)
            if delta_t > t:
                return y, delta_t
            else:
                return 1, delta_t
        yield fi

def abs_fun_(delta_t, lambd, y, t):
    if type(t) != int:
        t = int(t)
    if delta_t > t:
        slope = 2*lambd/(delta_t-1)
        val = (slope*t)+y-lambd
        return val, delta_t
    else:
        return 1, delta_t

def marco_group_1():
    const_tuples = [(96, 0.4, 0.01), (144, 0.28, 0.01), (192, 0.22, 0.01), (240, 0.19, 0.01), (288, 0.17, 0.01)]
    for delta_t, y, lambd in const_tuples:
        def fi(t: int) -> float:
            return abs_fun_(delta_t, lambd, y, t)
        yield fi

def marco_group_2():
    const_tuples = [(960, 0.4, 0.001), (1440, 0.28, 0.001),
                    (1920, 0.22, 0.001), (2400, 0.19, 0.001), (2880, 0.17, 0.001)]
    for delta_t, y, lambd in const_tuples:
        def fi(t: int) -> float:
            return abs_fun_(delta_t, lambd, y, t)
        yield fi


def marco_group_3():
    const_tuples = [(480, 0.2, 0.4), (720, 0.15, 0.3),
                    (960, 0.12, 0.24), (1200, 0.1, 0.2), (1440, 0.085, 0.17)]
    for delta_t, y, lambd in const_tuples:
        def fi(t: int) -> float:
            return abs_fun_(delta_t, lambd, y, t)
        yield fi

def marco_group_4():
    const_tuples = [(288, 0.25, 0), (576, 0.16, 0),
                    (864, 0.13, 0), (1152, 0.11, 0), (1440, 0.09, 0)]
    for delta_t, y, lambd in const_tuples:
        def fi(t: int) -> float:
            return abs_fun_(delta_t, lambd, y, t)
        yield fi
