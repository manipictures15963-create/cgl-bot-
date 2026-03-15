import os
import asyncio
from datetime import date, datetime
import pytz
from telegram import Bot
from telegram.request import HTTPXRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID   = int(os.environ.get("CHAT_ID", "0"))
IST       = pytz.timezone("Asia/Kolkata")

SCHEDULE = {
    "2026-03-16": {"day_no": "43", "date_str": "16.03.2026", "week": "Week 07", "maths": "Time & Work - Video 9,10", "english": "Pronoun - Video 1,2", "gs": "Revision - Modern History PYQ Q.536-760", "reasoning": "Pinnacle Series Pg.211 Q.168-267", "static_gk": "Monuments in India & their Builders (Part 2-4.4)", "vocab": "Nimisha Bansal Vocab PDF of 14/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-17": {"day_no": "44", "date_str": "17.03.2026", "week": "Week 07", "maths": "Revision - Time & Work Videos 1-10", "english": "Pronoun - Video 3,4,5", "gs": "Modern History PYQ Pg.214 Q.761-835", "reasoning": "Pinnacle Series Pg.211 Q.268-367", "static_gk": "Cremation Grounds of Famous Persons (Part 2-4.5)", "vocab": "Nimisha Bansal Vocab PDF of 15/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-18": {"day_no": "45", "date_str": "18.03.2026", "week": "Week 07", "maths": "Time & Work - Video 11,12", "english": "Pronoun Practice - Video 1", "gs": "Modern History PYQ Pg.214 Q.836-910", "reasoning": "Calendar - Video 1", "static_gk": "Full Revision (4.1-4.5, 2.1.5)", "vocab": "Nimisha Bansal Vocab PDF of 16/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-19": {"day_no": "46", "date_str": "19.03.2026", "week": "Week 07", "maths": "Time & Work - Video 13,14", "english": "Pronoun Practice - Video 2", "gs": "Polity - Video 1", "reasoning": "Calendar - Video 2", "static_gk": "Full Revision (4.1-4.5, 2.1.5)", "vocab": "Nimisha Bansal Vocab PDF of 17/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-20": {"day_no": "47", "date_str": "20.03.2026", "week": "Week 07", "maths": "Time & Work - Video 15,16", "english": "Voice - Video 1", "gs": "Polity - Video 2", "reasoning": "Calendar - Video 3", "static_gk": "Full Revision (3.1, 3.2)", "vocab": "Nimisha Bansal Vocab PDF of 19/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-21": {"day_no": "48", "date_str": "21.03.2026", "week": "Week 07", "maths": "Time & Work - Video 17,18", "english": "Voice - Video 2", "gs": "Polity - Video 3,4", "reasoning": "Calendar - Video 4", "static_gk": "Full Revision (3.3, 3.4, 3.5, 3.6)", "vocab": "Nimisha Bansal Vocab PDF of 20/01/2026 - Any 60 vocabs - Total 60"},
    "2026-03-22": {"day_no": "49", "date_str": "22.03.2026", "week": "Week 07", "maths": "Pinnacle Time & Work Pg.386 Q.48-97", "english": "Voice - Video 3", "gs": "Polity - Video 5,6", "reasoning": "Calendar - Video 5,6", "static_gk": "Full Revision (3.7, 3.8)", "vocab": "Nimisha Bansal Vocab PDF of 21/01/2026 - Any 60 vocabs - Total 60"},
}

def build_message():
    today_str = date.today().strftime("%Y-%m-%d")
    d = SCHEDULE.get(today_str)
    if not d:
        return "📌 Here is your Daily Task\n📚 Course: Combined Graduate Level (CGL) 2026 - Part-time\n\n🔁 Today is a REVISION DAY!\n\nGo through all topics covered this week.\nRevise notes, re-attempt weak questions, and stay consistent! 💪\n\n✨ Stay focused and complete all tasks ✅🚀"
    return (
        f"📌 Here is your Daily Task\n"
        f"📚 Course: Combined Graduate Level (CGL) 2026 - Part-time\n"
        f"🗓 Day {d['day_no']} ({d['date_str']}) - {d['week']}\n\n"
        f"🔢 Maths video / practice / test (1.5 hr)\n"
        f"🎥 Video - Maths in English and Tamil by Chandru sir\n"
        f"📌 Topic: {d['maths']}\n\n"
        f"✍️ English grammar video / practice / test (1 hr)\n"
        f"📝 Test - test folder - unlimited topic wise test folder - English\n"
        f"📌 Topic: {d['english']}\n\n"
        f"🌍 GS - GS video / revise (1 hr)\n"
        f"🎥 Video - GS in Tamil and English\n"
        f"📌 Topic: {d['gs']}\n\n"
        f"🧠 Reasoning video / practice / test (1 hr)\n"
        f"🎥 Video - Reasoning folder\n"
        f"📌 Topic: {d['reasoning']}\n\n"
        f"📖 Static GK (1 hr)\n"
        f"🎥 Video - New series Static GK by Pradeep Sir\n"
        f"📌 Topic: {d['static_gk']}\n\n"
        f"📝 Eng vocab (30 mints)\n"
        f"📖 Read - {d['vocab']}\n\n"
        f"⏳ Revision (30 mints extra)\n"
        f"✨ Stay focused and complete all tasks ✅🚀"
    )

async def send_schedule():
    for attempt in range(3):
        try:
            request = HTTPXRequest(connect_timeout=30, read_timeout=30, write_timeout=30)
            bot = Bot(token=BOT_TOKEN, request=request)
            async with bot:
                await bot.send_message(chat_id=CHAT_ID, text=build_message())
            print(f"[{datetime.now(IST).strftime('%Y-%m-%d %H:%M')} IST] Message sent successfully.")
            return
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(5)
    print("All 3 attempts failed.")

async def main():
    scheduler = AsyncIOScheduler(timezone=IST)
    scheduler.add_job(send_schedule, trigger="cron", hour=2, minute=0, id="job_2am")
    scheduler.start()
    print("CGL 2026 Bot is running.")
    print("Scheduled: 2:00 AM IST daily (16 Mar - 22 Mar 2026)")
    print("Sending test message now...")
    await send_schedule()
    print("Done.")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
