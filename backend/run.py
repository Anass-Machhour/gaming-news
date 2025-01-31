from app import create_app

app = create_app()
    
# For Production
if __name__ == '__main__':
    app.run()