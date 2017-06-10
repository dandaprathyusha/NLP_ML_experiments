import sys
from random import sample
from itertools import product
from functools import reduce
import random
import pickle


def make_denorm(all_list):
    denorm_all_list = list()
    denorm_dict = dict()

    denorm_dict['naku'] = ['naku', 'naaku']
    denorm_dict['pradeshalu'] = [
        'pradeshalu', 'pradheshalu', 'pradeshaalu', 'pradheshaalu']
    denorm_dict['chudalani'] = ['chudalani', 'choodalani']
    denorm_dict['undi'] = ['undi', 'undhi']
    denorm_dict['pradeshalaki'] = [
        'pradeshalaki', 'pradheshalaki', 'pradeshaalaki', 'pradheshaalaki']
    denorm_dict['vellalanundi'] = ['vellalanundi', 'velalanundhi']
    denorm_dict['pranthalaki'] = ['pranthalaki', 'praanthalaki']
    denorm_dict['pranthalu'] = ['pranthalu', 'praanthalu']
    denorm_dict['chupinchu'] = ['chupinchu', 'choopinchu']
    denorm_dict['chudalanukuntunnanu'] = [
        'chudalanukuntunnanu', 'choodalanukuntunnanu']
    denorm_dict['daggarunna'] = ['daggarunna', 'dagarunna', 'daggaruna']
    denorm_dict['chuttupakkala'] = [
        'chuttupakkala', 'chuttupakala', 'chuttupakkalaa']
    denorm_dict['unna'] = ['unna', 'una']
    denorm_dict['sandarshinchalani'] = [
        'sandarshinchalani', 'sandharshinchalani']
    denorm_dict['ki'] = ['ki', 'ky']
    for all_list_item in all_list:
        words_all_list_item_list = all_list_item.split()
        index_values_list = list()
        for index_word, word in enumerate(words_all_list_item_list):
            if word in denorm_dict:
                values_list = denorm_dict[word]
                index_values_list.append(values_list)
            else:
                index_values_list.append([word])
        denorm_all_list += [' '.join(product_list_item)
                            for product_list_item in product(*index_values_list)]
    return denorm_all_list


def create_kb(input_file):
    f = open(input_file, 'r')
    place, area, place_type, place_open_time, address, phone, tour_time, rating = list(
    ), list(), list(), list(), list(), list(), list(), list()
    dict_kb = dict()
    for line in f.readlines():
        line = line.strip()
        k = list()
        k = line.split('\t')
        place.append(k[0])
        area.append(k[1])
        place_type.append(k[2])
        place_open_time.append(k[3])
        address.append(k[4])
        phone.append(k[5])
        tour_time.append(k[6])
        rating.append(k[7])
        dict_kb[k[0]] = k[1:]
#    print(place, area, place_type, place_open_time, address, phone, tour_time, rating)
    unique_place = list(set(place))
    unique_area = list(set(area))
    unique_place_type = list(set(place_type))
    unique_place_open_time = list(set(place_open_time))
    unique_address = list(set(address))
    unique_phone = list(set(phone))
    unique_tour_time = list(set(tour_time))
    unique_rating = list(set(rating))

    return unique_place, unique_area, unique_place_type, unique_place_open_time, unique_address, unique_phone, unique_tour_time, unique_rating
#    print(len(unique_place),len(unique_area),len(unique_place_type),len(unique_place_open_time),len(unique_address),len(unique_phone),len(unique_tour_time),len(unique_rating))
#   43 29 7 31 43 34 11 16


def generator_denorm_all_user_place_type(denorm_all_user_place_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user):
    for num, denorm_all_user_place_type_list_item in enumerate(denorm_all_user_place_type_list):
        place_type = list()
        for key, value in tags_place_dict.items():
            if key in denorm_all_user_place_type_list_item:
                place_type.append(value)
        for key, value in tags_type_dict.items():
            for item in value:
                if item in denorm_all_user_place_type_list_item:
                    place_type.append(key)
        substory_list = list()
        itr = 1
        substory_list.append(
            str(itr) + ' ' + denorm_all_user_place_type_list_item + "\t" + all_sys_responses_list[0])
        itr += 1
        substory_list.append(
            str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[3])
        itr += 1
#        print(tags_all_user_place_type_list[num])
        temp_string = str(itr) + ' ' + silence_user + '\tapi_call'
        for item in place_type:
            temp_string += ' ' + item
        substory_list.append(temp_string)
#        output_file.write('\n'.join(substory_list) + "\n\n")
        k = '\n'.join(substory_list) + "\n\n"
        yield k


def generator_denorm_all_user_place(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user):
    for denorm_all_user_place_list_item in denorm_all_user_place_list:
        for denorm_all_user_type_list_item in denorm_all_user_type_list:
            place_type = list()
            for key, value in tags_place_dict.items():
                if key in denorm_all_user_place_list_item:
                    place_type.append(value)
            for key, value in tags_type_dict.items():
                for item in value:
                    if item in denorm_all_user_type_list_item:
                        place_type.append(key)
            substory_list = list()
            itr = 1
            substory_list.append(str(
                itr) + ' ' + denorm_all_user_place_list_item + "\t" + all_sys_responses_list[0])
            itr += 1
            substory_list.append(
                str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[1])
            itr += 1
            substory_list.append(str(
                itr) + ' ' + denorm_all_user_type_list_item + "\t" + all_sys_responses_list[0])
            itr += 1
            substory_list.append(
                str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[3])
            itr += 1
            temp_string = str(itr) + ' ' + silence_user + '\tapi_call'
            for item in place_type:
                temp_string += ' ' + item
            substory_list.append(temp_string)
            k = '\n'.join(substory_list) + "\n\n"
#            output_file.write('\n'.join(substory_list) + "\n\n")
            yield k


def generator_denorm_all_user_type(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user):
    for denorm_all_user_type_list_item in denorm_all_user_type_list:
        for denorm_all_user_place_list_item in denorm_all_user_place_list:
            place_type = list()
            for key, value in tags_place_dict.items():
                if key in denorm_all_user_place_list_item:
                    place_type.append(value)
            for key, value in tags_type_dict.items():
                for item in value:
                    if item in denorm_all_user_type_list_item:
                        place_type.append(key)
            substory_list = list()
            itr = 1
            substory_list.append(str(
                itr) + ' ' + denorm_all_user_type_list_item + "\t" + all_sys_responses_list[0])
            itr += 1
            substory_list.append(
                str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[2])
            itr += 1
            substory_list.append(str(
                itr) + ' ' + denorm_all_user_place_list_item + "\t" + all_sys_responses_list[0])
            itr += 1
            substory_list.append(
                str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[3])
            itr += 1
            temp_string = str(itr) + ' ' + silence_user + '\tapi_call'
            for item in place_type:
                temp_string += ' ' + item
            substory_list.append(temp_string)
            k = '\n'.join(substory_list) + "\n\n"
#            output_file.write('\n'.join(substory_list) + "\n\n")
            yield k


def generator_denorm_all_user_none(denorm_all_user_none_list, denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user):
    for denorm_all_user_none_list_item in denorm_all_user_none_list:
        for denorm_all_user_place_list_item in denorm_all_user_place_list:
            for denorm_all_user_type_list_item in denorm_all_user_type_list:
                place_type = list()
                for key, value in tags_place_dict.items():
                    if key in denorm_all_user_place_list_item:
                        place_type.append(value)
                for key, value in tags_type_dict.items():
                    for item in value:
                        if item in denorm_all_user_type_list_item:
                            place_type.append(key)
                substory_list = list()
                itr = 1
                substory_list.append(
                    str(itr) + ' ' + denorm_all_user_none_list_item + "\t" + all_sys_responses_list[0])
                itr += 1
                substory_list.append(
                    str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[2])
                itr += 1
                substory_list.append(
                    str(itr) + ' ' + denorm_all_user_place_list_item + "\t" + all_sys_responses_list[0])
                itr += 1
                substory_list.append(
                    str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[1])
                itr += 1
                substory_list.append(
                    str(itr) + ' ' + denorm_all_user_type_list_item + "\t" + all_sys_responses_list[0])
                itr += 1
                substory_list.append(
                    str(itr) + ' ' + silence_user + "\t" + all_sys_responses_list[3])
                itr += 1
                temp_string = str(itr) + ' ' + silence_user + '\tapi_call'
                for item in place_type:
                    temp_string += ' ' + item
                substory_list.append(temp_string)
                k = '\n'.join(substory_list) + "\n\n"
#                output_file.write('\n'.join(substory_list) + "\n\n")
                yield k


def create_user_utterances(input_file):
    user_none_f = open(
        '/home/danda/research/memnet/tourist_data/te_none.txt', 'r')
    user_place_f = open(
        '/home/danda/research/memnet/tourist_data/te_place.txt', 'r')
    user_type_f = open(
        '/home/danda/research/memnet/tourist_data/te_type.txt', 'r')
    user_place_type_f = open(
        '/home/danda/research/memnet/tourist_data/te_place_type.txt', 'r')
    types_for_slot_filling_f = open(
        '/home/danda/research/memnet/tourist_data/te_type_of_place', 'r')
    sys_responses_f = open(
        '/home/danda/research/memnet/tourist_data/te_sys_responses.txt', 'r')

    all_sys_responses_list = readlines_to_list(sys_responses_f)
    types_for_slot_filling_list = readlines_to_list(types_for_slot_filling_f)
    all_user_none_list = readlines_to_list(user_none_f)
    user_place_list = readlines_to_list(user_place_f)
    user_type_list = readlines_to_list(user_type_f)
    user_place_type_list = readlines_to_list(user_place_type_f)
    silence_user = "<SILENCE>"

    unique_place, unique_area, unique_place_type, unique_place_open_time, unique_address, unique_phone, unique_tour_time, unique_rating = create_kb(
        input_file)

    tags_place_dict = dict()

#    unique_area = unique_area[16:]
#    types_for_slot_filling_list = types_for_slot_filling_list[14:]

    for unique_area_item in unique_area:
        tags_place_dict[unique_area_item] = unique_area_item.replace(' ', '_')

    tags_type_dict = dict()
    tags_type_dict['historical'] = ['historical', 'prachena', 'purathana']
    tags_type_dict['religious'] = ['religious', 'dharmika']
    tags_type_dict['museum'] = ['museum']
    tags_type_dict['lake'] = ['lake']
    tags_type_dict['garden'] = ['garden']
    tags_type_dict['zoo'] = ['zoo']
    tags_type_dict['amusement'] = ['amusement park']


    all_user_place_list = list()
    all_user_type_list = list()
    all_user_place_type_list = list()

    denorm_all_user_none_list = list()
    denorm_all_user_place_list = list()
    denorm_all_user_type_list = list()
    denorm_all_user_place_type_list = list()

    tags_all_user_place_type_list = list()

    for unique_area_item in unique_area:
        for user_place_list_item in user_place_list:
            all_user_place_list.append(
                user_place_list_item.replace("PLACE", unique_area_item))

    for types_for_slot_filling_list_item in types_for_slot_filling_list:
        for user_type_list_item in user_type_list:
            if "ki" in types_for_slot_filling_list_item and "TYPE_ki" in user_type_list_item:
                all_user_type_list.append(
                    user_type_list_item.replace("TYPE_ki", types_for_slot_filling_list_item))
            elif "ki" not in types_for_slot_filling_list_item and "TYPE_ki" not in user_type_list_item:
                all_user_type_list.append(
                    user_type_list_item.replace("TYPE", types_for_slot_filling_list_item))

    for unique_area_item in unique_area:
        for types_for_slot_filling_list_item in types_for_slot_filling_list:
            for user_place_type_list_item in user_place_type_list:
                place_type = list()
                if "ki" in types_for_slot_filling_list_item and "TYPE_ki" in user_place_type_list_item:
                    all_user_place_type_list.append(user_place_type_list_item.replace(
                        "TYPE_ki", types_for_slot_filling_list_item).replace("PLACE", unique_area_item))
                    for key, value in tags_place_dict.items():
                        if key is unique_area_item:
                            place_type.append(value)
                    for key, value in tags_type_dict.items():
                        for item in value:
                            if item in types_for_slot_filling_list_item:
                                place_type.append(key)
                    tags_all_user_place_type_list.append(place_type)
                elif "ki" not in types_for_slot_filling_list_item and "TYPE_ki" not in user_place_type_list_item:
                    all_user_place_type_list.append(user_place_type_list_item.replace(
                        "TYPE", types_for_slot_filling_list_item).replace("PLACE", unique_area_item))
                    for key, value in tags_place_dict.items():
                        if key is unique_area_item:
                            place_type.append(value)
                    for key, value in tags_type_dict.items():
                        for item in value:
                            if item in types_for_slot_filling_list_item:
                                place_type.append(key)

                    tags_all_user_place_type_list.append(place_type)

    denorm_all_user_none_list = make_denorm(all_user_none_list)
    denorm_all_user_type_list = make_denorm(all_user_type_list)
    denorm_all_user_place_list = make_denorm(all_user_place_list)
    denorm_all_user_place_type_list = make_denorm(all_user_place_type_list)

#    print(denorm_all_user_none_list)
#    print(tags_all_user_place_type_list)
#    print(all_user_none_list, all_user_place_list, all_user_type_list, all_user_place_type_list)

    story_list = list()
#    output_file = open('/home/danda/research/memnet/tourist_data/test_creation_files/te_stories.txt', 'w')
    output_file_trn = open('/home/danda/research/memnet/tourist_data/with_denormalised_text/test_creation_files/dialog-babi-task1-API-calls-te-trn.txt', 'w')
#    output_file_tst = open('/home/danda/research/memnet/tourist_data/with_denormalised_text/test_creation_files/dialog-babi-task1-API-calls-te-tst.txt', 'w')

    train_denorm_all_user_place_type = list()
    train_denorm_all_user_place = list()
    train_denorm_all_user_type = list()
    train_denorm_all_user_none = list()

    enu_generator_denorm_all_user_place = enumerate(generator_denorm_all_user_place(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user))
    enu_generator_denorm_all_user_place_len = len(list(enu_generator_denorm_all_user_place))
    enu_generator_denorm_all_user_place_sample_list = sample(range(enu_generator_denorm_all_user_place_len), 5000)
    train_denorm_all_user_place = (data for index, data in enumerate(generator_denorm_all_user_place(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user)) if index in enu_generator_denorm_all_user_place_sample_list)
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_place_pickle.dat', mode='wb') as file:
        pickle.dump(list(train_denorm_all_user_place), file)
    exit()

    '''
    output_file_trn.write(''.join(list(train_denorm_all_user_place)) + "\n\n")
    enu_generator_denorm_all_user_place_type = enumerate(generator_denorm_all_user_place_type(denorm_all_user_place_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user))
    enu_generator_denorm_all_user_place_type_len = len(list(enu_generator_denorm_all_user_place_type))
    enu_generator_denorm_all_user_place_type_sample_list = sample(range(enu_generator_denorm_all_user_place_type_len), 5000)
    train_denorm_all_user_place_type = (data for index, data in enumerate(generator_denorm_all_user_place_type(denorm_all_user_place_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user)) if index in enu_generator_denorm_all_user_place_type_sample_list)
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_place_type_pickle.dat', mode='wb') as file:
        pickle.dump(list(train_denorm_all_user_place_type), file)

    output_file_trn.write(''.join(list(train_denorm_all_user_place_type)) + "\n\n")



    enu_generator_denorm_all_user_type = enumerate(generator_denorm_all_user_type(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user))
    enu_generator_denorm_all_user_type_len = len(list(enu_generator_denorm_all_user_type))
    enu_generator_denorm_all_user_type_sample_list = sample(range(enu_generator_denorm_all_user_type_len), 5000)

    train_denorm_all_user_type = (data for index, data in enumerate(generator_denorm_all_user_type(denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user)) if index in enu_generator_denorm_all_user_type_sample_list)
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text_all/test_creation_files/test_type_pickle.dat', mode='wb') as file:
        pickle.dump(list(train_denorm_all_user_type), file)
    print(list(train_denorm_all_user_type))





    output_file_trn.write(''.join(list(train_denorm_all_user_type)) + "\n\n")

    enu_generator_denorm_all_user_none = enumerate(generator_denorm_all_user_none(denorm_all_user_none_list, denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user))
    enu_generator_denorm_all_user_none_len = len(list(enu_generator_denorm_all_user_none))
    enu_generator_denorm_all_user_none_sample_list = sample(range(enu_generator_denorm_all_user_none_len), 5000)

    train_denorm_all_user_none = (data for index, data in enumerate(generator_denorm_all_user_none(denorm_all_user_none_list, denorm_all_user_place_list, denorm_all_user_type_list, tags_place_dict, tags_type_dict, all_sys_responses_list, silence_user)) if index in enu_generator_denorm_all_user_none_sample_list)
    with open('/home/danda/research/memnet/tourist_data/with_denormalised_text/test_creation_files/train_none_pickle.dat', mode='wb') as file:
        pickle.dump(list(train_denorm_all_user_none), file)
    output_file_trn.write(''.join(list(train_denorm_all_user_none)) + "\n\n")
    print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    exit()
'''






'''
#    story_list = train_denorm_all_user_place_type + train_denorm_all_user_place + train_denorm_all_user_type +train_denorm_all_user_none

#int(0.75*len(story_list))
#    train_stories_indices_list = sample(range(len(story_list)), 20000)
 #   test_stories_indices_list = sample(list(set(list(range(len(story_list)))) - set(train_stories_indices_list)), 5000)
#    train_stories_list = [story_list[i] for i in train_stories_indices_list]
#    test_stories_list = [story_list[i] for i in test_stories_indices_list]

#    output_file_trn.write('\n'.join(['\n'.join(train_stories_list_item) + "\n" for train_stories_list_item in train_stories_list]) + "\n\n")
#    output_file_tst.write('\n'.join(['\n'.join(test_stories_list_item) + "\n" for test_stories_list_item in test_stories_list]) + "\n\n")
#    print(len(story_list))

'''


def readlines_to_list(pointer_file):
    final_list = list()
    for line in pointer_file.readlines():
        final_list.append(line.strip())
    return final_list


if __name__ == '__main__':
    create_user_utterances(sys.argv[1])
