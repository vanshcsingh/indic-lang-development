# This module is to download x bytes from 

from indicnlp.tokenize import indic_tokenize
import codecs
import os 
import random
from ngram_splitter import ngram

'''
@Name:      open_x_features

@Desc:      will return a training set and test set of size described by params.
            It first shuffles the list of files in the provided language folder
            and then iterates the first x files such that the overall model set
            size is met.

@Params:    training_size:  size of trainign set to return
            lang_code:      language code
            flag:           If true, we extract words. Else, we extract n char grams
            n:              what char grams we are extracting 

@Return:    This will return a training set

            This will at least return a training set as large as specified by
            the training_size parameter. It may be off by one file's worth of
            words.

            If the size request is larger than the corpora can provide, it will
            return the maximum corpora's size.

            Also, the output is Non-Deterministic. Meaning with every call to
            open_x_features with the same parameters, it will not return the same
            output. 
'''
def open_x_features(training_size, lang_code, flag=True, n=2):
    
    # the language codes that this accepts
    corpora_dict = {'h': 'hindi', 'm': 'marathi', 'p': 'pali', 's':'sanskrit'}

    param_dir = corpora_dict[lang_code]

    random_files = os.listdir(param_dir)
    random.shuffle(random_files)

    overall_size = training_size
    
    feature_list = list()

    for _file in random_files:
        
        difference = overall_size - len(feature_list)

        with codecs.open(param_dir + '/' + _file, 'r', encoding='utf8') as f:

            data = f.read()
            data = data.replace('\r\n', ' ')

            tokenized = indic_tokenize.trivial_tokenize(data)


            working = tokenized if len(tokenized) <= difference else tokenized[:difference]

            if flag:
                feature_list.extend(working) 
            else:
                for word in working:
                    feature_list += ngram(word, n)


    return feature_list
