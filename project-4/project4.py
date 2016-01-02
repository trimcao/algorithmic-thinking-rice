"""
Project 4: Computing Alignments of Sequences
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: November 2015
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Build a scoring matrix for computing alignment methods
    """
    score_matrix = {}
    alphabet_dash = list(alphabet)
    alphabet_dash.append('-')
    alphabet_dash = set(alphabet_dash)
    # build the dictionaries:
    for each_char in alphabet_dash:
        new_dict = {}
        for other_char in alphabet_dash:
            if (each_char == '-') or (other_char == '-'):
                new_dict[other_char] = dash_score
            elif (each_char == other_char):
                new_dict[other_char] = diag_score
            elif (each_char != other_char):
                new_dict[other_char] = off_diag_score
        
        score_matrix[each_char] = new_dict
    return score_matrix        


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Compute an alignment matrix to assist the finding the global alignment or 
    local alignment later)
    """
    # note that x is row, y is column
    length_x = len(seq_x)
    length_y = len(seq_y)
    # initialize the matrix
    align_matrix = [[0 for dummy_col in range(length_y + 1)] 
                    for dummy_row in range(length_x + 1)]
    # add the score for alignment with dashes
    for idx in range(1, length_x + 1):
        score = align_matrix[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]['-']
        if (not global_flag) and (score < 0):
            align_matrix[idx][0] = 0
        else:
            align_matrix[idx][0] = score

    for idx in range(1, length_y + 1):
        score = align_matrix[0][idx - 1] + scoring_matrix['-'][seq_y[idx - 1]]
        if (not global_flag) and (score < 0):
            align_matrix[0][idx] = 0
        else:
            align_matrix[0][idx] = score
    
    # find the alignment scores for the rest of entries
    for idxi in range(1, length_x + 1):
        for idxj in range(1, length_y + 1):
            score = max((align_matrix[idxi - 1][idxj] + scoring_matrix[seq_x[idxi - 1]]['-']),
                        (align_matrix[idxi - 1][idxj - 1] + scoring_matrix[seq_x[idxi - 1]][seq_y[idxj - 1]]),
                        (align_matrix[idxi][idxj - 1] + scoring_matrix['-'][seq_y[idxj - 1]]))
            if (not global_flag) and (score < 0):
                align_matrix[idxi][idxj] = 0
            else:
                align_matrix[idxi][idxj] = score

    return align_matrix



def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute the global alignment of two sequences 
    """
    result_x = ''
    result_y = ''
    idxi = len(seq_x)
    idxj = len(seq_y)
    final_score = alignment_matrix[idxi][idxj]
    # trace back from the end of the alignment_matrix
    while (idxi > 0) and (idxj > 0):
        if (alignment_matrix[idxi][idxj] == alignment_matrix[idxi - 1][idxj - 1] + scoring_matrix[seq_x[idxi - 1]][seq_y[idxj - 1]]):
            result_x = seq_x[idxi - 1] + result_x
            result_y = seq_y[idxj - 1] + result_y
            idxi -= 1
            idxj -= 1

        elif (alignment_matrix[idxi][idxj] == alignment_matrix[idxi - 1][idxj] + scoring_matrix[seq_x[idxi - 1]]['-']):
            result_x = seq_x[idxi - 1] + result_x
            result_y = '-' + result_y
            idxi -= 1
        
        else:
            result_x = '-' + result_x
            result_y = seq_y[idxj - 1] + result_y
            idxj -= 1

    # add dashes if needed
    while (idxi > 0):
        result_x = seq_x[idxi - 1] + result_x
        result_y = '-' + result_y
        idxi -= 1

    while (idxj > 0):
        result_x = '-' + result_x
        result_y = seq_y[idxj - 1] + result_y
        idxj -= 1

    return (final_score, result_x, result_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Compute Local Alignment of two sequences
    """
    result_x = ''
    result_y = ''
    idxi = len(seq_x)
    idxj = len(seq_y)
    # find the maximum score
    max_score = 0
    for idx1 in range(len(seq_x) + 1):
        for idx2 in range(len(seq_y) + 1):
            if (alignment_matrix[idx1][idx2] > max_score):
                max_score = alignment_matrix[idx1][idx2]
                idxi = idx1
                idxj = idx2
                
    # trace back from the end of the alignment_matrix
    while (alignment_matrix[idxi][idxj] > 0) and (idxi > 0) and (idxj > 0):
        if (alignment_matrix[idxi][idxj] == alignment_matrix[idxi - 1][idxj - 1] + scoring_matrix[seq_x[idxi - 1]][seq_y[idxj - 1]]):
            result_x = seq_x[idxi - 1] + result_x
            result_y = seq_y[idxj - 1] + result_y
            idxi -= 1
            idxj -= 1

        elif (alignment_matrix[idxi][idxj] == alignment_matrix[idxi - 1][idxj] + scoring_matrix[seq_x[idxi - 1]]['-']):
            result_x = seq_x[idxi - 1] + result_x
            result_y = '-' + result_y
            idxi -= 1
        
        else:
            result_x = '-' + result_x
            result_y = seq_y[idxj - 1] + result_y
            idxj -= 1

    return (max_score, result_x, result_y)

#scores = build_scoring_matrix(set(['A', 'T', 'U', 'C', 'G']), 10, 4, -6)
###print scores
##
#test = compute_alignment_matrix('AA', 'TAAT', scores, False)
##print test
##
#result = compute_local_alignment('AA', 'TAAT', scores, test)
#print result
