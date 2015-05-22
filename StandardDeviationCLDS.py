import sqlite3 as lite
import math as math

con = lite.connect('D:\\Msc\\Neural Networks\\sampledbo\\sample.db')

with con:
    cursor = con.cursor()

    #cursor.execute("ALTER TABLE origination ADD COLUMN standard_deviation_clds REAL")

    cursor.execute("SELECT loan_sequence_number from origination WHERE five_years_payment = 'Y'")
    sequenceNumbers = cursor.fetchall()

    std_dev_clds = []

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
        cldsValues = list(map(int, cldsValues))
        mean = sum(cldsValues)/numCldsValues

        #subtract each clds value from the mean and square the value to obtain deviations
        deviations = list(map(lambda x: math.pow((x-mean), 2), cldsValues))
        variance = sum(deviations)/numCldsValues
        standardDeviation = math.sqrt(variance)

        std_dev_clds.append([standardDeviation, sequenceNumber[0]])

    updateStdDevCldsQuery = "UPDATE OR REPLACE origination SET standard_deviation_clds = ? WHERE loan_sequence_number = ?"
    cursor.executemany(updateStdDevCldsQuery, std_dev_clds)
