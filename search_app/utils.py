def get_name(search_name, query):
    queryset = query.filter(movie_name__icontains=search_name)
    return queryset

def get_director(search_director, query):
    if query.filter(director__iexact=search_director).count() > 0:
        queryset = query.filter(director__iexact=search_director)
    else:
        msg = {'message': 'No data exists for this Director'}
        return msg
    return queryset

def get_rating(rating, query):
    if query.filter(imdb_rating__gte=rating).count() > 0:
        queryset = query.filter(imdb_rating__gte=rating)
    else:
        msg = {'message': 'No movies above this rating exists in the database'}
        return msg
    return queryset

def get_popularity(search_popularity, query):
    if query.filter(movie_popularity__gte=search_popularity).count() > 0:
        queryset = query.filter(movie_popularity__gte=search_popularity)
    else:
        return {'message': 'No movies above this popularity exists in the database'}
    return queryset

def get_genre(search_genre, query):
    if query.filter(genres__genre_name__iexact=search_genre).count() > 0:
        queryset = query.filter(genres__genre_name__iexact=search_genre)
    else:
        return {'message': 'No data exists for this Genre'}
    return queryset
