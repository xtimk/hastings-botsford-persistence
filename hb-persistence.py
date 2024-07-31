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
    return np.array(matrix, dtype=np.float64)

def build_zero_matrix_schema(matrix: np.array):
    size = matrix.shape[0]
    zero_matrix = np.full((size, size), 1, dtype=int)
    for x in range(0, size):
        for y in range(0, size):
            if (matrix[x][y] == 0):
                zero_matrix[x][y] = 0
    
    logger.debug(zero_matrix)
    return zero_matrix


## Returns a couple (num, text)
##  - num contains the actual calculation
##  - text contains the generic formula
def gen_diseq_items_of_matrix(matrix, zeroMatrixSchema, actualCalc = False):
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
    textOpStringF = ""
    numOp = 0
    for perm in perms_to_consider:
        skipElement = False
        skipSinceDenominatorIsZero = False
        p = Permutation(perm)
        logger.debug(f"Considering permutation: {[el+1 for el in perm]}. Parity: {p.parity()}, Inversions: {p.inversions()}")
        textOpString = ""
        textOpString += " + ("
        textOpString += f"({sgn_adapted(p)}) *"

        sgn_op = sgn_adapted(p)

        numerator_op = 1
        # generate numerator
        for k, l in zip(ks, perm):
            if (zeroMatrixSchema[k][l] == 0):
                skipElement = True
            textOpString += f" Q_{k+1}{l+1}"
            numerator_op *= matrix[k][l]
        
        # generate denominator
        textOpString += "/"

        denominator_op = 1
        for k in ks:
            if (k == 0):
                skipSinceDenominatorIsZero = True
            textOpString += f" Q_{k+1}{k+1}"
            denominator_op *= (1 - matrix[k][k])
                
        if (actualCalc):
            if(numerator_op != 0 and denominator_op != 0):
                logger.debug(f"Numerator/Denominator: {numerator_op} / {denominator_op}")
                logger.debug(numerator_op/denominator_op)

        textOpString += ")"
        ## Denominator is 0 for Q_11. So in this case just skip it
        if (denominator_op != 0):
            numOp += sgn_op * (numerator_op/denominator_op)
        if (actualCalc):
            if(numerator_op != 0 and denominator_op != 0):
                logger.debug(f"NumOp: {numOp}")

        logger.debug(textOpString)

        if (not skipElement):
            textOpStringF += textOpString
        
    logger.debug(f"NumOp: {numOp}")
    return numOp, textOpStringF

def main():
    ## Read input matrix from text
    initialMatrix = np.loadtxt("inputMatrix.txt", dtype=np.float64)
    # initialMatrix = build_n_n_matrix(4)
    # initialMatrix = np.array([[1,2,1,0.5],
    #                  [0.3,0.6,0.8,1],
    #                  [2,3,1.4,0.8],
    #                  [0,0,1,3]])
    
    m = initialMatrix.shape[0]
    logger.info(f"Initial matrix\n{initialMatrix}")
    logger.info(f"Matrix shape: {initialMatrix.shape}")
    logger.info(f"Matrix size: {m}")
    initialMatrixSchema = build_n_n_matrix(m)
    zeroMatrixSchema = build_zero_matrix_schema(initialMatrix)
    zeroMatrixSchemaFull = build_zero_matrix_schema(initialMatrixSchema)   

    ## Generate text formula (just to see it).
    ## Perform this on the matrixSchema (a matrix built with fake elements, named with indexes)
    ## Example of matrixSchema
    ## 11 12 13
    ## 21 22 23
    ## 31 32 33
    textStr = ""
    logger.info("Calculating disequations...")
    logger.info("Calculating full text formula...")
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrixSchema, i)
        for matrix in matrices:
            _, textOp = gen_diseq_items_of_matrix(matrix, zeroMatrixSchema)
            textStr += textOp


    logger.info("Calculating simplified text formula, considering presence of zeros in the input matrix...")
    textStrFull = ""
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrixSchema, i)
        for matrix in matrices:
            _, textOp = gen_diseq_items_of_matrix(matrix, zeroMatrixSchemaFull)
            textStrFull += textOp

    ## Perform actual calculation on the real matrix
    logger.info("Calculating actual result...")
    numRes = 0
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrix, i)
        for matrix in matrices:
            numOp, _ = gen_diseq_items_of_matrix(matrix, zeroMatrixSchema, actualCalc=True)
            numRes += numOp
            # logger.info(f"HEREEE: {numOp}")
            # logger.info(f"NUMRES: {numRes}")

    ## Log text formula
    logger.info(f"Generic Full Disequation: {textStrFull[3:]} > 1")
    
    logger.info(f"Generic Disequation also considering presence of zeros: {textStr[3:]} > 1")

    ## and actual result
    logger.info(f"Actual Disequation: {numRes} > 1")
    logger.info("All done")


if __name__ == "__main__":
    main()
