from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

pacific_tz = pytz.timezone('America/Los_Angeles')

def pandamailparse(email):
    contents = email

    # Find elements with inline styles containing !important
    soup = BeautifulSoup(contents, 'html.parser')

# Find the element containing the code
    code_elements = soup.find_all('span', style=lambda value: value and 'important' in value)

# Extract the text from each element
    codes = []
    for code_element in code_elements:
        code = code_element.text.strip()
        codes.append(code)

    # Print the extracted codes
    if codes:
        #print("Codes found:")
        #print(codes[2])
        #print(codes[3])

        date_pattern = r'\d{2}/\d{2}/\d{4}'

        dates = re.findall(date_pattern, codes[3])
        first_date = dates[0] if dates else None
        #print(first_date)

        return codes[2], first_date
        # date_format = "%m/%d/%Y"

        # Parse the date string into a datetime object
        # date_object = datetime.strptime(first_date, date_format)
        # localized_date_object = pacific_tz.localize(date_object)

        # Convert the datetime object to a Unix timestamp
        # unix_timestamp = int(date_object.timestamp())

        # Print the Unix timestamp
        # print(unix_timestamp)

        # expiredate = unix_timestamp - 24 * 60 * 60
        # print(expiredate)

        # formatted_date = datetime.fromtimestamp(expiredate, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        # print(formatted_date)

        # unix_time_pacific = int(datetime.now(pacific_tz).timestamp())
        # print(unix_time_pacific)
        # current_date = datetime.fromtimestamp(unix_time_pacific, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        # print(current_date)
    else:
        print("Codes not found")
        return "NO CODE", "NO DATE"
    
def main():
    

    code, expiredate = pandamailparse(email)
    print(code)
    print(expiredate)

if __name__ == "__main__":
    main()