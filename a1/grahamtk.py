'''
Graham Kelly
4/5/2017
CSE 415 Spring 2017
A1 B:
A conversational agent.

***
THIS REQUIRES PYTHON PACKAGE 'seinfeld' TO BE INSTALLED.
ALSO REQUIRES 'seinfeld.db' WHICH WAS PACKAGED ALONG WITH
THIS CODE.
IF YOU DON'T HAVE THESE THIS SCRIPT WILL DOWNLOAD/INSTALL
THEM AUTOMATICALLY.
***
'''

from re import *   # Loads the regular expression module.
import os.path
from random import choice
from difflib import SequenceMatcher

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

no_response = ['Hello! Uncle Leo?!', 'If you don\'t say anything, then I can\'t either.', 'Is this a joke?!']

commands = ['Available Commands and Input/Output Combos:',
            '- \'help\' : prints commands',
            '- \'\' (nothing / whitespace) : prints silence prompts',
            '- \'(<obj> is) my favorite {character|episode}\' OR \'my favorite {character|episode} (is <obj>)\' : sets favorite character or episode to <obj>',
            '- \'random\' : returns a random quote',
            '- \'I don\'t understand\' OR \'context\' : prints the quotes surrounding the previous quote shared. enter command again to get more context.',
            '- \'...opera...\' : opens the opera house...',
            '- \'remove preferences\' : deletes episode and character preferences',
            '- \'add subject <subj>\' : adds a subject to the list of possible subjects for random quotes',
            '- \'show {\'\'|default|my} subjects\' : prints available subjects. depending on modifier will print all, default, or user-added subjects',
            '- \'show preferences\' : prints user\'s current preferences',
            '- \'I am the master of my domain\' : are you sure?',
            '- \'...from my favorite episode...\' : prints a quote from the user\'s favorite episode',
            '- \'who is {jerry seinfeld|larry david}\' : prints a short bio about Jerry Seinfeld or Larry David',
            ]

stop_words = {"a", "about", "above," "after", "again", "against", "all", "am", "an", "and", "any", "are",
              "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
              "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
              "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
              "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
              "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
              "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
              "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
              "other", "ought", "our", "ours    ourselves", "out", "over", "own", "same", "shan't", "she",
              "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
              "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
              "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
              "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
              "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
              "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
              "yours", "yourself", "yourselves"}

sw_pattern = compile(r'\b(' + r'|'.join(stop_words) + r')\b\s*') #maybe superfluous

def remove_punctuation(text):
    '''Returns a string without any punctuation.'''
    return sub(punctuation_pattern, '', text)

class NoEpisodeException(Exception):
    pass

class NoCharacterException(Exception):
    pass

class CrazyJoe(object):
    db_name = 'seinfeld.db'
    db_loc = 'https://noswap.com/pub/seinfeld.db'
    agent_name = 'Crazy Joe'

    def __init__(self):
        self.fave_ep = None
        self.fave_char = None
        self.prev_quote = None
        self.no_response_count = 0
        self.context_count = 0
        try:
            from seinfeld import Seinfeld
        except ImportError:
            import pip
            print('Crazy Joe: Installing necessary dependency: \'seinfeld\'...')
            pip.main(['install', 'seinfeld'])
        finally:
            from seinfeld import Seinfeld

        if not os.path.isfile(self.db_name): #looking in current dir only.
            import urllib.request as rq
            print('Crazy Joe: Downloading Seinfeld Database...')
            rq.urlretrieve(self.db_loc, self.db_name)
        
        self.seinfeld = Seinfeld(self.db_name)
        self.eps = {v.title.lower() : k for k, v in self.seinfeld.episode().items()}
        self.chars = ['jerry', 'elaine', 'george', 'kramer', 'leo', 'newman', 'maestro', 'puddy', 'peterman',]
        self.def_subjects = ['keys', 'tips', 'tipping', 'kavorka', 'tv', 'parents', 'sex', 'comedy', 'nothing',]
        self.new_subjects = []
        self.jerry = False
        self.larry = False

    @classmethod
    def kmp(self, text, pattern):
        '''returns index of first subsequence in text matching pattern. -1 if DNE'''
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        
        for pos in range(len(pattern)):
            while shift <= pos and pattern[pos] != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos + 1] = shift
        
        start = 0
        match_len = 0
        for c in text:
            while match_len == len(pattern) or match_len >= 0 and not match(pattern[match_len], c):
                start += shifts[match_len]
                match_len -= shifts[match_len]
            match_len += 1
            if match_len == len(pattern):
                return start
        return -1
    
    def introduce(self):
        return '''
Good evening ladies and gentlemen, how are you doing tonight?
Good? Good. I'm Crazy Joe Devola, I used to write for acclaimed sitcom 'Seinfeld.' 
I have a hard time differentiating between myself and my characters so WATCH OUT.
I can only respond in 'Seinfeld' quotes, so bear with me.
If anything I say or do offends you, too bad!...Although you could try contacting
my creator Graham Kelly at grahamtk@uw.edu.
What do you want to hear, quotes? Do you have a favorite episode? A favorite character?
You can read my manual too if you need direction. (type 'help')'''

    def respond(self, the_input):
        '''Returns a response based on the passed input.'''
        if not the_input.strip(): # rule 0, respond to no input
            self.prev_quote = None
            if self.no_response_count >= len(no_response):
                self.no_response_count = 0
                return self._get_good_quote() # default to just saying quote if no_responses exhausted.
            else:
                self.no_response_count += 1
                return no_response[self.no_response_count - 1]
        
        clean_input = remove_punctuation(the_input)
        # filtered_input = sw_pattern.sub('', clean_input) # filter stop words

        wordlist = split(' ', clean_input)
        wordlist[0] = wordlist[0].lower()
        sub_wordlist = [w for w in wordlist if w not in stop_words]
        
        return self.make_response(wordlist, sub_wordlist)

    def make_response(self, wordlist, sub_wordlist):
        '''generates a response to the passed wordlist based on several rules'''
        if wordlist[0] == 'help': #rule 1: HELP ME!
            self.prev_quote = None
            return '\n\t'.join(commands)
        
        if wordlist[0] == 'random': #rule 2: random quote.
            return self._get_random_quote()
        
        if wordlist == ['i', 'am', 'the', 'master', 'of', 'my', 'domain']: # rule 11: master of my domain
            self.fave_ep = self.seinfeld.episode(id=self.eps['the contest'])
            return self._get_good_quote(episode=self.fave_ep)
        
        if wordlist[0:2] == ['who', 'is']:
            self.prev_quote = None
            if wordlist[2:4] == ['jerry', 'seinfeld']: #rule 13: learn about jerry seinfeld
                if not self.jerry:
                    return 'Jerome Allen "Jerry" Seinfeld (born April 29, 1954) is an American comedian, actor, writer, producer, and director. He is known for playing a semifictional version of himself in the sitcom Seinfeld, which he created and wrote with Larry David. Seinfeld was heavily involved in the Bee Movie, in which he voiced its protagonist. In 2010, he premiered a reality series called The Marriage Ref. He directed Colin Quinn in the Broadway show Long Story Short at the Helen Hayes Theater, which ran until January 2011. He is the creator and host of the web series Comedians in Cars Getting Coffee. In his stand-up comedy career, Seinfeld is known for specializing in observational comedy, often ranting about relationships and embarrassing social situations.'
                else:
                    return 'I already told you about him!'
            if wordlist[2:4] == ['larry', 'david']: #rule 14: learn about larry david
                if not self.larry:
                    return 'Lawrence Gene "Larry" David (born July 2, 1947) is an American comedian, writer, actor, playwright, and television producer. He and Jerry Seinfeld created the television series Seinfeld, where he served as its head writer and executive producer from 1989 to 1996. David has subsequently gained further recognition for the HBO series Curb Your Enthusiasm, which he also created, in which he stars as a semi-fictionalized version of himself. He is worth an estimated $900 million US dollars. David\'s work won him a Primetime Emmy Award for Outstanding Comedy Series in 1993. Formerly a stand-up comedian, David went into television comedy, writing and starring in ABC\'s Fridays, as well as writing briefly for Saturday Night Live. He has won two Primetime Emmy Awards, and was voted by fellow comedians and comedy insiders as the 23rd greatest comedy star ever in a 2004 British poll to select "The Comedian\'s Comedian."'
                else:
                    return 'I already told you about him!'
                    
        if 'opera' in sub_wordlist: #rule 6: opera house
            self.fave_char = self.seinfeld.speaker(name='Devola')
            self.fave_ep = self.seinfeld.episode(id=self.eps['the opera'])
            lines = ['You have entered the opera house and unleashed my true persona: Crazy Joe Devola.',
                    'Muahahaha, I have changed your favorite episode and character settings.']
            lines.append(self._get_good_quote())
            return '\n'.join(lines)
        
        if self.kmp(wordlist, ['from', 'my', 'favorite', 'episode']) >= 0: #rule 12: quote from favorite episode
            if self.fave_ep:
                return self._get_good_quote(episode=self.fave_ep)
        
        if self.kmp(wordlist, ['my', 'favorite']) >= 0:
            if 'episode' in sub_wordlist: #rule 3: set fave ep
                try:
                    try:
                        e_loc = wordlist.index('episode')
                        i_loc = wordlist.index('is')
                        if i_loc < e_loc:
                            ep_name = ' '.join(wordlist[0: i_loc]).lower() #pattern: XYZ is my favorite episode...
                        else:
                            ep_name = ' '.join(wordlist[i_loc + 1:]).lower() #pattern: ...my favorite episode is XYZ
                        self.fave_ep = self.seinfeld.episode(id=self.eps[ep_name])
                    except KeyError:
                        for k in self.eps.keys():
                            if SequenceMatcher(None, k, ep_name).ratio() >= .75:
                                self.fave_ep = self.seinfeld.episode(id=self.eps[k])
                        if not self.fave_ep:
                            raise NoEpisodeException
                except (IndexError, NoEpisodeException):
                    return '\n'.join(['I can\'t seem to figure out what episode you meant.', 
                                    # 'This is what I got: "' + ep_name + '."',
                                    self._get_random_quote(subject='stupid'),])
                else:
                    return ' '.join(['Oh yeah,', self.fave_ep.title, 'is a great episode.', 'Here\'s a quote:', 
                                    self._get_good_quote()
                                    ])
            if 'character' in sub_wordlist: #rule 4: set fave character 
                try:
                    try:
                        c_loc = wordlist.index('character')
                        i_loc = wordlist.index('is')
                        if i_loc < c_loc:
                            c_name = ' '.join(wordlist[0: i_loc]).lower() #pattern: XYZ is my favorite char...
                        else:
                            c_name = ' '.join(wordlist[i_loc + 1:]).lower() #pattern: ...my favorite char is XYZ
                        self.fave_char = self.seinfeld.speaker(name=c_name.capitalize())
                    except KeyError:
                        for c in self.chars:
                            if SequenceMatcher(None, c, c_name).ratio() >= .75:
                                self.fave_char = self.seinfeld.character(name=c)
                        if not self.fave_char:
                            raise NoCharacterException
                except (IndexError, NoCharacterException):
                    return '\n'.join(['I can\'t seem to figure out what character you meant.', 
                                    # 'This is what I got: "' + ep_name + '."',
                                    self._get_random_quote(subject='character'),])
                else:
                    return ' '.join(['Oh yeah,', self.fave_char.name, 'is funny.', 'Here\'s a quote: \n', 
                                    self._get_good_quote()
                                    ])
        if self.kmp(wordlist, ['add', 'subject']) >= 0: # rule 8: add subject
            self.prev_quote = None
            try:
                subject = wordlist[wordlist.index('subject') + 1]
                self.new_subjects.append(subject)
                return 'I will remember that one for later.'
            except (IndexError, ValueError):
                return 'Unable to remember that one...'
        
        if self.kmp(wordlist, ['show', r'\w*', 'subjects']) >= 0 or self.kmp(wordlist, ['show', 'subjects']) >= 0: # rule 9: show subjects
            self.prev_quote = None
            index = max(self.kmp(wordlist, ['show', r'\w*', 'subjects']), self.kmp(wordlist, ['show', 'subjects']))
            try:
                if 'default' in wordlist[index : index + 2]:
                    return 'Here are the default subjects: ' + ', '.join(self.def_subjects) + '.'
                elif 'my' in wordlist[index : index + 2]:
                    return 'Here are the subjects I remember: ' + ', '.join(self.new_subjects) + '.'
                elif len(wordlist[index:index+2]) == 2:
                    return 'These are all the subjects I know: ' + ', '.join(self.def_subjects + self.new_subjects) + '.'
                else:
                    return 'I\'m not quite sure what subjects you want.' 
            except (IndexError, ValueError):
                return 'I\'m not quite sure what subjects you want.'
                
        if self.kmp(wordlist, ['show', 'preferences']) >= 0: # rule 10: show current user prefs.
            self.prev_quote = None
            lines = ['Here are the preferences I know:',
                     'Favorite character: ' + (self.fave_char.name if self.fave_char else 'NONE'),
                     'Favorite episode: ' + (self.fave_ep.title if self.fave_ep else 'NONE')]
            return '\n\t'.join(lines)
        
        if self.prev_quote and 'context' in sub_wordlist or self.kmp(wordlist, ['i', 'don\'t', 'understand']) >= 0: #rule 5 give context with cycle
            if self.context_count < 5: #CYCLE
                p = self.seinfeld.passage(self.prev_quote, length=self.context_count * 3 + 8)
                lines = ['Perhaps this will help:']
                for q in p.quotes:
                    lines.append(q.speaker.name + ': ' + q.text)
                self.context_count += 1
                return '\n\t'.join(lines)
            else:
                self.context_count = 0
                return 'Seems like you\'re just not going to understand this one...\n' + self._get_random_quote(subject='understand')
        
        if self.kmp(wordlist, ['remove', 'preferences']) >= 0: #rule 7: remove preferences
            self.fave_char = None
            self.fave_ep = None
            self.prev_quote = None
            return '\n'.join(['I\'ve forgotten everything you told me.', self._get_random_quote(subject='forgot')])


        try: #default response
            return self._get_good_quote(subject=choice(sub_wordlist) if sub_wordlist else None)
        except IndexError:
            return self._get_good_quote()

    def _get_good_quote(self, subject=None, episode=None):
        q = None
        qtext = ''
        while len(split(' ', qtext)) < 8:
            if episode:
                q = choice(self.seinfeld.search(episode=episode, random=True, limit=10))
            elif any([self.fave_char, subject]):
                q = choice(self.seinfeld.search(speaker=self.fave_char, random=True, limit=10, subject=subject))
            else:
                q = choice(self.seinfeld.search(subject=choice(self.def_subjects + self.new_subjects), random=True, limit=10)) #essentially random quote
            qtext = q.text

        self.prev_quote = q
        self.context_count = 0
        return q.speaker.name.strip() + ': ' + qtext

    def _get_random_quote(self, subject=None):
        q = None
        qtext = ''
        while len(split(' ', qtext)) < 8:
            q = self.seinfeld.random(subject=subject, speaker=choice(self.chars) if not subject else None)
            qtext = q.text

        self.prev_quote = q
        self.context_count = 0
        return q.speaker.name.strip() + ': ' + qtext

    def agentName(self):
        return self.agent_name