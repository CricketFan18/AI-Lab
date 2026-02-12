class Stack:
    def __init__(self,size=5):
        self.stack = [-1] * size
        self.size = size
        self.top = -1
        
    def is_full(self):
        return self.top + 1 == self.size

    def is_empty(self):
        return self.top == -1

    def push(self,x):
        if not self.is_full():
            self.top += 1
            self.stack[self.top] = x
        else:
            print("Stack is Full")

    def pop(self):
        if self.is_empty():
            print("Stack is Empty")
            return -9999
        else:
            x = self.stack[self.top]
            self.top -= 1
            return x

    def print_stack(self):
        print("[", end=" ")
        if not self.is_empty():
            for i in range(self.top + 1):
                if(i != self.top):
                    print(self.stack[i], end=", ")
                else:
                    print(self.stack[i], end=" ")
        print("]")

def main():
    size = int(input("Enter size of the stack: "))
    my_stack = Stack(size)
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
                my_stack.push(num)
            case 2: 
                val = my_stack.pop() 
                if val != -9999:
                    print(f"Popped: {val}")
            case 3: 
                my_stack.print_stack()
            case 4: 
                done = True
        if done:
            break
    print("Exiting...")
        
main()