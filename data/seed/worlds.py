class Worlds:
    def __init__(self, connection):
        self.connection = connection

    def create(self):
        # Types
        self.connection.execute_query(create_desert_planet)

        # Planets
        self.connection.execute_query(create_tatooine)

# Types
create_desert_planet = """
INSERT INTO world_type (
    natural_id,
    display_name
)
SELECT 
    "world_type_desert_planet",
    "Desert Planet"
WHERE NOT EXISTS (
    SELECT 1 FROM world_type WHERE natural_id = "world_type_desert_planet"
);
"""

# Planets
create_tatooine = """
INSERT INTO world (
    natural_id,
    type_id,
    display_name
)
SELECT
    "world_tatooine",
    "Tatooine",
    "world_type_desert_planet"
WHERE NOT EXISTS (
    SELECT 1 FROM world WHERE natural_id = "world_tatooine"
);
"""