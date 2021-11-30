def main():
    import sys
    from os import urandom
    from time import sleep
    from timeit import default_timer as timer
    from itertools import product
    from secrets import choice
    from hashlib import pbkdf2_hmac

    details = ""
    chars = "0123456789"
    num = 0
    check = 0

    def leave():
        print("Exiting...")
        sleep(1)
        sys.exit()

    while True:
        try:
            pinlength = int(input("PIN length: "))
            if pinlength <= 0:
                print("Please enter a value higher than 0")
            else:
                break
        except ValueError:
            print("Please enter an integer value.")

    print("\nHow often would you like to see check output? (0 = None) (1 = All)")
    print("The less output the faster the program will run.")
    while True:
        try:
            prints = int(input("Response: "))
            if prints <= -1:
                print("Please enter a value higher than -1")
            else:
                break
        except ValueError:
            print("Please enter an integer value.")
    if prints != 0:
        while True:
            details = input("Would you like these checks to contain the current elapsed time [y/n]? ")
            if details == "y" or details == "n":
                break
            else:
                print("Invalid Response.")

    while True:
        showpin = input("Would you like to view the cleartext pin for this session [y/n]? ")
        if showpin == "y" or showpin == "n":
            break
        else:
            print("Invalid Input.")

    if prints == 1:
        print("All checks will be outputted.")
    elif prints == 0:
        print("You will recieve no check output.")
    else:
        print(f"You will see output once every {prints} checks.")
    if details == "y":
        print("These will contain the current elapsed time.")

    print("\nCalculating pin...")

    pin =  ''.join(choice(chars) for _ in range(pinlength))
    if showpin == "y":
        print("Cleartext PIN: "+ str(pin))

    salt = urandom(32)

    pin = pbkdf2_hmac('sha256', str(pin).encode('utf-8'), salt, 100000).hex()

    print("\nPIN for this session: " + str(pin))

    while True:
        a = input("Would you like to start cracking [y/n]? ")
        if a == "y":
            print("Cracking...")
            start = timer()
            for i in product(range(10), repeat=pinlength):
                attempt = ("%s" % ''.join(map(str, i)))
                attempthash = pbkdf2_hmac('sha256', str(attempt).encode('utf-8'), salt, 100000)
                attempthash = attempthash.hex()
                num += 1
                check += 1
                if attempthash == pin:
                    end = timer()
                    print(f"PIN cracked! {attempt} ({attempthash}) [Attempt: {num}]")
                    elapsed = end - start
                    print("Elapsed: " + str(elapsed) + "(s)")
                    a = input("Press enter to exit...")
                    leave()
                else:
                    if check == prints and prints != 0:
                        print(f"Attempted {attempt} ({attempthash}) [Failed]")
                        if details == "y":
                            middle = timer()
                            elapsed = middle - start
                            print("Elapsed: " + str(elapsed) + "(s)")
                        check = 0
        elif a == "n":
            leave()
        else:
            print("Invalid Input.")

if __name__ == '__main__':
    main()