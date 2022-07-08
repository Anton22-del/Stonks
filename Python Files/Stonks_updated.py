# Anton's Code

import collections
import csv
import time
from itertools import zip_longest
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def Convert(string):
    li = list(string.split("/"))
    return li

print("Note: ")
print("Senator data will only show up if they file paperless")
print("Parser warning can be ignored")
print("If the program fails before opening try updating the chromedriver")
print("file found in the same directory as the executable")
print("High wifi speeds and repeated use may lead to the website flagging the connection")
print(" ")
print('Example:')
print('Year = 2020')
print('Month = 09')
print('Big/Small = Small')
print('Corrupt_Senators = Alexander Lamar/Loeffler, Kelly/Inhofe, James M.')
print('Stocks/Bonds = Stock/Stock Option/Corporate Bond')
print('File_name = Stock Data.csv')
print('Stock Name = DuPont de Nemours, Inc.')
print('Pages = 7')
print(" ")

Year = str(input("Year = ") or "2020")
Month = str(input("Month = ") or "03")
Big_Small = str(input("Big/Small = ") or "Small")
Corrupt_Senators = Convert(str(input("Corrupt Senators = ")) or "Alexander Lamar/Loeffler, Kelly/Inhofe, James M.")
StocksorBonds = Convert(str(input("Stocks/Bonds = ")) or "Stock/Stock Option/Corporate Bond")
File_name = str(input("File Name = ") or "Stock Data.csv")
Stock_Name = str(input("Stock Name = ") or "DuPont de Nemours, Inc.")
Pages = int(input("Pages = ") or int(7))

if len(StocksorBonds) < 3:
    for l in range(3 - len(StocksorBonds)):
        StocksorBonds.append(StocksorBonds[-1])

# START//START//START//START//START//START//START//START//START//START//START//START//START//START//START//START//START//START//

start_time = time.time()

while True:
    amendeddict1 = {}
    amendeddict2 = {}
    amendeddict3 = {}
    dic1 = {}
    testlis = []
    link_list2 = {}
    noduplinks = []
    PDF_links = []
    link_list = []
    whitelist_nums = set('1234567890')
    whitelist_date = set('1234567890/')
    whitelist_letters = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    driver = webdriver.Chrome()  # open automated chrome
    wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(10)
    r = driver.get('https://efdsearch.senate.gov/search/')  # open site
    driver.find_element_by_id("agree_statement").click()  # Check ethics box
    driver.find_element_by_id("filerTypes").click()  # Click senators box
    driver.find_element_by_id("reportTypeLabelPtr").click()  # Click periodic transactions
    element = driver.find_element_by_id("reportTypeLabelPtr")  # look at the periodic transactions element
    element.send_keys(Keys.ENTER)  # Enter = search
    searchbox = driver.find_element_by_id("filedReports_filter").click()  # This clicks the search box
    driver.find_element_by_xpath('//*[@id="filedReports_filter"]/label/input').send_keys(
        Year)  # This filters data by the year Var
    # We have now navigated the web site and filtered results.
    for i in range(Pages):
        time.sleep(1)
        elems = driver.find_elements_by_partial_link_text('Periodic Transaction Report for')
        for elem in elems:
            # time.sleep(.5)
            href = elem.get_attribute('href')
            if href is not None:
                link_list.append(href)
        # We now have every link we need on the current page

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filedReports_next"]'))).click()
    # We now click the next button Pages times
    # We now have everylink on the site stored in link_list
    # (with the year filter and assuming there aren't more than Pages(var) pages)

    print(len(link_list), 'links')

    for k in range(len(link_list)):
        link_list2[link_list[k]] = k
    for i in link_list2.keys():
        noduplinks.append(i)

    print("Obtained link list")
    print(len(noduplinks), 'links after removing duplicates')

    time.sleep(1)
    # for links in link_list:
    test002 = {}

    for links in noduplinks:
        r = driver.get(links)
        html = driver.page_source
        doc = BeautifulSoup(html)#, features="html5lib")
        test001 = doc.find_all("td")
        Header = doc.find("h1")
        Senator = doc.find("h2")
        Senator = str(Senator)
        start = Senator.find('(')
        end = Senator.find(')')
        if start != -1 and end != -1:
            Senator = Senator[start + 1:end]
        test001.insert(0, Senator)
        test001.insert(0, Header)
        test001.insert(1, links)
        for i in range(len(test001)):
            test001[i] = str(test001[i])
        if len(test001) > 3:
            dict_key = len(test002)
            test002[dict_key] = test001.copy()
            boost = 0
            for length in range(int((len(test001) - 3) / 9)):
                test002[dict_key][3 + boost] = ''.join(
                    filter(whitelist_nums.__contains__, test002[dict_key][3 + boost]))
                test002[dict_key][4 + boost] = ''.join(
                    filter(whitelist_date.__contains__, test002[dict_key][4 + boost]))
                test002[dict_key][4 + boost] = test002[dict_key][4 + boost][:-1]# Delete this line to get a mm/dd/yyyy/ format instead of ##### in the csv
                test002[dict_key][5 + boost] = test002[dict_key][5 + boost][4:-5]
                hyperlink = test002[dict_key][6 + boost].find('--')
                if hyperlink > 0:
                    test002[dict_key][6 + boost] = 'No Link'
                else:
                    test002[dict_key][6 + boost] = test002[dict_key][6 + boost][6:-7]
                test002[dict_key][7 + boost] = BeautifulSoup(test002[dict_key][7 + boost]).text[86:]
                test002[dict_key][8 + boost] = test002[dict_key][8 + boost][4:-5]
                test002[dict_key][9 + boost] = test002[dict_key][9 + boost][4:-5]
                test002[dict_key][10 + boost] = test002[dict_key][10 + boost].split('-')
                for n in range(len(test002[dict_key][10])):
                    test002[dict_key][10 + boost][n] = ''.join(
                        filter(whitelist_nums.__contains__, test002[dict_key][10 + boost][n]))
                comments = test002[dict_key][11 + boost].find('--')
                if comments > 0:
                    test002[dict_key][11 + boost] = 'No Comments'
                else:
                    test002[dict_key][11 + boost] = test002[dict_key][11 + boost][6:-7]
                boost += 9
            Amended = test002[dict_key][0].find("Amendment 1")
            if Amended > 0:
                amendeddict1[dict_key] = test002[dict_key].copy()
            Amended2 = test002[dict_key][0].find("Amendment 2")
            if Amended2 > 0:
                amendeddict2[dict_key] = test002[dict_key].copy()
            Amended3 = test002[dict_key][0].find("Amendment 3")
            if Amended3 > 0:
                amendeddict3[dict_key] = test002[dict_key].copy()
        else:
            PDF_links.append(links)
    print(len(test002), 'useable links (non PDF)')
    print("Links to non-useable links in 'PDF_links'")
    # Pulling page info and formatting above
    print("Obtained and formatted page info")
    dic1 = {}
    amend2 = 0
    for stupid in amendeddict1:
        for everything in test002:
            if amendeddict1[stupid][2] == test002[everything][2] and ''.join(
                    filter(whitelist_date.__contains__, test002[stupid][0]))[1:-3] == ''.join(
                    filter(whitelist_date.__contains__, test002[everything][0]))[1:-2]:
                dic1[everything] = stupid
    print(len(dic1), 'reports amended once')
    for stupid in amendeddict2:
        for everything in amendeddict1:
            if ''.join(filter(whitelist_date.__contains__, amendeddict2[stupid][0]))[2:-3] == ''.join(
                    filter(whitelist_date.__contains__, amendeddict1[everything][0]))[2:-3] and amendeddict2[stupid][
                2] == amendeddict1[everything][2]:
                amend2 += 1
                dic1[everything] = stupid
    print(amend2, 'reports amended twice')
    for screwups in dic1:
        test002.pop(screwups)

    # duplicate checker below
    for i in test002:
        testlis.append(test002[i][1])


    def checkIfDuplicates_1(testlis):
        ''' Check if given list contains any duplicates '''
        if len(testlis) == len(set(testlis)):
            return False
        else:
            return True


    result = checkIfDuplicates_1(testlis)
    if result:
        print('Dictionary contains duplicates')
    else:
        print('No duplicates found in list')

    input_data = test002
    transposed_data = list(zip_longest(*input_data.values()))

    with open(File_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(input_data.keys())
        for items in transposed_data:
            writer.writerow(items)
    # Saving the dictionary to csv above
    print("Downloaded page info")
    print(len(test002), 'links after removing senator screw ups')
    if (len(link_list) % 25 == 0):
        print('Maxed out the pages, try increasing Pages.var?')
    if len(amendeddict3) > 0:
        print("At least one report has been amended 3 times")
#    if amend2 >= 1 and len(dic1) >= 5 and len(test002) >= 68:  # I belive there is now 72 dictionary entries for 2020
#        print('Probably a successful web scrape')
    print("Online script took %s seconds to execute" % (time.time() - start_time))
    break

start_time = time.time()
better = {}
Investors = 0
Removers = 0
Amount = 0
for i in test002:
    boost2 = 0
    for transactions in range(int((len(test002[i]) - 3) / 9)):
        if test002[i][8 + boost2] == "Stock" or test002[i][8 + boost2] == "Stock Option":
            if str(int(Year) - 1) not in ''.join(filter(whitelist_nums.__contains__, test002[i][4 + boost2])):
                if test002[i][9 + boost2] == "Sale (Partial)" or test002[i][9 + boost2] == "Sale (Full)":
                    if Big_Small.upper() == "BIG":
                        Amount = -int(test002[i][10 + boost2][1])
                    if Big_Small.upper() == "SMALL":
                        Amount = -int(test002[i][10 + boost2][0])
                    if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in better.keys():
                        Investors = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                        Removers = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                        Removers += 1
                        Amount = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                        if Big_Small.upper() == "BIG":
                            Amount -= int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount -= int(test002[i][10 + boost2][0])
                        better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors, Removers,
                                                                                                    Amount]
                    else:
                        Removers = 1
                        Investors = 0
                        better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors, Removers,
                                                                                                    Amount]
                        Removers = 0
                if test002[i][9 + boost2] == "Purchase":
                    if Big_Small.upper() == "BIG":
                        Amount = int(test002[i][10 + boost2][1])
                    if Big_Small.upper() == "SMALL":
                        Amount = int(test002[i][10 + boost2][0])
                    if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in better.keys():
                        Investors = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                        Removers = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                        Investors += 1
                        Amount = better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                        if Big_Small.upper() == "BIG":
                            Amount += int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount += int(test002[i][10 + boost2][0])
                        better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors, Removers,
                                                                                                    Amount]
                    else:
                        Investors = 1
                        Removers = 0
                        better[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors, Removers,
                                                                                                    Amount]
                        Investors = 0
                boost2 += 9
best = {}
Investors = 0
Removers = 0
Amount = 0
for i in range(len(Corrupt_Senators)):
    Corrupt_Senators[i] = Corrupt_Senators[i].upper()
for i in test002:
    boost2 = 0
    for transactions in range(int((len(test002[i]) - 3) / 9)):
        if test002[i][2].upper() in Corrupt_Senators:
            if test002[i][8 + boost2] == "Stock" or test002[i][8 + boost2] == "Stock Option":
                if str(int(Year) - 1) not in ''.join(filter(whitelist_nums.__contains__, test002[i][4 + boost2])):
                    if test002[i][9 + boost2] == "Sale (Partial)" or test002[i][9 + boost2] == "Sale (Full)":
                        if Big_Small.upper() == "BIG":
                            Amount = -int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount = -int(test002[i][10 + boost2][0])
                        if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in best.keys():
                            Investors = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                            Removers = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                            Removers += 1
                            Amount = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                            if Big_Small.upper() == "BIG":
                                Amount -= int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount -= int(test002[i][10 + boost2][0])
                            best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors,
                                                                                                      Removers, Amount]
                        else:
                            Removers = 1
                            Investors = 0
                            best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors,
                                                                                                      Removers, Amount]
                            Removers = 0
                    if test002[i][9 + boost2] == "Purchase":
                        if Big_Small.upper() == "BIG":
                            Amount = int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount = int(test002[i][10 + boost2][0])
                        if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in best.keys():
                            Investors = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                            Removers = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                            Investors += 1
                            Amount = best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                            if Big_Small.upper() == "BIG":
                                Amount += int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount += int(test002[i][10 + boost2][0])
                            best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors,
                                                                                                      Removers, Amount]
                        else:
                            Investors = 1
                            Removers = 0
                            best[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [Investors,
                                                                                                      Removers, Amount]
                            Investors = 0
                    boost2 += 9
better_recent = {}
Investors = 0
Removers = 0
Amount = 20
for i in test002:
    boost2 = 0
    for transactions in range(int((len(test002[i]) - 3) / 9)):
        if test002[i][8 + boost2] == "Stock" or test002[i][8 + boost2] == "Stock Option":
            if test002[i][4 + boost2].split('/')[0] == Month:
                if str(int(Year) - 1) not in ''.join(filter(whitelist_nums.__contains__, test002[i][4 + boost2])):
                    if test002[i][9 + boost2] == "Sale (Partial)" or test002[i][9 + boost2] == "Sale (Full)":
                        if Big_Small.upper() == "BIG":
                            Amount = -int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount = -int(test002[i][10 + boost2][0])
                        if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in better_recent.keys():
                            Investors = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                0]
                            Removers = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                1]
                            Removers += 1
                            Amount = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                            if Big_Small.upper() == "BIG":
                                Amount -= int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount -= int(test002[i][10 + boost2][0])
                            better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                Investors, Removers, Amount]
                        else:
                            Removers = 1
                            Investors = 0
                            better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                Investors, Removers, Amount]
                            Removers = 0
                    if test002[i][9 + boost2] == "Purchase":
                        if Big_Small.upper() == "BIG":
                            Amount = int(test002[i][10 + boost2][1])
                        if Big_Small.upper() == "SMALL":
                            Amount = int(test002[i][10 + boost2][0])
                        if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in better_recent.keys():
                            Investors = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                0]
                            Removers = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                1]
                            Investors += 1
                            Amount = better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][2]
                            if Big_Small.upper() == "BIG":
                                Amount += int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount += int(test002[i][10 + boost2][0])
                            better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                Investors, Removers, Amount]
                        else:
                            Investors = 1
                            Removers = 0
                            better_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                Investors, Removers, Amount]
                            Investors = 0
                    boost2 += 9
best_recent = {}
Investors = 0
Removers = 0
Amount = 0
for i in range(len(Corrupt_Senators)):
    Corrupt_Senators[i] = Corrupt_Senators[i].upper()
for i in test002:
    boost2 = 0
    for transactions in range(int((len(test002[i]) - 3) / 9)):
        if test002[i][2].upper() in Corrupt_Senators:
            if test002[i][4 + boost2].split('/')[0] == Month:
                if test002[i][8 + boost2] == "Stock" or test002[i][8 + boost2] == "Stock Option":
                    if str(int(Year) - 1) not in ''.join(filter(whitelist_nums.__contains__, test002[i][4 + boost2])):
                        if test002[i][9 + boost2] == "Sale (Partial)" or test002[i][9 + boost2] == "Sale (Full)":
                            if Big_Small.upper() == "BIG":
                                Amount = -int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount = -int(test002[i][10 + boost2][0])
                            if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in best_recent.keys():
                                Investors = \
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                                Removers = \
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                                Removers += 1
                                Amount = best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                    2]
                                if Big_Small.upper() == "BIG":
                                    Amount -= int(test002[i][10 + boost2][1])
                                if Big_Small.upper() == "SMALL":
                                    Amount -= int(test002[i][10 + boost2][0])
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                    Investors, Removers, Amount]
                            else:
                                Removers = 1
                                Investors = 0
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                    Investors, Removers, Amount]
                                Removers = 0
                        if test002[i][9 + boost2] == "Purchase":
                            if Big_Small.upper() == "BIG":
                                Amount = int(test002[i][10 + boost2][1])
                            if Big_Small.upper() == "SMALL":
                                Amount = int(test002[i][10 + boost2][0])
                            if (test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2]) in best_recent.keys():
                                Investors = \
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][0]
                                Removers = \
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][1]
                                Investors += 1
                                Amount = best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])][
                                    2]
                                if Big_Small.upper() == "BIG":
                                    Amount += int(test002[i][10 + boost2][1])
                                if Big_Small.upper() == "SMALL":
                                    Amount += int(test002[i][10 + boost2][0])
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                    Investors, Removers, Amount]
                            else:
                                Investors = 1
                                Removers = 0
                                best_recent[(test002[i][7 + boost2].splitlines()[0], test002[i][4 + boost2])] = [
                                    Investors, Removers, Amount]
                                Investors = 0
                        boost2 += 9
full_data = [better, best, better_recent, best_recent]

# This will find the most and least popular stock (This is currently untested)
# CONSIDER MAKING A LIST OF TOP 5 STOCKS BOUGHT AND SOLD

nn = 0
for full in full_data:
    pops = {}
    for i in full:
        if i[0] not in pops.keys():
            pops[i[0]] = full[i][0]
        else:
            pops[i[0]] += full[i][0]
    popsneg = {}
    for i in full:
        if i[0] not in popsneg.keys():
            popsneg[i[0]] = full[i][1]
        else:
            popsneg[i[0]] += full[i][1]
    pp = 0
    pn = 0
    Least_pop = " "
    Most_pop = " "
    for negative in popsneg:
        if popsneg[negative] > pn:
            pn = popsneg[negative]
            Least_pop = negative
    for positive in pops:
        if pops[positive] > pp:
            pp = pops[positive]
            Most_pop = positive
    if full == better:
        print(Least_pop, "Is The Most Sold Stock with", pn, "Senator Sales")
        print(Most_pop, "Is The Most Bought Stock with", pp, "Senator Investments")
    if full == better_recent:
        print(Least_pop, "Is The Most Sold Stock in your selected month with", pn, "Senator Sales")
        print(Most_pop, "Is The Most Bought Stock in your selected month with", pp, "Senator Investments")
    if full == best:
        print(Least_pop, "Is The Most Sold Stock Among Corrupt Senators, with", pn, "Senator Sales")
        print(Most_pop, "Is The Most Bought Stock Among Corrupt Senators, with", pp, "Senator Investments")
    if full == best_recent:
        print(Least_pop, "Is The Most Sold Stock Among Corrupt Senators in your selected month with", pn,
              "Senator Sales")
        print(Most_pop, "Is The Most Bought Stock Among Corrupt Senators in your selected month with", pp,
              "Senator Investments")

t1 = "Error"
t2 = "Error"
Stock_Name2 = "Error"

for full in full_data:
    dd = {}
    if full == better:
        t1 = "All Investing Senators"
        t2 = "Total Amount Invested"
    if full == best:
        t1 = "Corrupt Investing Senators"
        t2 = "Corrupt Amount Invested"
    if full == better_recent:
        t1 = "All Recent Investing Senators"
        t2 = "Total Recent Amount Invested"
    if full == best_recent:
        t1 = "Corrupt Recent Investing Senators"
        t2 = "Corrupt Recent Amount Invested"
    for stock in full:
        dd[stock[1]] = full[stock]
    od = collections.OrderedDict(sorted(dd.items()))

    Dupont_dates = []
    Dupont_Invest = []
    Dupont_Remove = []
    Dupont_Amountp = []
    Dupont_Amountn = []
    for stock in od:
        Dupont_dates.append(stock[:-5])
        Dupont_Invest.append(od[stock][0])
        Dupont_Remove.append(-od[stock][1])
        if od[stock][2] >= 0:
            Dupont_Amountp.append(od[stock][2])
            Dupont_Amountn.append(0)
        if od[stock][2] < 0:
            Dupont_Amountp.append(0)
            Dupont_Amountn.append(od[stock][2])
    x = Dupont_dates

    leftmargin = 0.5  # inches
    rightmargin = 0.3  # inches
    categorysize = 1.0  # inches

    n = len(x)

    figwidth = leftmargin + rightmargin + (n + 1) * categorysize

    if len(x) > 0:
        negative_data = Dupont_Remove
        positive_data = Dupont_Invest
        plt.figure(figsize=(figwidth, 5))
        plt.xlabel('Date of Transaction', size=15)
        plt.ylabel("# of Purchasing Senators ", size=15)
        plt.title(t1, size=20)

        ax = plt.subplot(1, 1, nn + 1)
        ax.bar(x, negative_data, width=1, color='orangered')
        ax.bar(x, positive_data, width=1, color='mediumspringgreen')

        negative_data = Dupont_Amountn
        positive_data = Dupont_Amountp
        plt.figure(figsize=(figwidth, 5))

        plt.ylabel("Amount Invested", size=15)
        plt.xlabel('Date of Transaction', size=15)
        plt.title(t1, size=20)
        ax = plt.subplot(1, 1, nn + 1)
        ax.bar(x, negative_data, width=1, color='darkviolet')
        ax.bar(x, positive_data, width=1, color='dodgerblue')

print("Offline script took %s seconds to execute" % (time.time() - start_time))

# This will graph a stock by it's investors and investment
# Note graphs will not be made if there isn't any data to be graphed

for i in full_data:
    if i == better:
        Stock_Name2 = Stock_Name + " (Full list)"
    if i == best:
        Stock_Name2 = Stock_Name + " (Corrupt list)"
    if i == better_recent:
        Stock_Name2 = Stock_Name + " (Full Month Based list)"
    if i == best_recent:
        Stock_Name2 = Stock_Name + " (Corrupt Month Based list)"

    dd = {}
    for stock in i:
        if stock[0] == Stock_Name:
            dd[stock[1]] = i[stock]
    od = collections.OrderedDict(sorted(dd.items()))
    Dupont_dates = []
    Dupont_Invest = []
    Dupont_Remove = []
    Dupont_Amountp = []
    Dupont_Amountn = []
    for stock in od:
        Dupont_dates.append(stock)
        Dupont_Invest.append(od[stock][0])
        Dupont_Remove.append(-od[stock][1])
        if od[stock][2] >= 0:
            Dupont_Amountp.append(od[stock][2])
            Dupont_Amountn.append(0)
        if od[stock][2] < 0:
            Dupont_Amountp.append(0)
            Dupont_Amountn.append(od[stock][2])
    x = Dupont_dates

    leftmargin = 0.5  # inches
    rightmargin = 0.3  # inches
    categorysize = 1.1  # inches

    n = len(x)

    figwidth = leftmargin + rightmargin + (n + 1) * categorysize

    if len(x) > 0:
        negative_data = Dupont_Remove
        positive_data = Dupont_Invest
        plt.figure(figsize=(figwidth, 5))
        ax = plt.subplot(1, 1, nn + 1)
        ax.bar(x, negative_data, width=1, color='orangered')
        ax.bar(x, positive_data, width=1, color='mediumspringgreen')
        plt.xlabel('Date of Transaction', size=15)
        plt.ylabel("# of Purchasing Senators ", size=15)
        plt.title(Stock_Name2, size=20)

        x = Dupont_dates
        negative_data = Dupont_Amountn
        positive_data = Dupont_Amountp
        plt.figure(figsize=(figwidth, 5))
        ax = plt.subplot(1, 1, nn + 1)
        ax.bar(x, negative_data, width=1, color='darkviolet')
        ax.bar(x, positive_data, width=1, color='dodgerblue')
        plt.xlabel('Date of Transaction', size=15)
        plt.ylabel("Amount Invested", size=15)
        plt.title(Stock_Name2, size=20)

contains = 0
for p in better:
    if Stock_Name in p[0]:
        contains += 1
if contains <= 0:
    print("No Senators have purchased or sold this stock")
if contains > 0:
    print("This stock has been purchased/sold", contains, "or more times")

plt.show(block=True)