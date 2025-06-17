"""This function notify_user takes two arguments: license_plate and speed. It simulates notifying a user about a violation by printing an alert message to the console. The message includes the license plate of the vehicle and the speed at which it was detected. While this is just a placeholder (printing to the console), the function could later be expanded to send notifications through other methods, such as emails, push notifications, or SMS, depending on the application's requirements.
"""

def notify_user(license_plate, speed):
    # For now, we just print the notification; this can be an email or push notification.
    print(f'ALERT: Violation detected! License Plate: {license_plate}, Speed: {speed} km/h')
