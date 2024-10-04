# Expense-Tracker
The Link for the live demonstration of this project is :  https://youtu.be/-fW-UqbdvJU


### Expense Tracker System  - Code Walkthrough:

**Project Overview:**
The Expense Tracker System is a Flask-based application that manages personal expenses, enabling users to add, edit, and delete expense records. It also includes functionalities for setting a budget, checking monthly expenses, visualizing expenses using charts, and sending updates via email. The project uses MySQL for data storage and integrates SMTP for email notifications.

---

#### Key Components of the Code:

1. **Flask App Setup:**
   - The Flask app serves templates from the folder structure `"../Frontend1/Template"` and static assets from `"../Frontend1/Static"`. The routing is handled using multiple routes like `/`, `/budget_check`, `/add_expense`, etc.

2. **MySQL Database Connection:**
   - The app connects to a MySQL database named `"Budget"`, where the expense data is stored in a table named `expenses`. The connection is managed using the `mysql.connector` (`sqltor`) library.

3. **Email Notification Function (`email`):**
   - A key feature of the project is the ability to send email notifications using SMTP. The `email` function composes and sends emails to notify users about expenses added, budget overages, or other significant actions (like data deletion or updates). It uses `smtplib` and `MIMEText` from the `email` library to format and send the messages.

4. **Budget Check (`/budget_check`):**
   - The `/budget_check` route allows users to input their monthly budget and compare it against their total expenses for the selected month. The result (whether the user has exceeded their budget or is within limits) is sent via email and displayed on the screen.

5. **Monthly Expenses Visualization:**
   - In the `/monthly_expenses_selection` and `/process-date` routes, the application fetches data for a selected month or date and visualizes it using a pie chart and bar graph. These charts, generated using `matplotlib`, display the distribution of expenses across categories.
   - Categories and their respective amounts are fetched from the MySQL database and used as labels and data for the charts.

6. **Adding Expenses (`/add_expense`):**
   - The `/add_expense` route handles the addition of new expenses to the system. Users submit data like expense name, amount, category, date, and optional expense limit. This data is inserted into the MySQL `expenses` table. If the user has set an expense limit and exceeds it, a warning is displayed, and a notification is sent via email.

7. **Deleting Expenses (`/delete-data`):**
   - Users can delete expense records by name using the `/delete-data` route. The app performs a MySQL `DELETE` operation to remove the record, and an email is sent to notify the user of the deletion.

8. **Editing Expenses (`/edit-data`):**
   - The `/edit-data` route allows users to update existing expense records. After receiving new data for an expense (amount, category, date), the app updates the corresponding record in the MySQL database and sends an email detailing the changes.

---

#### Main Functionalities:

1. **Expense Management:**
   - Users can add, edit, and delete expenses, with each change reflected in the MySQL database. The app keeps track of total expenses and warns users if they exceed their set budget.

2. **Email Notifications:**
   - Important actions, such as adding a new expense, exceeding the budget, and deleting or editing expense data, trigger email notifications to the user, enhancing the app's usability.

3. **Data Visualization:**
   - The app provides graphical representations (pie charts and bar graphs) of monthly or daily expenses, helping users better understand their spending patterns.

4. **User-Friendly Interface:**
   - Through templates, the app provides forms and displays data to users. Pages such as index, expense list, and budget check make interacting with the system simple.

---
