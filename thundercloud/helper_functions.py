from data_structures import BikeRecord


def get_average_speed(ride_data: list[BikeRecord]):
    sum_of_speed = sum(record.speed for record in ride_data)
    return sum_of_speed / len(ride_data) if ride_data else 0


def get_duration(ride_data: list[BikeRecord]):
    if len(ride_data) < 2:
        return 0
    return (ride_data[-1].timestamp - ride_data[0].timestamp) / 60
