import serial, time, smtplib, gspread, csv, socket
import requests, json, urllib
import pytextnow
import timeit
from datetime import datetime
from gpiozero import CPUTemperature

#Email stuff

SMTP_SERVER = 'smtp.gmail.com'              #Email Server (don't change!)
SMTP_PORT = 587                             #Server Port (don't change!)
GMAIL_USERNAME = 'voltmeterazgfd@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'asuEPICS2021'             #change this to match your gmail password
emailSubject = "SMS Alert"

MAX_VOLTS = 130.0
MIN_VOLTS = 110.0

MAX_FREQ = 65.0
MIN_FREQ = 55.0

# ~ address1 = '6026863778@vtext.com'
# ~ address2 = '6026153692@vtext.com'
number1 = "6026153692"
number2 = "3162109128"

# ~ class Emailer:
    # ~ def sendmail(self, recipient, subject, content):

        # ~ #Create Headers
        # ~ headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   # ~ "MIME-Version: 1.0", "Content-Type: text/html"]
        # ~ headers = "\r\n".join(headers)
 
        # ~ #Connect to Gmail Server
        # ~ session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # ~ session.ehlo()
        # ~ session.starttls()
        # ~ session.ehlo()

        # ~ #Login to Gmail
        # ~ session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
 
        # ~ #Send Email & Exit
        # ~ session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        # ~ session.quit

# ~ sender = Emailer()

# ~ def sendTexts(subject, content):
	# ~ # uncomment the following lines after putting a valid address for the corresponding address variables
	
	# ~ sender.sendmail(address1, subject, content)
	# ~ sender.sendmail(address2, subject, content)
	# ~ #sender.sendmail(address3, subject, content)
	# ~ pass


# textnow
client = pytextnow.Client("voltmeterazgfd", "s%3As2im46Bq2CRkNHKNg1hLf6iJLG_dFoD3.Ff1minkuVvQfxYKlZQYea7KbW9nOHjjuUbVy%2Bokt%2BUs", "s%3AdGOyx3y6WK07laRLUcb7yPbU.n2nJeTvOcL7iNWR0JqCWV5hBlkb2PX1UxqOcWu2foKw")

# setup access to spreadsheet
gc = gspread.service_account(filename='/home/pi/Documents/credentials.json')
sh = gc.open_by_key('1_RyT4Af2-h3I4QhH54W8xKC2mMbebXPHp1qDH9N4BL8')

def getDateTime():
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
	return dt_string
	

def updateSheet(info):
	# find next available row on the spreadsheet
	worksheet = sh.sheet1
	str_list = list(filter(None, worksheet.col_values(1)))
	n = len(str_list)+1
	
	# insert the info into the empty row
	worksheet.insert_row(info, n)
	pass
	

if __name__ == '__main__':
	
	# Arduino connection through USB port 
	while True:
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
			ser.reset_input_buffer();
			break
			
		# Oops! You forgot to plug in the Arduino
		except serial.serialutil.SerialException:
			print("Please plug in Arduino.")
			time.sleep(3)
		
	while True:
		#try:
		
		# check if the CPU is overheating
		if (CPUTemperature().temperature > 80.0):
			print("System overheating, shutting down.")
			break
		
		# collect measurements from Arduino
		if ser.in_waiting > 0:
			
			# ~ start = timeit.timeit()
			
			start = datetime.now()
			# ~ time = formatDateTime(start, 'hh:mm:ss')
			# Add defaults
			voltage = ser.readline().decode('utf-8').rstrip()
			print(voltage + " Volts")
			
			freq = ser.readline().decode('utf-8').rstrip()
			print(freq + " Hz")
			
			# voltage too high
			if (float(voltage) > MAX_VOLTS):
				
				dt = getDateTime()
				
				emailContent = "".join(("Voltage critically high: ", voltage, " volts. Measurement taken at ", dt))
				
				#sendTexts(emailSubject, emailContent)
				client.send_sms(number1, emailContent)
				client.send_sms(number2, emailContent)
				
				updateSheet([voltage, freq, dt, "Voltage too high"])
					
			# voltage too low
			elif (float(voltage) < MIN_VOLTS):
	
				dt = getDateTime()
				
				emailContent = "".join(("Voltage critically low: ", voltage, " volts. Measurement taken at ", dt))
				
				#sendTexts(emailSubject, emailContent)
				client.send_sms(number1, emailContent)
				client.send_sms(number2, emailContent)

				
				updateSheet([voltage, freq, dt, "Voltage too low"])
				
			# Frequency too high
			elif (float(freq) > MAX_FREQ):
				
				dt = getDateTime()
				
				emailContent = "".join(("Frequency critically high: ", freq, " Hz. Measurement taken at ", dt))
				
				#sendTexts(emailSubject, emailContent)
				client.send_sms(number1, emailContent)
				client.send_sms(number2, emailContent)

				
				updateSheet([voltage, freq, dt, "Freq too high"])
				
			# Frequency too low
			elif (float(freq) < MIN_FREQ):
				
				dt = getDateTime()
				
				emailContent = "".join(("Frequency critically high: ", freq, " Hz. Measurement taken at ", dt))
				
				#sendTexts(emailSubject, emailContent)
				client.send_sms(number1, emailContent)
				client.send_sms(number2, emailContent)

				
				updateSheet([voltage, freq, dt, "Freq too low"])
			
			
			time.sleep(1)
			# ~ end = timeit.timeit()
			# ~ print(end-start)
			end = datetime.now()
			print(end-start)
