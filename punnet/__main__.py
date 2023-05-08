import os

from . import PunnetSquare
from namedtuple import NamedTuple
from .misc import format


def clearscreen():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


firstTime = True

while (
    firstTime
    or input(f'\nPress {format.reverse}enter{format.reset} to try again. ')
    == ''
):
    clearscreen()
    PunnetSquare.drawPunnetSquare(
        input("Enter mom's genotype: "), input("Enter dad's genotype: ")
    )
    firstTime = False
