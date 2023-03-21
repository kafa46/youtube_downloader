import math

def round_size(size: float, digit:int = 2):
    '''소수점 2째 자리에서 반올림 3.14 -> 3.1'''
    return round(size, digit)