class Races:
    def __init__(self, connection):
        self.connection = connection
    
    def create(self):
        self.connection.execute_query(create_human_race)
        self.connection.execute_query(create_twilek_race)

create_human_race = """
INSERT INTO race (
    natural_id, 
    display_name, 
    description
) 
SELECT 
    "race_human",
    "Human",
    "The galaxy's most numerous and politically dominant sentient species with millions of major and minor colonies galaxywide."
WHERE NOT EXISTS (
    SELECT 1 FROM race WHERE natural_id = "race_human"
);
"""

create_twilek_race = """
INSERT INTO race (
    natural_id,
    display_name,
    description
)
SELECT
    "race_twilek",
    "Twilek",
    "A tall near-human species whose most striking feature is a pair of long appendages protruding from their skulls, called lekku."
WHERE NOT EXISTS(
    SELECT 1 FROM race WHERE natural_id = "race_twilek"
);
"""