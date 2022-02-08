# Assignment 1

For Assignment 1 I have used the *Levenshtein distance* of all the words in the **Brikbeck** corpus with every word in **WordNet** corpus.
The task aims to find correct spelling of mis-spelled words in the Brikbeck corpus.

## Setup
To setup the environment which I used to create this project. Just run 
```
pip install -r requirements.txt
```

## Assumptions
The task of finding distance of one word against every other word is very unnecessary and time consuming. So I have a made the following assumptions to reduce the amount of time required to finish the analysis:
- Only those words who have atleast one character in common with the mis-spelled word are considered as contenders for correct spelling. This assumption holds for all the words that I manually investigated.
- tok-k words, based on distance can have more than k-words. All the words with same edit-distance are given the same rank.

## Preprocessing
The [corpus](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/0643) itself contains a lot of text files each with a slightly different rule to extract the incorrect and correct word pairing. So we used a processed version of the same corpus (src: [Roger-Milton (same author)](https://www.dcs.bbk.ac.uk/~roger/corpora.html)). This is just easier to read the ditonary from.

## Structuce
All the essential/useful functions have been added to the **utils folder** and the python script `assignment1.py` and the notebook `assignment1.ipynb` just uses these function to generate results.


## Parallelization 
Since the task to be performed is too intensive for one machine we need to parallelize the job distribution in a machine and across different machines as well. 

To parallelize the tasks across different cores a CPU, I used `concurency.futures` **ProcessPool** because the tasks are CPU intensive. (I also used Threading Pool but the process pool gave a better speed up so I used that finally). Whereas to parallelize the runs across multiple machines I used caching the function results to local-disk and then assembling all the results together in one disk to generate evaluations results.


