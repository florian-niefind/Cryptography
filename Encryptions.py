#!/usr/bin/python
# Simple versions of encryption algorithms described in 'Codes' by Simon Singh.
# Everything works on lowercase ASCII only, it's just about the principles,
# not about useable and user-friendly code.
import string, re
from collections import OrderedDict
from random import shuffle

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

#TODO: enigma, gpg
