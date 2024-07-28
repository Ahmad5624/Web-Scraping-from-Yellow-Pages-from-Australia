
# Web Scraping from Yellow Pages from Australia
There are two code files, one for collecting links from the specified categories and the other for collecting data from the website.






## Note: Chromedriver.exe file must be in the path to run "yellow_pages_au.py".

## Deployment

To run the "yellow_pages_au.py":

```bash
  pip install scrapy-selenium
  pip install pandas as pd
```
To run the "Links.py":
```bash
  pip install beautifulsoup4
  pip install playwright
```
## Usage(yellow_pages_au.py)

```javascript
import pandas as pd
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class YellowPagesAuSpider(scrapy.Spider):
    name = "yellow_pages_au"
    allowed_domains = ["www.yellowpages.com.au"]
    start_urls = ["https://www.yellowpages.com.au/"]
    processed_links = set()  # Set to store processed links

    def start_requests(self):
        # Read the Excel file with URLs
        df = pd.read_excel('Final Links.xlsx')  # Change to your Excel file's name
        # Iterate over the rows in the Excel file
        for index, row in df.iterrows():
            # Access the value of the 'Links' column
            link = row['Links']
            yield SeleniumRequest(
                url=link,
                callback=self.parse,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "h1 a.listing-name"))
            )

    def parse(self, response):
        # 1.Name
        Name = response.css("h1 a.listing-name::text").get()
        # 2.Category
        try:
            Category = response.xpath("//h2[@class='listing-heading']//text()").get()
        except:
            Category = 'Category not found'

        # 3.Address
        try:
            Address = response.xpath("//div[@id='business-profile-page']/@data-full-address").get()
        except:
            Address = 'Address not found'

        # 4.Suburb
        try:
            Suburb = response.xpath("//div[@id='business-profile-page']/@data-suburb").get().replace("suppressed", '')
        except:
            Suburb = 'Suburb not found'

        # 5.State
        try:
            State = response.xpath("//div[@id='business-profile-page']/@data-state").get().replace("suppressed", '')
        except:
            State = 'State not found'

        # 6.Zip Code
        try:
            Zip_Code = response.xpath("//div[@id='business-profile-page']/@data-postcode").get()
        except:
            Zip_Code = 'Zip Code not found'

        # 7.Contact Number
        Contact_number = 'Contact Number not found'
        try:
            Contact_number1 = response.xpath("//div[@class='contact-group']//a[@title='Phone']//text()")
            Contact_number2 = response.xpath("//a[@data-number]/@data-number")
            # Initialize an empty set to hold unique contact numbers
            unique_numbers = set()

            # Check if Contact_number1 exists and process it
            if Contact_number1:
                # Extract the values, strip whitespace, and add to the set
                contact_numbers1 = [number.strip() for number in Contact_number1.extract()]
                unique_numbers.update(contact_numbers1)

            # Check if Contact_number2 exists and process it
            if Contact_number2:
                # Extract the values, strip whitespace, and add to the set
                contact_numbers2 = [number.strip() for number in Contact_number2.extract()]
                unique_numbers.update(contact_numbers2)

            # Join the unique contact numbers with a comma
            Contact_number = ', '.join(unique_numbers)
        except:
            pass

        # 8.Email
        try:
            Email1 = response.xpath("//span[@class='glyph icon-contact-mail']//span//text()")
            Email2 = response.xpath("//div[@class='contact-group']//a[@data-email]//@data-email")
            # Initialize an empty set to hold unique contact numbers
            unique_numbers = set()

            # Check if Email1 exists and process it
            if Email1:
                # Extract the values, strip whitespace, and add to the set
                Emails1 = [number.strip().replace('Send Email ', '') for number in Email1.extract()]
                unique_numbers.update(Emails1)

            # Check if Contact_number2 exists and process it
            if Email2:
                # Extract the values, strip whitespace, and add to the set
                Emails2 = [number.strip() for number in Email2.extract()]
                unique_numbers.update(Emails2)

            # Join the unique contact numbers with a comma
            Email = ', '.join(unique_numbers)
        except:
            Email = 'Email not found'

        # 9.Number of Employees
        try:
            Number_of_employees = response.xpath("//dd[@class='number-of-employees']//text()").get()
        except:
            Number_of_employees = ''

        # 10.Website
        try:
            Website = response.xpath("//a[@class='contact contact-main contact-url']/@href").get()
        except:
            Website = 'Website not found'

        print("Name:", Name)
        print("Category:", Category)
        print("Address:", Address)
        print("Suburb:", Suburb)
        print("State:", State)
        print("Zip Code:", Zip_Code)
        print("Contact Number:",  Contact_number)
        print("Email:", Email)
        print("Number of Employees:", Number_of_employees)
        print("Website:", Website)
        yield {
               'Links': response.url,
               'Name': Name,
               'Category': Category,
               "Address": Address,
               "Suburb": Suburb,
               "State": State,
               "Zip Code": Zip_Code,
               "Contact Number": Contact_number,
               "Email": Email,
               "Employees Count": Number_of_employees,
               "Website": Website
               }
```

## Usage(Links.py)
```javascript
from playwright.sync_api import sync_playwright
import csv
from bs4 import BeautifulSoup

OUTPUT_FILE_NAME = "Links.csv"


# Write to the file
def write_to_file(rows):
    file = open(OUTPUT_FILE_NAME, 'a', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)
    writer.writerows(rows)
    file.close()


# Main Function
def main():
    links = [
        "Put your desired links that must contain the categories."

    ]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel='chrome')
        page = browser.new_page()
        # Set viewport size (width, height)
        viewport_size = {"width": 1280, "height": 720}
        page.set_viewport_size(viewport_size)
        # browser = p.chromium.connect_over_cdp("http://localhost:9223")
        # default_context = browser.contexts[0]
        # page = default_context.pages[0]
        # Get to the website
        length = 0
        count = 1
        count1 = 1
        for main_link in links:
            for i in range(1, 100000):
                main_link1 = f"{main_link}{i}"
                page.goto(f"{main_link}{i}")
                print("Page No.:", count)
                soup = BeautifulSoup(page.content(), 'html.parser')
                links = soup.find_all("div", {'class': 'Box__Div-sc-dws99b-0 jxCSTY'})
                for link in links:
                    if link.find("a", href=True):
                        link = 'https://www.yellowpages.com.au' + link.find("a", href=True).get('href')
                        output_results = [link]
                        write_to_file([output_results])
                        print(count1, " Main Link:", main_link1)
                        print(link)
                        print(".......................")
                        count1 += 1
                # Check for the end of the page
                checker = soup.select("div.Box__Div-sc-dws99b-0.jxCSTY")
                # Check for the end of the page
                if not checker:
                    count += 1
                    print('love you')
                    break
                count += 1

        # Keep the browser open (you can add a sleep here to keep it open for a while)
        input("Press Enter to exit...")
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

```
# Support
For support email me at: razawarraich2334@gmail.com