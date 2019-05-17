def main():
    while True:
        i = int(input("height of wall: "))
        if i > 0 and i <= 23:
            break 

# print out this many rows
    for s in range(i):
        
        for a in range(i):
            if s + 1 + a < i:
                print(" ", end="")
            else:
                print("#", end="")
        print()
if __name__== "__main__":
    main()