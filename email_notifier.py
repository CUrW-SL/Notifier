import pymysql.cursors
import pytz
from datetime import datetime
from datetime import timedelta

from config import DATABASE_CONFIG, SOURCES, FORECAST_DAYS
from config import NO_ALERT_MESSAGE, ALERT_MESSAGE, EMAIL_ALERT_TEMPLATE
from email_utils import send_email


def utc_to_sl(utc_dt):
    sl_timezone = pytz.timezone('Asia/Colombo')
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(tz=sl_timezone)


# Connect to the database.
connection = pymysql.connect(host=DATABASE_CONFIG['host'],
                             port=DATABASE_CONFIG['port'],
                             user=DATABASE_CONFIG['user'],
                             password=DATABASE_CONFIG['password'],
                             db=DATABASE_CONFIG['db'])

print("Successfully connected to %s database at cms-v1 (%s)." % (DATABASE_CONFIG['db'], DATABASE_CONFIG['host']))

try:
    # SQL query to get the end date of the last added run of the corresponding source.
    sql = "SELECT end_date FROM run_view WHERE source='%s' ORDER BY end_date DESC limit 1;"
    # Current date.
    now_date = utc_to_sl(datetime.now()).date()

    for source in SOURCES:

        print("###################### Checking %s Data Consistency on %s #####################" % (source, now_date))

        with connection.cursor() as cursor:

            # Execute query.
            sql_query = sql % source
            print("SQL query to be executed:", sql_query)
            cursor.execute(sql_query)

            # Last end_date recorded at the database.
            last_date_time = cursor.fetchone()[0]
            print("Last end date time recorded at the database against %s is:" % source, last_date_time)

            if isinstance(last_date_time, datetime):
                last_date = last_date_time.date()  # last recorded date
                time_delta = last_date - now_date
                print("Time  gap between the last recorded end_date and the current date:", time_delta)

                # if the time gap between the last recorded end_date in the 'run_view' table and the current date
                # is greater than the corresponding source's forecast days means models have run properly and data
                # is available in the 'curw' database.
                if timedelta(days=FORECAST_DAYS[source]) <= time_delta:
                    print(NO_ALERT_MESSAGE % (last_date, now_date, FORECAST_DAYS[source]))
                    print("Therefore no alert generation is required...")
                else:
                    alert_message = ALERT_MESSAGE % (last_date, now_date, FORECAST_DAYS[source])
                    print(alert_message)
                    print("Generating email alerts...")
                    send_email(run_source=source, checked_date=now_date,
                               msg=EMAIL_ALERT_TEMPLATE % (alert_message, source))

            else:
                # No last recorded end_date can be found for the source
                alert_message = "No last end_date found for the source %s." % source
                send_email(run_source=source, checked_date=now_date,
                           msg=EMAIL_ALERT_TEMPLATE % (alert_message, source))
            cursor.close()

except Exception as ex:
    print("Exception occurred while trying to run email_notifier: ", ex)

finally:
    # Close connection.
    connection.close()
