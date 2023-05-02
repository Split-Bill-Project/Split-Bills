from flask import Flask, render_template, request
from split import *


table_name = ""
member_names = []


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="india@123",
    database="split_bill"
)

# Create a cursor object
cursor = db.cursor()



app = Flask(__name__)

@app.route("/")
def home():
    title = 'Split Bill - Home'
    return render_template('index.html', title=title)

@app.route('/split_expense_show_group', methods=['GET', 'POST'])
def split_expense_show_group():
    group_names = show_group_name()

    return render_template('select_group.html', groups=group_names)
    # return render_template("select_group.html")
    # return render_template("split_an_expense.html")

@app.route('/show_member', methods=['POST'])
def show_member():
    if request.method == 'POST':
        table_name = request.form['group']
        print(table_name)
    member_names = show_column_name(table_name)
    print(member_names)
    return render_template("show_member.html",members = member_names)


@app.route('/split_expense_result', methods=['GET', 'POST'])
def split_expense():
    split_an_expense()
    return render_template("split_expense_result.html")



@app.route('/create_group',methods = ['GET','POST'])
def create_group():
    # if request.method == 'POST':
    #     table_name = request.form['groupName']
    #     member_names = request.form['member[]']
    #     create_group(table_name,member_names)
    #     print(table_name)  
    return render_template("create_group.html")

@app.route('/create_group_result',methods = ['GET','POST'])
def create_group_result():
    if request.method == 'POST':
        table_name = request.form['groupName']
        member_names = request.form.getlist['member[]']
        createGroup(table_name,member_names)
    return render_template("create_group_result.html")



@app.route('/genrate_bill',methods = ['GET','POST'])
def genrate_bill():
    return render_template("genrate_bill.html")

@app.route('/split_expense_result',methods = ['GET','POST'])
def split_result():
    split_an_expense()
    return render_template("split_result.html")


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get form data
#         total = float(request.form['total'])
#         num_people = int(request.form['num_people'])
        
#         # Calculate split amount
#         split_amount = round(total / num_people, 2)
        
#         # Render template with results
#         return render_template('result.html', split_amount=split_amount)
    
#     # Render index template
#     return render_template('index.html')


if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
    cursor.close()