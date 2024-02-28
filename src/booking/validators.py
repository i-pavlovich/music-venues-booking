def is_correct_time_period(booking: dict) -> bool:
    if booking["check_in"] >= booking["check_out"]:
        return False
    return True
