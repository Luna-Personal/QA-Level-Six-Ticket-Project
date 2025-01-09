#importing packages
from app import create_app


#Creating an instance of the Flask App
app = create_app()

if __name__ == '__main__':
    #Running the Flask App in debug mode
    app.run(debug=True)