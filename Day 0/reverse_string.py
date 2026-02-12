s = input("Enter a string: ")
stack = []
for ch in s:
    stack.append(ch)
rev = ""
for i in range(len(stack)):
    rev += stack.pop()
print(f"Reverse : {rev}")