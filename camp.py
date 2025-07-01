import asyncio
from pyppeteer import launch

async def claim_campnetwork_faucet(wallet_address):
    browser = await launch(headless=False, args=['--start-maximized'])
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})

    # Navigate to the faucet page
    await page.goto('https://faucet.campnetwork.xyz/', {'waitUntil': 'networkidle2'})
    print("Faucet page loaded")

    try:
        # Wait for wallet input field (update selector if needed)
        wallet_input_selector = 'input[type="text"][placeholder*="wallet"]'
        await page.waitForSelector(wallet_input_selector, timeout=15000)

        # Clear and type wallet address
        await page.evaluate(f'''selector => document.querySelector(selector).value = ""''', wallet_input_selector)
        await page.type(wallet_input_selector, wallet_address)
        print(f"Entered wallet address: {wallet_address}")

        # Wait for the claim button and click it (update selector if needed)
        claim_button_selector = 'button:enabled'  # You may need a more specific selector
        await page.waitForSelector(claim_button_selector, timeout=15000)
        await page.click(claim_button_selector)
        print("Clicked claim button")

        # Wait for confirmation message (update selector if needed)
        confirmation_selector = '.toast-message, .success-message, .alert-success'
        await page.waitForSelector(confirmation_selector, timeout=20000)
        message = await page.evaluate(f'''selector => document.querySelector(selector).innerText''', confirmation_selector)
        print(f"Faucet response: {message}")

    except Exception as e:
        print(f"Error during faucet claim: {e}")

    # Take a screenshot for verification
    await page.screenshot({'path': 'campnetwork_faucet_result.png'})
    print("Screenshot saved")

    await browser.close()

if __name__ == '__main__':
    # Replace with your actual wallet address
    my_wallet_address = '0xYourWalletAddressHere'
    asyncio.get_event_loop().run_until_complete(claim_campnetwork_faucet(my_wallet_address))
