Clone the repository to the desired location:
    
    git clone https://github.com/evinlort/ryanair_app.git

cd to the project directory:
    
    cd ryanair_app

Create virtual environment:

    python -m virtualenv vryanairapp

Activate virtual environment:

    source vryanairapp/bin/activate

Install requirements:

    pip install -r requirements.txt

Run the application:

    flask --app app run --host=0.0.0.0 --port=5500



All in one line:
    
    git clone https://github.com/evinlort/ryanair_app.git && cd ryanair_app && python -m virtualenv vryanairapp && source vryanairapp/bin/activate && pip install -r requirements.txt && flask --app app run --host=0.0.0.0 --port=5500