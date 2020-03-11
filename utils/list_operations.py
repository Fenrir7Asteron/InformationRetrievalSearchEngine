"""
All lists are supposed to store increasing sequences of integers
"""


def merge_lists(a: list, b: list):
    i = 0
    j = 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif b[j] < a[i]:
            res.append(b[j])
            j += 1
        else:
            i += 1
            j += 1
    while i < len(a):
        res.append(a[i])
        i += 1
    while j < len(b):
        res.append(b[j])
        j += 1
