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
    numOp = 0
    for perm in perms_to_consider:
        p = Permutation(perm)
        logger.debug(f"Considering permutation: {[el+1 for el in perm]}. Parity: {p.parity()}, Inversions: {p.inversions()}")
        textOpString += " + ("
        textOpString += f"({sgn_adapted(p)}) *"

        sgn_op = sgn_adapted(p)

        numerator_op = 1
        # generate numerator
        for k, l in zip(ks, perm):
            textOpString += f" Q_{matrix[k][l]}"
            numerator_op *= matrix[k][l]
        # generate denominator
        textOpString += "/"

        denominator_op = 1
        for k in ks:
            textOpString += f" Q_{matrix[k][k]}"
            denominator_op *= matrix[k][k]
        
        textOpString += ")"

        numOp += sgn_op * (numerator_op/denominator_op)
        logger.debug(textOpString)
    logger.debug(f"NumOp: {numOp}")
    return numOp, textOpString

def main():
    ## Read input matrix from text
    initialMatrix = np.loadtxt("inputMatrix.txt", dtype=float) 
    # initialMatrix = np.array([[1,2,1,0.5],
    #                  [0.3,0.6,0.8,1],
    #                  [2,3,1.4,0.8],
    #                  [0,0,1,3]])
    
    m = initialMatrix.shape[0]
    logger.info(f"Initial matrix\n{initialMatrix}")
    logger.info(f"Matrix shape: {initialMatrix.shape}")
    logger.info(f"Matrix size: {m}")
    logger.info("-------------")
    logger.info("-------------")
    initialMatrixSchema = build_n_n_matrix(m)

    ## Generate text formula (just to see it)
    textStr = ""
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrixSchema, i)
        for matrix in matrices:
            _, textOp = gen_diseq_items_of_matrix(matrix)
            textStr += textOp

    ## Perform actual calculation
    numRes = 0
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrix, i)
        for matrix in matrices:
            numOp, _ = gen_diseq_items_of_matrix(matrix)
            numRes += numOp

    ## Print text formula
    logger.info(f"{textStr[3:]} > 1")
    ## And actual result
    logger.info(f"{numOp} > 1")

if __name__ == "__main__":
    main()
