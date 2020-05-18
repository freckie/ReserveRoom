import datetime

def is_available(reservations: list, target: tuple):
    for reservation in reservations:
        if ((target[0] > reservation[0]-datetime.timedelta(minutes=15)) and (target[0] < reservation[1]+datetime.timedelta(minutes=15))) 
        or ((target[1] < reservation[1]+datetime.timedelta(minutes=15)) and (target[1] > reservation[0]-datetime.timedelta(minutes=15)):
            return False
        elif (target[0] < reservation[0]-datetime.timedelta(minutes=15) and reservation[1] < target[1]+datetime.timedelta(minutes=15)):
            return False
    return True

