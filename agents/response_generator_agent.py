class ResponseGeneratorAgent:
    def __init__(self):
        pass

    def generate(self, applicant_data, is_compliant):

        reasons = []

        if is_compliant:
            return f"Approved: Congratulations {applicant_data.get('name', 'Applicant')}! You're eligible for a credit card with limit: 50,000."

        if applicant_data.get("age", 0) < 21:
            return f"Rejected: Sorry {applicant_data.get('name', 'Applicant')}, your application was not approved. Reason: Under minimum age requirement is 21"

        if applicant_data.get("credit_history_score", 0) < 750:
            reasons.append(f"Low credit score {applicant_data.get('credit_history_score', 'N/A')}")

        if applicant_data.get("missed_payments_last_12m", 0):
            reasons.append(f"Missed payments in the last {applicant_data.get('missed_payments_last_12m', 'N/A')} months.")

        reason_text = " & ".join(reasons) if reasons else "Does not meet eligibility criteria"
        return f"Rejected: Sorry {applicant_data.get('name', 'Applicant')}, your application was not approved. \nReason: {reason_text}"




