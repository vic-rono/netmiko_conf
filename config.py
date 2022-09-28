import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler



ip = '192.168.122.72'


device_type = 'cisco_ios'


username = 'korir'
password = 'cisco'


command = 'show run'


#Connecting to the device via SSH
session = ConnectHandler(device_type = device_type, ip = ip, username = username, password = password, global_delay_factor = 3)
#global delay factor is for slow connections gives it time to load
#Entering enable mode
enable = session.enable()

#Sending the command and storing the output (running configuration)
output = session.send_command(command)

#Defining the file from yesterday, for comparison.
device_cfg_old = 'cfgfiles/' + ip + '_' + (datetime.date.today() - datetime.timedelta(days = 1)).isoformat()

#Writing the command output to a file for today.
with open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
    device_cfg_new.write(output + '\n')


#Extracting the differences between yesterday's and today's files in HTML format
with open(device_cfg_old, 'r') as old_file, open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday', todesc = 'Today')

    
#Sending the differences via email
#Defining the e-mail parameters
fromaddr = 'vicrontest@gmail.com'
toaddr = 'vicrontest@gmail.com'


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Configuration Management Report'
msg.attach(MIMEText(difference, 'html'))

#Sending the email via Gmail's SMTP server on port 465
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)



#Logging in to Gmail and sending the e-mail
server.login('vicrontest@gmail.com', 'mwcqoqpfrcjxkwac')
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()


