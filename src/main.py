from helpers import *

def main():
    arg = arg_parse()

    db = DBManager()
    db.conn_db()

    db.load_data(arg.locations, LocationsParse, 'locations')
    db.load_data(arg.devices, DevicesParse, 'devices')
    db.load_data(arg.events, EventsParse, 'events')

    db.conn.commit()
    db.conn.close()

    executor = Executor(db)
    all_results = executor.run()

if __name__ == "__main__":
    main()
