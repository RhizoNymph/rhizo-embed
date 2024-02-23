from scholarly import scholarly, ProxyGenerator

def search_authors(author_name, top_n=3):
    print("Searching for {}".format(author_name))
    search_query = scholarly.search_author(author_name)
    authors = []
    for i in range(top_n):
        try:
            author = next(search_query)
            filled_author = scholarly.fill(author)
            
            for field in ["container_type", "filled", "source", "coauthors"]:
                if field in filled_author:
                    del filled_author[field]
            
            for field_list in ["publications"]:
                if field_list in filled_author:
                    for entry in filled_author[field_list]:
                        for field in ["container_type", "filled", "source"]:
                            if field in entry:
                                del entry[field]
            authors.append(filled_author)
        except:
            print("No more authors found")
            break

    print("Found {} authors".format(len(authors)))
    
    return authors

def search_pubs(pub_title, top_n=3):
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    
    print("Searching for {}".format(pub_title))
    search_query = scholarly.search_pubs(pub_title)
    pubs = []
    
    for i in range(top_n):
        try:
            pub = next(search_query)            
            
            for field in ["container_type", "filled", "source"]:
                if field in pub:
                    del pub[field]
            pubs.append(pub)
        except:
            print("No more publications found")
            break
            
    return pubs

