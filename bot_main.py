
import datetime
import asyncio
import aiohttp
import json
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8199983014:AAHDlXMX047RfrU5izmRa5AIwnFy1m3xI84"
premium_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    if username in premium_users and premium_users[username] > datetime.datetime.now():
        await update.message.reply_text(f"✅ Halo @{username}, kamu user premium sampai {premium_users[username].date()}")
    else:
        await update.message.reply_text(f"""👋 Selamat datang @{username}!

🚀 Bot ini akan mengirimi kamu info crypto otomatis jika kamu jadi user premium.

💬 Contoh info:
- Whale Alert: 100M USDT pindah ke Binance
- Coin Trending: PEPE, WIF, BONK
- Token Unlock: ARB unlock 92 juta token
- Event Penting: Launch, Listing, Halving
- Berita Politik Dunia yang pengaruh ke market

💸 Premium 1 Tahun = Rp20.000
Bayar via DANA: https://link.dana.id/minta?full_url=https://qr.dana.id/v1/281012092025070146201267
Setelah bayar, kirim username ke admin untuk aktivasi.
""")

async def aktifkan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Gunakan format: /aktifkan @username")
        return
    username = context.args[0].replace('@', '')
    expired = datetime.datetime.now() + datetime.timedelta(days=365)
    premium_users[username] = expired
    await update.message.reply_text(f"✅ @{username} sudah diaktifkan sampai {expired.date()}")

async def cekuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not premium_users:
        await update.message.reply_text("📭 Belum ada user premium.")
        return
    msg = "📋 Daftar Premium:\n"
    for user, exp in premium_users.items():
        msg += f"@{user} → aktif s/d {exp.date()}\n"
    await update.message.reply_text(msg)

async def fetch_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                coins = [coin['item']['name'] for coin in data['coins'][:5]]
                pesan = "🔥 *Trending Coins Saat Ini:*\n"
                pesan += "\n".join([f"• {coin}" for coin in coins])
                return pesan
    except:
        return None

async def auto_send(bot):
    while True:
        pesan = await fetch_trending_coins()
        if pesan:
            for username in premium_users:
                try:
                    await bot.send_message(chat_id=f"@{username}", text=pesan, parse_mode='Markdown')
                except Exception as e:
                    print(f"Gagal kirim ke @{username}: {e}")
        await asyncio.sleep(600)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aktifkan", aktifkan))
    app.add_handler(CommandHandler("cekuser", cekuser))
    bot = Bot(token=TOKEN)
    asyncio.create_task(auto_send(bot))
    print("Bot jalan dan auto-send aktif...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
