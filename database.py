import sqlite3

conn = sqlite3.connect('glasses.db')
c = conn.cursor()

# Create the glasses table with additional fields for gender and type
c.execute('''
    CREATE TABLE glasses (
        id INTEGER PRIMARY KEY,
        path TEXT NOT NULL,
        gender TEXT NOT NULL,
        type TEXT NOT NULL
    )
''')

# Insert data into the glasses table
glasses_data = [
    (1, 'Glasses Image\\Male\\Male Glasses\\BIMINI ROAD 320 - Male.png', 'Male', 'Glasses'),
    (2, 'Glasses Image\\Male\\Male Glasses\\BIMINI ROAD 500 - Male.png', 'Male', 'Glasses'),
    (3, 'Glasses Image\\Male\\Male Glasses\\MARIANA TRENCH 410 - Male.png', 'Male', 'Glasses'),
    (4, 'Glasses Image\\Male\\Male Glasses\\MARIANA TRENCH 500 - Male.png', 'Male', 'Glasses'),
    (5, 'Glasses Image\\Male\\Male Glasses\\OCEAN RIDGE 800 - Male.png', 'Male', 'Glasses'),
    (6, 'Glasses Image\\Male\\Male Glasses\\OCEAN RIDGE 820 - Male.png', 'Male', 'Glasses'),
    (7, 'Glasses Image\\Male\\Male Sunglasses\\ANTILLE - Male.png', 'Male', 'Sunglasses'),
    (8, 'Glasses Image\\Male\\Male Sunglasses\\FERG XL - Male.png', 'Male', 'Sunglasses'),
    (9, 'Glasses Image\\Male\\Male Sunglasses\\GRAND CATALINA - Male.png', 'Male', 'Sunglasses'),
    (10, 'Glasses Image\\Male\\Male Sunglasses\\KING TIDE 8 - Male.png', 'Male', 'Sunglasses'),
    (11, 'Glasses Image\\Male\\Male Sunglasses\\RINCONCITO - Male.png', 'Male', 'Sunglasses'),
    (12, 'Glasses Image\\Male\\Male Sunglasses\\TAILFIN - Male.png', 'Male', 'Sunglasses'),
    (13, 'Glasses Image\\Female\\Female Glasses\\FERNANDINA RX - Female.png', 'Female', 'Glasses'),
    (14, 'Glasses Image\\Female\\Female Glasses\\MARIANA TRENCH 430 - Female.png', 'Female', 'Glasses'),
    (15, 'Glasses Image\\Female\\Female Glasses\\OCEAN RIDGE 210 - Female.png', 'Female', 'Glasses'),
    (16, 'Glasses Image\\Female\\Female Glasses\\OCEAN RIDGE 510 - Female.png', 'Female', 'Glasses'),
    (17, 'Glasses Image\\Female\\Female Glasses\\SALINA RX - Female.png', 'Female', 'Glasses'),
    (18, 'Glasses Image\\Female\\Female Sunglasses\\ANAA - Female.png', 'Female', 'Sunglasses'),
    (19, 'Glasses Image\\Female\\Female Sunglasses\\CALDERA - Female.png', 'Female', 'Sunglasses'),
    (20, 'Glasses Image\\Female\\Female Sunglasses\\CATHERINE - Female.png', 'Female', 'Sunglasses'),
    (21, 'Glasses Image\\Female\\Female Sunglasses\\EGRET - Female.png', 'Female', 'Sunglasses'),
    (22, 'Glasses Image\\Female\\Female Sunglasses\\FERNANDINA - Female.png', 'Female', 'Sunglasses'),
    (23, 'Glasses Image\\Female\\Female Sunglasses\\GANNET - Female.png', 'Female', 'Sunglasses'),
    (24, 'Glasses Image\\Female\\Female Sunglasses\\NUSA - Female.png', 'Female', 'Sunglasses'),
    (25, 'Glasses Image\\Female\\Female Sunglasses\\PALMAS - Female.png', 'Female', 'Sunglasses'),
    (26, 'Glasses Image\\Female\\Female Sunglasses\\PANGA - Female.png', 'Female', 'Sunglasses'),
    (27, 'Glasses Image\\Female\\Female Sunglasses\\WATERWOMAN - Female.png', 'Female', 'Sunglasses'),
]

c.executemany('''
    INSERT INTO glasses (id, path, gender, type) VALUES (?, ?, ?, ?)
''', glasses_data)

conn.commit()
conn.close()
