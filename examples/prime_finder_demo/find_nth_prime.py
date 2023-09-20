import time

import click

from oplog import Operation


def is_prime(num):
    with Operation(name='is_prime').progressive(total=num) as op:
        if num <= 1:
            return False

        for i in range(2, num):
            time.sleep(0.1)
            op.progress()
            if num % i == 0:
                return False

        return True


@click.command()
@click.argument('idx', default=10, type=int)
def find_prime(idx: int) -> None:
    with Operation(name='find_prime').progressive(total=idx) as op:
        prime_count = 0
        candidate = 1
        while prime_count < idx:
            candidate += 1
            if is_prime(candidate):
                prime_count += 1
                op.progress()
    click.echo(f'Prime #{idx} found: {candidate}')


if __name__ == '__main__':
    find_prime()
