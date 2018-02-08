# Problem Set 4A
# Name: Whil Piavis
# Date: 2/7/2018
# Collaborators:
# Time Spent: 1:14
# Notes: I'm still trying to figure out why the lines 36 - 38 can not be boiled 
# down into one statement.  For the longest time, as one statement it was returning
# a lot of "None."

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
    
    if len(sequence) == 1:
        permutations.append(sequence)
    else:
        first_letter = sequence[0]
        for item in get_permutations(sequence[1:]):
            for i in range(len(item) + 1):
                working_item = list(item)
                working_item.insert(i, first_letter)
                permutations.append(''.join(working_item))
                
    return permutations
    

if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    print('Test 1:', get_permutations('dog'))
    print('Test 2:', get_permutations('ab'))
    print('Test 3:', get_permutations('lego'))