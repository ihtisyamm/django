#!/usr/bin/env python3
import argparse
import requests
import getpass
import json
import sys

class ProfessorRatingClient:
    def __init__(self):
        self.base_url = None
        self.session = requests.Session()
        self.auth_token = None

    def register(self):
        """Register a new user"""
        username = input("Username: ")
        email = input("Email: ")
        password = getpass.getpass("Password: ")
        
        if not self.base_url:
            print("Error: You need to login first to set the base URL")
            return
            
        url = f"{self.base_url}/api/register/"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Registration successful! You can now login.")
            else:
                print(f"Registration failed: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def login(self, url):
        """Login to the service"""
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        self.base_url = url.rstrip('/')
        
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        auth_url = f"{self.base_url}/api/api-auth/login/"
        
        # First, get the CSRF token
        try:
            response = self.session.get(auth_url)
            
            # Then authenticate
            login_data = {
                "username": username,
                "password": password,
            }
            
            response = self.session.post(auth_url, data=login_data)
            
            if response.status_code == 200:
                print("Login successful!")
            else:
                print(f"Login failed: {response.text}")
                self.base_url = None
        except Exception as e:
            print(f"Error connecting to {url}: {str(e)}")
            self.base_url = None

    def logout(self):
        """Logout from the service"""
        if not self.base_url:
            print("Error: Not logged in")
            return
            
        try:
            self.session = requests.Session()
            print("Logged out successfully")
        except Exception as e:
            print(f"Error during logout: {str(e)}")

    def list_modules(self):
        """List all module instances and professors teaching them"""
        if not self.base_url:
            print("Error: Not logged in")
            return
            
        url = f"{self.base_url}/api/module-instances/"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                modules = response.json()
                
                if not modules:
                    print("No module instances found.")
                    return
                
                # Print formatted output
                for module in modules:
                    code = module['module_code']
                    name = module['module_name']
                    year = module['year']
                    semester = module['semester']
                    
                    # Format professors list
                    professors = ", ".join([f"{p['id']}, Professor {p['name']}" for p in module['professors']])
                    
                    print(f"Code\tName\tYear\tSemester\tTaught by")
                    print(f"{code}\t{name}\t{year}\t{semester}\t{professors}")
                    print("-" * 100)
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def view_ratings(self):
        """View ratings of all professors"""
        if not self.base_url:
            print("Error: Not logged in")
            return
            
        url = f"{self.base_url}/api/professor-ratings/"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                ratings = response.json()
                
                if not ratings:
                    print("No professors found.")
                    return
                
                for prof in ratings:
                    prof_id = prof['id']
                    name = prof['name']
                    rating = prof['average_rating']
                    stars = "*" * rating
                    
                    print(f"The rating of Professor {name} ({prof_id}) is {stars}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def view_average(self, professor_id, module_code):
        """View the average rating of a professor in a module"""
        if not self.base_url:
            print("Error: Not logged in")
            return
            
        url = f"{self.base_url}/api/professor-module-rating/{professor_id}/{module_code}/"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                name = data['name']
                rating = data['module_rating']
                stars = "*" * rating
                
                print(f"The rating of Professor {name} ({professor_id}) in module {module_code} is {stars}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def rate_professor(self, professor_id, module_code, year, semester, rating):
        """Rate a professor for a module instance"""
        if not self.base_url:
            print("Error: Not logged in")
            return
            
        url = f"{self.base_url}/api/rate-professor/"
        
        data = {
            "professor_id": professor_id,
            "module_code": module_code,
            "year": int(year),
            "semester": int(semester),
            "rating": int(rating)
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code in [200, 201]:
                print(f"Successfully rated Professor {professor_id} in {module_code} (Year {year}, Semester {semester}) with {rating} stars")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Professor Rating Service Client")
    parser.add_argument('command', choices=['register', 'login', 'logout', 'list', 'view', 'average', 'rate'], 
                        help='Command to execute')
    parser.add_argument('args', nargs='*', help='Additional arguments for the command')
    
    args = parser.parse_args()
    
    client = ProfessorRatingClient()
    
    if args.command == 'register':
        client.register()
    elif args.command == 'login':
        if len(args.args) != 1:
            print("Error: login requires a URL argument")
            print("Usage: login <url>")
            sys.exit(1)
        client.login(args.args[0])
    elif args.command == 'logout':
        client.logout()
    elif args.command == 'list':
        client.list_modules()
    elif args.command == 'view':
        client.view_ratings()
    elif args.command == 'average':
        if len(args.args) != 2:
            print("Error: average requires professor_id and module_code")
            print("Usage: average <professor_id> <module_code>")
            sys.exit(1)
        client.view_average(args.args[0], args.args[1])
    elif args.command == 'rate':
        if len(args.args) != 5:
            print("Error: rate requires professor_id, module_code, year, semester, and rating")
            print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
            sys.exit(1)
        client.rate_professor(args.args[0], args.args[1], args.args[2], args.args[3], args.args[4])

if __name__ == "__main__":
    main()