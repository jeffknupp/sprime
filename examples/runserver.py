import models
from sandman import custom_class_app

app = custom_class_app('sqlite+pysqlite:///examples/db.sqlite3')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
