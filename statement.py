mport pandas as pd
import json
from fpdf import FPDF
df = pd.read_csv("transaction.csv")
with open("info.json", "r") as f:
    user = json.load(f)
df["Balance"] = df["Amount"].cumsum()
total_due = df["Amount"].sum()
min_due = total_due * 0.12  
class AxisStatementPDF(FPDF):
    def header(self):
        self.image("logo.png", 10, 8, 40)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "MY ZONE CREDIT CARD STATEMENT", ln=True, align="C")
        self.ln(5)
    def add_customer_info(self):
        self.set_font("Arial", "", 12)
        self.cell(0, 8, user["name"], ln=True)
        for line in user["address"].split('\n'):
            self.cell(0, 8, line, ln=True)
        self.cell(0, 8, user["pincode"], ln=True)
        self.ln(5)
    def add_payment_summary(self):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 250)
        self.cell(45, 10, "Total Due", 1, 0, 'C', 1)
        self.cell(45, 10, "Min Payment Due", 1, 0, 'C', 1)
        self.cell(50, 10, "Statement Period", 1, 0, 'C', 1)
        self.cell(50, 10, "Due Date", 1, 1, 'C', 1)
        self.set_font("Arial", "", 12)
        self.cell(45, 10, f"INR{total_due:.2f}", 1, 0, 'C')
        self.cell(45, 10, f"INR{min_due:.2f}", 1, 0, 'C')
        self.cell(50, 10, user["statement_period"], 1, 0, 'C')
        self.cell(50, 10, user["due_date"], 1, 1, 'C')
        self.ln(5)
    def add_transaction_table(self):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(200, 220, 255)
        self.cell(30, 10, "Date", 1, 0, 'C', 1)
        self.cell(70, 10, "Description", 1, 0, 'C', 1)
        self.cell(30, 10, "Category", 1, 0, 'C', 1)
        self.cell(30, 10, "Amount", 1, 0, 'C', 1)
        self.cell(30, 10, "Balance", 1, 1, 'C', 1)
        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            self.cell(30, 10, row["Date"], 1)
            self.cell(70, 10, row["Description"], 1)
            self.cell(30, 10, row["Category"], 1)
            self.cell(30, 10, f'{row["Amount"]:.2f}', 1, 0, 'R')
            self.cell(30, 10, f'{row["Balance"]:.2f}', 1, 1, 'R')
    def add_footer_info(self):
        self.ln(5)
        self.set_font("Arial", "I", 8)
        self.multi_cell(0, 8, "Note: This is a system-generated statement. For queries contact: 1800-123-456")
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
pdf = AxisStatementPDF()
pdf.add_page()
pdf.add_customer_info()
pdf.add_payment_summary()
pdf.add_transaction_table()
pdf.add_footer_info()
pdf.output("statement_etl.pdf")
print("PDF generated: statement_etl.pdf")
