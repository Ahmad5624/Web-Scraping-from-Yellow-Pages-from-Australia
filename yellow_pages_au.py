# import pandas as pd
# import scrapy
# from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
# class YellowPagesAuSpider(scrapy.Spider):
#     name = "yellow_pages_au"
#     allowed_domains = ["www.yellowpages.com.au"]
#     start_urls = ["https://www.yellowpages.com.au/"]
#     processed_links = set()  # Set to store processed links
#
#     def start_requests(self):
#         # Read the Excel file with URLs
#         df = pd.read_excel('Postal Codes.xlsx')  # Change to your Excel file's name
#         # Iterate over the rows in the Excel file
#         for index, row in df.iterrows():
#             # Access the value of the 'Links' column
#             link = row['Links']
#             yield SeleniumRequest(
#                 url=link,
#                 callback=self.parse,
#                 wait_time=10,
#                 wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class*='MuiTypography-root']"))
#             )
#
#     def parse(self, response):
#         links = response.xpath("//div[@class='Box__Div-sc-dws99b-0 dAyAhR']//a[@href]/@href").extract()
#         for link in links:
#             full_link = 'https://www.yellowpages.com.au' + link
#             # Check if the link has already been processed
#             if full_link not in self.processed_links:
#                 self.processed_links.add(full_link)
#                 yield {'Current Link': response.url,
#                        'Links': full_link}
#         # Check if 'a[href*='pageNumber=']' exists
#         pagination_link = response.xpath("//span[contains(text(), 'Next')]//parent::a/@href").get()
#         if pagination_link:
#             next_page_url = response.urljoin(pagination_link)
#             # Check if the pagination link has already been processed
#             if next_page_url not in self.processed_links:
#                 self.processed_links.add(next_page_url)
#                 # Continue crawling the pagination links
#                 yield SeleniumRequest(
#                     url=next_page_url,
#                     callback=self.parse,
#                     wait_time=10,
#                     wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class*='MuiTypography-root']"))
#                 )
#         else:
#             # Move to the next link if the pagination element doesn't exist
#             self.logger.info("No pagination link found, moving to next URL")


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
