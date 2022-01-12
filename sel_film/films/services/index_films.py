import datetime as dt


def read_id_from_log():
    log_id = {}

    with open('logs/films/logs.log', 'r') as f:
        for row in f:
            if 'Искали фильм 1:' in row or 'Искали фильм 2:' in row:
                id = row.split()[8][0]
                if id in log_id:
                    log_id[id] += 1
                else:
                    log_id[id] = 1
    return sorted(log_id.items(), key=lambda x: x[1], reverse=True)




def count_of_films(log):
    pass

