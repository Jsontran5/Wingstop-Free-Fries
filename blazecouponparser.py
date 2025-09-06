
from bs4 import BeautifulSoup
import re

def blazeemailparse(email_body):
    """
    Parse Blaze Pizza email to extract coupon code and expiration date.
    
    Args:
        email_body (str): The HTML body of the Blaze Pizza email
        
    Returns:
        tuple: (code, realexpiredate) where code is the coupon code and 
               realexpiredate is in MM/DD/YYYY format
    """
    try:
        soup = BeautifulSoup(email_body, 'html.parser')
        
        # Find the coupon code - look for text that contains "Code:"
        code = None
        code_elements = soup.find_all('p', style=lambda value: value and 'font-weight:bold' in value)
        
        for element in code_elements:
            text = element.get_text().strip()
            if text.startswith('Code:'):
                # Extract the code part after "Code: "
                code = text.replace('Code:', '').strip()
                break
        
        # If the above method doesn't work, try a more general approach
        if not code:
            # Look for any text containing "Code:" in the HTML
            all_text = soup.get_text()
            code_match = re.search(r'Code:\s*([A-Z0-9]+)', all_text)
            if code_match:
                code = code_match.group(1)
        
        # Find the expiration date - look for text that contains "Expires:"
        expire_date = None
        all_paragraphs = soup.find_all('p')
        
        for p in all_paragraphs:
            text = p.get_text().strip()
            if text.startswith('Expires:'):
                # Extract the date part after "Expires: "
                date_text = text.replace('Expires:', '').strip()
                # Convert format from "10 / 04 / 2025" to "10/04/2025"
                date_text = re.sub(r'\s*/\s*', '/', date_text)
                expire_date = date_text
                break
        
        # If the above method doesn't work, try regex pattern matching
        if not expire_date:
            # Look for date patterns in the format MM / DD / YYYY or MM/DD/YYYY
            all_text = soup.get_text()
            date_pattern = r'Expires:\s*(\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{4})'
            date_match = re.search(date_pattern, all_text)
            if date_match:
                expire_date = re.sub(r'\s*/\s*', '/', date_match.group(1))
        
        # Return results or fallback values
        if code and expire_date:
            return code, expire_date
        else:
            print(f"blazeemailparse(): Could not find code={code} or expire_date={expire_date}")
            return "NO CODE", "NO DATE"
            
    except Exception as e:
        print(f"blazeemailparse(): Error parsing email - {str(e)}")
        return "ERROR", "ERROR"

def main():
    """
    Test function for the blazeemailparse function.
    """
    # Sample Blaze Pizza email HTML content
    test_email = '''
    <div style="font-family:Arial,sans-serif">
    <div align="center" style="font-size:19px;font-family:Arial,&#39;Helvetica Neue&#39;,Helvetica,sans-serif;color:#555;line-height:24px">
    <p style="margin:0;font-size:19px">
    <br>
    Thanks for sharing your feedback! We love hearing from our guests and will make sure your comments reach the right team.
    <br>
    <br>
    Enjoy a <strong>free dessert*</strong> on your next online order with code below — either the Blaze Pizza App or blazepizza.com.
    </p>
    <p style="margin:0;font-size:19px"> </p>
    <p style="margin:0;font-size:19px;text-align:center;font-weight:bold">
    Code: SMGKRZ7M2D7CLXH
    </p>
    <p style="margin:0;font-size:19px;text-align:center">
    Expires: 10 / 04 / 2025
    </p>
    </div>
    </div>
    '''
    
    print("Testing blazeemailparse function...")
    code, expire_date = blazeemailparse(test_email)
    print(f"Extracted Code: {code}")
    print(f"Extracted Expire Date: {expire_date}")
    
    # Expected results
    expected_code = "SMGKRZ7M2D7CLXH"
    expected_date = "10/04/2025"
    
    print(f"\nValidation:")
    print(f"Code correct: {code == expected_code}")
    print(f"Date correct: {expire_date == expected_date}")

if __name__ == "__main__":
    main()