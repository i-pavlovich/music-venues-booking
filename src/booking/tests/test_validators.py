from datetime import datetime, timedelta

from ..validators import is_correct_time_period


def test_is_correct_time_period_validator():
    booking = {
        "check_in": datetime.utcnow(),
        "check_out": datetime.utcnow() + timedelta(hours=3),
    }
    assert is_correct_time_period(booking) == True
    booking["check_in"] += timedelta(days=7)
    assert is_correct_time_period(booking) == False
    booking["check_in"] = booking["check_out"]
    assert is_correct_time_period(booking) == False
