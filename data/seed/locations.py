class Locations:
    def __init__(self, connection):
        self.connection = connection

    def create(self):
        # Types
        self.connection.execute_query(create_city_location)

        # Cities
        self.connection.execute_query(create_anchorhead)

# Types
create_city_location = """
INSERT INTO location_type (
    natural_id,
    display_name
)
SELECT
    "location_type_city",
    "City"
WHERE NOT EXISTS (
    SELECT 1 FROM location_type WHERE natural_id = "location_type_city"
);
"""

# Cities
create_anchorhead = """
INSERT INTO location (
    natural_id,
    type_id,
    world_id,
    display_name,
    description
)
SELECT
    "location_anchorhead",
    "location_type_city",
    "world_tatooine",
    "Anchorhead",
    "A small salavage town, much of the economy is derived from the salvage and trade of scrap found at the nearby ruins of the old Imperial Fort Ironhand."
WHERE NOT EXISTS (
    SELECT 1 from location WHERE natural_id = "location_anchorhead"
);
"""