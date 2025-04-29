import os
import streamlit as st
from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent
from agents.compliance_validator_agent import ComplianceValidatorAgent
from agents.response_generator_agent import ResponseGeneratorAgent
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from io import BytesIO

# Ensure PDF folder exists
PDF_FOLDER = "pdf"
os.makedirs(PDF_FOLDER, exist_ok=True)

st.set_page_config(page_title="Bharat Bank", layout="centered")

st.title("🏦 Bharat Bank Credit Assessment Portal")

user_id_input = st.text_input("Enter Applicant User ID:")

if st.button("Assess Credit Eligibility"):
    if not user_id_input.isdigit():
        st.error("Please enter a valid numeric User ID.")
    else:
        user_id = int(user_id_input)
        knowledge_agent = KnowledgeRetrievalAgent()
        applicant_data = knowledge_agent.fetch(user_id)

        if applicant_data:
            compliance = ComplianceValidatorAgent().is_credit_card_eligible(applicant_data)
            response = ResponseGeneratorAgent().generate(applicant_data, compliance)

            st.subheader("📄 Assessment Result")
            st.info(response)

            st.subheader("📎 Download Credit Report")

            pdf_buffer = BytesIO()

            def generate_pdf(applicant_data, response, output_buffer):
                c = canvas.Canvas(output_buffer, pagesize=letter)
                width, height = letter
                margin = 50
                y = height - margin

                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#1e3a8a"))
                c.drawString(margin, y, "Bharat Bank")
                y -= 25
                c.setFont("Helvetica", 12)
                c.setFillColor(colors.black)
                c.drawString(margin, y, "Credit Assessment Report")
                y -= 10
                c.line(margin, y, width - margin, y)
                y -= 20

                today = datetime.today().strftime("%B %d, %Y")
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(width - 150, height - margin + 5, f"Date: {today}")

                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, "Applicant Information")
                y -= 15
                c.setStrokeColor(colors.grey)
                c.setLineWidth(0.5)
                c.line(margin, y, width - margin, y)
                y -= 20

                table_data = [
                    ["User ID", applicant_data['user_id']],
                    ["Name", applicant_data['name']],
                    ["Income", f"{applicant_data['monthly_income']:,}"],
                    ["Employment Status", applicant_data['employment_status']],
                    ["Credit History Score", applicant_data['credit_history_score']],
                    ["Monthly Balance", f"{applicant_data['avg_monthly_bank_balance']:,}"],
                    ["Credit Card Utilization", f"{applicant_data['credit_card_utilization_pct']}%"],
                    ["Missed Payments (Last 12 Months)", applicant_data['missed_payments_last_12m']],
                    ["Age", applicant_data['age']],
                ]

                table = Table(table_data, colWidths=[200, 300])
                table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))

                table_height = len(table_data) * 18
                if y - table_height < margin:
                    c.showPage()
                    y = height - margin

                table.wrapOn(c, width, height)
                table.drawOn(c, margin, y - table_height)
                y -= table_height + 30

                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, "Credit Recommendation")
                y -= 15
                c.line(margin, y, width - margin, y)
                y -= 15

                c.setFont("Helvetica", 11)
                textobject = c.beginText(margin, y)
                max_width = width - 2 * margin
                lines = response.split('\n')

                for original_line in lines:
                    words = original_line.split()
                    line = ""
                    for word in words:
                        test_line = f"{line} {word}".strip()
                        if c.stringWidth(test_line, "Helvetica", 11) <= max_width:
                            line = test_line
                        else:
                            if y < margin + 40:
                                c.drawText(textobject)
                                c.showPage()
                                y = height - margin
                                textobject = c.beginText(margin, y)
                                textobject.setFont("Helvetica", 11)
                            textobject.textLine(line)
                            y -= 15
                            line = word
                    if line:
                        textobject.textLine(line)
                        y -= 15

                c.drawText(textobject)
                c.save()

            generate_pdf(applicant_data, response, pdf_buffer)
            pdf_buffer.seek(0)

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"{applicant_data['user_id']}_{applicant_data['name']}.pdf",
                mime="application/pdf"
            )

        else:
            st.error("❌ No applicant found with this ID.")
