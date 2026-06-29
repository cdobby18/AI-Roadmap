"""
One Piece character dataset for semantic search.
Each character has a bio written as a description of their role and abilities —
not using their name, so the search is genuinely semantic, not keyword-based.
"""

CHARACTERS = [
    {
        "name": "Monkey D. Luffy",
        "role": "Pirate Captain",
        "bio": (
            "A rubber-bodied pirate captain who ate the Gum-Gum Devil Fruit, granting him "
            "the ability to stretch his body like rubber. He is completely immune to blunt "
            "impacts and lightning. His ambition is to find the legendary treasure and become "
            "King of the Pirates. He fights using his stretched limbs as weapons and later "
            "awakens the ability to transform into a giant deity-like form using advanced Haki."
        ),
    },
    {
        "name": "Roronoa Zoro",
        "role": "Pirate Swordsman",
        "bio": (
            "A three-sword style swordsman who holds one blade in each hand and one in his "
            "mouth. A former bounty hunter who defected to join a pirate crew. His singular "
            "goal is to become the greatest swordsman in the world by defeating the current "
            "titleholder. He trains relentlessly, rarely sleeps, and gets lost constantly. "
            "He is the first mate and second strongest member of his crew."
        ),
    },
    {
        "name": "Nami",
        "role": "Pirate Navigator",
        "bio": (
            "A skilled navigator and cartographer who can read the weather with near-perfect "
            "accuracy. She grew up in an orange grove village occupied by fish-men pirates and "
            "spent years stealing treasure to buy her village's freedom. She uses a weapon "
            "called the Clima-Tact that lets her control weather phenomena, creating lightning "
            "bolts, storm clouds, and mirages in battle."
        ),
    },
    {
        "name": "Usopp",
        "role": "Pirate Sniper",
        "bio": (
            "A long-nosed sniper and compulsive liar who is the son of a legendary pirate "
            "marksman. He is a coward by nature but forces himself into dangerous situations "
            "out of love for his crewmates. He builds his own weapons from scrap and plant-based "
            "ammunition. His alter ego is a brave warrior of the sea named Sogeking."
        ),
    },
    {
        "name": "Sanji",
        "role": "Pirate Cook",
        "bio": (
            "A chef and martial artist who never uses his hands in battle, fighting exclusively "
            "with powerful kicks. He grew up in a North Blue kingdom as a prince, then trained "
            "under a legendary pirate chef. His kicks generate flames and later invisible cutting "
            "air pressure. He is devoted to women and dreams of finding the All Blue, a legendary "
            "sea containing all species of fish in the world."
        ),
    },
    {
        "name": "Tony Tony Chopper",
        "role": "Pirate Doctor",
        "bio": (
            "A reindeer who ate the Human-Human Devil Fruit, giving him human intelligence and "
            "the ability to transform into various hybrid and full human or animal forms. He is "
            "the ship's doctor and a skilled medical practitioner, having studied under a "
            "renowned doctor on Drum Island. Despite his fearsome transformations, he is childlike "
            "and easily flattered."
        ),
    },
    {
        "name": "Nico Robin",
        "role": "Pirate Archaeologist",
        "bio": (
            "An archaeologist who ate the Flower-Flower Devil Fruit, allowing her to sprout "
            "copies of her body parts — hands, eyes, mouths, limbs — on any surface. She is "
            "the only person alive who can read Poneglyphs, the ancient stone tablets that "
            "record the true history of the world. The World Government hunted her since "
            "childhood, placing a bounty on her head at age eight."
        ),
    },
    {
        "name": "Franky",
        "role": "Pirate Shipwright",
        "bio": (
            "A cyborg shipwright who built and modified his own body with steel and machinery "
            "after surviving a near-fatal accident. He built his pirate crew's ship from the "
            "legendary Adam Tree wood. He can fire cannonballs from his chest, use a sword "
            "built into his arm, and is powered by cola. He is flamboyant, wears no shirt, "
            "and considers himself super cool."
        ),
    },
    {
        "name": "Brook",
        "role": "Pirate Musician",
        "bio": (
            "A living skeleton who ate the Revive-Revive Devil Fruit, which allowed his soul "
            "to return to his body after death. He spent fifty years alone on a ghost ship "
            "waiting for his crew. He fights with a thin blade hidden in a cane and uses "
            "music and ice powers from his soul. He is a former captain of a pirate crew and "
            "a renowned rock star known as Soul King."
        ),
    },
    {
        "name": "Jinbe",
        "role": "Pirate Helmsman",
        "bio": (
            "A whale-shark fish-man and former Warlord of the Sea. He is a master of Fish-Man "
            "Karate, which uses water as a weapon and can be lethal even to Devil Fruit users. "
            "He served under the Whitebeard Pirates and was a childhood hero to the crew's "
            "captain. He is deeply honorable, calm under pressure, and serves as the ship's helmsman."
        ),
    },
    {
        "name": "Trafalgar D. Water Law",
        "role": "Pirate Captain",
        "bio": (
            "A surgeon and pirate captain who ate the Op-Op Devil Fruit, granting him a "
            "spherical zone of control where he can rearrange, disconnect, and teleport "
            "anything within it. A former Warlord of the Sea, he is a calculating strategist "
            "who forms alliances for mutual benefit. He grew up in a country destroyed by a "
            "World Government conspiracy and seeks revenge against those responsible."
        ),
    },
    {
        "name": "Boa Hancock",
        "role": "Pirate Empress",
        "bio": (
            "The pirate empress of Amazon Lily and former Warlord of the Sea. She ate the "
            "Love-Love Devil Fruit, which turns anyone who feels attraction or admiration "
            "for her to stone. She is considered the most beautiful woman in the world. "
            "Despite her cold exterior, she is devoted to the protagonist. She was formerly "
            "enslaved by the World Nobles and bears their mark."
        ),
    },
    {
        "name": "Shanks",
        "role": "Pirate Emperor",
        "bio": (
            "One of the Four Emperors of the Sea, a red-haired pirate captain who inspired "
            "the series protagonist to become a pirate. He is a master of all three forms of "
            "Haki, including Conqueror's Haki so powerful it can render an entire fleet "
            "unconscious. He lost one arm saving the protagonist as a child. He is the most "
            "mysterious Emperor and rarely acts aggressively despite his immense power."
        ),
    },
    {
        "name": "Edward Newgate (Whitebeard)",
        "role": "Pirate Emperor",
        "bio": (
            "The strongest man in the world and one of the Four Emperors, known as Whitebeard. "
            "He ate the Tremor-Tremor Devil Fruit, giving him the power to create earthquakes "
            "and tsunamis. He commanded the largest fleet in the world and considered every "
            "crew member his son. He died defending his crew at Marineford, where he alone "
            "shook the entire ocean."
        ),
    },
    {
        "name": "Gol D. Roger",
        "role": "Pirate King",
        "bio": (
            "The legendary Pirate King who conquered the Grand Line and discovered the "
            "legendary treasure. He turned himself in to the Marines before his execution, "
            "declaring that his treasure was out there for anyone to find — sparking the "
            "Great Pirate Era. He was the only man confirmed to have mastered all forms of "
            "Haki and could hear the voice of all things."
        ),
    },
    {
        "name": "Smoker",
        "role": "Marine Vice Admiral",
        "bio": (
            "A cigar-smoking Marine officer who ate the Smoke-Smoke Devil Fruit, turning his "
            "body into smoke. His smoke can immobilize Devil Fruit users by gripping them. "
            "He is obsessed with capturing the protagonist and follows a strong personal code "
            "of justice. Unlike most Marines, he disobeys corrupt orders and despises the "
            "World Government's political corruption."
        ),
    },
    {
        "name": "Kuzan (Aokiji)",
        "role": "Marine Admiral",
        "bio": (
            "A former Marine Admiral who ate the Ice-Ice Devil Fruit, allowing him to freeze "
            "anything he touches — including the sea itself. He has a relaxed, easygoing "
            "personality that masks immense power. He resigned from the Marines after losing "
            "a ten-day duel against the man who became Fleet Admiral. His true allegiance "
            "remains ambiguous."
        ),
    },
    {
        "name": "Sakazuki (Akainu)",
        "role": "Fleet Admiral",
        "bio": (
            "The current Fleet Admiral of the Marines and the most powerful Marine in the "
            "world. He ate the Magma-Magma Devil Fruit, which burns hotter than fire and "
            "can even burn fire itself. He follows an extreme philosophy of absolute justice "
            "and believes even innocent bystanders must be eliminated if they carry risk. "
            "He killed a major character at Marineford in front of the protagonist."
        ),
    },
    {
        "name": "Dracule Mihawk",
        "role": "Warlord / Swordsman",
        "bio": (
            "The greatest swordsman in the world, wielding a jet-black blade called Yoru — "
            "one of the twelve Supreme Grade swords. He lives alone in a castle on a remote "
            "island and trains those he deems worthy. He fought the protagonist's swordsman "
            "crewmate and spared his life after recognizing his potential. He is a man of "
            "very few words and acts only on his own judgment."
        ),
    },
    {
        "name": "Donquixote Doflamingo",
        "role": "Pirate Warlord",
        "bio": (
            "A flamboyant, pink-feather-coat-wearing former Warlord and king of Dressrosa. "
            "He ate the String-String Devil Fruit, allowing him to produce unbreakable "
            "razor-thin strings he controls like puppeteer wires. He was a World Noble who "
            "renounced his status and became a crime lord dealing in Devil Fruits and weapons. "
            "He is sadistic, theatrical, and controls people with fear."
        ),
    },
    {
        "name": "Kaido",
        "role": "Pirate Emperor",
        "bio": (
            "One of the Four Emperors, known as the world's strongest creature. He ate a "
            "Mythical Zoan Devil Fruit that lets him transform into a massive eastern dragon. "
            "He has survived every execution attempt ever made on him and seeks to die in "
            "the greatest war the world has seen. He conquered Wano Country and ruled it "
            "through fear, force, and political control for over twenty years."
        ),
    },
    {
        "name": "Charlotte Linlin (Big Mom)",
        "role": "Pirate Emperor",
        "bio": (
            "One of the Four Emperors who rules Totto Land, a nation of islands populated "
            "by every race in the world. She ate the Soul-Soul Devil Fruit, allowing her to "
            "steal the lifespan and soul of anyone who fears her and insert souls into "
            "inanimate objects. She has 85 children and uses them to maintain political "
            "marriages across the seas. She has catastrophic hunger pangs that destroy "
            "entire cities."
        ),
    },
    {
        "name": "Sir Crocodile",
        "role": "Pirate Warlord",
        "bio": (
            "A former Warlord of the Sea who ate the Sand-Sand Devil Fruit, giving him full "
            "control over sand including the ability to dry out and crumble anything he "
            "touches. He secretly orchestrated a civil war in the kingdom of Alabasta to "
            "seize control and find an ancient weapon. He runs a crime organization under "
            "the guise of a legitimate peacekeeping force called Baroque Works."
        ),
    },
    {
        "name": "Fujitora (Issho)",
        "role": "Marine Admiral",
        "bio": (
            "A blind Marine Admiral who ate the Gravity-Gravity Devil Fruit, granting him "
            "control over gravitational forces. He can pull meteors from orbit, float "
            "battleships, and crush enemies under crushing force. Despite his rank, he openly "
            "apologized to the people of Dressrosa for the World Government's failures — "
            "an act almost unheard of for a Marine of his standing."
        ),
    },
    {
        "name": "Portgas D. Ace",
        "role": "Pirate Commander",
        "bio": (
            "The second division commander of the Whitebeard Pirates and the protagonist's "
            "adopted older brother. He ate the Flame-Flame Devil Fruit, transforming his "
            "body into fire and controlling it freely. He is the biological son of the "
            "Pirate King. He was captured and publicly executed to draw out a figure from "
            "the Revolutionary Army, triggering the war at Marineford."
        ),
    },
]


def get_all_characters():
    return CHARACTERS


def get_bios():
    return [c["bio"] for c in CHARACTERS]


def get_names():
    return [c["name"] for c in CHARACTERS]


if __name__ == "__main__":
    print(f"Total characters: {len(CHARACTERS)}")
    for c in CHARACTERS:
        print(f"  [{c['role']:25s}] {c['name']}")
