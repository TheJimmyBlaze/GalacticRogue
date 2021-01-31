class Rooms:
    def __init__(self, connection):
        self.connection = connection

    def create(self):
        # Anchorhead
        self.connection.execute_query(create_room_anchorhead_cantina)
        self.connection.execute_query(create_room_anchorhead_maindrag)
        self.connection.execute_query(create_room_anchorhead_scrapdealer)

# Anchorhead
create_room_anchorhead_cantina = """
INSERT INTO room (
    natural_id,
    location_id,
    display_name,
    description
)
SELECT
    "room_anchorhead_cantina",
    "location_anchorhead",
    "Rogue\'s Den",
    "The most popular Cantina in Anchorhead, the only Cantina in Anchorhead."
WHERE NOT EXISTS (
    SELECT 1 FROM room WHERE natural_id = "room_anchorhead_cantina"
);
"""

create_room_anchorhead_maindrag = """
INSERT INTO room (
    natural_id,
    location_id,
    display_name,
    description
)
SELECT
    "room_anchorhead_maindrag",
    "location_anchorhead",
    "Anchorhead Main Drag",
    "Anchorhead\'s main \'Street\'."
WHERE NOT EXISTS (
    SELECT 1 FROM room WHERE natural_id = "room_anchorhead_maindrag"
);
"""

create_room_anchorhead_scrapdealer = """
INSERT INTO room (
    natural_id,
    location_id,
    display_name,
    description
)
SELECT
    "room_anchorhead_scrapdealer",
    "location_anchorhead",
    "Gifted Hand Emporium",
    "Purveyors of scrap and salvage."
WHERE NOT EXISTS (
    SELECT 1 FROM room WHERE natural_id = "room_anchorhead_scrapdealer"
);
"""