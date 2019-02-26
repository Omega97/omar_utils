""" Google Hash utils
26/2/2019
"""
from omar_utils.file_basics import *


def google_hash(solution, score_method, name='new_solution'):
    """"""
    # eval score of the solution
    score = score_method(solution)
    print('\nnew score =', score)

    # create dir with named "name" where the solution and score will be saved
    make_dir(name)

    # find prev max score
    list_ = list_files_in_dir(name)

    score_list = []
    v = [file_to_list(name + '/' + i) for i in list_]

    for i in v:
        try:
            score_list += [float(i[0].split()[-1])]
        except:
            pass

    create_new = False

    if len(score_list) > 0:
        max_score = max(score_list)
        print('prev max = ', max_score)
        if score > max_score:
            create_new = True

    id_ = len(list_) + 1
    if id_ == 1:
        create_new = True

    # create new file if the new solution is better then all the previous ones
    if create_new:
        print('\n New result! \n')
        write_file(name + '/' + str(id_) + '.sol',
                   'score = {:s}\n\n{:s}\n'.format(str(score), str(solution)))


if __name__ == "__main__":
    ...
