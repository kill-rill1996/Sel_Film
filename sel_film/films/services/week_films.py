import datetime


def read_id_from_log():
    log_id = {}
    default_films = [100, 101, 102, 103, 104, 105, 106]
    with open('logs/films/logs.log', 'r') as f:
        list_file = [row.split() for row in f if 'Искали фильм 1:' in row or 'Искали фильм 2:' in row]
        time_now = datetime.datetime.now()
        for log in list_file[::-1]:
            time = log[1] + log[2]
            time_dt = datetime.datetime.strptime(time, "%H:%M.%S%d.%m.%Y")
            if time_now - time_dt > datetime.timedelta(weeks=1):
                break
            film_id = log[8][0]
            if film_id in log_id:
                log_id[film_id] += 1
            else:
                log_id[film_id] = 1
    res = sorted(log_id.items(), key=lambda x: x[1], reverse=True)
    if len(res) < 7:
        for i in range((7 - len(res))):
            res.append((default_films[i], 1))
    return [x[0] for x in res]

