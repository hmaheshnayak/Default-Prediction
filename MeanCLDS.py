import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')

with con:
    cursor = con.cursor()

    #cursor.execute("ALTER TABLE origination ADD COLUMN mean_clds REAL")

    cursor.execute("SELECT loan_sequence_number from origination WHERE five_years_payment = 'Y'")
    sequenceNumbers = cursor.fetchall()

    mean_clds = []

    for sequenceNumber in sequenceNumbers:
        paymentDatesQuery = "SELECT monthly_reporting_period, clds from monthly where loan_sequence_number = ?"

        cursor.execute(paymentDatesQuery, sequenceNumber)
        allLoansPaymentDates = cursor.fetchall()

        paymentYears = list(map(lambda x: str(x[0])[:4], allLoansPaymentDates))
        cldsValues = list(map(lambda x: str(x[1]), allLoansPaymentDates))

        uniquePaymentYears = set(paymentYears)

        #find last year payment was made and remove corresponding clds values
        lastPaymentYear = max(uniquePaymentYears)
        numPaymentsInLastYear = paymentYears.count(lastPaymentYear)
        del cldsValues[-numPaymentsInLastYear:]

        #remove all the -1 clds values and compute mean
        cldsValues = list(filter(lambda x: int(x) != -1, cldsValues))
        numCldsValues = len(cldsValues)
        cldsValues = map(int, cldsValues)
        mean = sum(cldsValues)/numCldsValues

        mean_clds.append([mean, sequenceNumber[0]])

    updateMeanCldsQuery = "UPDATE OR REPLACE origination SET mean_clds = ? WHERE loan_sequence_number = ?"
    cursor.executemany(updateMeanCldsQuery, mean_clds)
