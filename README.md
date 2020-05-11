Thomas Westra, Vihan Patel, Mistee Branchek
5/17/20
CSC_470
Final Project - Deliverable 1


Tasks:

    - T2: Implemented in the file T2.py
    - T3:
    - T4:
________________________________________________________
Deliverables:

    - D1:
    - D2: The train and test sets can be found in the directories "before" and "after". Each directory contains a train and test directory, which in turn contain a set of files. The files are split into the respective "before" and "after" directory based on whether they were published before or after the median published date. The files are further split up into "test" or "train" randomly, where each directory contains 1/10 and 9/10 of the total split files (i.e. if there are 10,000 files altogether, "before" contains 5,000, and "after contains 5,000. Each directory's"test" and train" contain 500 and 4500 files, respectively)
    - D3:
    - D4:
________________________________________________________   
File List and Use Instructions:

    - README.md: You are here.

    - T2.py: This file contains our implementation of the task described in T2. It will create 6 directories - two parent directories containing 2 children each. The four children contain the complete set of articles, after they have been split according to their category of test, train, before, or after. This program does need some input - it takes a command line argument, formatted as so: 
    *****python T2.py /path/to/json_folder /path/to/beforeSet /path/to/afterSet metadata.csv*****
    where /path/to/json_folder is the path to the directory containing all of the uncategorized articles, /path/to/beforeSet is the path to the directory where we would like to write our files that are before the median publishing date (this can already exist, but it doesn't have to), /path/to/afterSet is the path to the directory where we would like to write our files that are after the median publishing date (again, this can already exist, but it doesn't have to), and metadata.csv is of course the path to the csv file containing the metadata.

    - after: this directory contains two subdirectories, train and test, that contain the articles published after the median publishing date.
    
    - before: this directory, contains two subdirectories, train and test, that contain the articles published before the median publishing date.
    
