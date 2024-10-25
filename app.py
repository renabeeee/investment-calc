import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import SUCCESS

# Function to calculate taxes


def calculate_taxes():
    try:
        # Get the input values
        target_profit = float(entry_profit.get())  # Futures trading profit
        ordinary_income = float(entry_income.get())  # Ordinary income

  # Federal tax brackets (2024) for Single Filers (Revised)
        federal_brackets = [
            (0.10, 0),
            (0.12, 11600),
            (0.22, 47150),
            (0.24, 100525),
            (0.32, 191950),
            (0.35, 243725),
            (0.37, 609351)  # Updated the limit for the highest bracket
        ]

        # State tax brackets (California 2024) (Revised)
        state_brackets = [
            (0.01, 0),
            (0.01, 10412),  # 1% on first $10,412
            (0.02, 24684),  # 2% on $10,413 to $24,684
            (0.04, 38959),  # 4% on $24,685 to $38,959
            (0.06, 54081),  # 6% on $38,960 to $54,081
            (0.08, 68350),  # 8% on $54,082 to $68,350
            (0.093, 349137),  # 9.3% on $68,351 to $349,137
            (0.103, 418961),  # 10.3% on $349,138 to $418,961
            (0.113, 698271),  # 11.3% on $418,962 to $698,271
            (0.123, float('inf'))  # 12.3% on $698,272 or more
        ]

        # Function to calculate progressive tax

        def calculate_progressive_tax(income, brackets):
            tax = 0.0
            for i in range(len(brackets) - 1):
                rate, limit = brackets[i]
                next_limit = brackets[i + 1][1] if i + \
                    1 < len(brackets) else float('inf')
                if income > limit:
                    tax += (min(income, next_limit) - limit) * rate
                else:
                    break
            if income > brackets[-1][1]:
                tax += (income - brackets[-1][1]) * brackets[-1][0]
            return tax

        # Function to determine current tax bracket
        def get_current_bracket(income, brackets):
            for i in range(len(brackets) - 1):
                rate, limit = brackets[i]
                next_limit = brackets[i + 1][1]
                if income < next_limit:
                    return rate * 100  # Return the percentage value of the tax rate
            return brackets[-1][0] * 100  # Return the highest tax rate

        # Function to calculate amount remaining before next bracket
        def amount_remaining_before_next_bracket(income, brackets):
            for i in range(len(brackets) - 1):
                _, limit = brackets[i]
                next_limit = brackets[i + 1][1]
                if income < next_limit:
                    return next_limit - income
            return 0  # If income exceeds all brackets, return 0

        # Calculate taxes
        # This is only your job income since taxes are already withheld for it
        total_income = ordinary_income

        # Federal and state tax without futures trading profits
        federal_tax_without_futures = calculate_progressive_tax(
            total_income, federal_brackets)
        state_tax_without_futures = calculate_progressive_tax(
            total_income, state_brackets)

        # Federal and state tax including futures profits
        total_income_with_futures = ordinary_income + target_profit
        federal_tax_with_futures = calculate_progressive_tax(
            total_income_with_futures, federal_brackets)
        state_tax_with_futures = calculate_progressive_tax(
            total_income_with_futures, state_brackets)

        # Futures-specific tax (60/40 split)
        futures_long_term_tax = target_profit * 0.60 * \
            0.20  # 60% at 20% long-term capital gains
        futures_short_term_tax = target_profit * 0.40 * 0.24  # 40% at 24% short-term
        futures_tax = futures_long_term_tax + futures_short_term_tax

        # Calculate take-home future profits
        take_home_profit = target_profit - total_tax

        # Remaining amount before entering the next tax bracket
        amount_before_next_federal_bracket = amount_remaining_before_next_bracket(
            total_income_with_futures, federal_brackets)
        amount_before_next_state_bracket = amount_remaining_before_next_bracket(
            total_income_with_futures, state_brackets)

        # Current tax brackets
        current_federal_bracket = get_current_bracket(
            total_income_with_futures, federal_brackets)
        current_state_bracket = get_current_bracket(
            total_income_with_futures, state_brackets)

# Add the label for total take-home future profits
        label_take_home_profit.config(text=f"Total Take-Home Future Profits: \n\n${
                                      take_home_profit:,.2f}", font="-size 11 -weight bold", anchor='w')

        # Remaining amount before entering the next bracket
        label_next_federal_bracket.config(text=f"Amount Remaining Before Next Federal Bracket: \n\n${
                                          amount_before_next_federal_bracket:,.2f}", font="-size 11", anchor='w')
        label_next_state_bracket.config(text=f"Amount Remaining Before Next State Bracket: \n\n${
                                        amount_before_next_state_bracket:,.2f}", font="-size 11", anchor='w')

        # Current federal and state tax brackets
        label_current_federal_bracket.config(text=f"Current Federal Tax Bracket: {
                                             current_federal_bracket:.1f}%", font="-size 11", anchor='w')
        label_current_state_bracket.config(text=f"Current State Tax Bracket: {
                                           current_state_bracket:.1f}%", font="-size 11", anchor='w')

    except ValueError:
        label_federal_tax.config(
            text="Invalid Input!", font="-size 10 -weight bold")
        label_state_tax.config(text="")
        label_total_tax.config(text="")
        label_take_home_profit.config(text="")

        label_next_federal_bracket.config(text="")
        label_next_state_bracket.config(text="")
        label_current_federal_bracket.config(text="")
        label_current_state_bracket.config(text="")


# Create the main window
app = ttk.Window(themename="flatly")
app.title("California Futures Tax Withholding Calculator")
# app.geometry("600x650")  # Increased width

# Add a new label for take-home profits
label_take_home_profit = ttk.Label(app, text="", anchor='w')
label_take_home_profit.pack(pady=5, padx=10, fill='x')

# Labels and input fields
label_title = ttk.Label(
    app, text="Futures Tax Withholding Calculator", font="-size 18 -weight bold")
label_title.pack(pady=10)

label_profit = ttk.Label(app, text="Enter Futures Trading Profit ($):")
label_profit.pack()
entry_profit = ttk.Entry(app)
entry_profit.pack(pady=5)

label_income = ttk.Label(app, text="Enter Ordinary Income ($):")
label_income.pack()
entry_income = ttk.Entry(app)
entry_income.pack(pady=5)

# Button to calculate taxes
button_calculate = ttk.Button(
    app, text="Calculate Taxes", bootstyle=SUCCESS, command=calculate_taxes)
button_calculate.pack(pady=10)

# Labels for current tax brackets
label_current_federal_bracket = ttk.Label(app, text="", anchor='w')
label_current_federal_bracket.pack(pady=5, padx=10, fill='x')

label_current_state_bracket = ttk.Label(app, text="", anchor='w')
label_current_state_bracket.pack(pady=5, padx=10, fill='x')

# Separator line (stay)
separator_line = ttk.Separator(app, orient='horizontal')
separator_line.pack(pady=10, fill='x')

# Labels for results (with improved styling)
label_federal_tax = ttk.Label(app, text="", anchor='w')
label_federal_tax.pack(pady=5, padx=10, fill='x')

label_state_tax = ttk.Label(app, text="", anchor='w')
label_state_tax.pack(pady=5, padx=10, fill='x')

label_total_tax = ttk.Label(app, text="", anchor='w')
label_total_tax.config(font="-size 11 -weight bold")
label_total_tax.pack(pady=15, padx=10, fill='x')

label_take_home_profit = ttk.Label(app, text="", anchor='w')
label_take_home_profit.pack(pady=5, padx=10, fill='x')

# Separator line
separator_line = ttk.Separator(app, orient='horizontal')
separator_line.pack(pady=10, fill='x')

# Separator line
separator_line = ttk.Separator(app, orient='horizontal')
separator_line.pack(pady=10, fill='x')

# Labels for remaining amount before next bra cket
label_next_federal_bracket = ttk.Label(app, text="", anchor='w')
label_next_federal_bracket.pack(pady=5, padx=10, fill='x')

label_next_state_bracket = ttk.Label(app, text="", anchor='w')
label_next_state_bracket.pack(pady=5, padx=10, fill='x')


# Start the app
app.mainloop()
