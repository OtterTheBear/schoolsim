#! /usr/bin/python3
import sys

def checkAnswer(x, y, op, answer):
    if op in ("a", "add"):
        if answer == x + y:
            return True
        else:
            return False

    elif op in ("s", "sub"):
        if answer == x - y:
            return True
        else:
            return False

    elif op in ("m", "mul"):
        if answer == x * y:
            return True
        else:
            return False

    elif op in ("d", "div"):
        if answer == x / y:
            return True
        else:
            return False

def main(difficulty=1000, numtimes=11):
    import random as r
    import decimal as d
    import readline
    d.getcontext().prec = 4
    d.getcontext().rounding = d.ROUND_FLOOR
    score = 0


    difficulty = 1000
    counter = 0

    print("Welcome to somemathqs.")

    try:
        difficulty = float(input("Pick the maximum number in equations or press enter for 1000."))
    except:
        pass

    ptval = difficulty / 1000

    print("Type \"sm\" or \"q\" at any time to switch mode and quit respectively.\n")
    print("IMPORTANT NOTE: Please use 4 significant digits (including trailing 0's before decimal points) in questions where the proper result is longer.\n")
    mode = "sm"
    #mode = input("""Pick a mode:
    """        a) Addition
            s) Subtraction
            m) Multiplication
            d) Division
            l) Show score
            q) Quit
    """
    prevmode = "sm"
    while True:
        x = d.Decimal(r.randint(1, difficulty))
        y = d.Decimal(r.randint(1, difficulty))
        if mode in ("a", "s", "m", "d"): 
            if mode == "a":
                op = "+"
            elif mode == "s":
                op = "-"
            elif mode == "m":
                op = "times"
            elif mode == "d":
                op = "divided by"
            answer = input(f"What is {x} {op} {y}?")
            try:
                answer = d.Decimal(answer)
                if checkAnswer(x, y, mode, answer):
                    print("Correct!")
                    score += ptval
                else:
                    print("Nope")


            except:
                if answer == "q":
                    break
                elif answer == "sm":
                    mode = "sm"
                    continue
                elif answer == "l":
                    mode = "l"
                    continue
                elif answer == "sd":
                    mode = "sd"
                    continue
        elif mode == "sm":
            mode = input("""Pick a mode:
                a) Addition
                s) Subtraction
                m) Multiplication
                d) Division
                l) Show scores
               sd) Switch difficulty
                q) Quit
    """)
        elif mode == "l":
            print(f"Your score: {score}")
            mode = (prevmode if prevmode != "l" else "sm")

        elif mode == "sd":
            try:
                difficulty = float(input("Pick the maximum number in equations."))
                ptval = difficulty / 1000
            except KeyboardInterrupt:
                raise
            finally:
                mode = prevmode if prevmode != mode else "sm"


        elif mode == "q":
            break
        else:
            print("I have no idea what that means.")
            mode = "sm"
        prevmode = mode
        counter += 1
        if __name__ != "__main__":
            if counter == numtimes:
                return score


if __name__ == "__main__":
    main(sys.argv)


