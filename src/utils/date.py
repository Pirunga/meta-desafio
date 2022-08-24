from datetime import datetime

from dateutil import tz

UTC = tz.gettz('UTC')
HERE = tz.gettz('America/Sao_Paulo')


class Date:
    def try_parsing_date(self, date):
        """
        Try to convert data to datetime

        :param str date: value that will be converted
        """
        formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']

        for fmt in formats:
            try:
                return datetime.strptime(date, fmt).replace(tzinfo=UTC).astimezone(HERE)
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def datetime_now(self, is_string=False):
        """
        Get the current date

        :param bool is_string: se true convert a data para string
        """
        now = datetime.now().replace(tzinfo=UTC).astimezone(HERE)
        return now.strftime('%Y-%m-%d %H:%M:%S.%f') if is_string else now
