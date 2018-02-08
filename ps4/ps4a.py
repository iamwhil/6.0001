# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    permutations = []
    
    print(sequence[1:])
    if len(sequence) == 1:
        print("len is 1: ", sequence)
        permutations.append(sequence)
        print("permutations: ", permutations)
        return permutations
    else:
        print("sequence: ", sequence)
        first_letter = sequence[0]
        for item in get_permutations(sequence[1:]):
            for i in range(len(item) + 1):
                working_item = list(item)
                print("here")
                working_item.insert(i, "k")
                print(working_item))
                permutations.append(list(item).insert(i, first_letter))
        return permutations
    

if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'ab'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

