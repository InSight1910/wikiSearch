from discord import Client, HTTPException
import wikipedia

prefix = "!wiki "
wikipedia.set_lang("es")


class MyClient(Client):
    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, msg):
        try:
            text = msg.content.replace(prefix, "")
            if msg.content.startswith(prefix):
                search = wikipedia.summary(text, sentences=8)
                if len(search) >= 2000:
                    search = wikipedia.summary(text, sentences=3)

                search += "\n\n" + ("-" * 180) + "\n\n"

                await msg.channel.send(search, delete_after=200.0, mention_author=True)

        except HTTPException as e:
            try:
                search = wikipedia.summary(text, sentences=4)
                await msg.channel.send(search)
            except HTTPException as ex:
                search = wikipedia.summary(text, sentences=1)
                await msg.channel.send(search)

        except wikipedia.DisambiguationError as e:
            text = msg.content.split(prefix)
            res = f"La palabra {text[1]} no se ha encontrado porfavor prueba con "
            for option in e.options:
                if option:
                    res += f"{option},"
            await msg.channel.send(res)


client = MyClient()
client.run("")
