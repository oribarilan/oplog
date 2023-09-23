import time

import click

from oplog import Operation


def modulo(dividend, divisor):
    with Operation(name='modulo').progressable(iterations=dividend) as op:
        if divisor == 0:
            raise ZeroDivisionError()

        remainder = dividend
        while remainder >= divisor:
            time.sleep(remainder/divisor * 0.1)
            op.progress()
            remainder -= divisor

        return remainder


def is_prime(num):
    with Operation(name='is_prime').progressable(iterations=num) as op:
        if num <= 1:
            return False

        for i in range(2, num):
            time.sleep(0.1)
            op.progress()
            if modulo(num, i) == 0:
                return False

        return True


@click.command()
@click.argument('n', default=10, type=int)
def find_nth_prime(n: int) -> None:
    with Operation(name='find_prime').progressable(iterations=n) as op:
        prime_count = 0
        candidate = 1
        while prime_count < n:
            candidate += 1
            if is_prime(candidate):
                prime_count += 1
                op.progress()
    click.echo(f'Prime #{n} found: {candidate}')


if __name__ == '__main__':
    find_nth_prime()
