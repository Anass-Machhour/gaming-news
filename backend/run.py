from app import create_app

app = create_app()

# For Development
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
    
# For Production
if __name__ == '__main__':
    app.run()