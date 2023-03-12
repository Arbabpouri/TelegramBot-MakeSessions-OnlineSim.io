from Api.Api import Request
from asyncio import sleep
from time import time
from random import choice
from json import loads
from telethon.sync import TelegramClient
from telethon.errors import PhoneNumberBannedError, PhoneNumberInvalidError, PhoneCodeEmptyError, FloodWaitError


class Cr(object):
    def __init__(self, CountryID: int) -> None:
        self.country_id: int = CountryID
        myList = loads(open('Sessinos/APIS/APIs.json', 'r').read())["API"]
        random = dict(choice(myList))
        self.api_id = int(*random.keys())
        self.api_hash = str(*random.values())
        self.namelist = ["Mmd", "Ali", "تنهای وحشی", "Hitler", "Mobarak", "hassan", "islam", "خامنه ای",
                         "رییسی", "313", "سرباز", "soldier", "God of War", ":))))", "Hell", "جهنم", "بهشت زوری"]

    async def try_for_create(self):  # Session creator
        getPhone = await Request().buy_number(int(self.country_id))  # Get Number
        if getPhone["response"] == 1:  # if geting number phone
            # create client for send code request to number
            client = TelegramClient(
                str(getPhone["number"]), self.api_id, self.api_hash)
            await client.connect()  # connect to telegram

            try:
                # send request for ready to resive sms
                await Request().change_status(1, getPhone["tzid"])
                # send code request
                req = await client.send_code_request(getPhone["number"])
            except PhoneNumberBannedError:
                await client.disconnect()
                return "PhoneNumberBannedError", getPhone
            except PhoneNumberInvalidError:
                await client.disconnect()
                return "PhoneNumberInvalidError", getPhone
            except FloodWaitError:
                await client.disconnect()
                return "FloodWaitError", getPhone
            except Exception as ex:
                print(ex)

            if req.type == "SentCodeType.APP":
                return "NotSMS", getPhone

            await sleep(10)
            # request for Resive Code
            getCode = await Request().get_sms(getPhone["tzid"])
            if getCode[0]["response"] == "TRY_AGAIN_LATER":
                await sleep(20)
                getCode = await Request().get_sms(getPhone["tzid"])
                if getCode["response"] == "TRY_AGAIN_LATER":
                    return "TRY_AGAIN_LATER", getPhone
                else:
                    pass

            if getCode[0]["response"] == "TZ_NUM_WAIT":  # if code not resive
                Lim, Number = time() + 300, 0
                while True:
                    await sleep(1)
                    # request for Resive Code
                    getCode = await Request().get_sms(getPhone["tzid"])
                    Number += 1
                    if time() >= Lim:
                        return "NotSendCode", getPhone
                    elif Number == 120:
                        Number = 0
                        req = await client.send_code_request(getPhone["number"])
                    elif getCode[0]["response"] == "TZ_NUM_ANSWER":  # if get Code
                        break

            if getCode[0]["response"] == "TZ_NUM_ANSWER":
                Code = getCode[0]["msg"]
                try:
                    await client.sign_up(phone=getPhone["number"], phone_code_hash=req.phone_code_hash, code=Code, first_name=str(choice(self.namelist)))
                    return "True", getPhone
                except PhoneCodeEmptyError:
                    Num, Check = 0, 0
                    while Num == 1:
                        try:
                            if Check == 5:
                                return "NotSendCode", getPhone
                            Check += 1
                            req = await client.send_code_request(getPhone["number"])
                            await sleep(10)
                            getCode = await Request().get_sms(getPhone["tzid"])
                            Code = getCode[0]["msg"]
                            await client.sign_in(phone=getPhone["number"], code=Code, phone_code_hash=req.phone_code_hash)
                            Num = 1
                            return "True", getPhone
                        except PhoneCodeEmptyError:
                            Num = 0

            else:
                await client.disconnect()
                return "NotSendCode", getPhone
        else:
            return str(getPhone["response"])
