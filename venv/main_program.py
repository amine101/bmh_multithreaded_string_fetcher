import global_var
from sys import argv, exit
from comparer import Comparer
import bmh
import os
import threading

def calculate_NCT(Max_Mem_Size,NT):
    """
            This function calculates the worst case number of characters can be processed by each one of the threads
            (In the worst case, each UTF-8 Character is encoded in 4 bytes)
            (  to tackle eventual RAM MEMORY limitation when reading a file will consume memory larger than RAM )
            -Max_Mem_Size is on MB
     """
    return (Max_Mem_Size * 1000*1000)//(NT*4)

def calculate_s_position_next_substring(index,Nb_processed_blocs,last_s_position):
    """
            This function calculates the starting position of the substring to be read by a specific thread
            Each thread will process an exclusive single block/chunck of data from the main file
            The block is delimited by the number of characters rather than the number of bytes
    """
    if Nb_processed_blocs==0:
        return index*NCT
    else:
        return last_s_position+ TNC                                             # TNC=NCT*NT

def calculate_e_position_next_substring(index,Nb_processed_blocs, last_e_position):
    """
            This function calculates the ending position of the substring to be read by a specific thread
            e_position_ should go beyond the boundary  by M-1 characters in order to process the limit-case
    """
    if Nb_processed_blocs==0:
        return (index+1)*NCT+M-2
    else:
        return last_e_position+TNC                                              # TNC=NCT*NT

def thread_function(index):
    """
                In this function  the thread processes it's own chunk of data by reading it from the file object
                and attributing it to a variable text
    """
    Nb_processed_blocs=0                                                       #TODO : Nb_processed_blocs could be removed for more efficiency
    begin_pos=0
    end_pos=0                                                                  #TODO : end_pos could be removed for more efficiency
    print("Thread Nb:"+str(index)+" ************************************ ")
    while(1):
        begin_pos = calculate_s_position_next_substring(index, Nb_processed_blocs,begin_pos)
        end_pos = calculate_e_position_next_substring(index, Nb_processed_blocs,end_pos)
        print("Thread Nb: [" + str(index) + "]: bloc number[" + str(Nb_processed_blocs) + "]; Starting position=" + str(begin_pos) + "  Ending position=" + str(end_pos))
        length = end_pos - begin_pos + 1                                        # Length of the substring to be read from the file
        with open(path_to_the_text_file, 'r', encoding="utf-8") as f:           #TODO : open the file in the main thread and pass
                                                                                #        it to the threads without closing it
            f.seek(begin_pos)
            text = f.read(length)                                               # This method should be preferable for a file that can be single lined
        if len(text)==0:
            print("Thread Nb: [" + str(index) + "] EOF reached")
            return False                                                        # No more data, EOF reached
        r=bmh.run_bmh(table, text, pattern, M, compare)
        if(r>=0):
            print("Thread Nb: [" + str(index) + "] Pattern found after processing "+ str(Nb_processed_blocs+1) + " blocs")
            global_var.Match_found = True
            return True                                                         # Pattern found, stop the program
        elif r==-1 :
            Nb_processed_blocs+=1
            print("Thread Nb: [" + str(index) + "] Block processed (" + str(Nb_processed_blocs)+" blocs so far),  moving to the next block")
        else:
            print("Thread Nb: [" + str(index) + "] FORCED STOP")
            break



if __name__ == "__main__":
    try:
        path_to_the_text_file = argv[1]
        pattern = argv[2]
    except IndexError:
        print("usage: python main_program.py path_to_the_text_file string_to_be_found ")
        exit()
    NT=5                                         # Number of threads - Needs to be changed in accordance to performance
    Max_Mem_Size=1000                            # in MB : Maximum amount of memory to be extracted from the file by all the threads
                                                 #   ( Should be optimized in accordance with the available RAM memory and the type of
                                                 #   characters in the text file)
    NCT=calculate_NCT(Max_Mem_Size,NT)           # "worst case" number of characters that can be processed by each one of the threads
    TNC=NT*NCT                                   # total nmber of characters being processed by all threads

    #print(f"NCT (maximum Number of Characters per Thread)=" + str(NCT))

    M=len(pattern)

    #print("Size of the pattern: "+ str(M))

    print(f'Searching for "{pattern}" in "{path_to_the_text_file}" using BOYER MOORE HORSPOOL '
          f'algorithm under a multithreaded excecution paradigm (default number of threads is 5) ')
    print()
    compare = Comparer()
    table = bmh.precalc(pattern)                 # Preprocess the patern to extract the number of characters to shift by
                                                 # in the case of a mismatch

    print(f'Precomputed shift table: {dict(table)}')
    print()

    threads = list()
    for index in range(NT):
        print("Main    : create and start thread N°" + str(index))
        x = threading.Thread(target=thread_function, args=(index, ))
        threads.append(x)
        x.start()
    for x in threads:                             # Pause execution on the main thread by joining all of the running threads.
        x.join()
    if global_var.Match_found:
        print("The string is found in the TEXT _/")
    else:
        print("The string was not found in the TEXT X ")