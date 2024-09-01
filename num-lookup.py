import http.client
import json

def search_phone_number(phone_number):
    conn = http.client.HTTPSConnection("truecaller-data2.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "5194201a3bmsh928637328850ba0p182511jsn0f4e7f599df9",
        'x-rapidapi-host': "truecaller-data2.p.rapidapi.com"
    }

    conn.request("GET", f"/search/{phone_number}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

def parse_response(response):
    try:
        json_data = json.loads(response)
        data = json_data.get("data", {})
        
        # Extract information
        basic_info = data.get("basicInfo", {})
        internet_info = data.get("internetInfo", {})
        phone_info = data.get("phoneInfo", {})
        address_info = data.get("addressInfo", {})

        output = []

        # Format the information
        if basic_info.get("name", {}).get("fullName"):
            output.append(f"Name: {basic_info.get('name', {}).get('fullName', 'Not Available')}")
        if internet_info.get("email", {}).get("id"):
            output.append(f"Email: {internet_info.get('email', {}).get('id', 'Not Available')}")
        if phone_info.get("e164Format"):
            output.append(f"Phone Number: {phone_info.get('e164Format', 'Not Available')}")
        if address_info.get("city"):
            output.append(f"City: {address_info.get('city', 'Not Available')}")
        if address_info.get("countryCode"):
            output.append(f"Country: {address_info.get('countryCode', 'Not Available')}")
        if phone_info.get("carrier"):
            output.append(f"Carrier: {phone_info.get('carrier', 'Not Available')}")
        if phone_info.get("spamScore") is not None:
            output.append(f"Spam Score: {phone_info.get('spamScore', 'Not Available')}")

        if not output:
            return "No relevant data found."
        
        return "\n".join(output)
    
    except json.JSONDecodeError:
        return "Error parsing the JSON response."

def main():
    print("Enter the number you'd like to search:")
    phone_number = input().strip()

    if phone_number:
        response = search_phone_number(phone_number)
        formatted_output = parse_response(response)
        print(formatted_output)
    else:
        print("No phone number entered.")

if __name__ == "__main__":
    main()
