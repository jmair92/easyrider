def range_sum(numbers, start, end):
    nums = numbers.split(" ")
    _sum = 0
    for n in nums:
        if start <= int(n) <= end:
            _sum += int(n)
    return _sum


input_numbers = input()
_range = input().split()
a = int(_range[0])
b = int(_range[1])
print(range_sum(input_numbers, a, b))
