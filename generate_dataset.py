import pandas as pd
import random

# ---------- Define Products ----------
milk_animals = ['cow', 'buffalo', 'goat']
egg_sizes = ['small', 'medium', 'large']
egg_conditions = ['clean', 'dirty']
honey_types = ['light', 'dark']
fruits = ['mango','apple','banana','grapes','papaya','pineapple','guava','orange','pear','kiwi','strawberry','blueberry','watermelon']
vegetables = ['spinach','tomato','potato','onion','carrot','cabbage','cauliflower',
              'cucumber','pepper','lettuce','radish','beetroot','chilli','broccoli','zucchini']

storage_options = ['room','refrigerated']

# ---------- Generate Random Data ----------
rows = []

for _ in range(3000):
    product_type = random.choice(['milk','eggs','honey','fruits','vegetables'])

    if product_type == 'milk':
        animal = random.choice(milk_animals)
        time_of_day = random.choice(['morning','evening'])
        storage = random.choice(storage_options)
        days_since = random.randint(0,7)
        # Derived features
        if animal == 'cow':
            density, fat, snf = 1.03, 3.5, 8.5
        elif animal == 'buffalo':
            density, fat, snf = 1.04, 6.5, 9.0
        else:
            density, fat, snf = 1.032, 4.5, 8.0
        freshness = max(0, 100 - days_since*15)
        rows.append([product_type, animal, time_of_day, storage, days_since, density, fat, snf, '', '', '', '', '', '', '', '', freshness])

    elif product_type == 'eggs':
        size = random.choice(egg_sizes)
        condition = random.choice(egg_conditions)
        storage = random.choice(storage_options)
        days_since = random.randint(0,14)
        freshness = max(0, 100 - days_since*7)
        rows.append([product_type, '', '', storage, days_since, 0,0,0, size, condition, '', '', '', '', '', '', freshness])

    elif product_type == 'honey':
        htype = random.choice(honey_types)
        storage = random.choice(storage_options)
        days_since = random.randint(0,365)
        purity = 85 if htype=='light' else 80
        moisture = 17 if htype=='light' else 20
        freshness = max(0, 100 - days_since*0.1)
        rows.append([product_type, '', '', storage, days_since, 0,0,0, '', '', htype, purity, moisture, '', '', '', freshness])

    elif product_type == 'fruits':
        name = random.choice(fruits)
        size = random.choice(['small','medium','large'])
        ripeness = random.choice(['soft','medium','hard'])
        color = random.choice(['green','red','yellow'])
        quantity = random.randint(1,50)
        storage = random.choice(storage_options)
        days_since = random.randint(0,7)
        freshness = max(0, 100 - days_since*10)
        rows.append([product_type, '', '', storage, days_since, 0,0,0, size, '', '', '', '', name, ripeness, color, quantity, freshness])

    else:  # vegetables
        name = random.choice(vegetables)
        size = random.choice(['small','medium','large'])
        ripeness = random.choice(['soft','medium','hard'])
        color = random.choice(['green','red','yellow'])
        quantity = random.randint(1,50)
        storage = random.choice(storage_options)
        days_since = random.randint(0,7)
        freshness = max(0, 100 - days_since*10)
        rows.append([product_type, '', '', storage, days_since, 0,0,0, size, '', '', '', '', name, ripeness, color, quantity, freshness])

# ---------- Columns ----------
columns = ['product','animal','time_of_day','storage','days_since',
           'density','fat','snf','size','condition',
           'type','purity','moisture',
           'name','ripeness','color','quantity','freshness']

df = pd.DataFrame(rows, columns=columns)

# ---------- Assign Grade ----------
def assign_grade(freshness):
    if freshness >= 80:
        return 'A'
    elif freshness >=50:
        return 'B'
    else:
        return 'C'

df['grade'] = df['freshness'].apply(assign_grade)

# Save CSV
df.to_csv('dataset.csv', index=False)
print("Dataset generated with", len(df), "rows")
