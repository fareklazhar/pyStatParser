# http://bulba.sdsu.edu/jeanette/thesis/PennTags.html
TAGS = {
    'S',
    'SBAR',
    'SBARQ',
    'SINV',
    'SQ',
    'ADJP',
    'ADVP',
    'CONJP',
    'FRAG',
    'INTJ',
    'LST',
    'NAC',
    'NP',
    'NX',
    'PP',
    'PRN',
    'PRT',
    'QP',
    'RRC',
    'UCP',
    'VP',
    'WHADJP',
    'WHADVP',
    'WHNP',
    'WHPP',
    'CC',
    'CD',
    'DT',
    'EX',
    'FW',
    'IN',
    'JJ',
    'JJR',
    'JJS',
    'LS',
    'MD',
    'NN',
    'NNS',
    'NNP',
    'NNPS',
    'PDT',
    'POS',
    'PRP',
    'PRP$',
    'RB',
    'RBR',
    'RBS',
    'RP',
    'SYM',
    'TO',
    'UH',
    'VB',
    'VBD',
    'VBG',
    'VBN',
    'VBP',
    'VBZ',
    'WDT',
    'WP',
    'WP$',
    'WRB',
    '.',
    ',',
    ':',
    '-LRB-',
    '-RRB-',
    '``',
    "''",
    '#',
    '$',
    '',
    '-NONE-',
    'X',
}


def normalize_tag(tag):
    for sep in ('-', '=', '|'):
        i = tag.find(sep)
        if i > 0:
            return tag[:i]
    return tag


def normalize_word(word):
    return word.replace("\\/", '/')


TAG, SEPARATOR, WORD = 1, 2, 3
def parse_node(f, node, text):
    tag = []
    state = TAG
    while True:
        c = f.read(1) # default system buffering
        text.append(c)
        if c == '':
            raise Exception("Unexpected end of file")
        
        if state == TAG:
            if c.isspace():
                state = SEPARATOR
                tag = normalize_tag(''.join(tag))
                if tag not in TAGS:
                    raise Exception("Unrecognized tag: {%s}" % tag)
                node.append(tag)
            elif c == '(':
                # Handle starting ((
                state = SEPARATOR
                node.append('')
                branch = []
                node.append(branch)
                parse_node(f, branch, text)
            else:
                tag.append(c)
        
        elif state == SEPARATOR:
            if c.isspace():
                pass
            elif c == '(':
                branch = []
                node.append(branch)
                parse_node(f, branch, text)
            elif c == ')':
                break
            else:
                word = [c]
                state = WORD
        
        elif state == WORD:
            if c == ')':
                node.append(normalize_word(''.join(word)))
                break
            else:
                word.append(c)


def parse_treebank(file_path):
    f = open(file_path)
    text = None
    while True:
        try:
            c = f.read(1) # default system buffering
            if c == '': break
            
            if c == '(':
                tree = []
                text = [c]
                parse_node(f, tree, text)
                if tree[0] == '':
                    # Remove initial empty node from penn treebank
                    tree = tree[1]
                yield tree
        except Exception, e:
            print ''.join(text)
            print e
            import sys
            sys.exit()

REPLACEMENTS = (
    ('(` `)', '(`` ``)'),
    ("(' <)", "('' '')"),
    ('<', "'"),
    ('NPP', 'NP'),
    ('(! !)', '(. !)'),
    ('(? ?)', '(. ?)'),
)
def normalize_questionbank(in_path, out_path):
    with open(in_path) as original, open(out_path, 'w') as penn_norm:
        for line in original:
            for old, new in REPLACEMENTS:
                line = line.replace(old, new)
            penn_norm.write(line)
