import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import lyricsgenius

# ตั้งค่า API
TELEGRAM_TOKEN = '8709071604:AAFCxJ_nI6qUF95pbXUwIC2aD9NLZCxS1OE'
GENIUS_TOKEN = 'i18Jeyrkjmr9KCvIcUcTcxArRHaSt2X0PaN607YiMpDbqLQelJ7rdXeoHfykJ74K'

genius = lyricsgenius.Genius(GENIUS_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # ส่งข้อความ "กำลังค้นหา..." ให้ผู้ใช้เห็นว่าบอททำงานอยู่
    await update.message.reply_text("กำลังค้นหาเพลงจากเนื้อร้อง... รอสักครู่ครับ")
    
    # ค้นหาเพลงผ่าน Genius
    song = genius.search_song(text, get_full_info=False)
    
    if song:
        response = f"เจอแล้ว! 🎵\nชื่อเพลง: {song.title}\nศิลปิน: {song.artist}\nURL: {song.url}"
    else:
        response = "ขออภัยครับ ไม่พบเพลงจากเนื้อร้องนี้"
    
    await update.message.reply_text(response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # ให้บอทตอบกลับทุกข้อความที่มีการพิมพ์ส่งมา
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), find_song)
    application.add_handler(msg_handler)
    
    print("บอทกำลังทำงาน...")
    application.run_polling()
