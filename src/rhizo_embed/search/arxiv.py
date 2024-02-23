import arxiv

def general_search(query, top_n=3):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
      query = query,
      max_results = top_n,
      sort_by = arxiv.SortCriterion.Relevance
    )
    return search.results()