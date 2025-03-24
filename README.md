**User Login API**

This is a Django-based API for user authentication, including registration and login functionality.

### **Features**
- User registration
- User login
- Token-based authentication
- Password hashing for security
- User logout with cookie deletion

### **Installation**
1. Make sure you have Python and pip installed.
2. Install the required dependencies by running the following command:

    ```sh
    pip install -r requirements.txt
    ```

### **Database Setup**
Before running the project, you need to apply migrations to set up the database. Run these commands:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

### **Running the Server**
After setting up the database, you can start the Django development server with this command:

    ```sh
    python manage.py runserver
    ```

Once the server is running, you can access it at `http://127.0.0.1:8000/`.

### **API Endpoints**
- To register a new user, send a **POST** request to `/api/register/`. The request body should include `username`, `email`, and `password`.
- To log in, send a **POST** request to `/api/login/`. The request body should include `username` and `password`. The response will include `access` and `refresh` tokens, and the `username`.
- To log out, send a **POST** request to `/api/logout/`. The request body should include the `username` and `password`.

### **Notes**
- Make sure to configure your database settings in `settings.py`.
- The `LogoutView` will log out the user and delete the `username` cookie.

