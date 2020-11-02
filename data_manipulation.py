import itertools


def convert(tup, di):
    '''
    convert tuples to dictionnary
    :param tup: list tuples
    :param di: empty dictionnary
    :return di: dictionnary
    '''
    di = dict(tup)
    return di



def get_allIdeas(results):
    '''
    Clean results and get full list of ideas
    :param results: form result in dictionnary format
    :return all_ideas: list of all original ideas
    '''
    all_results = []
    for key in results.keys():
        all_results.append(key.split('_')[0])
    all_ideas = all_results[1:]
    all_ideas_unique = list(set(all_ideas))
    return all_ideas_unique


def sort_results(results):
    '''
    Clean the results of the form and only keep the answers with 'yes' in order to update the database
    :param results: form result in dictionnary format
    :return novel: novel idea list
    :return original: original idea list
    :return feasible: feasible idea list

    '''
    novelAnswer = {}
    originalAnswer = {}
    feasibleAnswer = {}
    for key, value in results.items():
        if '1' in key.split('_'):
            novelAnswer[key.split('_')[0]] = value
        elif '2' in key.split('_'):
            originalAnswer[key.split('_')[0]] = value
        else:
            feasibleAnswer[key.split('_')[0]] = value
    novel = [key for key, val in novelAnswer.items() if val == 'yes']
    original = [key for key, val in originalAnswer.items() if val == 'yes']
    feasible = [key for key, val in feasibleAnswer.items() if val == 'yes']
    return novel, original, feasible
