from app import app

from apis import initialize_routes
initialize_routes(app)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')