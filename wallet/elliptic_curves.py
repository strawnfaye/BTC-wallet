# A library implenting Finite Fields and Elliptic Curves to calculate wallet addresses.
from io import BytesIO
from random import randint
from unittest import TestCase

from helper import double_sha256, encode_base58, hash160

class FieldElement:

    def __init__(self, num, prime):
        self.num = num
        self.prime = prime
        if self.num >= self.prime or self.num < 0:
            error = 'Num {} not in field range 0 to {}'.format(
                self.num, self.prime-1)
            raise RuntimeError(error)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        if other is None:
            return True
        return self.num != other.num or self.prime != other.prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)
    
    # Takes two elements of a finite field, adds their values and modulo by their field's prime.
    def __add__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')
        fsum = (self.num + other.num) % self.prime
        return self.__class__(fsum, self.prime)

    # Takes two elements of a finite field, subtracts the second element from the first, and
    # modulo by their field's prime.
    def __sub__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')
        fdiff = (self.num - other.num) % self.prime
        return self.__class__(fdiff, self.prime)

    # Takes two elements of a finite field, multiplies them together and modulo by the field's prime. 
    def __mul__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')
        fproduct = (self.num * other.num) % self.prime
        return self.__class__(fproduct, self.prime)
    
    # Takes an element of a finite field and an exponent, uses Fermat's Little Theorem to
    # take the element to the nth power and modulo by the field's prime.
    def __pow__(self, n):
        fpower = pow(self.num, n % (self.prime - 1), self.prime)
        return self.__class__(fpower, self.prime)

    # Takes two elements of a finite field, uses Fermat's Little Theorem to multiply the first by the reciprocal
    # of the second to calculate the quotient.
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')
        fquo = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(fquo, self.prime)