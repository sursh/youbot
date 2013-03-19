 #!/usr/bin/python

from collections import defaultdict
import numpy
import string
#import twitterclient

TWEETING = False

class Markov(object):

    def read_file(self, filename):
        ''' Reads in training corpus text file. Cleans, splits, and adds beginning and end signifiers. '''

        with open(filename) as f:
            for line in f:
                yield ['^', '^'] + line.strip().lower().split() + ['$']


    def generate_trigrams(self, tokens):
        ''' Break headline into trigrams '''

        trigrams = []

        for idx, item in enumerate(tokens[:-2]):
            trigrams.append((item, tokens[idx+1], tokens[idx+2]))
        
        return trigrams


    def generate_matrix(self, filename):
        ''' Run through the list of trigrams and add them to the occurence matrix.

                There are two data structures here: 

                1) bigrams
                     keys: tuple of first two words in each trigram
                     values: list of all the words that come third in the training corpus
                     e.g. {(a, b): (c1, c2, c3), (b, c1): (d1, d2, d3)}

                2) matrix
                     keys: tuple of each trigram
                     values: tuple of # of occurences of the trigram, and a boolean seenBefore? flag
                     e.g. {(a, b, c): (5, True), (b, c, d): (2: True) ... }
        '''

        self.matrix = {}
        self.bigrams = defaultdict(list)

        headlines = self.read_file(filename)

        for headline in headlines:

            trigrams = self.generate_trigrams(headline)

            for trigram in trigrams:

                bigram = trigram[:2]
                current_word = trigram[-1]
                (old_count, seenBefore) = self.matrix.get(trigram, (0, False))

                if not seenBefore:
                    self.bigrams[bigram].append(current_word)

                self.matrix[trigram] = (1 + old_count, True)


    def generate_next_word(self, prev_word, current_word):
        ''' Based on prev_word and current_word, returns a third word to follow '''

        bigram = (prev_word, current_word)

        words = []
        counts = []

        for word in self.bigrams[bigram]:
            trigram = bigram + (word,)
            (count, _) = self.matrix[trigram]
            words.append(word)
            counts.append(count)

        if not counts: return '$' # aka the ending signifier

        # pick ONE of the possibilities, with probability weighted by frequency in training corpus
        cumcounts = numpy.cumsum(counts)
        coin = numpy.random.randint(cumcounts[-1])
        for index, item in enumerate(cumcounts):
            if item >= coin:
                return words[index]


    def generate_paragraph(self, initial_word=None):
        ''' Generates a new headline '''
        
        if not initial_word:
                initial_word = self.generate_next_word('^', '^')
                
        prev_word = '^'
        current_word = initial_word
        paragraph = [ initial_word ]

        while (current_word != '$'): 
            paragraph.append(current_word)
            prev_word, current_word = current_word, self.generate_next_word( prev_word, current_word )

        paragraph = ' '.join(paragraph[1:])    # strip off leading caret
        return paragraph


def markov_it(filename, number = 1):
    print "* Generating tweets. This may take a while."
    m = Markov()
    m.generate_matrix(filename) # memory-intensive

    if not TWEETING:
        for i in range(number):

            while True:
                tweet = m.generate_paragraph() 
                if len(tweet) < 120: # leave room for RTs
                    break

            print tweet

    # To tweet, add your credentials to twitterclient.py
    if TWEETING:
        
        while True:
            tweet = m.generate_paragraph() 
            if len(tweet) < 120:
                break

        twitterclient.postTweet(tweet)


if __name__ == '__main__':
    main()
