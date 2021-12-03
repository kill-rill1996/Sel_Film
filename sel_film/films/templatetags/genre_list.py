from django import template

register = template.Library()


@register.filter(name='split_genres')
def split_genres(genre_list):
    genre_titles = [g.title for g in genre_list]
    genres = []
    for title in genre_titles:
        if genre_titles.index(title) + 1 != len(genre_titles):
            genres.append(title + ', ')
    return genres + [genre_titles.pop()]