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

## Here set max decimals when performing all multiplications/divisions
round_decimals = 8

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
def gen_diseq_items_of_matrix(matrix, actualCalc = False):
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
        p = Permutation(perm)
        logger.debug(f"Considering permutation: {[el+1 for el in perm]}. Parity: {p.parity()}, Inversions: {p.inversions()}")
        textOpString = ""
        textOpString += " + ("
        if (sgn_adapted(p) == 1):
            textOpString += f""
        else:
            textOpString += f"-"

        sgn_op = sgn_adapted(p)

        numerator_op = 1
        # generate numerator
        for k, l in zip(ks, perm):
            if (matrix[k][l] == 0):
                skipElement = True
            textOpString += f" Q_{k+1}{l+1}"
            numerator_op = round(numerator_op * matrix[k][l], round_decimals)
        
        # generate denominator
        textOpString += "/"

        denominator_op = 1
        for k in ks:
            textOpString += f"(1 - Q_{k+1}{k+1})"
            denominator_op = round(denominator_op * (1 - matrix[k][k]), round_decimals)
                
        if (actualCalc):
            if(numerator_op != 0 and denominator_op != 0):
                logger.debug(f"Numerator/Denominator: {numerator_op} / {denominator_op}")
                logger.debug(numerator_op/denominator_op)

        textOpString += ")"
        ## Denominator can be 0 if at least one elem in diagonal is 0. Since this can happen, I need to handle this
        if (denominator_op != 0):
            numOp += sgn_op * round(numerator_op/denominator_op, round_decimals)
        if (actualCalc):
            if(numerator_op != 0 and denominator_op != 0):
                logger.debug(f"NumOp: {numOp}")

        logger.debug(textOpString)

        if (not skipElement):
            textOpStringF += textOpString
        else:
            logger.debug(f"Will skip {textOpString}")
        
    logger.debug(f"NumOp: {numOp}")
    if(textOpStringF != ""):
        textOpStringF = "\n" + textOpStringF
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

    textStrFull = ""
    logger.info("Calculating disequations...")
    
    # Step 1: Get full text formula. To do this I use a fake NxN matrix populated with values different from 0
    logger.info("Calculating full text formula...")
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrixSchema, i)
        for matrix in matrices:
            _, textOp = gen_diseq_items_of_matrix(matrix)
            textStrFull += textOp

    # Step 2: Get simplified text formula. This formula is obtained by removing operands with zeros.
    # So I launch this with the real matrix
    logger.info("Calculating simplified text formula, considering presence of zeros in the input matrix...")
    textStr = ""
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrix, i)
        for matrix in matrices:
            _, textOp = gen_diseq_items_of_matrix(matrix)
            textStr += textOp

    ## Step 3: Perform actual calculation on the real matrix
    ## BTW this has been already calculated at step 1
    logger.info("Calculating actual result...")
    numRes = 0
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(initialMatrix, i)
        for matrix in matrices:
            numOp, _ = gen_diseq_items_of_matrix(matrix, actualCalc=True)
            numRes += numOp

    ## Log results
    print("\n---\n")
    logger.info(f"Generic Full Disequation: {textStrFull[3:]} > 1")
    
    logger.info(f"Generic Disequation also considering presence of zeros: {textStr[3:]} > 1")

    ## and actual result
    logger.info(f"Actual Disequation: {numRes} > 1")
    logger.info("All done")


if __name__ == "__main__":
    main()
