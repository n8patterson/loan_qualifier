# Import pathlib
from pathlib import Path

# Import fileio
from qualifier.utils.fileio import load_csv, save_csv

# Import Calculators
from qualifier.utils.calculators import calculate_monthly_debt_ratio, calculate_loan_to_value_ratio

# Import Filters
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value
from qualifier.filters.max_loan_size import filter_max_loan_size

def test_save_csv():
    # Use Path from pathlib to output the test csv to ./data/output/qualifying_loans.csv

    # Test data
    test_header = ["Lender", "Max Loan Amount",
                   "Max LTV,Max DTI", "Min Credit Score", "Interest Rate"]
    test_data = [["West Central Credit Union - Premier Option", 400000, 0.9, 0.35,
                  760, 2.7], ["FHA Fannie Mae - Starter Plus", 200000, 0.9, 0.37, 630, 4.2]]

    # Test save_csv() function
    csvpath = Path("./qualifier/data/output/qualifying_loans.csv")
    save_csv(csvpath, test_data, test_header)
    assert Path(csvpath).exists() == True


def test_calculate_monthly_debt_ratio():
    assert calculate_monthly_debt_ratio(1500, 4000) == 0.375


def test_calculate_loan_to_value_ratio():
    assert calculate_loan_to_value_ratio(210000, 250000) == 0.84


def test_filters():
    # Test vars
    bank_data = load_csv(Path('./qualifier/data/daily_rate_sheet.csv'))
    current_credit_score = 750
    loan = 210000
     
    # Calculated test data
    monthly_debt_ratio = 0.375
    loan_to_value_ratio = 0.84

    # Test filtered list data
    test_filter_data = [["Bank of Big - Premier Option", "300000", "0.85", "0.47", "740", "3.6"],
                        ["Bank of Fintech - Premier Option","300000",
                            "0.9", "0.47", "740", "3.15"],
                        ["Prosper MBS - Premier Option",
                            "400000", "0.85", "0.42", "750", "3.45"],
                        ["Bank of Big - Starter Plus",
                            "300000", "0.85", "0.39", "700", "4.35"],
                        ["FHA Fredie Mac - Starter Plus",
                            "300000", "0.85", "0.45", "550", "4.35"],
                        ["iBank - Starter Plus", "300000", "0.9", "0.4", "620", "3.9"],
                        ]

    # Test using each separete filter
    bank_data_filtered = filter_credit_score(current_credit_score, bank_data)
    bank_data_filtered = filter_max_loan_size(loan, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(
        monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(
        loan_to_value_ratio, bank_data_filtered)

    # Assert statements, first test length
    assert len(bank_data_filtered) == len(test_filter_data)

    # Then assert vs. test_filter_data
    for index in range(len(test_filter_data)):
        out_example = all([a == b for a, b in zip(test_filter_data[index], bank_data_filtered[index])])
        assert out_example
