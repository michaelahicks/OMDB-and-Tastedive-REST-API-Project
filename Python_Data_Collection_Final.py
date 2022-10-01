import requests_with_caching #local to Coursera environment, need to change for general use
import json

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
    return result

def extract_movie_titles(movie_dict):
    dict_list = []
    for x in range(5):
        print("      ", movie_dict['Similar']['Results'][x]['Name'])
        dict_list.append(movie_dict['Similar']['Results'][x]['Name'])
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
    score = 0
    print("********movie rating function*********")
    for dict in mov_data['Ratings']:
        if dict['Source'] == "Rotten Tomatoes":
            val = dict['Value']
            score = score + int(val.replace("%", ""))
            print(score)
    print("***********movie rating function exit**********")
    return score

def get_sorted_recommendations(movie_list):
    rel_list = get_related_titles(movie_list)
    print("*************sorting function*******")
    print(rel_list)
    tomat_scor = []
    reco_lst  = []
    for mov in rel_list:
        print(mov)
        ret_score = get_movie_rating(get_movie_data(mov))
        print("******sorted score*****")
        print(ret_score)
        tomat_scor.append(ret_score)
    mov_score = zip(rel_list, tomat_scor)
    print("*********after ret_score********")
    print(tomat_scor)
    print(rel_list)
    for tup in mov_score:
        #print(tup[1])
        reco_lst.append(tup)
    print(reco_lst)
    reco_lst = sorted(reco_lst, reverse=True, key = lambda x: (x[1], x[0]))
    print(reco_lst)
    final_lst_reco = []
    for tup in reco_lst:
        final_lst_reco.append(tup[0])
    print(final_lst_reco)
    return final_lst_reco

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
