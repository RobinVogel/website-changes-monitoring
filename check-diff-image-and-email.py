# Parts of this script originate from:
# https://stackoverflow.com/questions/189943/how-can-i-quantify-difference-between-two-images
import sys
import datetime
from PIL import Image
import numpy as np

GMAIL_LOGIN_LOC = "gmail_auth.txt"
RECEIVER = "receiver@gmail.com"


def send_email(content, receiver=RECEIVER,
               subject="automated message"):
    with open(GMAIL_LOGIN_LOC, "rt") as f:
        login, password = f.read().split("\n")[:2]

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(content))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(login, password)
    mailserver.sendmail(login, receiver, msg.as_string())
    mailserver.quit()


def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = np.sum(np.abs(diff))  # Manhattan norm
    z_norm = np.linalg.norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)


def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        # average over the last axis (color channels)
        return np.mean(arr, axis=-1)  
    else:
        return arr


def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def imread(s):
    return np.array(Image.open(s))


def main():
    site_no = sys.argv[1]
    site_name = sys.argv[2]

    img_new = imread("monitor_{}/new.jpg".format(site_no)).astype(float)
    img_old = imread("monitor_{}/old.jpg".format(site_no)).astype(float)

    # compare
    n_m, n_0 = compare_images(img_old, img_new)
    print(site_name)
    print("Manhattan norm:", n_m, "/ per pixel:", n_m/img_old.size)
    print("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img_old.size)
    change_magnitude = n_m/img_old.size
    epsilon = np.finfo(np.float32).eps

    if change_magnitude > epsilon:
        msg = ("Changes detected on {}, ".format(site_name)
               + "magnitude is {}.\n".format(change_magnitude)
               + "Time is: {}".format(datetime.datetime.now()))
        send_email(msg,
                   subject="{} changed !".format(site_name))
        print("Email sent !")


if __name__ == "__main__":
    main()
