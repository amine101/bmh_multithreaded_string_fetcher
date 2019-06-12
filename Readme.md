# bmh_multithreaded_string_fetcher

This project provides a command-line implementation of  Boyer-Moore-Horspool algorithm in Python using multithreading paradigm, the program takes a path to a large file text and a pattern P to search for in the string ,and checks if the pattern matches exactly  a specific substring in the text or not .


## Boyer-Moore-Horspool
After studying the most famous exact string search algorithms (Brut force, Rabin Karp, Knuth Morris Pratt,Boyer Moore ... ), I found that Boyer Moore Horspool algorithm is not just one of the best efficient algorithms  for pattern search in a large texts with many alphabets, but it's also  easy to understand  and to implement.
    
The (complete) Boyer-Moore algorithm uses two heuristics in order to determine the shift distance of the pattern in case of a mismatch:
- The bad-character heuristic: try to find a bad character (from the text T) which is not matching with the pattern. When the mismatch has occurs, we shift the entire pattern forward until the mismatch becomes a match, otherwise, pattern moves backwards the bad character.
- The good-suffix heuristic        

While the Horspool algorithm uses only the bad-character heuristic but in a different way : 
If there is a mismatch, any one of the characters (from the text T) in the suffix can be used to perform the bad character heuristic (= shift)
(The Boyer-Moore algorithm always uses the mismatched character)

In other words, this algorithm prepares a shift table for each character in the pattern, representing the number of alignments that can be skipped when a mismatch occurs. The shift is given by the number of characters that occur after the last occurrence of a given character in the pattern.
The naïve algorithm is then run, with the exception that the string is matched from the right-hand side, and when a mismatch is found, the pattern is not shifted by one position, but rather by the value in the shift table corresponding to the character in the text lined up with the end of the pattern.

- Complexity of preprocessing the pattern P is  O(|P|) time.
- Worst case complexity is O(|T| |P|), but in the average case the runtime is O(|T|).
- The more alphabets we have and the larger the pattern is, the better performance we get.

## Usage

```bash
python main_program.py path_to_the_text_file string_to_be_found 
```

## Assumptions 
- The Text file is encoded in UTF-8 format and doesnt necessarily have ASCII characters, thus characters can have 1,2,3 or 4 bytes representation.  
- The Text file is of a large size (150-250 GB) and can be single lined. 
- No inter-thread blocking occurs when a thread reads from a specific subset of the file even when we have concurrency mode ( No I/O blocking ).
 


## Inspired by
[xsanda / string-matching](https://github.com/xsanda/string-matching)

[Akhtar Rasool et al. / International Journal on Computer Science and Engineering (IJCSE) / ](https://pdfs.semanticscholar.org/db88/1b63b73155e3fa8a99b5a4644d0a49ce5750.pdf?_ga=2.182993120.796037676.1560111262-1566878875.1560111262)

