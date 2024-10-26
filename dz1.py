import os

def fork():
        n = input()
        if n.isdigit():
            p = os.fork()
            if p == 0:
                fork()
            else:
                os.waitpid(p, 0)
                print(n)
fork()
