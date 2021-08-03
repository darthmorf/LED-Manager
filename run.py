from app import app

if __name__ == '__main__':
  start()

def start():
  app.run(debug=True, host= '0.0.0.0', use_reloader=False)