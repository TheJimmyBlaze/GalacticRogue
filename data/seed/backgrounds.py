class Backgrounds:
    def __init__(self, connection):
        self.connection = connection

    def create(self):
        self.connection.execute_query(create_bounty_hunter)
        self.connection.execute_query(create_starship_mechanic)
        self.connection.execute_query(create_heir)

create_bounty_hunter = """
INSERT INTO background (
    natural_id,
    display_name,
    description,
    observation
)
SELECT
    "background_bounty_hunter",
    "Bounty Hunter",
    "An upstart chasing a payday, armed with a blaster and the skill to use it.",
    "you don't look like much."
WHERE NOT EXISTS(
    SELECT 1 FROM background WHERE natural_id = "background_bounty_hunter"
);
"""

create_starship_mechanic = """
INSERT INTO background (
    natural_id,
    display_name,
    description,
    observation
)
SELECT
    "background_starship_mechanic",
    "Starship Mechanic",
    "Their trusty wrench could work on a starship. Good for smacking Wamp Rats too.",
    "you ever work on a warship?"
WHERE NOT EXISTS(
    SELECT 1 FROM background WHERE natural_id = "background_starship_mechanic"
);
"""

create_heir = """
INSERT INTO background (
    natural_id,
    display_name,
    description,
    observation
)
SELECT
    "background_heir",
    "Wealthy Heir",
    "The favoured child of a wealthy family of traders. A priviledge upbringing, but not much to show for it.",
    "you're credits won't go far here."
WHERE NOT EXISTS(
    SELECT 1 FROM background WHERE natural_id = "background_heir"
);
"""