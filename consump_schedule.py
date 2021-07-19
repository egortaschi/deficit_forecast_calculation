import csv


def consump_schedule_calc_x1():
    """function for getting values of energy consumption of the district
    for each hour of the day x-1 (tomorrow)"""

    with open('initial_data/consumption_x1.csv') as file:
        csv_reader = csv.reader(file)
        dict_schedule = {}
        hour_increment = 1
        for hour in csv_reader:
            dict_schedule[hour_increment] = int(hour[0])
            hour_increment += 1

    p_consump = dict_schedule
    return p_consump


def transfers_calc_x1():
    """function for getting values of the load that can be transferred from the energy district
    for each hour of the day x-1 (tomorrow)"""

    with open('initial_data/load_transfer_x1.csv') as file:
        csv_reader = csv.reader(file)
        dict_transfers = {}
        hour_increment = 1
        for hour in csv_reader:
            dict_transfers[hour_increment] = int(hour[0])
            hour_increment += 1

    load_transfer = dict_transfers
    return load_transfer


def consump_schedule_calc_x2():
    """function for getting values of energy consumption of the district
    for each hour of the day x-2 (day after tomorrow)"""

    with open('initial_data/consumption_x2.csv') as file:
        csv_reader = csv.reader(file)
        dict_schedule = {}
        hour_increment = 1
        for hour in csv_reader:
            dict_schedule[hour_increment] = int(hour[0])
            hour_increment += 1

    p_consump = dict_schedule
    return p_consump


def transfers_calc_x2():
    """function for getting values of the load that can be transferred from the energy district
    for each hour of the day x-2 (day after tomorrow)"""

    with open('initial_data/load_transfer_x2.csv') as file:
        csv_reader = csv.reader(file)
        dict_transfers = {}
        hour_increment = 1
        for hour in csv_reader:
            dict_transfers[hour_increment] = int(hour[0])
            hour_increment += 1

    load_transfer = dict_transfers
    return load_transfer


if __name__ == "__main__":
    consump_schedule_calc_x1()
    consump_schedule_calc_x2()
    transfers_calc_x1()
    transfers_calc_x2()
