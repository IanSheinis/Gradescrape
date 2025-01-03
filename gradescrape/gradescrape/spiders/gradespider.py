import scrapy
import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv

#TODO add function descriptions
#env
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
env_file = os.path.join(parent_dir, '.env')

load_dotenv(env_file)
gradescope_user = os.getenv('GRADESCOPE_USER')
gradescope_pass = os.getenv('GRADESCOPE_PASS')

SCOPES = ["https://www.googleapis.com/auth/calendar"]

#Google workspace
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        #Find credentials.json
        file_path = os.path.join(parent_dir, 'credentials.json')
        flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)  
        creds = flow.run_local_server(port=0)

    with open("token.json","w") as token:
        token.write(creds.to_json())

def createCalender(name, end_time):
    try:
        service = build("calendar", "v3", credentials=creds)

        start_time = end_time - dt.timedelta(hours=12)

        #If there is already an event do nothing
        if(event_exists(service, start_time, end_time, name)): return

        now_minutes = minutes_until_future_time(end_time)
        if now_minutes > 40320: now_minutes = 40320
        event = {
            'summary' : name,
            'start' : {
                'dateTime' : start_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end' : {
                'dateTime' : end_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'colorId' : "8", #dark gray
            "reminders": {
                "useDefault": False,
                "overrides": [
                {
                    "method": "popup",
                    "minutes": 1440 #one day
                },
                {
                    "method": "popup",
                    "minutes": now_minutes #gives a notification immediately
                }
                ]
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('id')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def minutes_until_future_time(future_datetime):
    """
    Calculate the number of minutes from the current time to a given future datetime.
    
    Parameters:
    - future_datetime (datetime): A future datetime object.
    
    Returns:
    - int: The number of minutes until the future datetime.
    """
    now = dt.datetime.now()
    if future_datetime <= now:
        raise ValueError("The provided datetime is not in the future.")
    
    time_difference = future_datetime - now
    return int(time_difference.total_seconds() // 60)

def event_exists(service, start_time, end_time, summary):
    """
    Check if an event with the same datetime and summary exists on the calendar.
    Args:
        service: Google Calendar API service object.
        start_time: Start time of the event to check.
        end_time: End time of the event to check.
        summary: The summary of the event to check.
    Returns:
        bool: True if the event exists, False otherwise.
    """
    time_min = start_time.isoformat() 
    time_max = end_time.isoformat() 
    
    events_result = service.events().list(
        calendarId= "primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True
    ).execute()

    events = events_result.get('items', [])
    
    for event in events:
        if event.get('summary') == summary:
            return True
    return False

class GradespiderSpider(scrapy.Spider):
    
    name = "gradespider"
    allowed_domains = ["gradescope.com"]
    start_urls = ["https://gradescope.com"]

    

    def parse(self, response):
        authenticity_token = response.css('input[name="authenticity_token"]::attr(value)').get()
        utf8 = response.css('input[name="utf8"]::attr(value)').get()

        login_data = {
            "authenticity_token": authenticity_token,
            "session[email]": gradescope_user,  
            "session[password]": gradescope_pass,       
            "utf8": utf8,
        }

        yield scrapy.FormRequest(
            url="https://www.gradescope.com/login",  
            formdata=login_data,
            callback=self.after_login,
        )

    def after_login(self, response):
        '''
        
        '''
        
        #TODO change to [1] after
        course_list = response.xpath('(//div[@class="courseList--term"])[1]/following-sibling::div[1]//a/@href').getall()

        for course in course_list:
            yield response.follow("https://www.gradescope.com" + course, callback = self.parse_course_page)

    def parse_course_page(self, response):
        '''
        Scrape names and due dates from all assignments
        '''

        #Course title
        course_title = response.css('h1.courseHeader--title::text').get()

        #Create a list of tuples where assignment name is first element and assignment due date is second element
        assignments = []

        #list of all rows of assignments
        rows = response.xpath('//table[@id="assignments-student-table"]/tbody/tr')

        for row in rows:
            name = row.xpath('.//th[@class="table--primaryLink"]/a/text()').get()
            due_date = row.xpath('.//time[contains(@class, "submissionTimeChart--dueDate")][1]/@datetime').get()

            if name and due_date:
                assignments.append((name.strip(), due_date.strip()))

        #Sort assignments by datetime from soonest to latest
        sorted_assignments = sorted(assignments, key=lambda x: dt.datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S %z'))
        sorted_assignments.reverse()

        #TODO Create notification that assignment was added
        for assignment in sorted_assignments:
            assignment_date = dt.datetime.strptime(assignment[1], '%Y-%m-%d %H:%M:%S %z')
            datetime_now = dt.datetime.now(tz=dt.timezone.utc)
            if(assignment_date > datetime_now):
                name = course_title + " " + assignment[0]
                createCalender(name, assignment_date)
            else:
                break
        
        
        