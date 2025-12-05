def is_full(stack, top):
    return top + 1 == len(stack)

def is_empty(top):
    return top == -1

def push(stack, top, x):
    if not is_full(stack, top):
        top += 1
        stack[top] = x
    else:
        print("Stack is Full")
    return top

def pop(stack, top):
    if is_empty(top):
        print("Stack is Empty")
        return -9999, top
    else:
        x = stack[top]
        top -= 1
        return x, top

def print_stack(stack, top):
    print("[", end=" ")
    if not is_empty(top):
        for i in range(top + 1):
            if(i != top):
                print(stack[i], end=", ")
            else:
                print(stack[i], end=" ")
    print("]")

def main():
    size = int(input("Enter size of the stack: "))
    stack = [-1] * size
    top = -1
    print("----MENU----")
    print("1 -> Push")
    print("2 -> Pop")
    print("3 -> View")
    print("4 -> Exit")
    print("------------")
    while True:
        ch = int(input("Enter your choice: "))
        done = False
        match ch:
            case 1: 
                num = int(input("Enter number: "))
                top = push(stack, top, num) 
            case 2: 
                val, top = pop(stack, top) 
                if val != -9999:
                    print(f"Popped: {val}")
            case 3: 
                print_stack(stack, top)
            case 4: 
                done = True
        if done:
            break
        print("Exiting...")


main()