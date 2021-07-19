import sqlite3
import weather_forecast


def get_planned_scheme():
    """function for getting the planned
     network scheme specified by user"""

    con = sqlite3.connect('temp_db.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT scheme FROM temp_db")

    while True:
        row = cur.fetchone()
        str_row = ','.join([i for i in row])

        if row is None:
            break
        else:
            return str_row


def get_values_for_scheme():
    """function for obtaining the values of the maximum power flows
     from the database, depending on the planned network scheme (step - 5 degrees Celsius)"""

    plan_scheme = get_planned_scheme()
    if plan_scheme == 'Две ВЛ 220 кВ':
        con = sqlite3.connect('max_flows_db.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT t_m_5, t_0, t_p_5, t_p_10, t_p_15, t_p_20, t_p_25, t_p_30, t_p_35, t_p_40\
             FROM flows_at_temp WHERE id=3")

        while True:
            row = cur.fetchone()
            list_row = [int(i) for i in row]

            if row is None:
                break
            else:
                return list_row

    elif plan_scheme == 'Одна ВЛ 220 кВ':
        con = sqlite3.connect('max_flows_db.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT t_m_5, t_0, t_p_5, t_p_10, t_p_15, t_p_20, t_p_25, t_p_30, t_p_35, t_p_40\
             FROM flows_at_temp WHERE id=2")

        while True:
            row = cur.fetchone()
            list_row = [int(i) for i in row]

            if row is None:
                break
            else:
                return list_row
    else:
        print('База данных пуста')


def interpolating_values_of_scheme():
    """function for interpolating values
     of maximum overflows (step - 1 degree Celsius)"""

    initial_max_overflows = get_values_for_scheme()
    interpolated_max_overflows = []
    for i in range(len(initial_max_overflows)-1):
        increment = abs((initial_max_overflows[i+1] - initial_max_overflows[i])/5)
        interpolated_max_overflows.append(initial_max_overflows[i])
        j = 0
        while j < 4:
            interpolated_max_overflows.append(interpolated_max_overflows[len(interpolated_max_overflows)-1]-increment)
            j += 1
    interpolated_max_overflows.append(initial_max_overflows[len(initial_max_overflows)-1])
    interpolated_overflows_dict = dict(zip([temp for temp in range(-5, 41)], interpolated_max_overflows))
    return interpolated_overflows_dict


def overflow_at_temperature_x1(hour):
    """function for getting the maximum overflow
    for a specific hour of the day x-1 (tomorrow)"""

    overflow_list = interpolating_values_of_scheme()
    temperature_list = weather_forecast.make_temperature_list_x1()
    max_overflow_at_hour = overflow_list[temperature_list[hour]]
    return round(max_overflow_at_hour)


def overflow_at_temperature_x2(hour):
    """function for getting the maximum overflow
    for a specific hour of the day x-2 (day after tomorrow)"""

    overflow_list = interpolating_values_of_scheme()
    temperature_list = weather_forecast.make_temperature_list_x2()
    max_overflow_at_hour = overflow_list[temperature_list[hour]]
    return round(max_overflow_at_hour)


if __name__ == "__main__":
    # get_values_for_scheme()
    # interpolating_values_of_scheme()
    overflow_at_temperature_x1(1)
