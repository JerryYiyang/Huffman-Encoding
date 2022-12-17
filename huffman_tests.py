
import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_decode_error(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode('hello.txt', 'hello_out.txt')

    def test_parse_header1(self):
        header_string = '97 3 98 4 99 2'
        freqlist = parse_header(header_string)
        self.assertEqual(freqlist[97:100], [3, 4, 2])


    def test_parse_header2(self):
        header_string = '89 5 90 2 92 3 93 5 94 2'
        freqlist = parse_header(header_string)
        self.assertEqual(freqlist[89:95], [5, 2, 0, 3, 5, 2])


    def test_01a_test_file1_parse_header(self):
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()        
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)
        
    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_02_test_file2_decode(self):
        huffman_decode("file2_compressed_soln.txt", "file2_decoded.txt")
        err = subprocess.call("diff -wb file2.txt file2_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_declaration_decode(self):
        huffman_decode("declaration_compressed_soln.txt", "declaration_decoded.txt")
        err = subprocess.call("diff -wb declaration.txt declaration_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_onechar_decode(self):
        huffman_decode("onechar_out_compressed.txt", "onechar_decoded.txt")
        err = subprocess.call("diff -wb onechar.txt onechar_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_samechar_decode(self):
        huffman_decode("samechar_out_compressed.txt", "samechar_decoded.txt")
        err = subprocess.call("diff -wb samechar.txt samechar_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_empty_decode(self):
        huffman_decode("empty_out_compressed.txt", "empty_decoded.txt")
        err = subprocess.call("diff -wb empty.txt empty_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)


    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)
        freqlist = cnt_freq('file1.txt')
        self.assertEqual(freqlist[ord('d')], 1)
        self.assertEqual(freqlist[ord('a')], 4)
        self.assertEqual(freqlist[ord('c')], 2)
        self.assertEqual(freqlist[ord(' ')], 3)
        self.assertEqual(freqlist[ord('b')], 3)
        with self.assertRaises(FileNotFoundError):
            cnt_freq('hello.txt')

        
    def test_lt_and_eq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertTrue(HuffmanNode(97, 8) < HuffmanNode(99, 10))
        self.assertTrue(HuffmanNode(97, 8) < HuffmanNode(99, 8))
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)
        self.assertEqual(HuffmanNode(97, 2), HuffmanNode(97, 2))
                    
                    
    def test_create_huff_tree(self):
        self.assertEqual(create_huff_tree([]), None)
        oneitem = [0] * 256
        oneitem[7] = 3
        create_huff_tree(oneitem)
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)


    def test_create_huff_tree1(self):
        freqlist = cnt_freq('file1.txt')
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.char, ord(' '))
        self.assertEqual(hufftree.freq, 13)

        
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        freqlist1 = cnt_freq('file1.txt')
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        self.assertEqual(create_header(freqlist1), '32 3 97 4 98 3 99 2 100 1')

        
    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertEqual(create_code(None), [''] * 256)

        
    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        #capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)


    def test_02_textfile(self):
        huffman_encode("file2.txt", "file2_out.txt")
        #capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)


    '''def test_03_textfile(self):
        huffman_encode("file_WAP.txt", "file_WAP_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file_WAP_out_compressed.txt file_WAP_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)'''


    def test_04_textfile(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call('diff -wb declaration_out.txt declaration_soln.txt', shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)


if __name__ == '__main__': 
   unittest.main()
