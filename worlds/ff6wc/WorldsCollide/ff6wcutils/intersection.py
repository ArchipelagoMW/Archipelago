# find the intersection of two lists
# ref: https://www.geeksforgeeks.org/python-intersection-two-lists/#
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3