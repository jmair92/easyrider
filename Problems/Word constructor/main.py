string_1 = input()
string_2 = input()
output = ""
for s_1, s_2 in zip(string_1, string_2):
    output += s_1
    output += s_2
print(output)
