from helpers import DBManager, LocationsParse, DevicesParse, EventsParse

def main():
    db = DBManager()
    db.conn_db()

    db.load_data('data/locations.json', LocationsParse, 'locations')
    db.load_data('data/devices.json', DevicesParse, 'devices')
    db.load_data('data/events.json', EventsParse, 'events')

    db.conn.commit()
    db.conn.close()

if __name__ == "__main__":
    main()
