import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("8621871224:AAEBjiD4pth2A8ViDnPHml1Rvm5NCu_MzZo")

gastos = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Envie gastos assim:\n"
        "Ex: 45 feira\n"
        "Ex: 50gasolina\n\n"
        "Use /resumo\n"
        "Use /limpar"
    )

async def salvar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    try:
        valor = ""
        descricao = ""

        for i in texto:
            if i.isdigit():
                valor += i
            else:
                descricao += i

        valor = float(valor)
        descricao = descricao.strip()

        data = datetime.now().strftime("%d/%m %H:%M")

        gastos.append({
            "valor": valor,
            "descricao": descricao,
            "data": data
        })

        await update.message.reply_text(
            f"✅ Salvo: R$ {valor} - {descricao} ({data})"
        )

    except:
        await update.message.reply_text("❌ Use formato: 50 mercado")

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not gastos:
        await update.message.reply_text("Sem gastos.")
        return

    total = sum(g["valor"] for g in gastos)

    texto = "📊 Resumo:\n\n"
    for g in gastos:
        texto += f"{g['data']} - R$ {g['valor']} ({g['descricao']})\n"

    texto += f"\n💰 Total: R$ {total}"

    await update.message.reply_text(texto)

async def limpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gastos.clear()
    await update.message.reply_text("🧹 Apagado.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("resumo", resumo))
app.add_handler(CommandHandler("limpar", limpar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, salvar))

app.run_polling()
