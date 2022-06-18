from secrets import user
from g_service_helper import Create_Service
from googleapiclient.errors import HttpError
import datetime
import iso8601

api_name = "calendar"
api_version = "v3"



def main():
    """
    """
    try:
        service = Create_Service(user, api_name, api_version)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            print('No calendars found.')
            return

        eventlist = []
        for calendar in calendars:
            if calendar["id"] == 'en.usa#holiday@group.v.calendar.google.com': continue
            events_result = service.events().list(calendarId=calendar["id"], timeMin=now,
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime').execute()
            events = events_result.get('items', [])

            for event in events:
                eventlist.append(
                    {'start':event['start']['dateTime'], 
                    'end':event['end']['dateTime'],
                    'color':calendar['backgroundColor'],
                    'summary':event['summary']}
                    )
                
        
        eventlist.sort(key=lambda e:e['start'])
        current_event = eventlist[0]
        now = iso8601.parse_date(datetime.datetime.utcnow().isoformat())
        start = iso8601.parse_date(current_event['start'])
        end = iso8601.parse_date(current_event['end'])
        total = end - start
        elapsed = now - start
        left = end - now
        left = datetime.timedelta(seconds=left.seconds)
        left = datetime.timedelta(seconds=(left.seconds - left.seconds%60))
        left = str(left)
        left = left.removesuffix(':00')
        # for event in eventlist:
        #     print(event['start'], event['summary'])
        print(f"<tool>{left} left</tool><bar>{(elapsed/total)*100}</bar><txtclick>xdg-open https://calendar.google.com</txtclick><txt>  <span color='black' background='{current_event['color']}'> {current_event['summary']} </span>  </txt>")


    except HttpError as err:
        print(err)

if __name__ == '__main__':
    #beg = datetime.datetime.utcnow()
    main()
    #end = datetime.datetime.utcnow()
    #print(end - beg)

