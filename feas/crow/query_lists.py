import os


gts_file = '/data8T/ycf/project/data/Paris/gts'

def load_query_lists():
    query_lists = []
    for gt in os.listdir(gts_file):
        if gt.endswith('query.txt'):
            with open(os.path.join(gts_file, gt)) as ptr:
                for line in ptr:
                    query_lists.append(line.split(' ')[0])
    return query_lists

