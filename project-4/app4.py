"""
Application 4
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: November 2015
"""
import random
import project4
import matplotlib.pyplot as plt
import pickle

# load the files for question 1

#f = open('alg_FruitflyEyelessProtein.txt', 'r')
#fruitfly_protein = f.read()
#fruitfly_protein = fruitfly_protein[:-2]
##print list(fruitfly_protein)
#f.close()
#
##print fruitfly_protein
#
#f = open('alg_HumanEyelessProtein.txt', 'r')
#human_protein = f.read()
#human_protein = human_protein[:-2]
#f.close()
#
## load the scoring matrix
#
#f = open('alg_PAM50.txt', 'r')
#score_data = []
#for line in f:
#    # split without argument will split by whitespaces
#    score_data.append(line.split())
#f.close()
#
#scores = {}
#
##print score_data[1][0]
##print len(score_data[0])
##print len(score_data[1])
##print len(score_data)
#
#for row in range(1, len(score_data)):
#    num_col = len(score_data[row])
#    scores[score_data[row][0]] = {}
#    for col in range(1, num_col):
#        scores[score_data[row][0]][score_data[0][col - 1]] = int(score_data[row][col])

#print scores
#print scores['-']['-']
#print scores['M']['N']

#print scores

def question1():
    # QUESTION 1
    align_matrix = project4.compute_alignment_matrix(fruitfly_protein, human_protein, scores, False)
    local_alignment_eyeless = project4.compute_local_alignment(fruitfly_protein, human_protein, scores, align_matrix) 
    #
    #for each in local_alignment_eyeless:
    #    print each

    #print local_alignment_eyeless[0]
    local_human = local_alignment_eyeless[2]
    local_fruitfly = local_alignment_eyeless[1]
    #print local_human
    #print local_fruitfly

def question2():
    # QUESTION 2
    # delete the dashes in local alignments
    local_human_new = ''
    local_fruitfly_new = ''
    for idx in range(len(local_human)):
        if (local_human[idx] != '-'):
            local_human_new += local_human[idx]
        if (local_fruitfly[idx] != '-'):
            local_fruitfly_new += local_fruitfly[idx]

    #print local_human_new
    #print local_fruitfly_new

    # compute the global alignment

    f = open('alg_ConsensusPAXDomain.txt', 'r')
    consensus = f.read()
    consensus = consensus[:-2]
    f.close()

    align_matrix_human = project4.compute_alignment_matrix(local_human_new, consensus, scores, True)
    global_align_human = project4.compute_global_alignment(local_human_new, consensus, scores, align_matrix_human)
    print global_align_human
    global_human = global_align_human[1]
    global_consensus_human = global_align_human[2]
    similarity = 0
    for idx in range(len(global_human)):
        if (global_human[idx] == global_consensus_human[idx]):
            similarity += 1
    human_percentile = similarity / float(len(global_human)) * 100
    print human_percentile


    #
    align_matrix_fruitfly = project4.compute_alignment_matrix(local_fruitfly_new, consensus, scores, True)
    global_align_fruitfly = project4.compute_global_alignment(local_fruitfly_new, consensus, scores, align_matrix_fruitfly)
    print global_align_fruitfly

    global_fruitfly = global_align_fruitfly[1]
    global_consensus_fruitfly = global_align_fruitfly[2]

    similarity = 0
    for idx in range(len(global_fruitfly)):
        if (global_fruitfly[idx] == global_consensus_fruitfly[idx]):
            similarity += 1
    fruitfly_percentile = similarity / float(len(global_fruitfly)) * 100
    print fruitfly_percentile

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Function for question 4
    """
    ## make a copy of seq_y:
    #new_seq_y = ''
    #for each_char in seq_y:
    #    new_seq_y += each_char

    list_seq_y = list(seq_y)
    scoring_distribution = {}
    for dummy_idx in range(num_trials):
        #random.shuffle(new_seq_y)
        random.shuffle(list_seq_y)
        new_seq_y = ''.join(list_seq_y)
        align_matrix = project4.compute_alignment_matrix(seq_x, new_seq_y, scores, False)
        local_result = project4.compute_local_alignment(seq_x, new_seq_y, scores, align_matrix)
        if (local_result[0] in scoring_distribution):
            scoring_distribution[local_result[0]] += 1
        else:    
            scoring_distribution[local_result[0]] = 1

        print dummy_idx

    return scoring_distribution

def data_for_q4():
    """
    Generate data for Question 4
    """
    distribution = generate_null_distribution(human_protein, fruitfly_protein, scores, 1000)
    # load dictionary
    #distribution = pickle.load( open( "q4_scoring_distribution.p", "rb" ) )
    #print distribution
    # save to file
    pickle.dump(distribution, open("q4_scoring_distribution.p", "wb"))
    #print distribution

def question4():
    """
    Plot for question 4
    """
    distribution = pickle.load( open( "q4_scoring_distribution.p", "rb" ) )
    score_list = distribution.keys()
    score_list.sort()
    #print score_list
    value_list = []
    for each in score_list:
        value_list.append(distribution[each] / 1000.0) # 1000.0 is the # trials
    # plot
    plt.bar(score_list, value_list)
    plt.xlabel('Scores')
    plt.ylabel('Fraction of Trials')
    plt.title('Scoring Distribution of Local Alignment Trials')
    plt.show()

#data_for_q4()
#question4()

distribution = pickle.load( open( "q4_scoring_distribution.p", "rb" ) )

def question5():
    """
    Question 5
    """
    # find the mean of the scores
    score_list = distribution.keys()
    num_trials = 1000.0
    total_score = 0
    for each_score in score_list:
        total_score += (each_score * distribution[each_score])
    mean = total_score / num_trials

    # find the standard deviation
    std_dev = 0
    for each_score in score_list:
        std_dev += distribution[each_score] * ((each_score - mean) ** 2)
    std_dev = (std_dev / num_trials) ** 0.5

    print mean
    print std_dev

#question5()

def question7():
    """
    Question 7
    """
    alphabet = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'])
    #print len(alphabet)
    score_matrix = project4.build_scoring_matrix(alphabet, 2, 1, 0)
    test1 = 'abcde'
    test2 = 'xycdefg'
    align_matrix = project4.compute_alignment_matrix(test1, test2, score_matrix, True)
    result = project4.compute_global_alignment(test1, test2, score_matrix, align_matrix)
    print test1
    print test2
    print result
    print len(test1) + len(test2) - result[0]



#question7()


f = open('assets_scrabble_words3.txt', 'r')
word_list = []
for line in f:
    # split without argument will split by whitespaces
    word_list.append(line[:-1])
f.close()

word_list = set(word_list)
#print word_list

def check_spelling(checked_word, dist, word_list):
    """
    Function for Question 8
    """
    # we should do some pre-processing with the word_list
    # only consider the words that has length between |checked_word| +- dist
    # (2) maybe should not consider the words that have letters not existed 
    # in the checked_word
    #word_list_new = []
    #for each_word in word_list:
    #    if (len(each_word) >= (len(checked_word) - dist)) and (len(each_word) <= (len(checked_word) + dist)): 
    #        word_list_new.append(each_word)

    alphabet = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'])
    #print len(alphabet)
    if (checked_word in word_list):
        return checked_word

    score_matrix = project4.build_scoring_matrix(alphabet, 2, 1, 0)
    words = []
    # build a set of chars in checked_word
    # I can even use a dictionary to check against the number of chars, it
    # would be more effective
    checked_word_chars = set(checked_word)
    num_checks = 0
    for each_word in word_list:
        each_word_chars = set(each_word)
        num_diffs = 0
        for char in each_word_chars:
            if char not in checked_word_chars:
                num_diffs += 1

        if (len(each_word) >= (len(checked_word) - dist)) and (len(each_word) <= (len(checked_word) + dist)
                and num_diffs <= 2): 
            align_matrix = project4.compute_alignment_matrix(checked_word, each_word, score_matrix, True)
            result = project4.compute_global_alignment(checked_word, each_word, score_matrix, align_matrix)
            if ((len(checked_word) + len(each_word) - result[0]) <= dist):
                words.append(each_word)
            num_checks += 1
    print num_checks    
    return words

#humble = check_spelling('humble', 1, word_list)
firefly = check_spelling('schuul', 2, word_list)
#print humble
print firefly


