import requests_with_caching #local to Coursera environment, need to change for general use
import json


# import requests

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
def get_movies_from_tastedive(tags_string):
    base_url = "https://tastedive.com/api/similar"
    params_dict = {}
    params_dict["q"] = tags_string
    params_dict["type"] = "movies"
    params_dict["limit"] = 5
    tastedive_response = requests_with_caching.get(base_url, params=params_dict)
    print(tastedive_response.url)
    print(type(tastedive_response))
    result = tastedive_response.json()
    print(type(result))
    print(result)
    print(result['Similar']['Results'][1]['Name'])
    five_returns = {}
    dict_list = []
    # if result[item_ref][item_ref_two][0]['Name'] != tags_string:
    for x in range(5):
        print("      ", result['Similar']['Results'][x]['Name'])
        dict_list.append(result['Similar']['Results'][x]['Name'])
    five_returns["Similar"] = dict_list
    """
    for item_ref in result:
        print("***Level 1***")
        print("  ", result[item_ref])
        for item_ref_two in result[item_ref]:
            print("***Level 2***")
            print("    ", result[item_ref][item_ref_two])
            for item_ref_three in result[item_ref][item_ref_two]:
                print("***Level 3***")
                dict_list = []
                if result[item_ref][item_ref_two][0]['Name'] != tags_string:
                    for x in range(5):
                        print("      ", result[item_ref][item_ref_two][x]['Name'])
                        dict_list.append(result[item_ref][item_ref_two][x]['Name'])
                five_returns["Similar"] = dict_list
    """
    print("*******Final Dict***********")
    print(five_returns)
    print("*******Final Dict***********")
    print(dict_list)
    return result

def extract_movie_titles(movie_dict):
    dict_list = []
    for x in range(5):
        print("      ", movie_dict['Similar']['Results'][x]['Name'])
        dict_list.append(movie_dict['Similar']['Results'][x]['Name'])
    print(dict_list)
    return dict_list

def get_related_titles(mov_lst):
    new_list = []
    for mov in mov_lst:
        print(mov)
        ret_lst = extract_movie_titles(get_movies_from_tastedive(mov))
        for item in ret_lst:
            if item not in new_list:
                new_list.append(item)
    print(new_list)
    return new_list

def get_movie_data(movie):
    base_url = "http://www.omdbapi.com/"
    params_dict = {}
    params_dict["t"] = movie
    params_dict["r"] = "json"
    OMBD_response = requests_with_caching.get(base_url, params = params_dict)
    print(OMBD_response.url)
    result = OMBD_response.json()
    return result

def get_movie_rating(mov_data):
    print(mov_data.keys())
    print("*****************")
    print(mov_data['Ratings'][1])
    score = 0
    if "Rotten Tomatoes" not in mov_data['Ratings'][1]['Source']:
        return score
    else:
        rot_tomat = (mov_data['Ratings'][1]['Value'])
        score = score + int(rot_tomat.replace("%", ""))
        print(type(score))
        print("********score*********")
        return score

def get_sorted_recommendations(movie_list):
    rel_list = get_related_titles(movie_list)
    print("*************sorting function*******")
    print(rel_list)
    for mov in rel_list:
        tomat_scor = []
        print(mov)
        ret_score = get_movie_rating(get_movie_data(mov))
        print(ret_score)
        tomat_scor.append(ret_score)
    print("*********after ret_score********")
    print(tomat_scor)
    return tomat_scor

'''
def get_movie_rating(mov_data):
    movie_rating = []
    print(mov_data.keys())
    print(mov_data.values())
    print(mov_data['Ratings'])
    print("********movie rating*********")
    print(mov_data['Ratings'][0])
    for dict in mov_data['Ratings']:
        print(dict)
    movie_rating.append(mov_data['Ratings'][1])
    print("***********appended**********")
    print(movie_rating)
    print("Rotten Tomatoes" in movie_rating[0]['Source'])
    score = 0
    if "Rotten Tomatoes" not in mov_data['Ratings'][1]['Source']:
        return score
    else:
        rot_tomat = (mov_data['Ratings'][1]['Value'])
        score = score + int(rot_tomat.replace("%", ""))
        print(type(score))
        print("********score*********")
        return score
'''