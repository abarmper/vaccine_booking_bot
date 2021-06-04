# vaccine_booking_bot
Bot for automatic vaccination booking for emvolio.gov.gr




This code can be used for automated vaccine booking. If you want to be the first, this is the way!
Just fill your credentials below and the python program will take care things for you. You just have
the last word (by accepting the vaccine).

IMPORTANT: this code performs in an automated way all but the last step! So... don't worry.
When in the last step, the vaccine vacancy is "blocked" so that no other person can take it
(at least for 2 minutes). So, making the last step non-automated is not e problem.

This code is for the ages 18-29. In these ages, Astra Zeneca Vaccine is not admissioned. 
Consequently, the code dose not check that. It only checks NOT to select a single-dose vaccine.
In other words, it avoids single dose vaccines (like Johnson) and accepts all the double dose vaccines.
If you want to aply this algorithm in a larger age group where Astra Zeneca is allowd and you want to avoid
Astra Zeneca too, you will have to amend the code and check the date stamps. If the two apointments are
less than 50 days apart, then it is most probably not the Astra Zeneca and you are ok.

The code requires to have been loged in manually for at least one time in the past. 
(Because, the first time you ever log in it is a little different.)

REQUIREMENTS:
python3
pip3 (google search: "install python 3 and pip")
selenium (pip3 install selenium)
geckodriver https://github.com/mozilla/geckodriver )
Mozilla Firefox

USAGE:
python3 auto.py
OR
python3 auto.py 3 0
OR GENERALY
python3 auto.py arg1 arg2

The first argument "arg" ("3" above) determins the prefered date and time of the first and second apointment in the following fassion:
day = arg1 div 4
time = arg1 mod 4
ALL THESE PROVIDED THAT EVERY SLOT IS AVAILABLE

The second argument determins the vaccination senter from which to begin searching.

WHAT THE CODE DOES
The code logins and then checks for vacances. If it finds a vacancy, checks if that vacancy is sigle dose. 
If it is, returns and changes vaccination center to check again. If it scans throw all the vaccination centers and no
double dose vacancy is found, then it repeats and cycles throw all the vaccination centers for the given zip code, again.
This is usefull because one can let the program run before the new vacances for the double dose vaccines open so as as soon
as they become available, the script will automatically reserve one for you to press the final submit button.

Be sure to change the SLEEP_TIME according to your internet connection. You can test the code before to be sure it's ok.
SLEEP_TIME of 2 seconds should be ok for urban internet speeds.

