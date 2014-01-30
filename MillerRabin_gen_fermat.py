# Copyright (c) 2013 the authors listed at the following URL, and/or
# the authors of referenced articles or incorporated external code:
# http://en.literateprograms.org/Miller-Rabin_primality_test_(Python)?action=history&offset=20110413052045
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Retrieved from: http://en.literateprograms.org/Miller-Rabin_primality_test_(Python)?oldid=17104

import random, sys

def pow_mod(x, y, z):
    "Calculate (x ** y) % z efficiently."
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

def if_fermat(n):
    return pow_mod(2, n-1, n) == 1

def miller_rabin_pass(a, s, d, n):
    #a_to_power = pow(a, d, n)
    a_to_power = pow_mod(a,d,n)
    if a_to_power == 1:
        return True
    for i in xrange(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1


def miller_rabin(n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1
	
    for repeat in xrange(20):#20 times test
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, s, d, n):
            return False
    return True

def if_divide_3(n):#quick divisibility test on 3
    sum_ = sum(int(i) for i in str(n))
    if sum_%3==0:
        return True
    else:
        return False

def if_divide_5(n):
    return n%10==5

def if_divide_7(n):
    return n%7==0#TODO speed up by checking the digits

if __name__ == "__main__":
    if sys.argv[1] == "test":
        n = long(sys.argv[2])
        print (miller_rabin(n) and "PRIME" or "COMPOSITE")
	print (if_fermat(n) and "PRIME" or "COMPOSITE")
    elif sys.argv[1] == "genprime":
        nbits = int(sys.argv[2])
        while True:
            p = random.getrandbits(nbits)
            p |= 2**nbits | 1
            if not (if_divide_3(p) or if_divide_5(p) or if_divide_7(p)):
		if if_fermat(p):#weak test on if a Fermat prime number
                    if miller_rabin(p):#strong test on if a Miller Rabin prime number
                        print p
                    break
