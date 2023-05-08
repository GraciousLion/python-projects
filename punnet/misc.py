from namedtuple import NamedTuple


def isValidGenotype(mom, dad):
    return True
    if mom.lower() != dad.lower():
        print(
            "Don't be silly. I can't draw a Punnet square without genotypes of the same genes for both parents. "
        )
        return False
    if mom[::2].lower() != mom[1::2].lower():
        print(
            "Don't be silly. I can't draw a Punnet square without two alleles for each gene. "
        )
        return False
    if not mom.isalpha():
        print(
            "Don't be silly. I can't draw a Punnet square for non-letter characters. "
        )
        return False
    return True


def alternate(*strings):
    return ''.join([''.join(sorted(i)) for i in zip(*strings)])


def isSorted(string):
    return all(
        [
            (sorted((allele1, allele2)) == [allele1, allele2])
            for allele1, allele2 in zip(string[::2], string[1::2])
        ]
    )


def phenotype(genotype, ifDominant='Dominant', ifRecessive='Recessive'):
    translate = {True: ifDominant, False: ifRecessive}
    return tuple([translate[allele.isupper()] for allele in genotype[::2]])


format = NamedTuple(
    starter='\x1b[',
    reset='\x1b[0m',
    bold='\x1b[1m',
    faint='\x1b[2m',
    italic='\x1b[3m',
    underline='\x1b[4m',
    reverse='\x1b[7m',
    strikethrough='\x1b[9m',
)


def form(type, condition):
    return type if condition else ''
