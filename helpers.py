import smtplib


def send_email(sender='123parsemail123@gmail.com', receivers=['visapprdv75@gmail.com','aiman.sokhall@gmail.com','danai.fournier@gmail.com','data.driven.wasp@gmail.com','aiman@aifi.com']):

    receivers_join = ', '.join(receivers)
    subject = 'IMPORTANT MESSAGE REGARDING YOUR VISA AIMAAAAAN '
    body = "Go now check the https://pprdv.interieur.gouv.fr/booking/create/948/1 \n\n- Yourself"

    email_text = f" \n From: {sender} \nTo: {receivers_join} \nSubject: {subject} \n\n {body}"

    print(email_text)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender, 'parsemail123')
        server.sendmail(sender, receivers, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(f'Something went wrong... \n{e}')
