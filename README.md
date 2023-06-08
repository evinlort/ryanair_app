Clone the repository to the desired location:
    
    git clone git@github.com:evinlort/ryanair_app.git

cd to the project directory:
    
    cd ryanair_app

Create virtual environment:

    python -m virtualenv vryanairapp

Activate virtual environment:

    source vryanairapp/bin/activate

Install requirements:

    pip install -r requirements.txt

Run the application:

    flask --app app run



All in one line:
    
    git clone git@github.com:evinlort/ryanair_app.git && cd ryanair_app && python -m virtualenv vryanairapp && source vryanairapp/bin/activate && pip install -r requirements.txt && flask --app app run 