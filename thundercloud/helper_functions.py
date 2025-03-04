from data_structures import BikeRecord
def find_average_speed(ride_data: list[BikeRecord]):
    sum_of_speed = sum(record.speed for record in ride_data)
    return sum_of_speed / len(ride_data) if ride_data else 0 