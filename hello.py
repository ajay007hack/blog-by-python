from flask import Flask , render_template
app = Flask(__name__ , template_folder= 'template')

@app.route("/")
def hello():
    return render_template('index.html')
@app.route("/about") 
def ajay():
    return render_template('about.html')

app.run(debug=True)    
  
