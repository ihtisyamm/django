import requests
from requests.auth import HTTPBasicAuth
import getpass
from django.contrib.auth import authenticate, login


class ClientApplication:
    def __init__(self):
        self.baseURL = "https://sc22mibs.pythonanywhere.com/"
        self.session = requests.Session()
        self.isAuthenticated = False

    def register(self):
        username = input("username: ")
        email = input("email: ")
        password = getpass.getpass("password: ")

        url = f"{self.baseURL}register/"
        data = {"username": username,
                "email": email,
                "password": password}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Registration successful!")
            else:
                print(f"Registration failed with status code {response.status_code}")
        except Exception as e:
            print(str(e))
    
    def login(self, url):
        if self.isAuthenticated:
            print("Already logged in. Logout first")
            return False

        if not url.startswith("https://"):
            url = f"https://{url}"

        if not url.endswith('/'):
            url += '/'
        
        username = input("username: ")
        password = getpass.getpass("password: ")

        if not username.strip() or not password.strip():
            print("Username or password cannot be blank")
            return False
        
        authURL = f"{url}api-token-auth/"
        
        try:
            response = requests.post(authURL,
                                     json={"username": username,
                                           "password": password})
            if response.status_code == 200:
                token = response.json().get("token")
                self.session = requests.Session()
                self.session.headers.update({"Authorization": f"Token {token}"})
                
                print(f"Login successful!")
                self.isAuthenticated = True
                
                return True
            elif response.status_code == 400:
                print("Wrong password or username")
                return False
            else:
                print(f"Login error with {response.status_code}")
                return False
        except Exception as e:
            print(f"Token auth error {str(e)}")
            return False
            
    

    def logout(self):
        if not self.isAuthenticated:
            print("Sorry. Not LOGIN yet. Use 'help'")
            return
        
        try:
            print("Successfully logout!")
            self.session = requests.Session()
            self.isAuthenticated = False
        except Exception as e:
            print(str(e))

    def list(self):
        
        url = f"{self.baseURL}/module-instances/"

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                modules = response.json()

                if not modules:
                    print("No module instances found")
                    return
                
                
                print(f"{'Code':<{8}} {'Name':<{46}} {'Year':<{8}} {'Semester':<{10}} {'Taught by'}")

                for module in modules:
                    code = module.get('moduleCode')
                    name = module.get('moduleName')
                    year = module.get('year')
                    semester = module.get('semester')

                    professorss = []
                    for p in module.get('professors', []):
                        professorss.append(f"{p['id']}, Professor {p['name']}")
                        
                    professors = ", ".join(professorss)

                    print(f"{code:<{8}} {name:<{46}} {year:<{8}} {semester:<{10}} {professors}")
                    print("-" * 100)
            else:
                print(f"Error with status code {response.status_code}")
        except Exception as e:
            print(str(e))

    def view(self):
        
        url = f"{self.baseURL}/professor-ratings/"

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                ratings = response.json()

                if not ratings:
                    print("No professors found")
                    return
                
                for prof in ratings:
                    profID = prof.get('id')
                    name = prof.get('name')
                    rating = prof.get('average_rating')
                    if rating is None or rating == 0:
                        print(f"The rating of Professor {name} ({profID}) is not available")
                    else:
                        stars = "*" * int(rating)
                        print(f"The rating of Professor {name} ({profID}) is {stars}")

            else:
                print(f"Error status code {response.status_code}")
        except Exception as e:
            print(f"Error {str(e)}")


    def average(self, professorID, moduleCode):
        
        url = f"{self.baseURL}/professor-module-rating/{professorID}/{moduleCode}/"

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                name = data.get('name')
                rating = data.get('module_rating')
                if rating is None or rating == 0:
                    print(f"The rating of Professor {name} ({professorID}) in module {moduleCode} is not available")
                else:
                    stars = "*" * int(rating)
                    print(f"The rating of Professor {name} ({professorID}) in module {moduleCode} is {stars}")
            else:
                print(f"Error status code {response.status_code}")

        except Exception as e:
            print(f"Error {str(e)}")

    
     
    def rate(self, professorID, moduleCode, year, semester, rating):
        if not self.isAuthenticated:
            print("Sorry. Not LOGIN yet. Use 'help'")
            return
            
        url = f"{self.baseURL}rate-professor/"
        
        try:

            data = {
                "professorID": professorID,
                "moduleCode": moduleCode,
                "year": int(year),
                "semester": int(semester),
                "rating": int(rating)
            }
        
            response = self.session.post(url, json=data)
            if response.status_code in [200, 201]:
                print(f"Successfully rated Professor {professorID} in {moduleCode} (Year {year}, Semester {semester}) with {rating} stars")
            else:
                print(f"Error status code {response.status_code} {self.session.cookies} {response.text}")
        except Exception as e:
            print(f"Error {str(e)}")         
   
    def run(self):
        print("Professor Rating Client Application")
        print("Type 'help' for a list of commands or 'exit' to quit")
        
        while True:
            try:
                commands = input("> ").strip()
                
                if not commands:
                    continue
                    
                parts = commands.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command == 'exit' or command == 'quit':
                    print("Goodbye and Thank You!")
                    break
                elif command == 'help':
                    self.help()
                elif command == 'register':
                    self.register()
                elif command == 'login':
                    if len(args) != 1:
                        print("Login requires a URL argument!")
                        print("Usage: login <url>")
                    else:
                        self.login(args[0])
                elif command == 'logout':
                    self.logout()
                elif command == 'list':
                    self.list()
                elif command == 'view':
                    self.view()
                elif command == 'average':
                    if len(args) != 2:
                        print("Average requires PROFESSOR ID and MODULE CODE!")
                        print("Usage: average <professorID> <module_code>")
                    else:
                        self.average(args[0], args[1])
                elif command == 'rate':
                    if len(args) != 5:
                        print("Rate requires PROFESSOR ID, MODULE CODE, YEAR, SEMESTER, and RATING!")
                        print("Usage: rate <professorID> <module_code> <year> <semester> <rating>")
                    else:
                        self.rate(args[0], args[1], args[2], args[3], args[4])
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for a list of commands")
            except KeyboardInterrupt:
                print("\nGoodbye and Thank You!")
                break
    
    def help(self):
        """Display help information"""
        print("Available commands:")
        print("  register - Register a new user")
        print("  login <url> - Login to the service")
        print("  logout - Logout from the service")
        print("  list - View all module instances and professors")
        print("  view - View ratings of all professors")
        print("  average <professorID> <module_code> - View average rating for a professor in a module")
        print("  rate <professorID> <module_code> <year> <semester> <rating> - Rate a professor")
        print("  help - Show this help message")
        print("  exit - Exit the client")


if __name__ == "__main__":
    client = ClientApplication()
    client.run()
