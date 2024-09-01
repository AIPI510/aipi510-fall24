import requests
import json

API_KEY = '0K17D4gSxSZPOejXfaa5ewB39zmbrk5lFg9Tkvax'
BASE_URL = "https://api.nal.usda.gov/fdc/v1/"

# Call api to grab the desire data.
def call_api(endpoint, API_KEY=API_KEY, query=None):

    params = {
        'api_key': API_KEY,
        'query': query,
    }
    response = requests.get(f'{BASE_URL}{endpoint}', params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        with open('response_data.json', 'w') as file:
            json.dump(response.json(), file, indent=4)
        print("Data successfully saved to 'response_data.json'.")
        return response.json()
    else:
        print("Failed to retrieve data: Status code", response.status_code)
        return None


# Search for food and its basic information.
def get_food_info(food_name):
    """Search for food and return its ID."""
    foods = call_api(endpoint='foods/search', query=food_name)
    if foods:
        food_item = foods.get('foods', [])[0]
        if food_item:
            fdc_id = food_item.get('fdcId')
            with open('foods_item.json', 'w') as file:
                json.dump(food_item, file, indent=4)
            print(f"Found FDC ID: {fdc_id} for food: {food_name}")
            
            # extract description of the searched food.
            food_name = food_item.get('description', 'N/A')
            # gain the calories information of the searched food.
            nutrients = food_item.get('foodNutrients', [])
            calories_info = next((nutrient for nutrient in nutrients if nutrient.get('nutrientName') == 'Energy'), {})
            calories = calories_info.get('value', 'N/A')

            print(f'Food: {food_name}, Calories: {calories} kcal')
            
            return fdc_id
    else:
        print(f'Failed to retrieve data.')
        return None


def get_nutrient_info(fdc_id):
    """Retrieve nutrients information for a specific food item by its FDC ID."""
    food_data = call_api(endpoint=f'food/{fdc_id}')
    nutrients = food_data.get('foodNutrients', [])[:5]
    for nutrient in nutrients:
        nutrient_details = nutrient.get('nutrient', {})
        print(f"Nutrient Name: {nutrient_details.get('name')}")
        print(f"Amount per 100g: {nutrient.get('amount')} {nutrient_details.get('unitName')}")
        print("---------------------------------------------------")
    return food_data


def analyse_nutrients(food_name):
    foods = call_api(endpoint='search', query=food_name)
    # some analysis on foods data.

    return foods


if __name__ == '__main__':
    food_name = input("Enter a food name to search: ")
    try:
        fdc_id = get_food_info(food_name)
        if fdc_id:
            get_nutrient_info(fdc_id)
        else:
            print("Food not found.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

