from src import init_app

app = init_app()

# @app.route("/")
# def home():
#     return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')