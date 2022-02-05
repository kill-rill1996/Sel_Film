import json


def get_points_by_year(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки за года"""
    year_1 = int(serial_1['year'][0])
    year_2 = int(serial_2['year'][0])
    current_year = int(current_serial['year'][0])

    if year_1 == year_2:
        if current_year == year_1:
            points = 13
        elif abs(current_year - year_1) == 1:
            points = 10
        elif abs(current_year - year_1) == 2:
            points = 8
        elif abs(current_year - year_1) == 3:
            points = 7
        else:
            points = 0
        return points
    else:
        if current_year in [year_1, year_2]:
            points = 11
        elif abs(current_year - year_1) == 1 or abs(current_year - year_2) == 1:
            points = 8
        elif abs(current_year - year_1) == 2 or abs(current_year - year_2) == 2:
            points = 6
        else:
            points = 0
        # SERIALS_POINTS[f'{current_serial["id"]}'] += points
        return points


# max 10
def get_points_by_duration(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки за продолжительность"""

    if serial_1['duration'] and serial_2['duration']:
        time_1 = serial_1['duration']
        time_2 = serial_2['duration']
    elif serial_1['duration'] or serial_2['duration']:
        for time in (serial_1['duration'], serial_2['duration']):
            if time:
                time_1 = time
        time_2 = 41.47
    else:
        time_1 = 41.47
        time_2 = 41.47

    average_duration = (time_1 + time_2) / 2
    points = 10 - abs(current_serial['duration'] - average_duration) * 0.2

    if points < 0:
        points = 0
    return points


# max 170
def get_points_by_genres(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки в соответствии с жанрами"""

    coinciding = list(set(serial_1['genres']) & set(serial_2['genres']))
    film1_genres = list(set(serial_1['genres']) - set(serial_2['genres']))
    film2_genres = list(set(serial_2['genres']) - set(serial_1['genres']))

    coinciding_count = 0
    film1_count = 0
    film2_count = 0

    if current_serial['genres']:
        for genre in current_serial['genres']:
            if genre in coinciding:
                coinciding_count += 1
            elif genre in film1_genres:
                film1_count += 1
            elif genre in film2_genres:
                film2_count += 1

        if film2_count and film1_count:
            points = (15 * coinciding_count * 1.5 ** coinciding_count) + \
                     (7 * film1_count * 1.3 ** film1_count) + \
                     (7 * film2_count * 1.3 ** film2_count)
        else:
            points = (12 * coinciding_count * 1.5 ** coinciding_count) + \
                     (5 * film1_count * 1.2 ** film1_count) + \
                     (5 * film2_count * 1.2 ** film2_count)
        if points > 170:
            points = 170
        return points
    return 0


# max 50
def get_points_by_country(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки за страну"""
    coinciding_countries = list(set(serial_1['countries']) & set(serial_2['countries']))
    film1_countries = list(set(serial_1['countries']) - set(serial_2['countries']))
    film2_countries = list(set(serial_2['countries']) - set(serial_1['countries']))

    coinciding_count = 0
    film1_count = 0
    film2_count = 0

    if current_serial['countries']:
        for country in current_serial['countries']:
            if country in coinciding_countries:
                coinciding_count += 1
            elif country in film1_countries:
                film1_count += 1
            elif country in film2_countries:
                film2_count += 1

        if film2_count and film1_count:
            points = (12 * coinciding_count * 1.5 ** coinciding_count) + \
                     (7 * film1_count * 1.3 ** film1_count) + \
                     (7 * film2_count * 1.3 ** film2_count)
        else:
            points = (12 * coinciding_count * 1.5 ** coinciding_count) + \
                     (5 * film1_count * 1.2 ** film1_count) + \
                     (5 * film2_count * 1.2 ** film2_count)
        if points > 50:
            points = 50
        return points
    return 0


# max 100
def get_points_by_directors(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки в соответствии с режиссером"""
    coinciding_directors = list(set(serial_1['directors']) & set(serial_2['directors']))
    film1_directors = list(set(serial_1['directors']) - set(serial_2['directors']))
    film2_directors = list(set(serial_2['directors']) - set(serial_1['directors']))

    coinciding_count = 0
    film1_count = 0
    film2_count = 0

    if current_serial['directors']:
        for director in current_serial['directors']:
            if director in coinciding_directors:
                coinciding_count += 1
            elif director in film1_directors:
                film1_count += 1
            elif director in film2_directors:
                film2_count += 1

    if film2_count and film1_count:
        points = (25 * coinciding_count * 1.5 ** coinciding_count) + \
                 (12 * film1_count * 1.3 ** film1_count) + \
                 (12 * film2_count * 1.3 ** film2_count)
    else:
        points = (25 * coinciding_count * 1.5 ** coinciding_count) + \
                 (10 * film1_count * 1.2 ** film1_count) + \
                 (10 * film2_count * 1.2 ** film2_count)
    if points > 150:
        points = 150
    return points


# max 100
def get_points_by_actors(serial_1, serial_2, current_serial) -> None:
    """Начисляет очки в соответствии с актерами"""
    coinciding_directors = list(set(serial_1['actors']) & set(serial_2['actors']))
    film1_directors = list(set(serial_1['actors']) - set(serial_2['actors']))
    film2_directors = list(set(serial_2['actors']) - set(serial_1['actors']))

    coinciding_count = 0
    film1_count = 0
    film2_count = 0

    if current_serial['actors']:
        for actor in current_serial['actors']:
            if actor in coinciding_directors:
                coinciding_count += 1
            elif actor in film1_directors:
                film1_count += 1
            elif actor in film2_directors:
                film2_count += 1

    if film2_count and film1_count:
        points = (10 * coinciding_count * 1.5 ** coinciding_count) + \
                 (7 * film1_count * 1.3 ** film1_count) + \
                 (7 * film2_count * 1.3 ** film2_count)

    else:
        points = (10 * coinciding_count * 1.5 ** coinciding_count) + \
                 (5 * film1_count * 1.2 ** film1_count) + \
                 (5 * film2_count * 1.2 ** film2_count)
    if points > 100:
        points = 100 + points / 100
    return points


def get_points_by_volume(serial_1, serial_2, current_serial):
    """Начисляет очки в зависимости от полного объема сериала (сезоны * серии)"""

    if serial_1['series'] and serial_2['series']:
        series_1 = serial_1['series']
        series_2 = serial_2['series']
    elif serial_1['series'] or serial_2['series']:
        for series in (serial_1['series'], serial_2['series']):
            if series:
                series_1 = series
        series_2 = 15
    else:
        series_1 = 15
        series_2 = 15

    average_duration = (series_1 + series_2) / 2
    if current_serial['series']:
        points = 10 - abs(current_serial['series'] - average_duration) * 0.2
    else:
        points = 10 - abs(15 - average_duration) * 0.2
    if points < 0:
        points = 0
    return points


def get_points_by_end_status(serial_1, serial_2, current_serial) -> None:
    points = 0
    if serial_1['end_status'] == serial_2['end_status']:
        if current_serial['end_status'] == serial_1['end_status']:
            points += 7
    else:
        points += 3
    return points


def get_objects() -> list:
    """Получает все фильмы"""
    with open('data/serials_info.json', 'r') as file:
        films = json.loads(file.read())
    return films[:2000]


def create_points_dict(films) -> dict:
    """Создает словарь (key - id сериала, value - кол-во очков)"""
    films_point_dict = {}
    for film in films:
        films_point_dict[f"{film['id']}"] = 0
    return films_point_dict


def get_serial_by_id(id, SERIALS) -> dict:
    """Получает объект по id и удаляет его из списка всех фильмов/сериалов"""
    for serial in SERIALS:
        if serial['id'] == id:
            return SERIALS.pop(SERIALS.index(serial))


def get_top_ten_serials(serials) -> list:
    """Возвращает лист из 12 кортежей (id, points)"""
    top_ten_list = []
    count = 0
    for k in sorted(serials, key=serials.get, reverse=True):
        if count == 12:
            break
        top_ten_list.append((k, serials[f'{k}']))
        count += 1
    return top_ten_list


def show_top_serials(serials, SERIALS_POINTS):
    top_ten = get_top_ten_serials(SERIALS_POINTS)
    top_serials_list = []
    for serial in serials:
        for serial_id, points in top_ten:
            if serial['id'] == int(serial_id):
                top_serials_list.append((serial, points))
    return sorted(top_serials_list, key=lambda x: x[1], reverse=True)


def find_serials(id_1, id_2):
    SERIALS = get_objects()
    SERIALS_POINTS = create_points_dict(SERIALS)

    # get searched serials
    serial_1 = get_serial_by_id(id_1, SERIALS)
    serial_2 = get_serial_by_id(id_2, SERIALS)

    # get points
    for current_serial in SERIALS:
        total_points = 0
        total_points += get_points_by_year(serial_1, serial_2, current_serial)
        total_points += get_points_by_duration(serial_1, serial_2, current_serial)
        total_points += get_points_by_genres(serial_1, serial_2, current_serial)
        total_points += get_points_by_country(serial_1, serial_2, current_serial)
        total_points += get_points_by_directors(serial_1, serial_2, current_serial)
        total_points += get_points_by_actors(serial_1, serial_2, current_serial)
        total_points += get_points_by_volume(serial_1, serial_2, current_serial)
        total_points += get_points_by_end_status(serial_1, serial_2, current_serial)

        if current_serial['rating']:
            total_points = total_points * (1 + (float(current_serial['rating']) - 7.0) * 0.07)
        #
        SERIALS_POINTS[f'{current_serial["id"]}'] += total_points

    return [id for id, _ in get_top_ten_serials(SERIALS_POINTS)]



