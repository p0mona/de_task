from helpers import *

def main():
    '''
    The main entry point for this application

    1. Parse command line arguments
    2. Load JSON data to database
    3. Execute SQL queries
    4. Export .json or .xml output file
    '''
    
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
