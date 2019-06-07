# Based on https://github.com/aquaticus/nexus433
clock = 80000000.0
usec = 1000000.0

FACTOR_USEC = clock / usec
# Empirically determined
STARTL = 500  * FACTOR_USEC
STARTH = 750  * FACTOR_USEC
START  = (STARTL + STARTH) / 2
ONEL   = 1500 * FACTOR_USEC
ONEH   = 2000 * FACTOR_USEC
ONE  = (ONEL + ONEH) / 2
ZEROL  = 500  * FACTOR_USEC
ZEROH  = 1000 * FACTOR_USEC
ZERO  = (ZEROL + ZEROH) / 2
MID   = ZERO + (ONE-ZERO)/2

def diff(a, b):
    return abs(a - b)


def display_bits(bits, text, l, r, f=lambda x: x):
    h = bits[l:] if r == 0 else bits[l:r]
    val = f(int(''.join(h), 2))
    print "{:<9} {:>12} {:>2} {:>4}".format(text, ''.join(h), len(h), val)
    return val


def humidity(bits):
    return display_bits(bits, "Humidity:", -8, 0)


def fixed(bits):
    return display_bits(bits, "Fixed:", -12, -8)


def batt(bits):
    return display_bits(bits, "Battery:", -28, -27)


def temperature(bits):
    return display_bits(bits, "Temp:", -24, -12, lambda x: x / 10.0)


def chan(bits):
    return display_bits(bits, "Chan:", -26, -24, lambda x: x + 1)


def zero(bits):
    return display_bits(bits, "Zero:", -27, -26)


def did(bits):
    return display_bits(bits, "Id:", -36, -28)


def dump_times(times):
    for i, t in enumerate(times):
        print "{}={:.0f}".format(i, cycle_to_usec(t)),
    print ""


def decode_times(times):
    bits = []
    zeros = 0
    ones  = 0

    for i, t in enumerate(times):
        if i % 2 == 0:
            if STARTL  < t < STARTH:
                pass
            else:
                print ("Unexpected start pulse timing: "
                       "{} {:4.0f} usec {}").format(
                           t, cycle_to_usec(t), diff(t, START))
                return
        else:
            if   ONEL  < t < ONEH:
                bits.append('1')
                ones += 1
            elif ZEROL < t < ZEROH:
                bits.append('0')
                zeros += 1
            else:
                print ("Unexpected one/zero timing: "
                       "{} {} {:4.0f} usec Z={} O={} S={}").format(
                           i, t, cycle_to_usec(t),
                           diff(t, ZERO), diff(t, ONE), diff(t, START))
                dump_times(times)
                return
    print "Decoded: {} len: {} 1's: {} 0's: {}".format(
        ''.join(bits), len(bits), ones, zeros)

    # Seems my device uses 37 instead of 36 bits and last one is used
    # for parity (DIGOO DG-R8H)
    if zeros % 2 != 0:
        print "Bad parity!"

    return bits


def cycle_to_usec(cycles):
    return (cycles / clock) * usec


def decode(times):
    val = decode_times(times)
    if val is not None:
        v = val[:-1]
        did(v)
        batt(v)
        zero(v)
        chan(v)
        temperature(v)
        fixed(v)
        humidity(v)
        print ""


def detect_times(times, f=lambda x: True, ti=0):
    starts = [x for i, x in enumerate(times) if (i % 2 == ti) and f(x)]
    avg  = sum(starts) / len(starts)
    minx = min(starts)
    maxx = max(starts)
    print ("Avg: {:>6}, min: {:>6}, max: {:>6}, avg: "
           "{:>5.0f} usec, min: {:>5.0f} usec, max: {:>5.0f} usec").format(
               avg, minx, maxx,
               cycle_to_usec(avg), cycle_to_usec(minx), cycle_to_usec(maxx))


def analyse(times):
    print "Start :",
    detect_times(times)
    print "Ones  :",
    detect_times(times, lambda x: x > MID, 1)
    print "Zeros :",
    detect_times(times, lambda x: x < MID, 1)

if __name__ == '__main__':
    # print ZERO, ONE, START, TOLERANCE
    with open('timings') as t:
        for line in t.readlines():
            times = [int(x) for x in line.split()]
            pause = times[0]
            print "Long pause: {} {:4.0f} usec".format(
                pause, cycle_to_usec(pause))
            pulse = times[1:]
            analyse(pulse)
            decode(pulse)
            print
