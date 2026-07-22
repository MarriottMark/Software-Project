import sqlite3

conn = sqlite3.connect('caffeine.db')
c = conn.cursor()

# Coffee types with average caffeine content per size
c.execute('''
    CREATE TABLE IF NOT EXISTS coffee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        size TEXT NOT NULL,
        caffeine_mg INTEGER NOT NULL
    )
''')

# Age-based caffeine recommendations (mg per day)
c.execute('''
    CREATE TABLE IF NOT EXISTS age_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age_min INTEGER NOT NULL,
        age_max INTEGER NOT NULL,
        max_caffeine_mg INTEGER NOT NULL
    )
''')

# User's drinks log
c.execute('''
    CREATE TABLE IF NOT EXISTS user_drinks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coffee_type TEXT NOT NULL,
        size TEXT NOT NULL,
        caffeine_mg INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# User profile (age)
c.execute('''
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL
    )
''')

# Insert coffee data (average caffeine values from FDA/Mayo Clinic)
coffee_data = [
    # Espresso-based drinks
    ('Espresso', 'Single', 63),
    ('Espresso', 'Double', 126),
    ('Latte', 'Small', 63),
    ('Latte', 'Medium', 126),
    ('Latte', 'Large', 150),
    ('Cappuccino', 'Small', 63),
    ('Cappuccino', 'Medium', 126),
    ('Cappuccino', 'Large', 150),
    ('Flat White', 'Small', 130),
    ('Flat White', 'Medium', 160),
    ('Flat White', 'Large', 195),
    ('Mocha', 'Small', 63),
    ('Mocha', 'Medium', 126),
    ('Mocha', 'Large', 175),
    ('Macchiato', 'Small', 63),
    ('Macchiato', 'Medium', 126),
    ('Macchiato', 'Large', 150),
    ('Americano', 'Small', 63),
    ('Americano', 'Medium', 126),
    ('Americano', 'Large', 150),
    # Brewed coffee
    ('Drip Coffee', 'Small', 95),
    ('Drip Coffee', 'Medium', 165),
    ('Drip Coffee', 'Large', 235),
    ('Cold Brew', 'Small', 100),
    ('Cold Brew', 'Medium', 200),
    ('Cold Brew', 'Large', 300),
    ('Instant Coffee', 'Small', 30),
    ('Instant Coffee', 'Medium', 60),
    ('Instant Coffee', 'Large', 90),
    # Tea-based
    ('Chai Latte', 'Small', 40),
    ('Chai Latte', 'Medium', 80),
    ('Chai Latte', 'Large', 120),
    ('Matcha Latte', 'Small', 40),
    ('Matcha Latte', 'Medium', 80),
    ('Matcha Latte', 'Large', 120),
]

c.executemany('INSERT OR IGNORE INTO coffee (type, size, caffeine_mg) VALUES (?, ?, ?)', coffee_data)

# Age-based recommendations (mg per day)
# Sources: FDA, American Academy of Pediatrics, Mayo Clinic
age_recs = [
    (0, 11, 0),       # Children: no caffeine recommended
    (12, 17, 100),    # Teens: max 100mg
    (18, 24, 200),    # Young adults: max 200mg
    (25, 64, 400),    # Adults: max 400mg (FDA standard)
    (65, 120, 200),   # Seniors: max 200mg (more sensitive)
]

c.executemany('INSERT OR IGNORE INTO age_recommendations (age_min, age_max, max_caffeine_mg) VALUES (?, ?, ?)', age_recs)

conn.commit()
conn.close()
print("Database created successfully!")