from django import template

register = template.Library()


@register.filter(name='split_genres')
def split_genres(genre_list):
    if len(genre_list) > 0:
        genre_titles = [g.title for g in genre_list]
        genres = []
        if len(genre_titles) > 3:
            genre_titles = genre_titles[:3]
        for title in genre_titles:
            if genre_titles.index(title) + 1 != len(genre_titles):
                genres.append(title + ', ')
        return genres + [genre_titles.pop()]
    else:
        return ''


@register.filter(name='split_countries')
def split_countries(country_list):
    if len(country_list) > 0:
        countries_titles = [g.title for g in country_list]
        countries = []
        if len(countries_titles) > 3:
            countries_titles = countries_titles[:3]
        for title in countries_titles:
            if countries_titles.index(title) + 1 != len(countries_titles):
                countries.append(title + ', ')
        return countries + [countries_titles.pop()]
    else:
        return ''

