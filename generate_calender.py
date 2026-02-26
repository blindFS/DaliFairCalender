import datetime
from borax.calendars.lunardate import LunarDate
from icalendar import Calendar, Event, vDuration

def create_calendar():
    cal = Calendar()

    # --- Standard Metadata ---
    cal.add('prodid', '-//Lunar Events Subscription//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'Lunar Events (三月街 & 银桥)')
    cal.add('x-wr-timezone', 'Asia/Shanghai')

    # --- Refresh Intervals (Half-Year / 182 Days) ---
    # X-PUBLISHED-TTL is the legacy/Microsoft standard
    cal.add('X-PUBLISHED-TTL', 'P182D') 
    # REFRESH-INTERVAL is the modern RFC 7986 standard
    cal.add('REFRESH-INTERVAL;VALUE=DURATION', 'P182D')

    current_year = datetime.datetime.now().year
    # We generate for the current year and the next year to ensure continuity
    years = [current_year, current_year + 1]

    # Your specific event days
    sanyuejie_days = [2, 9, 16, 23]
    yinqiao_days = [5, 13, 20, 28]

    for year in years:
        # Iterate through lunar months 1 to 12
        for month in range(1, 13):
            # Check for regular months AND leap months
            for is_leap in [False, True]:
                try:
                    # Generate 三月街 events
                    for day in sanyuejie_days:
                        lunar = LunarDate(year, month, day, is_leap)
                        add_to_cal(cal, lunar.to_solar_date(), "三月街")
                    # Generate 银桥 events
                    for day in yinqiao_days:
                        lunar = LunarDate(year, month, day, is_leap)
                        add_to_cal(cal, lunar.to_solar_date(), "银桥")
                except ValueError:
                    # This month/leap combination doesn't exist (very common)
                    continue

    # Write the file to the local directory
    with open('lunar_events.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Successfully generated lunar_events.ics with refresh headers.")

def add_to_cal(cal, date, summary):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', date)
    # Adding +1 day for the end date makes it a proper 'all-day' event in many clients
    event.add('dtend', date + datetime.timedelta(days=1))
    # Unique ID for each event based on date and name to prevent duplicates
    event.add('uid', f"{date.isoformat()}-{summary}@lunar-subscription")
    cal.add_component(event)

if __name__ == "__main__":
    create_calendar()
