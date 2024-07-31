from sympy.combinatorics.permutations import Permutation
from itertools import permutations
from itertools import combinations
import numpy as np
import sys

import logging
logger = logging.getLogger(__name__)

## Use logging.DEBUG to debug program
level = logging.INFO
# level = logging.DEBUG

loggingFormat = '[%(levelname)s] %(asctime)s: %(message)s'
logging.basicConfig(filename='hb-pers.log', level=level, format=loggingFormat)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(level=level)
formatter = logging.Formatter(loggingFormat)
handler.setFormatter(formatter)
logger.addHandler(handler)

def getSquareSubmatrices(matrix, size):
    matrices = []
    matrixDim = matrix.shape[0]
    combs = list(combinations(range(0,matrixDim), size))
    for c in combs:
        logger.debug(f"Submatrix for comb {[el+1 for el in c]}")
        logger.debug(matrix[np.ix_(c,c)])
        matrices.append(matrix[np.ix_(c,c)])
    return matrices

def sgn_perm(permutation: Permutation):
    if(permutation.parity() == 0):
        return 1
    else:
        return -1

def sgn_adapted(permutation: Permutation):
    if(permutation.length() % 2 == 0):
        return -sgn_perm(permutation)
    else:
        return sgn_perm(permutation)


def count_unchanged_index_in_perm(perm):
    unchanged = 0
    for idx, el in enumerate(perm):
        if(idx == el):
            unchanged += 1
    return unchanged

def build_n_n_matrix(n):
    nrows = n
    ncols = n
    matrix = np.random.randint(2, size=(n,n))
    for x in range(0, nrows):
        for y in range(0, ncols):
            matrix[x][y] = f"{x+1}{y+1}"
    return matrix


def gen_diseq_items_of_matrix(matrix):
    logger.debug("Working on matrix")
    logger.debug(matrix)
    logger.debug("-------------\n")
    matrixSize = matrix.shape[0]
    perms = list(permutations(range(0,matrixSize)))
    ks = range(0,matrixSize)

    logger.debug(f"Total permutations: {len(perms)}")
    logger.debug(f"Excluding permutations that leave 1 or more element unchanged")
    logger.debug(f"I.E. Include all permutations with at least (matrixSize - 1) inversions")

    perms_to_consider = []
    for perm in perms:
        if(count_unchanged_index_in_perm(perm) == 0):
            perms_to_consider.append(perm)

    logger.debug(f"Total permutations to consider: {len(perms_to_consider)}")
    for x in perms_to_consider:
        p = Permutation(x)
        logger.debug(f"{[el+1 for el in x]} - Parity: {p.parity()} | Inversions: {p.inversions()}")
    textOpString = ""
    for perm in perms_to_consider:
        p = Permutation(perm)
        logger.debug(f"Considering permutation: {[el+1 for el in perm]}. Parity: {p.parity()}, Inversions: {p.inversions()}")
        textOpString += f" + (({sgn_adapted(p)}) *"
        for k, l in zip(ks, perm):
            textOpString += f" {matrix[k][l]}"
        textOpString += ")"
        logger.debug(textOpString)
    return textOpString

def main():
    initialMatrix = build_n_n_matrix(3)
    logger.info(f"Initial matrix\n{initialMatrix}")
    logger.info("-------------")
    logger.info(f"Matrix shape: {initialMatrix.shape}")
    m = initialMatrix.shape[0]
    logger.info(f"Matrix size: {m}")
    logger.info("-------------\n\n")

    textStr = ""
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrix, i)
        for matrix in matrices:
            textStr += f"{gen_diseq_items_of_matrix(matrix)}"
            # logger.info(textStr)
    
    logger.info(textStr)

if __name__ == "__main__":
    main()
