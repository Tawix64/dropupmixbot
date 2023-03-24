import os
import zipfile
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Envoyez-moi une image ou une vidéo et je vais l'uploader sur Mixdrop et vous donner le lien de téléchargement !")

def compress_and_upload_file(update, context):
    # Récupérer le fichier envoyé par l'utilisateur
    file = context.bot.get_file(update.message.document.file_id)
    file_name = update.message.document.file_name
    file_ext = file_name.split(".")[-1]

    # Télécharger le fichier à partir de Telegram et le sauvegarder localement
    file.download(file_name)

    # Compresser le fichier dans un fichier ZIP
    zip_file_name = file_name.split(".")[0] + ".zip"
    with zipfile.ZipFile(zip_file_name, "w") as zip:
        zip.write(file_name)

    # Supprimer le fichier original
    os.remove(file_name)

    # Upload le fichier ZIP sur Mixdrop
    upload_url = "https://ul.mixdrop.co/api"
    api_key = "LAcZ4tF0kUt9JhnNVOZ"

    # Créer les données pour l'API Mixdrop
    data = {
        "key": api_key,
        "file": (zip_file_name, open(zip_file_name, "rb"))
    }

    # Envoyer une demande POST pour uploader le fichier ZIP sur Mixdrop
    response = requests.post(upload_url, files=data)

    # Supprimer le fichier ZIP local
    os.remove(zip_file_name)

    # Récupérer le lien de téléchargement direct de Mixdrop
    download_link = response.json()["result"]["url"]

    # Envoyer le lien de téléchargement à l'utilisateur
    context.bot.send_message(chat_id=update.effective_chat.id, text="Votre fichier a été uploadé sur Mixdrop ! Voici le lien de téléchargement direct : " + download_link)

def main():
    # Créer une instance Updater et passer le token de votre bot Telegram
    updater = Updater(token="6100598091:AAEGHS4xh7NLInnzpZWgkj9VGI_hpX_USUY", use_context=True)

    # Créer un gestionnaire pour la commande /start
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    # Créer un gestionnaire pour les fichiers envoyés par les utilisateurs
    file_handler = MessageHandler(Filters.document.category("video") | Filters.document.category("image"), compress_and_upload_file)
    updater.dispatcher.add_handler(file_handler)

    # Démarrer le bot
    updater.start_polling()

    # Bloquer jusqu'à ce que l'utilisateur arrête le bot avec Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
