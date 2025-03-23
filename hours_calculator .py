# Get user input
Regular_rate = float(input("Enter your regular hourly rate: "))
totalHours = float(input("Enter total hours worked: "))

# Set standard full-time hours
Standard_hours = 40

# Set overtime rate (e.g., 1.5x regular rate)
Overtime_rate = Regular_rate * 1.5

# Calculate pay
if totalHours <= Standard_hours:
    totalPay = totalHours * Regular_rate
else:
    regularPay = Standard_hours * Regular_rate
    overtimeHours = totalHours - Standard_hours
    overtimePay = overtimeHours * Overtime_rate
    totalPay = regularPay + overtimePay

# Display result
print(f"\nRegular Rate: ${Regular_rate:.2f}")
print(f"Overtime Rate: ${Overtime_rate:.2f}")
print(f"Total Hours Worked: {totalHours}")
if totalHours > Standard_hours:
    print(f"Overtime Hours: {overtimeHours}")
print(f"Total Pay: ${totalPay:.2f}")
