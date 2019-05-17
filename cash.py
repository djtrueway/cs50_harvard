def main():
#ask user !!!
    while True:
        print("O hai ! How much change is owed?", end="\n")
        n = float(input())
        if n >= 0:
            break
    
    n *= 100

    z = 0
    quarter = 25;

    while n >= 25:
        n -= quarter
        z += 1
    
    dime = 10
    while n >= 10:
        n = n - dime
        z += 1

    nicke = 5 
    while n >= 5:
        n = n - nicke
        z += 1

    penny = 1
    while n >= 1:
        n = n - penny
        z += 1

    print(z)


if __name__ =="__main__":
    main()