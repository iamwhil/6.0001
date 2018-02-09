# Problem Set 4B
# Name: Whil Piavis
# Date: 2/8/2017
# Collaborators:
# Time Spent: 0:40
# Notes it may be worth it, on much longer messages to decrypt, to only decrypt the first
# 50 words, and if none of them are 'valid' words, move on to the next shift.
import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        # Assert that the shift is acceptable.
        assert shift >= 0 and shift <= 26, "Shift must be greater than or equal to 0 and less than 26."
        
        letters = list(string.ascii_lowercase)
        shift_dict = {}
        for i in range(len(letters)):
            if i + shift > len(letters) - 1:
                shift_dict[letters[i]] = letters[i + shift - len(letters)]
            else: 
                shift_dict[letters[i]] = letters[i + shift]
        
        # For each of the keys in the shift dictionary make the upper case entry.
        shift_dict_copy = shift_dict.copy()
        for l in shift_dict_copy.keys(): 
            shift_dict[l.capitalize()] = shift_dict_copy[l].capitalize()
        
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        
        # Assert that the shift is acceptable.
        assert shift >= 0 and shift <= 26, "Shift must be greater than or equal to 0 and less than 26."
        
        # Build a list of all available letters.
        all_letters = list(string.ascii_lowercase + string.ascii_uppercase)
        shift_dict = self.build_shift_dict(shift)
        
        # Break the self.message_text into individual characters.
        original_text = list(self.get_message_text())
        shifted_text = []
        for char in original_text:
            if char in all_letters:
                shifted_text.append(shift_dict[char])
            else:
                shifted_text.append(char)
        
        return ''.join(shifted_text)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.get_shift())
        self.message_text_encrypted = self.apply_shift(self.get_shift())

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        
        assert shift >= 0 and shift <= 26, "Shift must be between 0 and 26."
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        best = 0
        max_count = 0

        for i in range(26):
            count = 0
            shifted_statement = self.apply_shift(26 - i)
            for word in shifted_statement.split(' '):
                if is_word(self.get_valid_words(), word):
                    count += 1
                if count >= max_count:
                    max_count = count
                    best = i
                    
        return (26 - best, self.apply_shift(26 - best))
            
            
if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello there', 2)
    print('Expected Output: jgnnq vjgtg')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq vjgtg')
    print('Expected Output:', (24, 'hello there'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Test Case
    plaintext2 = PlaintextMessage('In my younger days with few coins in my pockets.', 18)
    print('Expected Output: Af eq qgmfywj vsqk oalz xwo ugafk af eq hgucwlk.')
    print('Actual Output:', plaintext2.get_message_text_encrypted())
    
    ciphertext2 = CiphertextMessage('Af eq qgmfywj vsqk oalz xwo ugafk af eq hgucwlk.')
    print('Expected Output:', (18, 'In my younger days with few coins in my pockets.'))
    print('Actual Output:', ciphertext2.decrypt_message())

    cipher_story = CiphertextMessage(get_story_string())
    print(cipher_story.decrypt_message())

# Decrypted story.
# 12, 'Jack Florey is a mythical character created on the spur of a moment to help cover an insufficiently planned hack. He has been registered for classes at MIT twice before, but has reportedly never passed aclass. It has been the tradition of the residents of East Campus to become Jack Florey for a few nights each year to educate incoming students in the ways, means, and ethics of hacking.'