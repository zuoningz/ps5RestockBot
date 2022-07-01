# activate venv: source venv/bin/activate
# This works for BestBuy, faster than Selenium
from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time
import yagmail



myemail = "zahgz4011@gmail.com"
myEmailAppPwd  = "hmixjqxskmcfrbxx"
yag = yagmail.SMTP(myemail, myEmailAppPwd)


def sendEmail(productUrl, productName, retailer):
    to = 'zuoningz2001@gmail.com'
    subject = "Restock Alert at " + retailer
    body = '''Product: %s
              URL: %s
              %s is available at %s
              ''' % (productName, productUrl, productName, retailer)
    yag.send(to=to, subject=subject, contents=body)


async def BestBuyChecker(session, ProductName, ProductUrl):
    isAvailable = True
    r = await session.get(ProductUrl)
    Btns = r.html.find('button')
    for btn in Btns:
        if btn.text == "Sold Out":
            print(ProductName + " is not available at Best Buy")
            isAvailable = False
            break
    if(isAvailable):
        print(ProductName + " is available at Best Buy")
        sendEmail(ProductUrl, ProductName, "Best Buy")




async def AmazonChecker(session, ProductName, ProductUrl):
    start = time.time()
    isAvailable = True
    r = await session.get(ProductUrl)
    await r.html.arender(timeout=200)
    Btns = r.html.find('span')
    for btn in Btns:
        if btn.text == "Currently unavailable.":
            print(ProductName + " is not available at Amazon")
            isAvailable = False
            break
    if(isAvailable):
        print(ProductName + " is available at Amazon")
        sendEmail(ProductUrl, ProductName, "Amazon")


# AmazonChecker()

# def SonyChecker(): # this wont work for SONY because it needs Login to see if its available
#     PS5url = 'https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3006647'
#     session = HTMLSession()
#     r = session.get(PS5url)
#     r.html.render(timeout=100)
#     Btns = r.html.find('span')
#     for btn in Btns:
#         print(btn.text)
#         if btn.text == "Currently unavailable.":
#             print("This item not available")
#             break


async def GameStopChecker(session, ProductName, ProductUrl):
    r = await session.get(ProductUrl)
    isAvailable = False
    await r.html.arender(timeout=200)
    print(r.html.html)
    Btns = r.html.find('button')
    print(Btns)
    for btn in Btns:
        print(btn.text)
        if btn.text == "Add to Cart":
            print(ProductName + " is available at Game Stop")
            isAvailable = True
            break
    if isAvailable == False:
        print(ProductName + " is NOT available")


def TargetChecker():
    PS5url = 'https://www.target.com/p/playstation-5-console/A-81114595'
    session = HTMLSession()
    r = session.get(PS5url)
    r.html.render(timeout=500)
    Btns = r.html.find('p')

    # print(Btns[0].attrs)
    print(Btns)
    for btn in Btns:
        print(btn.text)



# main function
async def main():
    session = AsyncHTMLSession()
    products = [
        {
            "url": 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402',
            "itemName": "NVIDIA GTX3060 Ti",
            "retailer": "Best Buy"
        },
        {
            "url": "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
            "itemName": 'NVIDIA GTX3070',
            'retailer': 'Best Buy'
        },
        {
            "url": 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442',
            'itemName': 'NVIDIA GTX3080',
            'retailer': 'Best Buy'
        },
        {
            'url': 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434',
            'itemName': 'NVIDIA GTX3090',
            'retailer': 'Best Buy'
        },
        {
            "url": 'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161',
            "itemName": "PS5 Digital",
            "retailer": "Best Buy"
        },
        {
            'url': 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149',
            'itemName': 'PS5 Console',
            'retailer': 'Best Buy'
        },
        {
            "url": 'https://www.bestbuy.com/site/hp-envy-photo-7855-wireless-all-in-one-instant-ink-ready-inkjet-printer-black/5961901.p?skuId=5961901',
            "itemName": "HP Envy Photo",
            "retailer": "Best Buy"
        },
        {
            "url": 'https://www.amazon.com/PlayStation-5-Digital/dp/B09DFHJTF5?ref_=ast_sto_dp',
            "itemName": "PS5 Digital",
            "retailer": "Amazon"
        },
        { # Test
            "url": "https://www.amazon.com/Fish-Hub-Fishing-Tshirt-Fisherman/dp/B07JJPB4ZX/ref=rvi_sccl_4/142-0619040-8598520?pd_rd_w=mu9bk&content-id=amzn1.sym.f5690a4d-f2bb-45d9-9d1b-736fee412437&pf_rd_p=f5690a4d-f2bb-45d9-9d1b-736fee412437&pf_rd_r=DC8VRX8JRV7DJEVSFR4P&pd_rd_wg=dLy8J&pd_rd_r=81dc1852-e9a1-4cb5-926c-f26f62125a47&pd_rd_i=B07JJPB4ZX&psc=1",
            "itemName": "Fish Hub T shirt",
            "retailer": "Amazon"
        },
        {
            "url": 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?tag=georiot-us-default-20&ascsubtag=tomsguide-us-2379985863985833000-20&geniuslink=true',
            "itemName": "PS5 Console",
            "retailer": "Amazon"
        },
        # {
        #     "url": "https://www.gamestop.com/consoles-hardware/playstation-5/products/playstation-5/229025.html",
        #     "itemName": "PS5 Console",
        #     "retailer": "Game Stop"
        # },
        # { # Test
        #     "url": "https://www.gamestop.com/video-games/xbox-series-x%7Cs/products/halo-infinite---xbox-series-x/224750.html",
        #     "itemName": "Halo Infinite",
        #     "retailer": "Game Stop"
        # }

     ]

    print(len(products))
    tasks = []
    for item in products:
        print(item['itemName'])
        if item['retailer'] == "Best Buy":
            tasks.append(BestBuyChecker(session, item['itemName'], item['url']))
        elif item['retailer'] == "Amazon":
            tasks.append(AmazonChecker(session, item['itemName'], item['url']))
        elif item['retailer'] == "Game Stop":
            tasks.append(GameStopChecker(session, item['itemName'], item['url']))


    return await asyncio.gather(*tasks)

# start = time.time()
while True:
    results = asyncio.run(main())
# print( "Duration: "+ str(time.time() - start))

