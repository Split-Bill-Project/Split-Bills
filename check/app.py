from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process_form():
    group_name = request.form.get('group_name')

    # Perform any necessary validation or sanitation here

    # Retrieve the column names from the MySQL table
    # Replace 'your_mysql_database' and 'your_table_name' with the appropriate values
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='india@123',
        database='split_bill'
    )

    cursor = connection.cursor()
    cursor.execute(f"DESCRIBE {group_name}")
    column_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    return jsonify({'column_names': column_names})

if __name__ == '__main__':
    app.run()
