from datetime import date, datetime


def check_data(data: str | date):
    # переименовать
    if isinstance(data, str):
        data = datetime.strptime(data, "%Y-%m-%d").date()
    return data
