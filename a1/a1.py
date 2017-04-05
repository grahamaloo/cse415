'''
Graham Kelly
4/5/2017
CSE 415 Spring 2017
A1 A:
A file of simple function declarations.
'''

def four_x_cubed_plus_one(x):
    '''prints passed 'x' cubed, times four, plus one'''
    print(4*x**3+1)

def mystery_code(string, offset=0):
    '''translates passed string to mystery code'''
    output = []
    for c in string:
        if str.isalpha(c):
            output.append(chr(translate(c, offset % 26 if offset >= 0 else offset % -26)))
        else:
            output.append(c)
    print(''.join(output))

def translate(c, offset):
    '''actually computes the translation for a single character (used in `mystery_code`)'''
    if str.isupper(c):
        new = 97 + ord(c) - 65 + offset - 2 #2 = fudge factor
        return new if new <= 122 and new >= 97 else 97 + new - 123 if new > 122 else 123 - 97 + new
    elif str.islower(c):
        new = 65 + ord(c) - 97 + offset - 2 #2 = fudge factor
        return new if new <= 90 and new >= 65 else 65 + new - 91 if new > 90 else 91 - 65 + new

def quintuples(l):
    '''breaks passed list into lists of length 5 (or less for remainder or if len is < 5)'''
    output = [l[i:i + 5] for i in range(0, len(l), 5)]
    print(output)

def past_tense(words):
    '''utilizes a set of simple rules to turn each (english) word in passed list to past tense'''
    output = []
    vowels = ['a', 'e', 'i', 'o', 'u',] # 'andsometimesy']
    c_exceptions = ['w', 'y']
    d_irregulars = {'have':'had',
                    'be': 'was',
                    'eat':'ate',
                    'go':'went'}
    for word in words:
        word = str.lower(word)
        if word in d_irregulars.keys(): #d
            output.append(d_irregulars[word])
        elif word[-1] is 'e': #a
            output.append(word + 'd')
        elif word[-1] is 'y' and word[-2] not in vowels: #b
            output.append(word[:-1] + 'ied')
        elif word[-2] in vowels and word[-1] not in vowels and word[-1] not in c_exceptions and word[-3] not in vowels: #c
            output.append(word + word[-1] + 'ed')
        else: #e
            output.append(word + 'ed')
    print(output)


    
