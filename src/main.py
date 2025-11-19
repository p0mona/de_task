from helpers import *

def main():
    arg = arg_parse()
    output_file = "query_results"

    db = DBManager()
    db.conn_db()

    db.load_data(arg.locations, LocationsParse, 'locations')
    db.load_data(arg.devices, DevicesParse, 'devices')
    db.load_data(arg.events, EventsParse, 'events')

    db.conn.commit()

    executor = Executor(db)
    all_results = executor.run()

    exporter = Exporter(all_results, output_file)
    exporter.export(arg.format)

    db.conn.close()

if __name__ == "__main__":
    main()
