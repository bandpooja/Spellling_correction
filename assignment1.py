import concurrent.futures
import json
import nltk
import os
import pytrec_eval
import time
import tqdm

from utils.common_utils import return_top_1_5_10_words, return_success_at_k, find_closes_match

if __name__ == "__main__":
    # download the wordnet corpus
    nltk.download('wordnet')
    result_dir = r'Result'
    os.makedirs(result_dir, exist_ok=True)

    # with ZipFile('Data/0643.zip', 'r') as zipObj:
    #     zipObj.extractall()
    #
    # # There is just one file where there are incorrect words
    # f = open("ABODAT.643", "r")
    # data = []
    # count = 1

    correct_spellings = []
    incorrect_spellings = []
    file_ = open('Data/missp.dat', 'r')
    Lines = file_.readlines()

    # Strips the newline character
    crr_spell = ''
    icrr_spell = ''
    for line in Lines:
        if '$' in line:
            crr_spell = line.replace('$', '').replace('\n', '').lower()
        else:
            incrr_spell = line.lower().replace('\n', '')
            correct_spellings.append(crr_spell)
            incorrect_spellings.append(incrr_spell)

    incorrect_words = ['caugt', 'nit', 'siit', 'garl']
    # finiding matching words for 4 words without parallelization
    start = time.time()
    results = []
    for word in tqdm.tqdm(incorrect_words, desc='Without parallelization'):
        results.append(find_closes_match(word))
    print('#' * 60)
    print(f'Without parallelization the time taken is {round(time.time()-start, 4)} second(s)')
    print('#' * 60)
    del results
    print('\n')

    # finding matching words for 4 words with parallelization
    start = time.time()
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results.append(executor.map(find_closes_match, incorrect_words))
    print('#' * 60)
    print(f'With parallelization the time taken is {round(time.time() - start, 4)} second(s)')
    print('#' * 60)
    del results
    print('\n')

    results = []
    argument_list = [(icrr, crr) for icrr, crr in zip(incorrect_spellings, correct_spellings)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(return_top_1_5_10_words, argument_list):
            results.append(result)

    # # using multiprocessing threading pool
    # with ThreadPool() as pool:
    #     for result in pool.imap_unordered(save_top_1_5_10_15_words, argument_list):
    #         pass

    del argument_list

    success_at_k = return_success_at_k(results)

    query = {}
    results_eval = {}
    for result in results:
        query[result["incorrect"]] = {result["correct"]: 1}
        results_eval[result["incorrect"]] = {}
        for word in result[1]:
            results_eval[result["incorrect"]][word] = 1

        for word in result[5]:
            if word not in results_eval[result["incorrect"]].keys():
                results_eval[result["incorrect"]][word] = 1/5

        for word in result[10]:
            if word not in results_eval[result["incorrect"]].keys():
                results_eval[result["incorrect"]][word] = 1/10

    evaluator = pytrec_eval.RelevanceEvaluator(query, {'success'})

    print(json.dumps(evaluator.evaluate(results_eval), indent=1))
    eval = evaluator.evaluate(results_eval)

    for measure in sorted(list(eval[list(eval.keys())[0]].keys())):
        print(measure, 'average:',
              pytrec_eval.compute_aggregated_measure(
                  measure, [query_measures[measure] for query_measures in eval.values()])
              )
