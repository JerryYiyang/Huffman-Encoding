from ordered_list import *
from math import isclose
from huffman_bit_writer import *
from huffman_bit_reader import *

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return (type(other) == HuffmanNode and self.char == other.char and
                self.freq == other.freq)
        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return less_than(self, other)

    '''def __repr__(self):
        return ('HuffmanNode(%d, %d)' % (self.char, self.freq))'''
    

def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    char_freq = [0] * 256
    try:
        with open(filename) as test:
            pass
    except FileNotFoundError:
        raise FileNotFoundError
    fle = open(filename, 'r')
    strline = ''
    for line in fle:
        strline += line
    for chars in strline:
        char_freq[ord(chars)] += 1
    fle.close()
    return char_freq

def less_than(x, y):
    if x.freq == y.freq:
        return x.char < y.char
    return x.freq < y.freq

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    ordered = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            temp = HuffmanNode(i, char_freq[i])
            ordered.add(temp)
    if ordered.size() == 0:
        return None
    while ordered.size() > 1:
        x = ordered.pop(0)
        y = ordered.pop(0)
        freq = x.freq + y.freq
        if x.char < y.char:
            top = HuffmanNode(x.char, freq)
        elif y.char < x.char:
            top = HuffmanNode(y.char, freq)
        top.left = x
        top.right = y
        ordered.add(top)
    return ordered.pop(0)

def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    lst = [''] * 256
    if node is not None:
        return code_help(node, lst, '')
    return lst

def code_help(node, lst, path):
    if is_leaf(node):
        lst[node.char] = path
    else:
        code_help(node.left, lst, path + '0')
        code_help(node.right, lst, path + '1')
    return lst

def is_leaf(node):
    if node.left is None and node.right is None:
        return True
    else:
        return False

def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    result = ''
    for i in range(256):
        if freqs[i] != 0:
            result += '%d %d ' % (i, freqs[i])
    return result.rstrip()

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    freqlist = cnt_freq(in_file)
    header = create_header(freqlist)
    code = encode_help(freqlist, in_file)
    output = header + '\n' + code
    output.strip()
    fileout = open(out_file, 'w')
    fileout.write(output)
    fileout.close()
    #compressed
    comp = out_file[:-4] + '_compressed.txt'
    c = HuffmanBitWriter(comp)
    c.write_str(header + '\n')
    c.write_code(code)
    c.close()

def encode_help(freqlist, in_file):
    infile = open(in_file, 'r')
    hufftree = create_huff_tree(freqlist)
    codes = create_code(hufftree)
    code = ''
    lines = ''
    for line in infile:
        lines += line
    infile.close()
    for x in lines:
        code += codes[ord(x)]
    return code


def parse_header(header_string):
    h = header_string.split()
    freqlist = [0] * 256
    asc = []
    freq = []
    for i in range(0, len(h), 2):
        asc.append(h[i])
    for i in range(1, len(h), 2):
        freq.append(h[i])
    for i in range(len(asc)):
        freqlist[int(asc[i])] = int(freq[i])
    return freqlist

def huffman_decode(encoded_file, decode_file):
    try:
        f = open(encoded_file, 'r')
        f.close()
    except FileNotFoundError:
        raise FileNotFoundError
    efile = HuffmanBitReader(encoded_file)
    header_string = efile.read_str()
    freqlist = parse_header(header_string)
    hufftree = create_huff_tree(freqlist)
    temp = hufftree
    h = header_string.split()
    if len(h) == 0:
        fileout = open(decode_file, 'w')
        fileout.close()
    char_count = 0
    for i in range(1, len(h), 2):
        char_count += int(h[i])
    if len(h) == 2:
        final = str(chr(int(h[0])) * int(h[1]))
        fout = open(decode_file, 'w')
        fout.write(final)
        fout.close()
        efile.close()
        return None
    chars = 0
    result = ''
    while chars < char_count:
        check = efile.read_bit()
        temp = traverse(temp, check)
        if is_leaf(temp):
            result += chr(temp.char)
            chars += 1
            temp = hufftree
    efile.close()
    fileout = open(decode_file, 'w')
    fileout.write(result)
    fileout.close()
    
def traverse(node, check):
    if check is False:
        return node.left
    else:
        return node.right
