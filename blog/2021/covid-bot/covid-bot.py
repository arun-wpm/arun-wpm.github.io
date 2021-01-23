# tutorial from: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

import discord
from discord.ext import tasks
import os, random
import json
import requests
from datetime import date, timedelta
from keep_alive import keep_alive
from replit import db

client = discord.Client()

prefix = '?'
if ("last_updates" not in db):
  db["last_updates"] = {}
last_updates = db["last_updates"]
api_url = "https://covid19.th-stat.com/api/open/"
opendata_url = "https://opend.data.go.th/get-ckan/datastore_search_sql?sql=SELECT * from \"329f684b-994d-476b-91a4-62b2ea00f29f\" WHERE announce_date="
opendata_key = os.getenv('APIKEY')
modes = {"new", "total", "help", "random", "update_here", "detail"}
ERROR_MSG = "นพ.ทวีศิลป์ ไม่เข้าในคำถามจากสื่อมวลชนข้อนี้ครับ"
UNIMPLEMENTED_MSG = "นพ.ทวีศิลป์ ยังไม่สามารถตอบคำถามจากสื่อมวลชนข้อนี้ได้ครับ"
CHANNEL_MSG = "นพ.ทวีศิลป์จะมาอัพเดตข้อมูลใน channel นี้ทุกวันครับ"
HELP_MSG = "สวัสดีครับ นพ.ทวีศิลป์มารายงานข้อมูลโควิด-19 ให้ประชาชนทราบครับ\n" + \
           ":robot: บอทนี้สร้างโดย @rayaburong#2953 ไม่แน่ใจว่าเคยมีคนอื่นทำบอทนี้แล้วรึยัง แต่ไม่เป็นไรครับ ได้ลองเขียนบอทก็สนุกดีครับ\n\n" + \
           "**:pushpin: implemented commands:**\n" + \
           "{**new**, **total**, **help**, **random**, **update_here**}\n" + \
           "ต่อด้วย {**confirmed**, **recovered**, **hospitalized**, **deaths**} สำหรับ new หรือ total\n" + \
           "เช่น " + prefix + "new confirmed\n" + \
           ":construction: อย่างอื่นจะค่อยๆ ตามมาทีหลังนะครับ :construction:"

# https://www.bangkokbiznews.com/news/detail/876826
quotes = [
    "ผมอยู่ตรงนี้ ไม่ได้มีเบี้ยประชุมจากการทำงานที่ ศบค.เลย ทำงานกันทุกวัน ไม่ได้พูดเพื่อที่จะอะไรอย่างไร",
    "ไม่ประมาท การ์ดอย่าตก",
    "ป้องกันโรค ป้องกันโลก",
    "จิตเป็นนาย กายเป็นบ่าว",
    "ผมต้องขอขอบคุณคนที่จัดชุดข้อมูลของผมมากมาย บางคนไม่ได้นอนส่งข้อมูลถึงตี 2 ตี 3",
    "หน้าที่ของการแถลงข่าวตรงนี้ ก็ไม่ใช่อาชีพผมเหมือนกัน เรื่องของการแถลงข่าว เป็นภาระหน้าที่ที่ได้รับมอบหมายมาก็พยายามทำให้ดีที่สุด",
    "โควิดสมุทรสาคร ไม่ใช่การระบาดระลอก 2 นับเป็น *การระบาดใหม่*",
    "รวมกันเราติดหมู่ แยกกันอยู่เรารอด",
    "อย่าลืมสวมหน้ากากและรักษาสุขภาพให้แข็งแรงนะครับ",
    "หมอทวีศิลป์ รับรางวัล ผู้ใช้ภาษาไทยสร้างสรรค์ดีเด่น จากกระทรวงวัฒนธรรม",
    "note from the creator: แปปเดียวก็วนแล้ว เดี๋ยวไปหามาเพิ่ม 55555",
]

# graphing

# historical queries

# provincial queries

# basic features
def query(server, channel, mode, command):
    if (mode not in modes):
        return ERROR_MSG
    if (mode == "detail"):
        return UNIMPLEMENTED_MSG
    elif (mode == "help"):
        return HELP_MSG
    elif (mode == "random"):
        return quotes[random.randrange(len(quotes))]
    elif (mode == "update_here"):
        if (channel.id not in last_updates):
            last_updates[channel.id] = None
        db["last_updates"] = last_updates
        return CHANNEL_MSG

    text = requests.get(api_url + "timeline").text
    content = json.loads(text)
    latest_update = content["UpdateDate"]
    try:
        response = content["Data"][-1][("New" if mode == "new" else "") + command.capitalize()]
    except KeyError:
        return ERROR_MSG
    return "**" + mode + " " + command + "** วันนี้อยู่ที่ **" + str(response) + "** รายครับ (*ข้อมูลอัพเดตล่าสุด " + latest_update + "*)"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(prefix):
        words = message.content.split(' ')
        mode = words[0][1:] # "new", "total", "detail"
        command = words[1] if len(words) > 1 else "" # "confirmed", "recovered", "hospitalized", "deaths"
        await message.channel.send(query(message.guild.id, message.channel, mode, command))

emojis = {
    "ระยอง": ":game_die:",
    "สมุทรสาคร": ":shrimp:",
    "โรงงาน": ":factory:",
    "State Quarantine": ":hotel:",
    "ASQ": ":airplane:",
    "ระบุไม่ได้": ":question:",
    "บันเทิง": ":night_with_stars:",
    "สัมผัส": ":people_hugging:",
    "ชุมชน": ":cityscape:",
}
def find_emoji(group):
    for keyword in emojis:
        if (keyword in group):
            return emojis[keyword]
    return ""

# daily updates
@tasks.loop(minutes=5)
async def daily_update():
    print("checking for daily update...")
    today = date.today()
    print(today)
    print("last updates: " + str(last_updates))

    text = requests.get(api_url + "today").text
    try:
        content = json.loads(text)
    except json.decoder.JSONDecodeError:
        return
    latest_update = content["UpdateDate"]
    if (today.strftime("%d/%m/%Y") in latest_update):
        print("updating!")

        # case by case
        session = requests.Session()
        url = opendata_url + "'" + today.isoformat() + "T00:00:00'"
        request = requests.Request('GET', url)
        prepped = request.prepare()
        prepped.headers['api-key'] = opendata_key
        cases_text = session.send(prepped).text
        cases_content = json.loads(cases_text)["result"]
        if (len(cases_content["records"]) != content["NewConfirmed"]):
            return
        breakdown_group = {}
        breakdown_province = {}
        for case_details in cases_content["records"]:
            group = case_details["risk"]
            province = (case_details["province_of_onset"] if case_details["province_of_isolation"] == "" else case_details["province_of_isolation"])
            # print(group + " " + province)
            if (group not in breakdown_group):
                breakdown_group[group] = {"TOTAL":0}
            if (province not in breakdown_group[group]):
                breakdown_group[group][province] = 0
            if (province not in breakdown_province):
                breakdown_province[province] = 0
            breakdown_group[group][province] += 1
            breakdown_group[group]["TOTAL"] += 1
            breakdown_province[province] += 1

        # time to update!
        today_update = (today - timedelta(days=1)).strftime("%Y.%m.%d") + " noon - " + today.strftime("%Y.%m.%d") + " noon\n" + \
                        ":microbe: +" + str(content["NewConfirmed"]) + " :microbe: = " + str(content["Confirmed"]) + " total cases :cry:\n" + \
                        "***:map: Breakdown by Province***\n"
        for province in dict(sorted(breakdown_province.items(), key=lambda item: -item[1])):
            today_update += "    * " + str(breakdown_province[province]) + " " + province + "\n"
        today_update += "\n***:people_holding_hands: Breakdown by Group and Province***\n"
        for group in dict(sorted(breakdown_group.items(), key=lambda item: item[0])):
            today_update += "**" + str(breakdown_group[group]["TOTAL"]) + " " + group + " " + find_emoji(group) + "**\n"
            for province in dict(sorted(breakdown_group[group].items(), key=lambda item: -item[1])[1:]):
                today_update += "    * " + str(breakdown_group[group][province]) + " " + province + "\n"
        today_update += "*(ข้อมูลจาก data.go.th ซึ่งไม่แยกประเภท SQ/ติดเชื้อในประเทศ/ตรวจเชิงรุก/ชายแดนประเทศ*\n"
        today_update += "*ถ้ามีเวลา ผู้พัฒนาจะพยายามหาวิธีดึงรูปจาก แถลงการ ศบค. มาเป็นรายงานลักษณะนี้)*"
        for channel_id in last_updates:
            if (last_updates[channel_id] is None or last_updates[channel_id] < today):
                channel = client.get_channel(channel_id)
                await channel.send(today_update)
                last_updates[channel_id] = today

@client.event
async def on_ready():
    daily_update.start()

keep_alive()
client.run(os.getenv('TOKEN'))