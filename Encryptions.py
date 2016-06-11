#!/usr/bin/python
# Simple versions of encryption algorithms described in 'Codes' by Simon Singh.
# Everything works on lowercase ASCII only, it's just about the principles,
# not about useable and user-friendly code.
import string, re
from collections import OrderedDict
from random import shuffle
from copy import copy

def caesar(plaintext, shift):
    '''
    Simple caesar encryption without key
    '''
    # turn all text to lowercase
    plaintext = string.lower(plaintext)
    alphabet = string.ascii_lowercase

    # encrypt plaintext
    cyphertext = ''
    for letter in plaintext:
        letter_ix = alphabet.index(letter)
        cyphertext += alphabet[(shift + letter_ix) % 26]

    return cyphertext

print 'Plaintext: abcde'
print 'Caesar w/o key: ' + caesar('abcde',5)


def caesar_key(plaintext, shift, key):
    '''
    Caesar encryption with key
    '''
    # turn all text to lowercase
    plaintext = string.lower(plaintext)
    key = string.lower(key)
    plaintext_alphabet = string.ascii_lowercase

    # get unique letters from key
    key = ''.join(OrderedDict.fromkeys(key).keys())
    # create cyphertext alphabet
    cyphertext_alphabet = string.ascii_lowercase
    cyphertext_alphabet = key + re.sub('[' + key + ']', '', cyphertext_alphabet)

    # encrypt plaintext
    cyphertext = ''
    for letter in plaintext:
        letter_ix = plaintext_alphabet.index(letter)
        cyphertext += cyphertext_alphabet[(shift + letter_ix) % 26]

    return cyphertext

print 'Caesar with key: ' + caesar_key('abcde', 5, 'florianf')


def mono(plaintext, verbose=False):
    '''
    Simple monoalphabetic encryption
    :param boolean verbose: Print the cyphertext_alphabet
    '''
    # turn all text to lowercase
    plaintext = string.lower(plaintext)
    plaintext_alphabet = string.ascii_lowercase

    # create cyphertext alphabet
    cyphertext_alphabet = list(string.ascii_lowercase)
    shuffle(cyphertext_alphabet)
    cyphertext_alphabet = ''.join(cyphertext_alphabet)
    if verbose:
        print cyphertext_alphabet

    ## encrypt plaintext
    cyphertext = ''
    for letter in plaintext:
        letter_ix = plaintext_alphabet.index(letter)
        cyphertext += cyphertext_alphabet[(letter_ix) % 26]

    return cyphertext

print 'Monoalphabetic: ' + mono('abcde')


def vigenere_key(plaintext, key, verbose=False):
    '''
    Vigenere encryption with key
    :param boolean verbose: Print the offset (current row in Vigenere square
        as determined by the key) and the index of the plaintext letter to be
        encrypted in the alphabet.
    '''
    # turn all text to lowercase
    plaintext = string.lower(plaintext)
    key = string.lower(key)
    alphabet = string.ascii_lowercase

    # encrypt plaintext
    cyphertext = ''
    for letter_ix in xrange(len(plaintext)):
        offset_letter = key[letter_ix%len(key)]
        offset = alphabet.index(offset_letter)
        cypher_ix = alphabet.index(plaintext[letter_ix])
        if verbose:
            print 'o: ' + str(offset)
            print 'c: ' + str(cypher_ix)
        cyphertext += alphabet[(offset + cypher_ix) % 26]

    return cyphertext

print 'Vigenere: ' + vigenere_key('abcde', 'florian')


def one_time_pad(plaintext, pad):
    '''
    This function uses modular addition of letter indices
    A possible TODO is to write a function that creates the pads too
    @param string pad: the cypher pad to use for encryption
    '''
    if len(pad) < len(plaintext):
        return("Pad is to short. Repeating the pad makes the encryption " +
                    "breakable. Please choose a longer pad.")
    else:
        # turn all text to lowercase
        plaintext = string.lower(plaintext)
        pad = string.lower(pad)
        alphabet = string.ascii_lowercase

        # encrypt plaintext
        cyphertext = ''
        for letter_msg_ix in xrange(len(plaintext)):
            letter_ix = alphabet.index(plaintext[letter_msg_ix])
            pad_ix = alphabet.index(pad[letter_msg_ix])
            cyphertext += alphabet[(pad_ix + letter_ix) % 26]

        return cyphertext

print 'One time pad: ' + one_time_pad('abcde', 'qwert')


class Enigma(object):

    def __init__(self):
        '''
        Set up three rotors of different type and a reflector
        '''
        self.rotor_1 = Rotor(1)
        self.rotor_2 = Rotor(2)
        self.rotor_3 = Rotor(3)
        self.reflector = Reflector()
        #print self.rotor_1.rotor
        #print self.rotor_2.rotor
        #print self.rotor_3.rotor

    def encode(self, plaintext):
        '''
        Encoding is the same as decoding due to the reflector.
        The enigma is a polyalphabetic encryption.
        '''
        # turn all text to lowercase
        plaintext = string.lower(plaintext)
        alphabet = string.ascii_lowercase

        # encrypt plaintext
        cyphertext = ''
        for letter_msg_ix in xrange(len(plaintext)):
            letter_num = alphabet.index(plaintext[letter_msg_ix])
            letter_num = self.rotor_1.encode_forward(letter_num)
            letter_num = self.rotor_2.encode_forward(letter_num)
            letter_num = self.rotor_3.encode_forward(letter_num)
            letter_num = self.reflector.reflect(letter_num)
            letter_num = self.rotor_3.encode_backward(letter_num)
            letter_num = self.rotor_2.encode_backward(letter_num)
            letter_num = self.rotor_1.encode_backward(letter_num)
            self.rotor_1.turn(letter_msg_ix)
            self.rotor_2.turn(letter_msg_ix)
            self.rotor_3.turn(letter_msg_ix)
            cyphertext += alphabet[letter_num]
        return cyphertext

    def reset(self):
        '''
        Reset machine to initial state
        (e.g. needed to decode)
        '''
        self.rotor_1.reset()
        self.rotor_2.reset()
        self.rotor_3.reset()

class Reflector(object):
    '''
    The special reflector rotor which maps pairs of letters and never turns
    '''

    def __init__(self):
        '''
        To make a symmetric mapping between number pairs we create a randomized
        list and take a reversed copy. Doing so is a bit ugly due to the fact
        that neither shuffle nor reverse return the object, but work inplace.
        '''
        dummy = range(26)
        shuffle(dummy)
        self.rotor = copy(dummy)
        dummy.reverse()
        self.rotor_2 = dummy
        #print self.rotor
        #print self.rotor_2

    def reflect(self, letter_num):
        '''
        @param int letter_num: numeric representation of the letter to be
            encoded.
        '''
        return self.rotor_2[self.rotor.index(letter_num)]

class Rotor(object):
    '''
    Contains a list of random numbers [1:26] which is used to map an input
    letter (coded as number) to an output letter (coded as number). Also
    rotates with different frequency based on the type.
    '''

    def __init__(self, rotor_type):
        '''
        @param int rotor_type: Type 1 rotates after every encoding, type 2
            rotates after a full rotation of th e type 1 rotor (26 turns) and
            so on.
        '''
        self.rotor = range(26)
        shuffle(self.rotor)
        self.state = 0
        self.rotor_type = rotor_type

    def encode_forward(self, letter_num):
        '''
        The initial way of a letter through the rotor
        @param int letter_num: numeric representation of the letter to be
            encoded.
        '''
        output_letter_num = self.rotor[(letter_num + self.state)%26]
        return output_letter_num

    def encode_backward(self, letter_num):
        '''
        The way back through the rotor after the reflector.
        NOTE: Encode backwards does not mean decoding! Decoding is achieved
        by setting Enigma to the same initial state and just retyping the
        cyphertext.
        @param int letter_num: numeric representation of the letter to be
            encoded.
        '''
        output_letter_num = (self.rotor.index(letter_num)-self.state)%26
        return output_letter_num

    def turn(self, turn_counter):
        '''
        Method to decide if turning of the rotor is necessary
        @param in turn_counter: indicates whether the rotor turns and changes
            it's state
        '''
        if self.rotor_type == 1:
            self.state += 1
            #print 'Rotor 1 turn'
        elif self.rotor_type == 2 and turn_counter != 0:
            if turn_counter % 26 == 0:
                self.state += 1
                #print 'Rotor 2 turn'
        elif self.rotor_type == 3 and turn_counter != 0:
            if turn_counter % 676 == 0:
                self.state += 1
                #print 'Rotor 3 turn'

    def reset(self):
        '''
        Reset rotor to initial state
        '''
        self.state = 0

print 'Enigma:'
test = Enigma()
text = string.ascii_lowercase + string.ascii_lowercase
print 'Plaintext: ' + text
cypher = test.encode(text)
print 'Encrypted: ' + cypher
test.reset()
decode = test.encode(cypher)
print 'Decrypted: ' + decode

#TODO: gpg, make it so spaces are included
