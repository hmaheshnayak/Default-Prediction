DELETE FROM origination WHERE five_years_payment = 'N';

DELETE FROM monthly WHERE loan_sequence_number NOT IN (SELECT loan_sequence_number FROM origination);