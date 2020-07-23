# May need to go here accounts.google.com/DisplayUnlockCaptcha if doesn't work

def callback(*args, **kwargs):
    import smtplib

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(kwargs["SMTP_EMAIL"], kwargs["SMTP_PASSWORD"])


    results = None
    with open("/content/nohup.out", "r") as f:
        results = f.read()

    if results is not None:
        msg = "Colabocat Results:\\n $> {0}\\n\\n{1}".format(kwargs["HASHCAT_CMD"], results)
    else:
        msg = "Something went wrong when fetching the results..."

    server.sendmail(kwargs["SMTP_EMAIL"], kwargs["RESULTS_RECIPIENT"], kwargs["MESSAGE"])
    server.quit()
    