# < Coded by Samrat >
import asyncio
import aiohttp
import time
import random
import uuid
from pyrogram import *
from pyrogram.types import *
import pymongo

bot = Client("bot", api_id, "api_hash", bot_token="7669492702:AAGmtWhj5QkuYBkwWszyMla6vGheEuFC43k", in_memory=True)

temp = {}
alr = []
OWNER_ID = 123456789  # replace with your userid
mongodb_uri = "your mongodb uri"  # get this from mongodb.com (example: "mongodb+srv://<username>:<password>@<cluster>/?retryWrites=true&w=majority") [don't include <>]

client = pymongo.MongoClient(mongodb_uri)
db = client["HamsterKombat"]

def add(user_id, username):
    my_collection = db["users"]
    s = my_collection.find_one({"user_id": user_id})
    if not s:
        my_collection.insert_one({"user_id": user_id, "username": username, "hash": ""})

def get_hash(user_id):
    my_collection = db["users"]
    s = my_collection.find_one({"user_id": user_id})
    return s["hash"]

def add_hash(user_id, hash):
    my_collection = db["users"]
    return my_collection.update_one({"user_id": user_id}, {"$set": {"hash": hash}})  

def getall():
    my_collection = db["users"]
    return my_collection.find()

async def promogen(a, b, c, bot, msg, rep):

    app_token = a
    promo_id = b
  
    async def generate_client_id():
        hash_id = get_hash(msg.from_user.id)
        if len(hash_id) != 0:
            return hash_id
        else: 
            timestamp = int(time.time() * 1000)
            random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
            hash_id = f"{timestamp}-{random_numbers}"
            add_hash(msg.from_user.id, hash_id)
            return hash_id

    async def login_client():
        client_id = await generate_client_id()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('https://api.gamepromo.io/promo/login-client', json={
                    'appToken': app_token,
                    'clientId': client_id,
                    'clientOrigin': 'deviceid'
                }, headers={
                    'Content-Type': 'application/json; charset=utf-8',
                }) as response:
                    data = await response.json()
                    return data['clientToken']
            except Exception as error:
                # await rep.reply('**ERROR:** `failed to login`', quote=True)
                await asyncio.sleep(5)
                return await login_client()  

    async def register_event(token):
        event_id = str(uuid.uuid4())
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('https://api.gamepromo.io/promo/register-event', json={
                    'promoId': promo_id,
                    'eventId': event_id,
                    'eventOrigin': 'undefined'
                }, headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json; charset=utf-8',
                }) as response:
                    data = await response.json()
                    if not data.get('hasCode', False):
                        await asyncio.sleep(5)
                        return await register_event(token)
                    else:
                        return True
            except Exception as error:
                await asyncio.sleep(5)
                return await register_event(token)

    async def create_code(token):
        async with aiohttp.ClientSession() as session:
            response = None
            while not response or not response.get('promoCode'):
                try:
                    async with session.post('https://api.gamepromo.io/promo/create-code', json={
                        'promoId': promo_id
                    }, headers={
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json; charset=utf-8',
                    }) as resp:
                        response = await resp.json()
                except Exception as error:
                    await rep.reply('**ERROR:** `failed to get promoCode, trying again`', quote=True)
                    await asyncio.sleep(1)
            return response['promoCode']

    async def gen():
        token = await login_client()
        
        await register_event(token)
        code_data = await create_code(token)
        temp[msg.from_user.id].append(code_data)

    try:
        tasks = [gen() for _ in range(1)]
        await asyncio.gather(*tasks)
    except Exception as error:
        print(f'error: {error}')


games = {
    "ZOO": {
        "app_token": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
        "promo_id": "b2436c89-e0aa-4aed-8046-9b0515e1c46b",
    },
    "TILE": {
        "app_token": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
        "promo_id": "e68b39d2-4880-4a31-b3aa-0393e7df10c7",
    },
    "CUBE": {
        "app_token": "d1690a07-3780-4068-810f-9b5bbf2931b2",
        "promo_id": "b4170868-cef0-424f-8eb9-be0622e8e8e3",
    },
    "TRAIN": {
        "app_token": "82647f43-3f87-402d-88dd-09a90025313f",
        "promo_id": "c4480ac7-e178-4973-8061-9ed5b2e17954",
    },
    "MERGE": {
        "app_token": "8d1cc2ad-e097-4b86-90ef-7a27e19fb833",
        "promo_id": "dc128d28-c45b-411c-98ff-ac7726fbaea4",
    },
    "TWERK": {
        "app_token": "61308365-9d16-4040-8bb0-2f4a4c69074c",
        "promo_id": "61308365-9d16-4040-8bb0-2f4a4c69074c",
    },
    "POLY": {
        "app_token": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
        "promo_id": "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71",
    },
    "TRIM": {
        "app_token": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
        "promo_id": "ef319a80-949a-492e-8ee0-424fb5fc20a6",
    },
    "STONE": {
        "app_token": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
        "promo_id": "04ebd6de-69b7-43d1-9c4b-04a6ca3305af",
    },
    "BOUNC": {
        "app_token": "bc72d3b9-8e91-4884-9c33-f72482f0db37",
        "promo_id": "bc72d3b9-8e91-4884-9c33-f72482f0db37",
    },
    "HIDE": {
        "app_token": "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
        "promo_id": "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
    },
}


@bot.on_message(filters.command("broadcast_all"))
async def brd(bot, msg):
    if not msg.from_user.id in [OWNER_ID]:
        return    
    if msg.reply_to_message:
        ed = await msg.reply("Broadcasting...")
        try:
            users = getall()
            d = 0
            t = 0
            for x in users:
                t += 1
                user_id = x["username"] if x.get("username") else x["user_id"]
                try:
                    await msg.reply_to_message.copy(user_id)
                    d += 1
                    await asyncio.sleep(0.1)
                    if t % 25 == 0:
                        await ed.edit(f"Broadcasting... {t} done")
                except:
                    pass
                
            await msg.reply(f"Broadcast done to {d} out of {t} users!")    
            return
        except Exception as e:
            await msg.reply(e)
            return
                                                            
    await msg.reply("__reply to a msg to broadcast__") 


@bot.on_message(filters.command("stats"))
async def stats(bot, msg):
    if not msg.from_user.id in [OWNER_ID]:
        return
