def matches(open,close) -> bool:
    s1 = "({["
    s2 = ")}]"
    return s1.find(open) == s2.find(close)

s = input("Enter string: ")
myStack = []
flag = True
for ch in s:
    if("({[".find(ch) != -1):
        myStack.append(ch)
    if(")}]".find(ch) != -1):
        if len(myStack) != 0:
            open = myStack.pop()
            if(not matches(open,ch)):
                flag = False
        else:
            flag = False
    if(not flag):
        break
if len(myStack) != 0:
    flag = False
print("Valid" if flag else "Not Valid")