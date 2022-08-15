from secrets import user
from g_service_helper import Create_Service
from googleapiclient.errors import HttpError
from datetime import date
import time
import pandas as pd

api_name = "tasks"
api_version = "v1"
delay = 0.1


def main():
    """
    """
    try:
        service = Create_Service(user, api_name, api_version, "task_credentials.json")
        if False:
            '''
            # ####################################3
            # #Supported Frequencies:
            # daily = None
            # weekly = None
            # every_two_weeks = None
            # montly = None
            # every_two_months = None
            # yearly = None

            # # Get task lists
            # results = service.tasklists().list().execute()
            # items = results.get('items', [])
            # if not items:
            #     print('No task lists found.')
            #     return

            # #Set task lists
            # for item in items:
            #     if item['title'] == "Daily":
            #         daily = item['id']
            #     elif item['title'] == "Weekly":
            #         weekly = item['id']
            #     elif item['title'] == "Every 2 Weeks":
            #         every_two_weeks = item['id']
            #     elif item['title'] == "Monthly":
            #         montly = item['id']
            #     elif item['title'] == "Every 2 Months":
            #         every_two_months = item['id']
            #     elif item['title'] == "Yearly":
            #         yearly = item['id']
            # things = 'Task,List\n'
            # service.tasks().clear(tasklist=daily).execute()
            # results = service.tasks().list(tasklist=daily).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Daily\n"

            # results = service.tasks().list(tasklist=weekly).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Weekly\n"

            # results = service.tasks().list(tasklist=every_two_weeks).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Every 2 Weeks\n"

            # results = service.tasks().list(tasklist=montly).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Monthly\n"

            # results = service.tasks().list(tasklist=every_two_months).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Every 2 Months\n"

            # results = service.tasks().list(tasklist=yearly).execute()
            # existing = results.get('items', [])
            # for x in existing:   
            #     things += f"{x['title'].rstrip()},Yearly\n"

            # with open("test.csv", 'w') as token:
            #     token.write(things)

            # quit()
            '''

        # Supported Frequencies:
        daily = None
        weekly = None
        every_two_weeks = None
        montly = None
        every_two_months = None
        yearly = None

        # Get task lists
        results = service.tasklists().list().execute()
        items = results.get('items', [])
        if not items:
            print('No task lists found.')
            return

        # Set task lists
        for item in items:
            if item['title'] == "Daily":
                daily = item['id']
            elif item['title'] == "Weekly":
                weekly = item['id']
            elif item['title'] == "Every 2 Weeks":
                every_two_weeks = item['id']
            elif item['title'] == "Monthly":
                montly = item['id']
            elif item['title'] == "Every 2 Months":
                every_two_months = item['id']
            elif item['title'] == "Yearly":
                yearly = item['id']

        # Get list of tasks
        df = pd.read_csv(f"user_info/tasklist_{user}.csv")
        # Set Tasks to lists, assume tasklist runs daily

        def fill_tasklist(list_name, list_id):
            list_tasks = [task for task in df[df["List"] == list_name]["Task"]]
            list_tasks.reverse()

            service.tasks().clear(tasklist=list_id).execute()
            results = service.tasks().list(tasklist=list_id, maxResults=100).execute()
            existing = results.get('items', [])
            for x in existing:
                x['status'] = "completed"
                results = service.tasks().update(
                    tasklist=list_id, task=x['id'], body=x).execute()
                time.sleep(delay)

            i = 0
            for task in list_tasks:
                service.tasks().insert(
                    tasklist=list_id, body={'title': task}).execute()
                i += 1
                print(f"{i}/{len(list_tasks)}")
                time.sleep(delay)
            service.tasks().insert(tasklist=list_id, body={'title': f"Updated on: {date.today().strftime('%A, %B %d, %Y')}"}).execute()
            print(f"{list_name} complete")

        # Daily runs every day
        fill_tasklist("Daily", daily)
        # Weekly runs every monday
        if date.today().weekday() == 0:
            fill_tasklist("Weekly", weekly)
        # e2w runs every monday that is odd
        if date.today().weekday() == 0 and date.today().isocalendar()[1] % 2 == 1:
            fill_tasklist("Every 2 Weeks", every_two_weeks)
        # montly runs the first of every month
        if date.today().day == 1:
            fill_tasklist("Monthly", montly)
        # e2months runs the first of every month that is odd
        if date.today().day == 1 and date.today().month % 2 == 1:
            fill_tasklist("Every 2 Months", every_two_months)
        # yearly runs the first of every year
        if date.today().day == 1 and date.today().month == 1:
            fill_tasklist("Yearly", yearly)

        print("done")
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
