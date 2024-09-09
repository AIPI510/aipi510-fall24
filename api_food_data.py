import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import csv


API_KEY = '0K17D4gSxSZPOejXfaa5ewB39zmbrk5lFg9Tkvax'
BASE_URL = "https://api.nal.usda.gov/fdc/v1/"


# Call API to grab the desired data.
def call_api(endpoint, API_KEY=API_KEY, query=None):
    params = {
        'api_key': API_KEY,
        'query': query,
    }
    response = requests.get(f'{BASE_URL}{endpoint}', params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data!")
        return None


# Search for food and its basic information.
def get_food_info(food_name):
    foods = call_api(endpoint='foods/search', query=food_name)
    if foods:
        food_item = foods.get('foods', [])[0]
        if food_item:
            fdc_id = food_item.get('fdcId')
        return foods, fdc_id
    else:
        print(f'Failed to retrieve data!')
        return None


# Retrieve nutrients information for a specific food item by its FDC ID.
def get_nutrient_info(fdc_id):
    food_data = call_api(endpoint=f'food/{fdc_id}')
    nutrients = food_data.get('foodNutrients', [])
    return nutrients


# Return calories information of searched food.
def analyze_calories(food_name):
    food, fdc_id = get_food_info(food_name)
    food_item = food.get('foods', [])[0]
    if food_item:
        with open('food_item.json', 'w') as file:
            json.dump(food_item, file, indent=4)
        print(f"FDC ID of {food_name}: {fdc_id}.")

        nutrients = food_item.get('foodNutrients', [])
        calories_info = next((nutrient for nutrient in nutrients if nutrient.get('nutrientName') == 'Energy'), {})
        calories = calories_info.get('value', 'N/A')

        print(f'Food: {food_name}, Calories: {calories} kcal')


# Get nutrient information of searched food.
def analyze_nutrients(food_name):
    
    fdc_id = get_food_info(food_name)[1]
    if fdc_id:
        nutrients = get_nutrient_info(fdc_id)

        # extract nutrient data.
        nutrient_data = {}
        labels = []
        values = []
        other_value = 0

        for nutrient in nutrients:
            nutrient_name = nutrient.get('nutrient', {}).get('name')
            if nutrient_name:
                nutrient_amount = nutrient.get('amount')
                nutrient_unit = nutrient.get('nutrient', {}).get('unitName')
                nutrient_amount_grams = convert_to_grams(nutrient_amount, nutrient_unit)
                if nutrient_amount_grams is not None:
                    nutrient_data[nutrient_name] = nutrient_amount_grams

        # Sort by nutrient content.
        sorted_nutrients = sorted(nutrient_data.items(), key=lambda x: x[1], reverse=True)

        # Extract the top 6 nutrients, and the rest are classified as 'others'.
        for idx, (nutrient_name, nutrient_amount) in enumerate(sorted_nutrients):
            if idx < 6:
                labels.append(nutrient_name)
                values.append(nutrient_amount)
            else:
                other_value += nutrient_amount

        if other_value > 0:
            labels.append("Others")
            values.append(other_value)

        # Create a horizontal bar chart.
        plt.figure(figsize=(20, 10))
        colors = sns.color_palette("pastel", len(labels))  # Use the Seaborn palette
        bars = plt.barh(labels, values, color=colors)

        plt.xlabel('Amount (grams)')
        plt.title(f'Nutrient Composition of {food_name}')

        # Displays the value after each bar.
        for bar, value in zip(bars, values):
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{value:.2f}',
                     va='center', ha='left')

        plt.gca().invert_yaxis()
        plt.show()

    # save file to csv.
    file_name = 'nutrient_data.csv'
    save_data_to_csv(food_name, dict(sorted_nutrients), file_name)

    return fdc_id


# an assist funciton help to convert the food unit into grams.
def convert_to_grams(amount, unit):
    if unit.lower() == 'mg':
        return amount / 1000
    elif unit.lower() == 'g':
        return amount
    else:
        return None


# an assist function to save the retrieved data into a csv file.
def save_data_to_csv(foodname, data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([foodname])
        writer.writerow(['Nutrient', 'Amount (grams)'])

        for nutrient, amount in data.items():
            writer.writerow([nutrient, amount])


if __name__ == '__main__':
    food_name = input("Enter a food name: ")
    try:
        analyze_calories(food_name)
        fdc_id = analyze_nutrients(food_name)
        if not fdc_id:
            print("Food not found!")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")