from itertools import product
from functools import reduce

from .misc import isValidGenotype, alternate, isSorted, phenotype, format, form


def drawPunnetSquare(mom, dad):

    # Validate parameters as genotypes
    if not isValidGenotype(mom, dad):
        return
    numberOfGenes = int(len(mom) / 2)

    # Make a tuple of tuples with the possible alleles for each genotype
    alleles = tuple(
        [
            tupl
            for tupl in zip(mom[::2].upper(), mom[::2].lower())
            for _ in range(2)
        ]
    )

    # Find all possible combinations of alleles
    possibleGenotypes = tuple(
        filter(isSorted, map(''.join, product(*alleles)))
    )
    del alleles

    # Convert 'mom' and 'dad' to tuples of their alleles
    mom = tuple([(mom[i], mom[i + 1]) for i in range(0, len(mom), 2)])
    dad = tuple([(dad[i], dad[i + 1]) for i in range(0, len(dad), 2)])

    # Find the possible combinations of genes each parent could give
    momGives = tuple(map(''.join, product(*mom)))
    dadGives = tuple(map(''.join, product(*dad)))
    del mom, dad

    combinations = list(
        product(dadGives, momGives)
    )   # This produces a flat list, which is good for finding genotype counts, but not for printing in tables

    # Convert elements to strings
    for i in range(len(combinations)):
        combinations[i] = alternate(*combinations[i])

    # Find the number of cells with each genotype
    genotypicRatios = dict(
        zip(possibleGenotypes, map(combinations.count, possibleGenotypes))
    )

    # Find the phenotype of each genotype
    genosPhenos = dict(
        zip(possibleGenotypes, map(phenotype, possibleGenotypes))
    )
    # Find the phenotypic ratios
    phenosGenos = {
        pheno: tuple(
            [geno for geno in genosPhenos if genosPhenos[geno] == pheno]
        )
        for pheno in genosPhenos.values()
    }
    del genosPhenos

    phenotypicRatios = {
        phenotype: reduce(
            lambda prevSum, ele: prevSum + genotypicRatios[ele],
            phenosGenos[phenotype],
            0,
        )
        for phenotype in phenosGenos
    }

    numberOfColumns = int(len(combinations) ** 0.5)

    # Turn combinations from a flat list into a table
    combinations = tuple(
        [
            combinations[i : i + numberOfColumns]
            for i in range(0, len(combinations), numberOfColumns)
        ]
    )

    centeringString = '{:^' + str(numberOfGenes * 2 + 2) + '} '
    rowLine = (
        (' ' * numberOfGenes + ' ')
        + ('-' * numberOfColumns * (numberOfGenes * 2 + 3))
        + '-'
    )

    ### Printing Punnet square ###

    print(
        '\n ' * numberOfGenes
        + '  '
        + ((centeringString) * len(momGives)).format(*momGives)
    )
    print(rowLine)

    for i in range(len(combinations)):
        print(
            dadGives[i],
            '|' + (' {} |' * numberOfColumns).format(*combinations[i]),
        )
        print(rowLine)

    ### Printed Punnet square ###

    # Print genotypic ratio
    print('\nGenotypic ratio:\n')
    print(
        ' : '.join(
            map(
                (
                    lambda tupl: (
                        form(format.faint, tupl[0] == 0)
                        + str(tupl[0])
                        + ' '
                        + tupl[1]
                    )
                    + format.reset
                ),
                zip(genotypicRatios.values(), genotypicRatios.keys()),
            )
        )
    )

    # Print phenotypic ratio
    print('\nPhenotypic ratio:\n')
    print(
        ' : '.join(
            map(
                (
                    lambda tupl: (
                        form(format.faint, tupl[0] == 0)
                        + str(tupl[0])
                        + ' '
                        + ', '.join(tupl[1])
                        + format.reset
                    )
                ),
                zip(phenotypicRatios.values(), phenotypicRatios.keys()),
            )
        )
    )
