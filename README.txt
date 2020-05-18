Thomas Westra, Vihan Patel, Mistee Branchek
5/17/20
CSC_470
Final Project - Deliverable 1


Tasks:

    - T2: Implemented in the file T2.py
    - T3: Implemented in the file T3.py
    - T4: Implemented in the file T4.py
________________________________________________________
Deliverables:
    - D2: The train and test sets can be found in the directories "before" and "after". Each directory contains a train and test directory, which in turn contain a set of files. The files are split into the respective "before" and "after" directory based on whether they were published before or after the median published date. The files are further split up into "test" or "train" randomly, where each directory contains 1/10 and 9/10 of the total split files (i.e. if there are 10,000 files altogether, "before" contains 5,000, and "after contains 5,000. Each directory's"test" and train" contain 500 and 4500 files, respectively)
    
    - D3:
    T3 Analysis:
    
    T4 Analysis:
    
    - D4: 
    What was easy about this assignment? The easy part about this assignment was computing
    entropies and performing add-1 smoothing computations. Creating training and testing
    files were not very hard. 
    
    What was challenging about this assignment? The most challenging part about this 
    assignment was dealing with underflow. Although log space can be used to avoid
    underflow in many cases, it is not always ideal. Therefore, alternative methods
    were used when dealing with multiplication of probabilities. 
    
    What did you like about this assignment? I was able to build more knowledge
    about training a model and testing them on test sets. It is always interesting
    to see how well a model does in performing a certain task such as text classification. 
    
    What did you dislike about this assignment? There was not enough time given for
    this assignment to be done. This assignment could have been due on May 18 or 19. 
    Normally, we have no trouble completing projects on time.
    
    What did you learn from this assignment? I learned that certain 
    
________________________________________________________   
File List and Use Instructions:

    - README.txt: You are here.

    - T2.py: This file contains our implementation of the task described in T2. It will create 6 directories - two parent directories containing 2 children each. The four children contain the complete set of articles, after they have been split according to their category of test, train, before, or after. This program does need some input - it takes a command line argument, formatted as so: 
    *****python T2.py /path/to/json_folder /path/to/beforeSet /path/to/afterSet metadata.csv*****
    where /path/to/json_folder is the path to the directory containing all of the uncategorized articles, /path/to/beforeSet is the path to the directory where we would like to write our files that are before the median publishing date (this can already exist, but it doesn't have to), /path/to/afterSet is the path to the directory where we would like to write our files that are after the median publishing date (again, this can already exist, but it doesn't have to), and metadata.csv is of course the path to the csv file containing the metadata.

    - after: this directory contains two subdirectories, train and test, that contain the articles published after the median publishing date.
    
    - before: this directory, contains two subdirectories, train and test, that contain the articles published before the median publishing date.
    
    - T3.py: This file contains implementation of T3. It uses naive Bayes Text Classification to create a model which
    will be used when determining whether a certain text was written before, on or after a median date. This program takes
    two inputs. This is the format of the command line:
           python T3.py /path/to/beforeSet /path/to/afterSet
