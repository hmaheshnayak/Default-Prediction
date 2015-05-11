import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')

with con:
    cursor = con.cursor()

    #cursor.execute("ALTER TABLE origination ADD COLUMN current_default_status INTEGER")

    cursor.execute("SELECT loan_sequence_number from origination WHERE five_years_payment = 'Y'")
    sequenceNumbers = cursor.fetchall()

    default_status = []

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

        #loan is default status if clds >= 3 on last payment date
        currentStatus = 1 if int(cldsValues[-1]) >= 3 else 0
        default_status.append([currentStatus, sequenceNumber[0]])

    updateDefaultStatusQuery = "UPDATE OR REPLACE origination SET current_default_status = ? WHERE loan_sequence_number = ?"
    cursor.executemany(updateDefaultStatusQuery, default_status)
