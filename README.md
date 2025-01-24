Usage
git clone https://github.com/Abel-Tom/Interview-Scheduler.git
pip install -r requirements.txt
run migrations: python manage.py migrate
run the server: python manage.py runserver

To register a User

API: POST http://127.0.0.1:8000/auth/register/
payload: {
  'username': 'uniqueusername',
  'password' : 'Admin@123',
  'password2' : 'Admin@123',
  'email' : 'uniqueemail@gmail.com',
  'first_name': 'first_name',
  'last_name': 'last_name',
  'type': 'candidate'
}

user type can be 3 types:- 'candidate', 'manager', 'interviewer'
if you're running this locally for testing purposes no need to create any users. There are already existing users. You can login in as any of these users
{
  'username': 'cand1',
  'password': 'Admin@123'
}
type - candidate

{
  'username': 'int1',
  'password': 'Admin@123'
}
type - interviewer

{
  'username': 'manager1'
  'password': 'Admin@123'
}
type - manager

{
  'username': 'admin'
  'password': 'admin'
}
type - superuser


To login as manager, candidate or interviewer

API: POST http://127.0.0.1:8000/auth/login/
payload: {
  'username': 'int2',
  'password' : 'Admin@123'
}

The response will be refresh tokens and access tokens. 



To register a time slot

You need to put the access token in the request header as this is an authenticated view
Only interviewer and candidate user can register a time slot.
time should be given in 24 hour format
API: POST http://127.0.0.1:8000/register/
payload: {
  'start': '2025-01-26 9:00:00',
  'end' : '2025-01-26 12:00:00'
}

To get available time slots to schedule interview

You need to put the access token in the request header as this is an authenticated view
Only manager can get the available time slots of interviewer and the candidate
candidate and interviewer id should be given as the payload
API: GET http://127.0.0.1:8000/timeslots/

payload: {
  'candidate': '6',
  'interviewer' : '5'
}
response will be in this format 
[
 ['10:00 AM', '11:00 AM'],
 ['11:00 AM', '12:00 PM']
]

Assumptions made:
Only interviewer and candidate need to register a time slot
users will enter the start date and end date in 24 hour format
When manager requests available time slots time, only the time slots within that day will be shown.
Length of the interview slot is one hour. Time slots shorter than this are not counted

Need bonus points? Answer these questions.
1. Can you suggest a better solution to the above mentioned interview scheduling
problem?
Interviewer can register their availablility and the candidate can choose a suitable time based on the availablility of the interviewer there by freeing up HRManager's time.
3. If you had some more time how would you improve your solution?
   More filtering parameters:- Right now the manager can input candidate id and interviewer id and the time slots within the same day will be shown, tomorrow's time slots can only seen tomorrow. There's a need for a 3rd parameter date. Manager can input the date range
   time slots available within that date range will be shown. Right now only 1 hour long time slots will be shown. Time slots shorter than 1 hour which can useful for shorter interviews or introductory calls are not shown. A fourth parameter duration is needed. When
   this parameter is given, time slots of this duration will be shown.
   API to schedule the interview:- Manager can schedule the interview. Once the interview has been scheduled that block of time will be removed from both candidate's and interviewer's regisered time slot. A separate API will return the scheduled interviews.
   The candidate or the interviewer can cancel the interview if there are some unexpected events.
