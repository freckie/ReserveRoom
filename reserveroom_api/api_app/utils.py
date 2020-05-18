import datetime

def is_available(reservations: list, target: tuple):
    for reservation in reservations:
        start_limit = reservation[0]-datetime.timedelta(minutes=15)
        end_limit = reservation[1]+datetime.timedelta(minutes=15)
        if (target[0] > start_limit and target[0] < end_limit) or (target[1] < end_limit and target[1] > start_limit):
            
            return False
        elif target[0] < start_limit and target[1] > end_limit:
            return False
    return True

