#! /usr/bin/python3
import sys

import curses as c
import random as r


def center(twidth, strwidth):
    return twidth // 2 - strwidth // 2

def right(twidth, strwidth):
    return twidth - strwidth


def readcard(card):
    if card[1] in "123456789":
        return int(card[1])
    else:
        return 10

def readdeck(deck):
    output = 0
    for item in deck:
        output += readcard(item)
    return output


def main(fcc=False, money=1000):
    
    stdscr = c.initscr()
    c.noecho()
    bet = 0
    exiting = False
    while True:
        stdscr.clear()
        exiting = False
        stdscr.addstr(0, 0, "Type a number for your bet or type something starting with q to quit.")
        stdscr.addstr(2, 0, "To play:\nh - hit\ns - stand\nq - quit")
        stdscr.addstr(0, c.COLS//2, "Money: " + str(money) + " Bet> ")
        c.echo()
        betstr = stdscr.getstr(4)
        while True:
            try:
                bet = int(betstr)
                bet = abs(bet)
                if bet <= money:
                    money -= bet
                    break
                else:
                    stdscr.move(0, c.COLS//2+(len(str(money)) + 13))
                    stdscr.clrtoeol()
                    betstr = stdscr.getstr(4)


            except ValueError:
                if len(betstr) > 0 and betstr[0] in (b"q"[0], b"Q"[0]):
                    exiting = True
                    break
                else:
                    stdscr.move(0, c.COLS//2+(len(str(money)) + 13))
                    stdscr.clrtoeol()
                    betstr = stdscr.getstr(4)

        if exiting:
            c.endwin()
            return money
            
        c.noecho()
        stdscr.clear()
        
        deck = [
            "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s0", "s0", "s0", "s0",
            "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c0", "c0", "c0", "c0",
            "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d0", "d0", "d0", "d0",
            "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h0", "h0", "h0", "h0"
        ]

        playercards = []
        dealercards = []
        exitcode = 0  # 0 = quit 1 = ai wins 2 = player wins 3 = draw
        turn = 0
        r.shuffle(deck)
        testdeck = ["x7", "x7", "x7"]

        playercards.append(deck.pop())
        playercards.append(deck.pop())
        dealercards.append(deck.pop())
        dealercards.append(deck.pop())


        try:
            while True:
                stdscr.addstr(0, 0, "Your cards: " + " ".join(playercards))
                stdscr.addstr(0, c.COLS//2, "Total: " + str(readdeck(playercards)))
                stdscr.addstr(1, 0, "Dealer cards: " + (" ".join(dealercards) if turn != 0 else dealercards[0] + " ??"))
                stdscr.addstr(1, c.COLS//2, "Total: " + (str(readdeck(dealercards)) if turn != 0 else "??")) 
                stdscr.addstr(c.LINES - 1, 0, "Welcome to bjcurses", c.A_REVERSE)

                #stdscr.addstr(2, 0, "Dealer cards including hidden " + " ".join(dealercards))
                
                
                if turn % 2 == 0:
                    k = stdscr.getch()

                    if k == ord("h"):
                        playercards.append(deck.pop())
                        stdscr.addstr(0, 0, "Your cards: " + " ".join(playercards))
                        stdscr.addstr(0, c.COLS//2, "Total: " + str(readdeck(playercards)))
                        if readdeck(playercards) == 21:
                            exitcode = 2
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("Blackjack!")), "Blackjack!")
                            break
                        elif readdeck(playercards) > 21:
                            exitcode = 1
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("Bust")), "Bust")
                            break
                        
                        elif (readdeck(playercards)) < 21 and (len(playercards) == 5) and (fcc):
                            exitcode = 2
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("5-card charlie.")), "5-card charlie.")
                            break

                    elif k == ord("s"):
                        turn += 1

                    elif k == ord("q"):
                        return money - bet * 0.5

                

                elif turn % 2 == 1:
                    exiting = False


                    dealerchoice = 1
                    while dealerchoice != 0:
                        #if (readdeck(dealercards) < 17 and readdeck(playercards) >= 17) or (readdeck(dealercards) < 12):
                        if readdeck(dealercards) < 17:
                            dealercards.append(deck.pop())

                        else:
                            dealerchoice = 0


                        stdscr.addstr(1, 0, "Dealer cards: " + " ".join(dealercards))
                        stdscr.addstr(1, c.COLS//2, "Total: " + str(readdeck(dealercards)))
     
                        
                        if readdeck(dealercards) == 21: 
                            exitcode = 1
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("Blackjack!")), "Blackjack!")
                            exiting = True
                            break
                        
                        elif readdeck(dealercards) > 21:
                            exitcode = 2
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("Bust")), "Bust")
                            exiting = True
                            break
                        
                        elif readdeck(dealercards) > readdeck(playercards):
                            exitcode = 1
                            exiting = True
                            break

                        
                        
                        
                        


                    
                    if exiting:
                        break
                    
                    else:
                        if readdeck(playercards) == readdeck(dealercards):
                            exitcode = 3
                            stdscr.addstr(c.LINES//2+1, center(c.COLS, len("Push")), "Push")
                            break
                        
                        elif readdeck(playercards) > readdeck(dealercards):
                            exitcode = 2
                            break

                        turn += 1
                
                stdscr.refresh()

        except:
            raise
        finally:
            if exitcode == 0:
                c.endwin()
                break
            elif exitcode == 2:
                stdscr.addstr(c.LINES//2, center(c.COLS, len("You win!")), "You win!", c.A_UNDERLINE | c.A_BOLD)
                money += bet * 2
                bet = 0
            elif exitcode == 1:
                stdscr.addstr(c.LINES//2, center(c.COLS, len("Dealer wins.")), "Dealer wins.", c.A_BOLD)
                bet = 0
            elif exitcode == 3:
                money += bet
                bet = 0
                stdscr.addstr(c.LINES//2, center(c.COLS, len("Draw!")), "Draw!")
    
        if stdscr.getch(c.LINES - 1, len("Welcome to bjcurses")) not in (ord("y"), ord("Y"), 10, 13):
            c.echo()
            c.endwin()
            break
        else:
            continue


if __name__ == "__main__":
    main(sys.argv)
