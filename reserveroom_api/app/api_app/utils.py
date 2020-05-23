import datetime

def is_available(reservations: list, target: tuple):
    print(target)
    for reservation in reservations:
        start_limit = reservation[0]-datetime.timedelta(minutes=15)
        end_limit = reservation[1]+datetime.timedelta(minutes=15)
        print(start_limit)
        print(end_limit)
        if (target[0] > start_limit and target[0] < end_limit) or (target[1] < end_limit and target[1] > start_limit):
            print(1)
            return False
        if target[0] <= start_limit and target[1] >= end_limit:
            print(2)
            return False
    return True

