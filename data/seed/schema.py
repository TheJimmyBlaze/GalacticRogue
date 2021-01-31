from data.seed.worlds import Worlds
from data.seed.locations import Locations
from data.seed.rooms import Rooms
from data.seed.races import Races
from data.seed.backgrounds import Backgrounds

class Schema:
    def __init__(self, connection):
        self.connection = connection

    def create(self):
        print("Preparing schema...")
        self.__create_tables()
        self.__populate_rows()
        print("Schema ready")

    def __create_tables (self):
        self.connection.execute_query(create_world_type_table)
        self.connection.execute_query(create_world_table)
        self.connection.execute_query(create_location_type_table)
        self.connection.execute_query(create_location_table)
        self.connection.execute_query(create_room_table)
        self.connection.execute_query(create_item_type_table)
        self.connection.execute_query(create_item_size_table)
        self.connection.execute_query(create_item_table)
        self.connection.execute_query(create_container_table)
        self.connection.execute_query(create_inventory_table)
        self.connection.execute_query(create_furniture_table)
        self.connection.execute_query(create_furnishing_table)
        self.connection.execute_query(create_door_table)
        self.connection.execute_query(create_race_table)
        self.connection.execute_query(create_background_table)
        self.connection.execute_query(create_character_table)

    def __populate_rows(self):
        Worlds(self.connection).create()
        Locations(self.connection).create()
        Rooms(self.connection).create()
        Races(self.connection).create()
        Backgrounds(self.connection).create()

create_world_type_table = """
CREATE TABLE IF NOT EXISTS world_type (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE
);
"""

create_world_table = """
CREATE TABLE IF NOT EXISTS world (
    natural_id TEXT PRIMARY KEY,
    type_id TEXT NOT NULL,
    display_name TEXT NOT NULL UNIQUE,

    FOREIGN KEY (type_id) REFERENCES world_type (natural_id)
);
"""

create_location_type_table = """
CREATE TABLE IF NOT EXISTS location_type (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE
);
"""

create_location_table = """
CREATE TABLE IF NOT EXISTS location (
    natural_id TEXT PRIMARY KEY,
    type_id TEXT NOT NULL,
    world_id TEXT NOT NULL,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL UNIQUE,

    FOREIGN KEY (type_id) REFERENCES location_type (natural_id),
    FOREIGN KEY (world_id) REFERENCES world (natural_id)
);
"""

create_room_table = """
CREATE TABLE IF NOT EXISTS room (
    natural_id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,

    FOREIGN KEY (location_id) REFERENCES location (natural_id)
);
"""

create_item_type_table = """
CREATE TABLE IF NOT EXISTS item_type (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE
);
"""

create_item_size_table = """
CREATE TABLE IF NOT EXISTS item_size (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    value INTEGER NOT NULL UNIQUE
);
"""

create_item_table = """
CREATE TABLE IF NOT EXISTS item (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    type_id TEXT NOT NULL,
    size_id TEXT NOT NULL,

    FOREIGN KEY (type_id) REFERENCES item_type (natural_id),
    FOREIGN KEY (size_id) REFERENCES item_size (natural_id)
);
"""

create_container_table = """
CREATE TABLE IF NOT EXISTS container (
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_item_size_id TEXT NOT NULL,

    FOREIGN KEY (max_item_size_id) REFERENCES item_size (natural_id)
);
"""

create_inventory_table = """
CREATE TABLE IF NOT EXISTS inventory (
    container_id INTEGER NOT NULL,
    item_id TEXT NOT NULL,
    count INTEGER NOT NULL,

    FOREIGN KEY (container_id) REFERENCES container (identity_id),
    FOREIGN KEY (item_id) REFERENCES item (natural_id)
);
"""

create_furniture_table = """
CREATE TABLE IF NOT EXISTS furniture (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);
"""

create_furnishing_table = """
CREATE TABLE IF NOT EXISTS furnishing (
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    furniture_id TEXT NOT NULL,
    room_id TEXT NOT NULL,
    container_id TEXT NULL,

    FOREIGN KEY (room_id) REFERENCES room (natural_id),
    FOREIGN KEY (furniture_id) REFERENCES furniture (natural_id),
    FOREIGN KEY (container_id) REFERENCES container (identity_id) 
);
"""

create_door_table = """
CREATE TABLE IF NOT EXISTS door (
    room_one_id TEXT NOT NULL,
    room_two_id TEXT NOT NULL,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,

    PRIMARY KEY (room_one_id, room_two_id),
    FOREIGN KEY (room_one_id) REFERENCES room (natural_id),
    FOREIGN KEY (room_two_id) REFERENCES room (natural_id)
);
"""

create_race_table = """
CREATE TABLE IF NOT EXISTS race (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    observation TEXT NOT NULL
);
"""

create_background_table = """
CREATE TABLE IF NOT EXISTS background (
    natural_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    observation TEXT NOT NULL
);
"""

create_character_table = """
CREATE TABLE IF NOT EXISTS character (
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id TEXT NOT NULL,
    background_id TEXT NOT NULL,
    room_id TEXT NULL,
    container_id TEXT NULL,
    discord_id TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL UNIQUE,

    FOREIGN KEY (race_id) REFERENCES race (natural_id),
    FOREIGN KEY (background_id) REFERENCES background (natural_id),
    FOREIGN KEY (room_id) REFERENCES room (natural_id),
    FOREIGN KEY (container_id) REFERENCES container (identity_id)
);
"""