import consump_schedule
import max_allow_overflow
import sqlite3
import csv


def select_powers():
    """function for getting user data about power generation from a temporary database,
    where 'power_s' - planned power generation of the power plant,
    block_s - planned power generation of power plants of industrial enterprises(block-stations)"""

    try:
        sqlite_connection = sqlite3.connect('temp_db.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT power_s, block_s from temp_db"""
        cursor.execute(sqlite_select_query)
        powers = cursor.fetchone()
        cursor.close()
        return powers

    except sqlite3.Error as error:
        print("Error when working with SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def deficit_x1(k_load_distrib=0.73):
    """function for calculation of the consumption deficit for the day x-1 (tomorrow)
    k_load_distrib - load distribution coefficient between the district and the power system, 0.73 by default"""

    p_consump = consump_schedule.consump_schedule_calc_x1()  # predicted consumption of the energy district
    load_transfer = consump_schedule.transfers_calc_x1()  # predicted value of the power transmitted from the district
    powers = select_powers()  # predicted values of generation capacity in the energy district
    p_power_station = powers[0]  # predicted value of generation capacity of the power plant
    p_power_ent = powers[1]  # predicted value of generation capacity of power plants of industrial enterprises

    deficit_x1_list = []
    for item in range(1, 25):
        max_overflow = max_allow_overflow.overflow_at_temperature_x1(item)
        deficit_1 = int((k_load_distrib * p_consump[item])) - max_overflow - load_transfer[item] \
            - p_power_station - p_power_ent
        deficit_x1_list.append(deficit_1)
    deficit_x1_dict = {x: y for x, y in zip(range(1, 25), deficit_x1_list)}

    with open('deficit.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        dict_csv = deficit_x1_dict.items()
        print(dict_csv)
        for k, v in deficit_x1_dict.items():
            writer.writerow([k, v])


def deficit_x2(k_load_distrib=0.73):
    """function for calculation of the consumption deficit for the day x-2 (day after tomorrow)
    k_load_distrib - load distribution coefficient between the district and the power system, 0.73 by default"""

    p_consump = consump_schedule.consump_schedule_calc_x2()  # predicted consumption of the energy district
    load_transfer = consump_schedule.transfers_calc_x2()  # predicted value of the power transmitted from the district
    powers = select_powers()  # predicted values of generation capacity in the energy district
    p_power_station = powers[0]  # predicted value of generation capacity of the power plant
    p_power_ent = powers[1]  # predicted value of generation capacity of power plants of industrial enterprises

    deficit_x2_list = []
    for item in range(1, 25):
        max_overflow = max_allow_overflow.overflow_at_temperature_x2(item)
        deficit_2 = int((k_load_distrib * p_consump[item])) - max_overflow - load_transfer[item] \
            - p_power_station - p_power_ent
        deficit_x2_list.append(deficit_2)
    deficit_x2_dict = {x: y for x, y in zip(range(1, 25), deficit_x2_list)}

    with open('deficit.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        dict_csv = deficit_x2_dict.items()
        print(dict_csv)
        for k, v in deficit_x2_dict.items():
            writer.writerow([k, v])


if __name__ == "__main__":
    deficit_x1()
    deficit_x2()
    select_powers()
