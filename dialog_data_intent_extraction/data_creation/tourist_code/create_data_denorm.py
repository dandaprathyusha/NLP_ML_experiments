from random import sample
from random import shuffle
import pickle


def create_train_denorm_from_samples():
    pickle_place_type_list = list()
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_place_type_pickle.dat', mode='rb') as file:
        pickle_place_type_list = pickle.load(file)

    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_place_pickle.dat', mode='rb') as file:
        pickle_place_list = pickle.load(file)

    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_type_pickle.dat', mode='rb') as file:
        pickle_type_list = pickle.load(file)
        '''
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text/train_creation_files/train_place_type_pickle.dat', mode='rb') as file:
        pickle_place_type_list = pickle.load(file)
    '''
    the_list = list()
    the_list.append(pickle_place_type_list)
    the_list.append(pickle_place_list)
    the_list.append(pickle_type_list)
    str_the_list = ['place_type', 'place', 'type']

    train_list_all = list()
    test_list_all = list()
    print(the_list)
    for num, item in enumerate(the_list):
        list_name = item
        print(item)
        train_indices_list = sample(range(len(list_name)), 3500)
        test_indices_list = sample(
            list(set(list(range(len(list_name)))) - set(train_indices_list)), 1500)
        train_list = [list_name[i] for i in train_indices_list]
        test_list = [list_name[i] for i in test_indices_list]
        train_list_all += train_list
        test_list_all += test_list


        output_file_trn = open(
            '/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_3500_' + str_the_list[num] + '.txt', 'w')
        output_file_tst = open(
            '/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_1500_' + str_the_list[num] + '.txt', 'w')
        output_file_trn.write(''.join(list(train_list)))
        output_file_tst.write(''.join(list(test_list)))

    print(len(train_list_all))
    shuffle(train_list_all)
    shuffle(test_list_all)

    all_output_file_trn = open(
        '/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_3500*4' + '.txt', 'w')
    all_output_file_tst = open(
        '/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_1500*4' + '.txt', 'w')
    all_output_file_trn.write(''.join(list(train_list_all)))
    all_output_file_tst.write(''.join(list(test_list_all)))

if __name__ == '__main__':
    create_train_denorm_from_samples()
