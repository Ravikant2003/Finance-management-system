from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as sqltor
import matplotlib.pyplot as plt

app = Flask(__name__)

# Initialize variables
total_expenses = 0
expense_limit = None
expense_limit_warning = ""

def email(letter):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Email configuration
    sender_email = 'testingravikant@gmail.com'
    receiver_email = 'ravikantsaraf03@gmail.com'
    password = 'cuxqmmsqmtggenoz'  # You should use an app-specific password for security
    subject = 'Expense Tracker Update'
    message = letter

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server (Gmail example)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS encryption
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully')

    except Exception as e:
        print(f'Error: {str(e)}')

    finally:
        server.quit()  # Quit the SMTP server


@app.route('/')
def index():
    return render_template('index.html', total_expenses=total_expenses, expense_limit=expense_limit, expense_limit_warning=expense_limit_warning)

@app.route('/budget_check', methods=['POST'])
def budget_check():
    monthly_budget=int(request.form.get('monthly_budget'))
    monthly_budget_month=int(request.form.get('month'))
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute(f"Select Sum(Amount) from expenses where Month(date)={monthly_budget_month}")
    data5 = cursor.fetchall()
    if monthly_budget>data5[0][0]: # data5[0][0] is the amount you have spent for the month till now
        savings=monthly_budget-data5[0][0]
        message=f"You have spent around Rs {data5[0][0]} till now and can spend Rs {savings} for this Month"
        email(message)
        return render_template('budget_check.html',message=message)
    else:
        message=f"You have spent Rs {data5[0][0]} till now and your budget was Rs {monthly_budget} which you have crossed. Hence you can't spend further."
        email(message)
        return render_template('budget_check.html',message=message)
    
@app.route('/Monthly-expenses')
def monthly_expenses():
    return render_template('Monthly_expenses.html')

@app.route('/monthly_expenses_selection', methods=['POST', 'GET'])
def monthly_expenses_selection():
    if request.method == 'POST':
        selected_month = int(request.form.get('month'))
        mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
        cursor = mycon.cursor()
        cursor.execute(f"Select category,Amount from expenses where Month(date)={selected_month}")
        data1 = cursor.fetchall()
        labels = [] # Basically has all the category stored in them
        size = [] # Has all the cost of thoses categories in them

        for info in data1:
            if info[0] not in labels:
                labels.append(info[0])
        print(labels)
        for i in range(len(labels)):
            cursor.execute(f'select sum(amount) "{labels[i]}" from expenses where category="{labels[i]}"')
            data3 = cursor.fetchall()
            size.append(int(data3[0][0]))

        position = range(len(labels))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.pie(size, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        
        ax2.bar(position, size)
        ax2.set_ylabel('Amount')
        ax2.set_xlabel("Categories")
        xtick_positions = range(len(labels))
        xtick_labels = labels
        ax2.set_xticks(xtick_positions)
        ax2.set_xticklabels(xtick_labels)
        
        ax1.set_title('Pie Chart')
        ax2.set_title('Bar Graph')
        
        plt.tight_layout()
        plt.show()
        

        # Connect to MySQL and fetch data for the selected date
        mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
        cursor = mycon.cursor()
        cursor.execute(f"Select Name,category,Amount from expenses where Month(date)={selected_month}")
        data = cursor.fetchall() # Name has the Name of the item in it

        # Close the database connection when done
        mycon.close()

        # Pass the fetched data to the 'expense_list.html' template
        return render_template('Monthly_expenses.html', data=data)
    
    # If it's a GET request, just render the form
    return render_template('Monthly_expenses.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    global total_expenses, expense_limit, expense_limit_warning
    expense_name = request.form.get('expense_name')
    expense_amount = float(request.form.get('expense_amount'))
    expense_category = request.form.get('expense_category')
    expense_date = request.form.get('expense_date')
    expense_limit = request.form.get('expense_limit')
    # Update total expenses
    total_expenses += expense_amount

    if expense_limit is not None and total_expenses + expense_amount > expense_limit:
        expense_limit_warning = "Expense Limit Exceeded"
        return render_template('index.html', total_expenses=total_expenses, expense_limit=expense_limit, expense_limit_warning=expense_limit_warning)

    # Update total expenses
    total_expenses += expense_amount

    # You can store or process the entered expense data as needed    
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    val = (expense_name, expense_amount, expense_category, expense_date) 
    cursor.execute("INSERT INTO expenses VALUES (%s, %s, %s, %s)", val)
    message=f"""A new expense has been made:The details of which are as follows:
            
            1)Name of the item: {expense_name} 
            2)Amount:{expense_amount}
            3)Expense-category:{expense_category}
            4)Expense-date:{expense_date}
            The data has been fed into your MYSQL Database
    """  
    email(message) # Sends the message to user 
    mycon.commit()
    mycon.close()

    return render_template('index.html', total_expenses=total_expenses, expense_limit=expense_limit, expense_limit_warning=expense_limit_warning)

@app.route('/delete')
def delete_page():
    return render_template('delete.html')

@app.route('/delete-data', methods=['POST'])
def delete_data():
    if request.method == 'POST':
        name_to_delete = request.form.get('name')
        mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
        cursor = mycon.cursor()
        cursor.execute(f"Delete from expenses where name = '{name_to_delete}'")
        # Perform the MySQL delete operation using the name received
        # For example, use SQL DELETE query to delete records
        # Redirect to a success or confirmation page\
        message=f"You have deleted the expense related to name: {name_to_delete}. The data has been deleted from MYSQL"
        email(message) #Sends message to email 
        mycon.commit()
        mycon.close()
        return render_template('sucess_delete.html')
            

@app.route('/expense_list')
def show_expense_list():
    # This route can remain as is if you don't want to display data here
    return render_template('expense_list.html')

@app.route('/process-date', methods=['POST'])
def process_date():# used to make the graph for daily work
    selected_date = request.form.get('date')

    # Fetch data from MySQL for the selected date
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute(f"SELECT category, amount FROM expenses WHERE date = '{selected_date}'")
    data1 = cursor.fetchall()
    
    labels = [] # Basically has all the Category
    size = [] # Has the Cost of thoses items in that category

    for info in data1:
        if info[0] not in labels:
            labels.append(info[0])

    for i in range(len(labels)):
        cursor.execute(f'select sum(amount) "{labels[i]}" from expenses where category="{labels[i]}"')
        data3 = cursor.fetchall()
        size.append(int(data3[0][0]))

    position = range(len(labels))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.pie(size, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    
    ax2.bar(position, size)
    ax2.set_ylabel('Amount')
    ax2.set_xlabel("Categories")
    xtick_positions = range(len(labels))
    xtick_labels = labels
    ax2.set_xticks(xtick_positions)
    ax2.set_xticklabels(xtick_labels)
    
    ax1.set_title('Pie Chart')
    ax2.set_title('Bar Graph')
    
    plt.tight_layout()
    plt.show()
    

    selected_date = request.form.get('date')

    # Connect to MySQL and fetch data for the selected date
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute(f"SELECT name, category, amount FROM expenses WHERE date = '{selected_date}'") # Name has the Name of the item in it
    data = cursor.fetchall()

    # Close the database connection when done
    mycon.close()

    # Pass the fetched data to the 'expense_list.html' template
    return render_template('expense_list.html', data=data)

@app.route('/edit', methods=['GET'])
def edit_page():
    return render_template('edit.html')

# Handle the editing of records
@app.route('/edit-data', methods=['POST'])
def edit_data():
    # Retrieve the data from the form fields
    name = request.form.get('name') 
    amount = float(request.form.get('amount'))
    category = request.form.get('expense_category')
    date = request.form.get('date')
    

    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute("UPDATE expenses SET amount=%s, category=%s, date=%s WHERE name=%s", (amount, category, date, name))
    mycon.commit()
    mycon.close()

    message=f"""You Have made changes to your data in Expense tracker system. The Change is related to the name {name}
        the new details of this name are as follows:
        1) Name:{name}
        2) New Amount:{amount}
        3) New Category:{category}
        4) New Date:{date}
        The data has been changed in MYSQL database as well
        """
    email(message) # Sends message to email
    # Perform the edit operation using the data received
    # For example, use SQL UPDATE query to update records in your database

    # Redirect to a success or confirmation page
    return render_template('edit_sucess')
    
if __name__ == '__main__':
    app.run(debug=True)
