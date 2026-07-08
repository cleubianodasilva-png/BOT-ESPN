
import os, requests, json, time
from datetime import datetime, timedelta, timezone

# Configurações
TELEGRAM_TOKEN = os.environ.get("TG_TOKEN", "")
CHAT_IDS = [os.environ.get("TG_GROUP_ID", "")]
GITHUB_TOKEN = os.environ.get("GH_PAT", "")
BRT = timezone(timedelta(hours=-3))

def send_telegram(text, botoes=True):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_IDS[0], "text": text, "parse_mode": "HTML"}
    if botoes:
        payload["reply_markup"] = json.dumps({
            "inline_keyboard": [[
                {"text": "🟣 BET365 🟣", "url": "https://www.bet365.com"},
                {"text": "🔵 PARIPESA 🔵", "url": "https://www.paripesa.com"}
            ]]
        })
    r = requests.post(url, json=payload)
    return r.status_code == 200

def monitor():
    sep = "━━━━━━━━━━━━━━━━━━━━"
    # Exemplo de sinal solicitado pelo usuário
    exemplo = (
        f"{sep}\n⛳️🔥<b>ESCANTEIO LIMITE HT</b>🔥⛳️\n"
        f"⚽️ Placar: <b>1 - 1</b>\n"
        f"🌏 Liga: <b>Premier League</b>\n"
        f"📡 <b>Liverpool</b> x <b>Chelsea</b>\n"
        f"⏰️ Minuto: <b>37</b>\n{sep}\n"
        f"📊 <b>Análise ao Vivo da Entrada:</b>\n"
        f"🎯 Chutes no Gol: <b>3 - 2</b>\n"
        f"🚀 Chutes Fora: <b>4 - 2</b>\n"
        f"🔥 Ataques Perigosos: <b>45 - 32</b>\n"
        f"📈 Posse de Bola: <b>52% - 48%</b>\n"
        f"⛳ Escanteios: <b>5 - 3</b>\n"
        f"💰 Odd Mínima Recomendada: <b>1.70</b>\n{sep}\n"
        f"⛳️ Escanteios Atuais: <b>8</b>\n"
        f"📌 Entrada: <b>Mais de 8.5 Cantos</b>\n"
        f"✅ Critérios: <b>5/6</b>\n{sep}\n"
        f"⚠️Jogue com responsabilidade⚠️"
    )
    
    # Verifica comandos /radar e /relatorio
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates", params={"timeout": 1}).json()
        if r.get("ok"):
            for up in r.get("result", []):
                msg = up.get("message", {})
                text = msg.get("text", "")
                if text == "/radar":
                    send_telegram(f"{sep}\n📡 <b>RADAR AO VIVO</b> 📡\n{sep}\n✅ Robô operando normalmente.\n{sep}", botoes=False)
                elif text == "/relatorio":
                    send_telegram(f"{sep}\n📊 <b>RELATÓRIO</b> 📊\n{sep}\n✅ Tudo em ordem por aqui!\n{sep}", botoes=False)
    except: pass

    # Envia o exemplo apenas se for execução manual (workflow_dispatch)
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        send_telegram(exemplo)

if __name__ == "__main__":
    monitor()
