# website-changes-monitoring

Bash script to do screenshots of website, uses webscreenshot,
followed by a python script that checks the changes and sends
an email to a gmail account. I use it with cron to email myself
if a website changes.

Don't forget to check the spam folder.

## Requirements

* The gmail account is allowed to use less secure services,
* The target mail in `check-diff-image-and-email.py` and a file `gmail_auth.txt` contains the 
  origin email and password, on two separate lines.
* One has installed `webscreenshot`, `PIL` and `numpy` with `pip install XXX`, as well as `smtplib`.
