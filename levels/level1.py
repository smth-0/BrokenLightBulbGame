str1 = """
""".split('\n')
str2 = """"""
for i in str1:
    for j in i:
        str2 += '.' if j == '.' else '#'
    str2 += '\n'
print(str2)