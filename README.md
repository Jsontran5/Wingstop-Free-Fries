# WingstopFreeFries

Github Repository for the website [**wingstopfreefries.xyz**](https://wingstopfreefries.xyz)

Will generate you a coupon for the supported stores below by filling out the survey autmatically and bypassing the need for a survey code.
### Supported Stores:
```
Wingstop
Panda Express
Rubio's
Blaze Pizza
```



## Use it locally

### 1. Clone the Repository

```bash
git clone https://github.com/Jsontran5/Wingstop-Free-Fries.git
cd wingstop-free-fries/
```

### 2. Setup
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages in requirements.txt
```bash
pip install -r requirements.txt
```

Download the latest Stable chromedriver at https://googlechromelabs.github.io/chrome-for-testing/ and place `chromedriver.exe` in your root directory


### 3. Generate the Coupon
Open up your chosen restaurant's `function.py` file <br>  
Comment out the `chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome' ` line <br>    
Run the file

