import requests
from datetime import datetime, timezone
import smtplib
import time

MY_LAT = 30.2672  # Your latitude
MY_LONG = -97.7431  # Your longitude

username = "xxxxxxxx"  # Your email
password = 'xxxxxxxx'  # Your email password or token
to_email = "xxxxxxxx"  # Email recipient


def is_iss_visible():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if ISS Latitude is within 5 degrees lat/long of local lat/long
    if abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get UTC time from local time to compare with UTC time from API
    time_now = datetime.now(timezone.utc)
    time_now_hour = time_now.hour

    if time_now_hour >= sunset or time_now_hour <= sunrise:
        return True


while True:
    if is_iss_visible() and is_night():
        connection = smtplib.SMTP('smtp.mail.yahoo.com')
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(from_addr=username, to_addrs=to_email,
                            msg=f"Subject: Look up!!\n\nThe ISS is visible, look up!")
        connection.close()
    time.sleep(60)
