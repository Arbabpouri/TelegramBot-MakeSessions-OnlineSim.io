from requests import get

class Request:
    def __init__(self) -> None:
        self.APIKEY = ""
        self.OPERATOR: str = "any"
        self.SERVICE: str = 'telegram'

    async def balance(self):
        try:
            req = get(
                f"https://onlinesim.ru/api/getBalance.php?apikey={self.APIKEY}").json()["balance"]
            return req
        except Exception as ex:
            print(ex)

    async def buy_number(self, CountryID):
        try:
            req = get(
                f"https://onlinesim.ru/api/getNum.php?apikey={self.APIKEY}&service={self.SERVICE}&country={CountryID}&number={True}").json()
            return req
        except Exception as ex:
            print(ex)

    async def change_status(self, Status, ID):
        try:
            req = get(
                f"http://api-conserver.onlinesim.ru/stubs/handler_api.php?api_key={self.APIKEY}&action=setStatus&status={int(Status)}&id={int(ID)}").text
            return req
        except Exception as ex:
            print(ex)

    async def get_sms(self, ID):
        try:
            req = get(
                f"http://onlinesim.ru/api/getState.php?apikey={self.APIKEY}&tzid={int(ID)}&message_to_code={1}").json()
            return req
        except Exception as ex:
            print(ex)

    async def cancel(self, ID):
        try:
            req = get(
                f"https://onlinesim.io/api/setOperationOk.php?apikey={self.APIKEY}&tzid={int(ID)}&ban={1}").json()
            return req
        except Exception as ex:
            print(ex)
