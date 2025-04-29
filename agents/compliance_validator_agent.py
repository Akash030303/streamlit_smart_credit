class ComplianceValidatorAgent:
    def __init__(self):
        pass

    def is_credit_card_eligible(self, applicant_data):
        # RBI-aligned eligibility thresholds
        MIN_INCOME = 25000
        MIN_BANK_BALANCE_RATIO = int(0.3)
        MAX_CREDIT_UTILIZATION = 30
        MAX_MISSED_PAYMENTS = 1
        MIN_CREDIT_SCORE = 750
        MIN_AGE = 21
        MAX_AGE = 65

        credit_score = applicant_data.get("credit_history_score", 0)
        credit_utilization = applicant_data.get("credit_card_utilization_pct", 100)
        missed_payments = applicant_data.get("missed_payments_last_12m", 10)
        income = applicant_data.get("monthly_income", 0)
        monthly_balance = applicant_data.get("avg_monthly_bank_balance", 0)
        employment = applicant_data.get("employment_status", "").lower()
        age = applicant_data.get("age", 0)

        if (
                credit_score >= MIN_CREDIT_SCORE and
                credit_utilization <= MAX_CREDIT_UTILIZATION and
                missed_payments <= MAX_MISSED_PAYMENTS and
                income >= MIN_INCOME and
                monthly_balance >= income * MIN_BANK_BALANCE_RATIO and
                employment in ["employed", "self-employed"] and
                MIN_AGE <= age <= MAX_AGE
        ):
            return True
        else:
            return False

