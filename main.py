# in the name of god | ey bug sharm kon bime abbasam | coded with love by @Sardar_Cybery
# -------------------------------------------------- import -------------------------------------------------
try:
    from telethon.sync import TelegramClient
    from telethon.events import NewMessage, CallbackQuery
except ImportError:
    print('please wait')
    system('pip install telethon')
    print('telethon installed')
from asyncio import sleep
from Api.Api import Request
from os import system
from json import loads
from KeyBoard.KeyBoard import AllButtons
from os import remove
from Sessinos.SessionCreator import Cr
import logging
logging.basicConfig(filename="log.txt", filemode="a",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------- Bot Config ------------------------------------------------

Data = loads(open('Config/Config.json', 'r').read())
client = TelegramClient("main", Data["ApiID"], Data["ApiHash"]).start(
    bot_token=Data["Token"])
# -------------------------------------------------- Body Bot --------------------------------------------------


async def cancel_and_remove(Status):
    remove(f"{Status[1]['number']}.session")
    await sleep(300)
    await Request().cancel(Status[1]["tzid"])


# /start
@client.on(NewMessage(pattern='/start', func=lambda e: e.is_private and e.sender_id in Data["Admins"]))
async def StartMenu(event):
    await client.send_message(event.sender_id, "Hello welcome to bot", buttons=AllButtons.admin_buttons)


# get balance
@client.on(CallbackQuery(data='balance', func=lambda e: e.is_private and e.sender_id in Data["Admins"]))
async def GetBalance(event):
    await event.edit("چند لحظه صبر کنید ...")
    await event.edit(f"🔺 خب خب ببینیم چقد پول داریم , اینطوری که معلومه موجودی پنل برابره با = ** {await Request().balance()} دلار  **\nانشاالله 999999 باشه 😍👌", buttons=AllButtons.admin_buttons)


# send country menu
@client.on(CallbackQuery(data='create', func=lambda e: e.is_private and e.sender_id in Data["Admins"]))
async def SendCountryMenu(event):
    await event.edit("😀 سشن کدوم کشورو برات بسازم سرورم؟ 🤖", buttons=AllButtons.country_name_buttons)


# select country and request for create session
@client.on(CallbackQuery(func=lambda e: e.is_private and e.sender_id in Data["Admins"]))
async def SelectCountry(event: CallbackQuery.Event):
    CountryID = event.data.decode('utf-8')
    if CountryID.isnumeric():

        await event.edit("چند لحظه صبر کنید . . .")
        Status = await Cr(int(CountryID)).try_for_create()

        if len(Status) == 2 and Status[0] == "True":
            await client.send_file(event.sender_id, f"{Status[1]['number']}.session", caption="اینم خدمت شما استاد عزیز")
            await Request().change_status(6, Status[1]["tzid"])

        if Status == "NO_NUMBER":
            await event.delete()
            await client.send_message(event.sender_id, "💢 دکتر سایت میگه شماره این کشور رو نداریم😐\nاگر دوست داری یک کشور دیگه رو تست کن انشاالله به مراد دلت برسی 😂😂\n\n🤖اینم پنل مدیریت خدمت شما😄", buttons=AllButtons.admin_buttons)

        elif Status == "WARNING_LOW_BALANCE":
            await event.delete()
            await client.send_message(event.sender_id, "💸دکتر موجودیمون برای خرید کافی نیست , دست تو جیب مبارک کن و شارژ کن💰", buttons=AllButtons.admin_buttons)

        elif Status == "BAD_SERVICE":
            await event.delete()
            await client.send_message(event.sender_id, "❌دکتر این شماره ای که زدیم دیگه سرویس تلگرام نداره , رکب بدی خوردیم❌", buttons=AllButtons.admin_buttons)

        elif Status == "ERROR_WRONG_KEY":
            await event.delete()
            await client.send_message(event.sender_id, "❌دکتر دیدی چیشد؟\nمیگه APIKEY اشتباهه🥹\n\n🔺آموزش تعویض : ابتدا وارد پوشه API شده و سپس فایل Api.py رو باز میکنید و مقدار self.APIKEY رو با Api Key جدید عوض میکنی , به همین راحتی🤍", buttons=AllButtons.admin_buttons)

        elif len(Status) == 2 and Status[0] == "PhoneNumberBannedError":
            await event.delete()
            await client.send_message(event.sender_id, f"🤭دکتر سایت رکب بدی بهمون زد\nشماره ای که ازش گرفتم بن شده بود بی پدر😂\n\n⭕️خودم خرید شماره رو لغو میکنم جای نگرانی نیست💢\n\n📞شماره : {Status[1]['number']}\n🔋کد خرید : {Status[1]['tzid']}", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

        elif len(Status) == 2 and Status[0] == "NotSendCode":
            await event.delete()
            await client.send_message(event.sender_id, f"🤨دکتر این بی فانوس کد نمیده\n😅خریدشو کنسل میکنم تا موجودی برگرده به حساب🤙\n\n📞شماره : {Status[1]['number']}\n🔋کد خرید : {Status[1]['tzid']}", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

        elif len(Status) == 2 and Status[0] == "PhoneNumberInvalidError":
            await event.delete()
            await client.send_message(event.sender_id, f"🤨دکتر این شماره ایو که گرفتم تلگرام قبول نمیکنه\nپس خریدو کنسل میکنم تا موجودی برگرده😎\n\n📞شماره : {Status[1]['number']}\n🔋کد خرید :{Status[1]['tzid']}", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

        elif len(Status) == 2 and Status[0] == "NotSMS":
            await event.delete()
            await client.send_message(event.sender_id, f"🕯دکتر این شماره ای که گرفتم متاسفانه به صورت sms نیومد و ممکنه یه یابو توش باشه پس خریدو کنسل میکنم تا موجودی بک بخوره😀\n\n📞شماره : {Status[1]['number']}\n🔋کد خرید : {Status[1]['tzid']}", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

        elif len(Status) == 2 and Status[0] == "TRY_AGAIN_LATER":
            await event.delete()
            await client.send_message(event.sender_id, "😄سایت پاسخگو نیست و میگه بعدا تلاش کن\nخریدو کنسل میکنم تا موجودی برگرده🤨", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

        elif len(Status) == 2 and Status[0] == "FloodWaitError":
            await event.delete()
            await client.send_message(event.sender_id, f"🤡شماره ای که گرفتم انقد بهش رکوئست زدن تا کد بگیرن بگا رفته\nخریدو کنسل میکنم و توم یه شماره دیگه بگیر\n\n📞شماره : {Status[1]['number']}\n🔋کد خرید : {Status[1]['tzid']}", buttons=AllButtons.admin_buttons)
            await cancel_and_remove(Status)

print('Bot is online')
client.run_until_disconnected()