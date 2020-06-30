from search_book import get_matched_books

def unit_test_util():
    list_of_queries = ['is your problems',
                       'Rules for a Knight',
                       'skills three better',
                       'great you from']

    query_summary_ids = [0, 43, 54, 52]  # 1st top summary id of 3 top summaries.
    no_of_results = 3

    for index, query in enumerate(list_of_queries):
        result = get_matched_books([query], no_of_results)

        print("Assert Equal ", (result[0]['id'] == query_summary_ids[index]))
        print("Assert Equal ", (len(result) == 3))

unit_test_util()



