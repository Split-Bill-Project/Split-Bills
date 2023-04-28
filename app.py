from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    title = 'Split Bill - Home'
    return render_template('front.html', title=title)

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