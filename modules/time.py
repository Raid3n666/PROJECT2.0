from datetime import datetime

class Date:

    def __init__(self, date) -> None:
        self.date = date
        def format_date():
            year = self.date[0:4]
            month = self.date[5:7]
            day = self.date[8:10]
            return f"{day}/{month}/{year}"
        self.formatted_date = format_date()
        def format_date_back():
            year = self.date[6:10]
            month = self.date[3:5]
            day = self.date[0:2]
            new_date = f'{year}-{month}-{day}'
            return new_date
        self.undo_formatting = format_date_back()

    def __str__(self) -> str:
        return self.date

    def get_todays_date(self):
        date = str(datetime.now())
        date = date[:10]
        return date

    def has_passed(self):
        today = Date(self.get_todays_date())
        date = datetime.strptime(self.formatted_date, "%d/%m/%Y").date()
        todays_date = datetime.strptime(today.formatted_date, "%d/%m/%Y").date()
        if date <= todays_date:
            return True
        else:
            return False
    

