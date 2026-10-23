class Booking:

    def __init__(
        self,
        username,
        campus,
        resource_id,
        booking_date,
        start_time,
        duration
    ):
        self.username = username
        self.campus = campus
        self.resource_id = resource_id
        self.booking_date = booking_date
        self.start_time = start_time
        self.duration = duration