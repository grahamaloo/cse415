'''
Graham Kelly
4/5/2017
CSE 415 Spring 2017
A1 A:
A file of simple function declarations.
'''

def four_x_cubed_plus_one(x):
    print(4*x**3+1)

def mystery_code(string, offset=0):
    output = []
    for c in string:
        if str.isalpha(c):
            output.append(chr(translate(c, offset)))
        else:
            output.append(c)
    print(''.join(output))

def translate(c, offset):
    if str.isupper(c):
        new = 97 + ord(c) - 65 + offset - 2 #2 = fudge factor
        return new if new <= 122 else 97 + new - 123
    elif str.islower(c):
        new = 65 + ord(c) - 97 + offset - 2 #2 = fudge factor
        return new if new <= 90 else 65 + new - 91

def quintuples(l):
    output = [l[i:i + 5] for i in range(0, len(l), 5)]
    print(output)

def past_tense(words):
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


    
