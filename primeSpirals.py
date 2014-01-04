#!/usr/bin/env python2
'''
Just a Game of Primes - I coded the Ulam Prime Spiral,
and blogged about it here:

    http://users.softlab.ntua.gr/~ttsiod/primes.html

'''
import sys
import math
import itertools


def primeSpiralPixels():
    yield 255  # 1 is not prime (white)
    yield 0    # 2 is prime     (black)
    primesSoFar = [2]
    for candidate in itertools.count(3):
        for prime in (
                p for p in primesSoFar if p <= int(math.sqrt(candidate))):
            if 0 == candidate % prime:
                yield 255  # non-prime: white
                break
        else:
            primesSoFar.append(candidate)
            yield 0  # prime: black


def main():
    screen = {}
    rows = 202 if len(sys.argv) == 1 else int(sys.argv[1])
    moves = itertools.cycle([(1, 0), (0, -1), (-1,  0), (0, 1)])
    check = moves.next()
    move, check = check, moves.next()
    lastPosition = [int(rows / 2), int(rows / 2)]
    pixelsDone = 0
    oldPct = 0
    print "Generating picture...     ",
    for c in itertools.islice(primeSpiralPixels(), rows * rows):
        screen[lastPosition[0], lastPosition[1]] = c
        lastPosition[0] += move[0]
        lastPosition[1] += move[1]
        checkPosition = (
            lastPosition[0] + check[0],
            lastPosition[1] + check[1])
        if checkPosition not in screen:
            move, check = check, moves.next()
        pixelsDone += 1
        newPct = 100 * pixelsDone / (rows * rows)
        if newPct != oldPct:
            sys.stdout.write("\b\b\b\b%3d%%" % newPct)
            sys.stdout.flush()
            oldPct = newPct
    image = open("ulam.pgm", "w")
    image.write("P5\n" + str(rows - 1) + " " + str(rows - 1) + "\n255\n")
    for row in xrange(1, rows):
        for col in xrange(1, rows):
            image.write(chr(screen[col, row]))
    print "\nDone! Now go open 'ulam.pgm' with your picture viewer " + \
        "(e.g. feh, gqview, etc)..."


if __name__ == "__main__":
    main()
