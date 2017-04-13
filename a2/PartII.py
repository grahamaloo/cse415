'''
PartII.py
Graham Kelly, CSE 415, Spring 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 2 Part II.  ISA Hierarchy Manipulation

Status of the implementation of new features:

All forms of redundancy detection and processing are working.
 Extra credit (Cycle detection and processing) implemented and working.
'''

# Linneus3.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

from re import *   # Loads the regular expression module.

ISA = {}
INCLUDES = {}
ARTICLES = {}
SYN = {} #synonyms 
DEBUG = True #TODO: change for prod.

def store_isa_fact(category1, category2):
    '''Stores one fact of the form A BIRD IS AN ANIMAL'''
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try:
        c1list = ISA[category1]
        c1list.append(category2)
    except KeyError:
        ISA[category1] = [category2]
    try:
        c2list = INCLUDES[category2]
        c2list.append(category1)
    except KeyError:
        INCLUDES[category2] = [category1]
        
def get_isa_list(category1):
    '''Retrieves any existing list of things that CATEGORY1 is a'''
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []
    
def get_includes_list(category1):
    '''Retrieves any existing list of things that CATEGORY1 includes'''
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []
    
def isa_test1(category1, category2):
    '''Returns True if category 2 is (directly) on the list for category 1.'''
    c1list = get_isa_list(category1)
    return c1list.__contains__(category2)
    
def isa_test(category1, category2, depth_limit = 20, verbose = False):
    '''Returns True if category 1 is a subset of category 2 within depth_limit levels'''
    if category1 == category2:
        if verbose: print('You don\'t have to tell me that.')
        return True
    if isa_test1(category1, category2):
        if verbose: print('You already told me that.')
        return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            if verbose: print('You don\'t have to tell me that.')
            return True
    return False

def store_article(noun, article):
    '''Saves the article (in lower-case) associated with a noun.'''
    ARTICLES[noun] = article.lower()

def get_article(noun):
    '''Returns the article associated with the noun, or if none, the empty string.'''
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''

def linneus():
    '''The main loop; it gets and processes user input, until "bye".'''
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': 
            return 'Goodbye now!'
        elif DEBUG and info == 'printtree': #useful for debugging
            print(ISA)
            print(INCLUDES)
        elif DEBUG and info == 'clear': #useful for debugging
            ISA.clear()
            INCLUDES.clear()
            ARTICLES .clear()
            SYN.clear()
        else:
            process(info)

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)    
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    

def process(info) :
    '''Handles the user sentence, matching and responding.'''
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        
        x = items[1]
        y = items[3]
        if x in SYN:
            x = SYN[x]
        if y in SYN:
            y = SYN[y]
        
        if x == y:
            print('You don\'t have to tell me that.')
        else:
            special_case = False
            
            if not isa_test(x, y, verbose = True):
                store_isa_fact(x, y)
            if isa_test(y, x):
                cycle_fix(y, x)
                special_case = True
            elif handle_redundancies(y, x):
                special_case = True

            if not special_case: print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()

        x = items[1]
        y = items[3]
        if x in SYN:
            x = SYN[x]
        if y in SYN:
            y = SYN[y]
        
        answer = isa_test(x, y)
        if answer :
            print("Yes, it is.")
        else :
            print("No, as far as I have been informed, it is not.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if items[1] in SYN:
            a1 = get_article(SYN[items[1]])
            print(items[1].capitalize() + ' is another name for ' + a1 + ' ' + SYN[items[1]])
            return
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else :
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else :
                print("I don't know.")
        return
    result_match_object = why_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()

        y = items[3]
        if y in SYN:
            y = SYN[y]
        if not isa_test(items[1], y):
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return
    print("I do not understand.  You entered: ")
    print(info)

def handle_redundancies(y, x):
    '''checks for transitive redundancies and cycles. fixes these and reports to user'''
    redundant = redundancy_check(y, x)
    l = len(redundant)
    if DEBUG: print(redundant)
    
    if l == 1:
        r = redundant[0]
        get_isa_list(r[0]).remove(r[1])
        print('Your earlier statement that %s %s is %s %s is now redundant.' % (get_article(r[0]), r[0], get_article(r[1]), r[1]))
    elif l > 1:
        print('The following statements you made earlier are now all redundant:', end='')
        for i, r in enumerate(redundant):
            get_isa_list(r[0]).remove(r[1])
            print('\n%s %s is %s %s%s' % (get_article(r[0]), r[0], get_article(r[1]), r[1], ';' if i < l-1 else ''), end='')
        print('.')
    return redundant

def redundancy_check(y, x):
    '''checks for redundancies'''
    redundant = []
    for k in ISA:
        _trace_path(get_isa_list(k), redundant, [k], k)
    return redundant

def _trace_path(x, redundant, considered, prev):
    '''traces the path from leaves to respective root looking for redundancies (transitive or cycle)'''
    for i in x:
        if i in considered:
            redundant.append((considered[0],i))
        _trace_path(get_isa_list(i), redundant, considered + x, i)

def cycle_fix(x, z):
    '''fixes cycles that are identified and spelled out in path'''
    flat = [item for sublist in find_chain(x, z) for item in sublist]
    flat = set(flat)

    contender = x
    flat.remove(contender)

    new_isa = set(get_isa_list(x))
    new_includes = set(get_includes_list(x))

    for e in flat:
        if e != contender:
            new_isa.update(get_isa_list(e))
            new_includes.update(get_includes_list(e))
            add_syn(e, contender)
            del ISA[e]
            del INCLUDES[e]
    
    new_isa.discard(contender)
    new_includes.discard(contender)
    for e in flat:
        new_isa.discard(e)
        new_includes.discard(e)

    ISA[contender] = list(new_isa)
    INCLUDES[contender] = list(new_includes)
    
    for k in ISA:
        if k != contender: ISA[k] = list({x if x not in flat else contender for x in get_isa_list(k)})
    for k in INCLUDES:
        if k != contender: INCLUDES[k] = list({x if x not in flat else contender for x in get_includes_list(k)})

    out = 'I infer that ' + ', '.join(flat)
    out += ', and %s are all names for the same thing, and I\'ll call it %s.' % (contender, contender)
    print(out)


def answer_why(x, y):
    '''Handles the answering of a Why question.'''
    # print(find_chain(x, y))
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    return

from functools import reduce
def report_chain(x, y):
    '''Returns a phrase that describes a chain of facts.'''
    orig = y
    if orig in SYN:
        y = SYN[y]
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    if len(chain) == 1:
        main_phrase = reduce(lambda x, y: x + y, map(report_link, chain))
        last_phrase = ''
    else:
        main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
        last_phrase = "and " + report_link(last_link)
    if orig in SYN:
        new_last_phrase = last_phrase + 'and %s is another name for %s.' % (orig, y)
    else:
        new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase

def report_link(link):
    '''Returns a phrase that describes one fact.'''
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y + ", "
    
def find_chain(x, z):
    '''Returns a list of lists, which each sublist representing a link.'''
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
                return temp

def add_syn(syn, contender):
    # loop for when synonym previously referenced in cycle.
    for k, v in SYN.items():
        if v == syn:
            SYN[k] = contender
    SYN[syn] = contender

def test() :
    process("A turtle is a reptile.")
    process("A turtle is a shelled-creature.")
    process("A reptile is an animal.")
    process("An animal is a thing.")

# test()
linneus()

