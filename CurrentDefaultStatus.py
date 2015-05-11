import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')

with con:
    cursor = con.cursor()

    #cursor.execute("ALTER TABLE origination ADD COLUMN current_default_status INTEGER")

    cursor.execute("SELECT loan_sequence_number from origination WHERE five_years_payment = 'Y'")
    sequenceNumbers = cursor.fetchall()

    default_status = []

    for sequenceNumber in sequenceNumbers:
        cldsQuery = "SELECT clds from monthly where loan_sequence_number = ?"

        cursor.execute(paymentDatesQuery, sequenceNumber)
        allLoansPaymentDates = cursor.fetchall()

        currentclds = allLoansPaymentDates[len(allLoansPaymentDates)][0]


        default_count.append([currentclds, sequenceNumber[0]])

    #updateDefaultStatusQuery = "UPDATE origination SET current_default_status = ? WHERE loan_sequence_number = ?"
    #cursor.executemany(updateDefaultCountQuery, default_count)
