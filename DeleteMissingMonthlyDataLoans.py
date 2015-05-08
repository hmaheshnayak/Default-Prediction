import sqlite3 as lite

con = lite.connect('D:\\Msc\\Neural Networks\\sampledb\\sample.db')


with con:

    origCur = con.cursor()
	
    origCur.execute("SELECT origination.loan_sequence_number FROM origination WHERE NOT EXISTS (SELECT * FROM monthly WHERE origination.loan_sequence_number = monthly.loan_sequence_number)")

    nullDataLoans = origCur.fetchall()

    for nullLoan in nullDataLoans:
        deleteQuery = "DELETE FROM origination WHERE loan_sequence_number = ?"
        origCur.execute(deleteQuery, nullLoan)
	