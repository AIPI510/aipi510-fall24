import json

def lambda_handler(event, context):
    """
    Transforms user data by adding fields for email domain and full address,
    and formatting names to uppercase.

    Args:
        event (dict): Event data passed by Step Functions (output of Extract function).
        context (object): Lambda context object.

    Returns:
        dict: Response containing status code and transformed user data or an error.
    """
    # Extract data from the input event
    extracted_data = event.get('body', [])  # Output from the `extract` function
    
    # Initialize transformed data
    transformed_data = []

    try:
        # Transform logic for user data
        for item in extracted_data:
            # Combine address components
            address = item.get("address", {})
            full_address = f"{address.get('street', '')}, {address.get('city', '')}, {address.get('zipcode', '')}"
            
            # Extract email domain
            email = item.get("email", "")
            email_domain = email.split("@")[-1] if "@" in email else "unknown"

            # Append transformed item
            transformed_data.append({
                "id": item["id"],
                "name": item["name"].upper(),
                "username": item["username"],
                "email": item["email"],
                "email_domain": email_domain,
                "full_address": full_address,
                "phone": item["phone"],
                "company": item["company"]["name"]
            })
        
        # Log the transformed data
        print("Transformed Data:", transformed_data)

        # Return the transformed data
        return {
            "statusCode": 200,
            "transformed_data": transformed_data
        }
    
    except Exception as e:
        # Log any errors and return a failure response
        print(f"Error during transformation: {e}")
        return {
            "statusCode": 500,
            "error": str(e)
        }
