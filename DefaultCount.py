import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')

with con:
    cursor = con.cursor()
 
    #cursor.execute("ALTER TABLE origination ADD COLUMN default_count INTEGER")
	
    cursor.execute("SELECT loan_sequence_number from origination WHERE five_years_payment = 'Y'")
    sequenceNumbers = cursor.fetchall()
	
    default_count = []
	
    for sequenceNumber in sequenceNumbers:
        paymentDatesQuery = "SELECT monthly_reporting_period, clds from monthly where loan_sequence_number = ?"

        cursor.execute(paymentDatesQuery, sequenceNumber)
        allLoansPaymentDates = cursor.fetchall()

        paymentYears = list(map(lambda x: str(x[0])[:4], allLoansPaymentDates))
        cldsValues = list(map(lambda x: str(x[1])[:4], allLoansPaymentDates))

        uniquePaymentYears = set(paymentYears)
        #print(max(uniquePaymentYears))

        #find last year payment was made and remove corresponding clds values
        lastPaymentYear = max(uniquePaymentYears)
        numPaymentsInLastYear = paymentYears.count(lastPaymentYear)
        del cldsValues[-numPaymentsInLastYear:]

        numDefaults = 0

        #count number of times clds value was over 3, indicating default
        numDefaults = sum(int(clds) >= 3 for clds in cldsValues)

        default_count.append([numDefaults, sequenceNumber[0]])

    updateDefaultCountQuery = Query = "UPDATE origination SET default_count = ? WHERE loan_sequence_number = ?"
    cursor.executemany(updateDefaultCountQuery, default_count)

