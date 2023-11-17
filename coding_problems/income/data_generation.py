import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(0)

# Generate data for 50 employees
num_employees = 50

# Employee IDs (assuming they are just 1 to 50)
employee_ids = list(range(1, num_employees + 1))

# Number of children: About 20 employees will have 0 children
num_children = np.random.choice([0, 1, 2, 3, 4, 5], num_employees, p=[0.4, 0.15, 0.15, 0.15, 0.1, 0.05])

# Gender: All women
genders = ['Female'] * num_employees

# Salary: Average salary for women with 0 children higher than others
# Assuming a base salary range of 30000 to 70000
base_salaries = np.random.randint(30000, 70000, num_employees)
additional_for_no_children = np.where(num_children == 0, np.random.randint(5000, 10000), 0)
salaries = base_salaries + additional_for_no_children

# Create DataFrame
employee_data = pd.DataFrame({
    'Employee ID': employee_ids,
    'Number of Children': num_children,
    'Gender': genders,
    'Salary': salaries
})

# Save to CSV file
csv_output_path = 'employee_data.csv'
employee_data.to_csv(csv_output_path, index=False)
