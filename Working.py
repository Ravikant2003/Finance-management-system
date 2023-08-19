def prev():
    time = input("Enter the date in (YYYY-MM-DD) format.")
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute(f"select * from details where Date = '{time}'")
    data = cursor.fetchall()
    print(data)
    mycon.close()
##################################################################

def new():
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    ans='Yes'
    while ans=='Yes':
        cat=input("Enter the category of expenditure")
        date=input("Enter the date.")
        amt=int(input("Enter the amount"))
        account=input("Enter the account name")
        explain=input("Enter the explanation for the work.")
        code=int(input("Enter code"))
        val=(cat,date,amt,account,explain,code)
        cursor.execute(f"Insert into details values {val}")
        mycon.commit()
        ans=input("Do you want to continue?(Yes/No)")
    mycon.close()
############################################################################################

def delete():
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    ans = 'Yes'
    while ans == 'Yes':
        code=input("Enter the code related to the record.")
        cursor.execute(f"Delete from details where code={code}")
        mycon.commit()
        ans = input("Do you want to continue?(Yes/No)")
    mycon.close()

##################################################################################

def edit():
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    ans = 'Yes'
    while ans == 'Yes':
        code = int(input("Enter the code for edit you have"))
        cat = input("Enter the category of expenditure")
        date = input("Enter the date.")
        amt = int(input("Enter the amount"))
        account = input("Enter the account name")
        explain = input("Enter the explanation for the work.")
        val = (cat, date, amt, account, explain, code)
        cursor.execute(f"Insert into details values {val}")
        mycon.commit()
        ans = input("Do you want to continue?(Yes/No)")
    mycon.close()
#############################################################################################

def graph():
    time = input("Enter the date in (YYYY-MM-DD) format.")
    import mysql.connector as sqltor
    mycon = sqltor.connect(host="localhost", user="root", passwd='One2three4@2003', database="Budget")
    cursor = mycon.cursor()
    cursor.execute("Desc details")
    data = cursor.fetchall()
    print(data)
    '''import matplotlib.pyplot as plt
    labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
    sizes = [35, 25, 20, 10]  # Percentages

    # Create a pie chart
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add a title
    plt.title('Distribution of Fruits')

    # Display the pie chart
    plt.show()
graph()