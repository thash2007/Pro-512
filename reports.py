from database import get_total_bookings_per_campus
from database import get_most_used_resources
from database import get_average_duration


def generate_summary():

    report = []

    report.append(
        "SMART CAMPUS REPORT"
    )

    report.append(
        "\nBOOKINGS PER CAMPUS"
    )

    for row in get_total_bookings_per_campus():

        report.append(
            f"{row[0]} : {row[1]}"
        )

    report.append(
        "\nMOST USED RESOURCES"
    )

    for row in get_most_used_resources():

        report.append(
            f"{row[0]} : {row[1]}"
        )

    average = get_average_duration()

    report.append(
        f"\nAverage Duration: {average[0]}"
    )

    return report