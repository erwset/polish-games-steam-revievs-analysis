import steamreviews
# I used the steamreviews module to reviews gathering in json format
# https://github.com/woctezuma/download-steam-reviews

frame = pd.DataFrame(pd.read_csv("games.csv"))
app_ids = frame.iloc[:,0].tolist()
app_ids = np.unique(app_ids)
request_params = dict()
request_params['language'] = "english"


for i in app_ids:
    review_dict, query_count = steamreviews.download_reviews_for_app_id(i,
                                                                        chosen_request_params=request_params)


