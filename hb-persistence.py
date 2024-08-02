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
def gen_diseq_items_of_matrix(matrix, zeroMatrix, actualCalc = False):
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
            if (zeroMatrix[k][l] == 0):
                skipElement = True
            if(actualCalc):
                textOpString += f" {matrix[k][l]}"
            else:
                textOpString += f" Q_{matrix[k][l]}"
            numerator_op = round(numerator_op * matrix[k][l], round_decimals)
        
        # generate denominator
        textOpString += "/"

        denominator_op = 1
        for k in ks:
            if(actualCalc):
                textOpString += f"(1 - {matrix[k][k]})"
            else:
                textOpString += f"(1 - Q_{matrix[k][k]})"
            denominator_op = round(denominator_op * (1 - matrix[k][k]), round_decimals)
                
        if (actualCalc):
            if(numerator_op != 0 and denominator_op != 0):
                logger.debug(f"Numerator/Denominator: {numerator_op} / {denominator_op}")
                logger.debug(numerator_op/denominator_op)

        textOpString += ")"
        ## Denominator can be 0 if at least one elem in diagonal is 0. Since this can happen, I need to handle this
        if (denominator_op != 0 and numerator_op != 0):
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


def gen_hastings_botsford_diseq(matrix: np.ndarray, zeroMatrix: np.ndarray, actualCalc = False):
    textStrFull = ""
    numRes = 0
    m = matrix.shape[0]
    for i in range(2,m+1):
        matrices = getSquareSubmatrices(matrix, i)
        zeroMatrices = getSquareSubmatrices(zeroMatrix, i)
        for (m, z) in zip(matrices, zeroMatrices):
            numOp, textOp = gen_diseq_items_of_matrix(m, z, actualCalc)
            # logger.info(textOp)
            textStrFull += textOp
            numRes += numOp
    return numRes, textStrFull

def read_input_matrix(filepath: str):
    logger.info(f"Reading matrix from file {filepath}.")
    try:
        initialMatrix = np.loadtxt(filepath, dtype=np.float64)
    except:
        logger.error(f"Error while reading input matrix. Check that file {input_file} exists, and that contains a valid matrix.")
        exit(2)
    return initialMatrix

def log_base_matrix_infos(matrix: np.ndarray):
    logger.info(f"Initial matrix\n{matrix}")
    logger.info(f"Matrix shape: {matrix.shape}")

def sanity_check_matrix(matrix: np.ndarray):
    if(len(matrix.shape) != 2):
        logger.error("Error, this is not a bidimensinal matrix.")
        exit(1)
    if(matrix.shape[0] != matrix.shape[1]):
        logger.error("Error, input is not a square matrix. Exiting")
        exit(1)

def get_size_of_square_matrix(matrix: np.ndarray):
    return matrix.shape[0]

def main(input_file):
    logger.info(f"Starting program.")

    initialMatrix = read_input_matrix(input_file)
    
    log_base_matrix_infos(initialMatrix)

    sanity_check_matrix(matrix=initialMatrix)

    m = get_size_of_square_matrix(initialMatrix)

    print("Review input matrix, and press ENTER to continue or CTRL+C to exit.")
    input()

    logger.info("Initializing matrix schemas and zero-matrix")
    initialMatrixSchema = build_n_n_matrix(m)
    initialZeroMatrixSchema = build_zero_matrix_schema(initialMatrixSchema)
    initialZeroMatrix = build_zero_matrix_schema(initialMatrix)

    logger.info("Calculating disequations...")
    # Step 1: Get full text formula. To do this I use a fake NxN matrix populated with values different from 0
    logger.info("Calculating full text formula...")
    _, textStrFull = gen_hastings_botsford_diseq(initialMatrixSchema, initialZeroMatrixSchema)    

    # Step 2: Get simplified text formula. This formula is obtained by removing operands with zeros.
    # So I launch this with the real matrix
    logger.info("Calculating simplified text formula, considering presence of zeros in the input matrix...")
    _, textStr = gen_hastings_botsford_diseq(initialMatrixSchema, initialZeroMatrix)

    ## Step 3: Perform actual calculation on the real matrix
    logger.info("Calculating actual result...")
    numRes, textRealOps = gen_hastings_botsford_diseq(initialMatrix, initialZeroMatrix, actualCalc=True)

    ## Log results
    print("\n---\n")
    # logger.info(f"Generic Full Disequation: \n  {textStrFull[3:]} > 1")
    
    logger.info(f"Generic Disequation also considering presence of zeros: \n  {textStr[3:]} > 1")

    ## and actual result
    logger.info(f"Actual Disequation: {numRes} > 1")
    logger.info(f"Actual Disequation calcs: {textRealOps} > 1")
    logger.info("All done")


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        logger.error("Error, invalid parameters")
        logger.info("Example: .\\python hb-persistence.py <file-containing-input-matrix>")
        logger.info("Exiting.")
        exit(1)
    main(sys.argv[1])
