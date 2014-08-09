from sandman import reflect_all_app

app = reflect_all_app('sqlite+pysqlite:///examples/db.sqlite3')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
