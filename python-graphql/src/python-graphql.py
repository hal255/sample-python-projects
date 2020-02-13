import graphene

class MyApp:
    def __init__(self):
        self.message = "hello graphql"

    def run(self):
        print(self.message)

if __name__ == "__main__":
    driver = MyApp()
    driver.run()    
    pass