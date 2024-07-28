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
