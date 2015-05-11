import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')

with con:
    cursor = con.cursor()
	
	#the sql query inside quotes below will work when executed using sqlite command line directly. 
	#haven't tried it from python as sqlite seems to have no support for deleting columns ..in case something goes wrong
 
	#cursor.execute("ALTER TABLE origination ADD COLUMN five_years_payment char(1)")
	
    cursor.execute("SELECT loan_sequence_number from origination")
    sequenceNumbers = cursor.fetchall()
	
    is_paid_five_years = []
	
    for sequenceNumber in sequenceNumbers:
        paymentDatesQuery = "SELECT monthly_reporting_period from monthly where loan_sequence_number = ?"
        cursor.execute(paymentDatesQuery, sequenceNumber)

        allLoansPaymentDates = cursor.fetchall()

        paymentYears = list(map(lambda x: str(x[0])[:4], allLoansPaymentDates))
        uniquePaymentYears = set(paymentYears)


        is_paid_flag = 'Y'
        length = len(uniquePaymentYears)
        if length < 6:
            is_paid_flag = 'N'
        is_paid_five_years.append([is_paid_flag, sequenceNumber[0]])
		
    updatePaymentInfoQuery = "UPDATE OR REPLACE origination SET five_years_payment = ? WHERE loan_sequence_number = ?"
    cursor.executemany(updatePaymentInfoQuery, is_paid_five_years)








		