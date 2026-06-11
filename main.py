#Imports
from database.formaly_database_manager import init_db
from pages.login.formaly_login import FormalyLoginApp

# Starting the Formaly App
def main():
    # Initialise database
    init_db()
    
    # Creating and launching the login window
    app = FormalyLoginApp()
    app.mainloop()

# Running the application
if __name__ == "__main__":
    main()