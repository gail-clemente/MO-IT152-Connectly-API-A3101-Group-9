Directions:
  1. Create a new virtual environment:
     
     ``` python -m venv .venv ```
  2. Activate the virtual environment:
     
     ``` .\.venv\Scripts\activate ```
  3. Press 'CTRL + SHIFT + P' and select Python: Select Interpreter. Choose the one with your virtual environment.
  4. Open a terminal and copy this code:
     
     ``` pip install -r requirements.txt ```
  5. The requirements . txt includes all the necessary dependencies you will need
  6. Perform migrations:

     ``` python manage.py migrate ```

  7. For you to easily access tokens, create a superuser from django and input the asked credentials (please do not forget)

     ``` python manage.py createsuperuser ```

  8. Run the server:

     ``` python manage.py runserver_plus --cert-file cert.pem --key-file key.pem ```

  9. Paste this in your web browser and enter your admin credentials:

     ``` https://127.0.0.1:8000/admin/ ```


