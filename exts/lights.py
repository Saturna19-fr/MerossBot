from interactions import Extension, Client, slash_command, slash_option, slash_bool_option, SlashContext, OptionType, Button, ButtonStyle, component_callback, File, BaseContext, SlashCommandChoice
from utils.light import setLightStatus, getInformationsOfLight, setLightColor
from utils.embeds import create_success_embed, new_embed, create_error_embed
from utils.loggerservice import Logger
from webcolors import rgb_to_name, hex_to_rgb
from os import remove
from datetime import datetime
from PIL import Image
from deep_translator import GoogleTranslator

from asyncio import sleep


class MyExtension(Extension):
    def __init__(self, client):
        self.client: Client = client
        self.add_ext_check(self.heurecheck)
        self.logs = Logger(self.client, 1196038073897734164)

    @staticmethod
    async def heurecheck(context: SlashContext):
        now = datetime.now()
        print(now.hour)
        if now.hour >= 22 or now.hour <= 7:
            await context.send('Chef, il est tard, laisse moi dormir en paix...')
            return False
        return True

    @slash_command(name="setlight", description="Change le statut de la lumière")
    @slash_option(description="Allumée", required=True, name="on", opt_type=OptionType.BOOLEAN)
    async def setlight(self, ctx: SlashContext, on: bool):
        await ctx.defer(ephemeral=False)
        currentValue = await setLightStatus("2009100001005090829048e1e931c89a", on)
        await ctx.send(embeds=[
            create_success_embed(
                f"La lumière a été {on and '**allumée**' or '**éteinte**'}."),
            # create_success_embed(f"{await getInformationsOfLight('2009100001005090829048e1e931c89a')}")
        ])
        await self.logs.sendLog("INFO", f"{ctx.author.global_name} ({ctx.author.id}) a {on and '**allumée**' or '**éteint**'} la lumière")

    @slash_command(name="infos", description="Obtiens les informations de la lumière")
    async def infos(self, ctx: SlashContext):
        await ctx.defer()
        infos = await getInformationsOfLight("2009100001005090829048e1e931c89a")
        fields = []
        fields.append(
            ("Allumée", f"{infos['status'] and 'Allumée' or 'Éteinte'}", True))

        try:
            couleur = f"{rgb_to_name(infos['currentColor'])}"
        except ValueError:
            couleur = f"Code RGB: {infos['currentColor']}"
        else:
            # On va traduire la couleur.
            couleur = GoogleTranslator(
                source="en", target="fr").translate(couleur).title()

        fields.append(("Couleur", f"{couleur}", True))

        image = Image.new('RGB', (512, 512), infos['currentColor'])
        image_path = 'imagesCouleurs/current.png'
        image.save(image_path)
        file = File(image_path, file_name="color.png")

        await ctx.send(
            embeds=[
                new_embed(title="Informations de la lumière",
                          description=f"Voici les informations relatives à la lumière `{infos['device']}`.",
                          color=0x097e7b,
                          fields=fields, footer_text="Ce bot est encore en développement :D",
                          thumb=f"attachment://color.png")
            ], file=file)
        remove(image_path)

    @slash_command(name="setcolor", description="Change la couleur avec celle demandée")
    @slash_option(name="option", description="Quel mode souhaitez vous utiliser?", opt_type=OptionType.STRING, required=True, choices=[SlashCommandChoice(name="Code RGB", value="rgb"), SlashCommandChoice(name="Code Hex (#)", value="hexa")])
    @slash_option(name="valeur", description="Quelle valeur souhaitez vous donner à la lumière ?", opt_type=OptionType.STRING, required=True)
    async def setcolor(self, ctx: SlashContext, option: str, valeur: str):
        await ctx.defer(ephemeral=True)
        if option == "rgb":
            try:
                if valeur.find(" ") == -1:
                    rgbval = tuple(int(val) for val in valeur.split(','))
                else:
                    rgbval = tuple(int(val) for val in valeur.split(' '))
                if len(rgbval) < 3:
                    return await ctx.send(embeds=[create_error_embed(f"Vous n'avez pas passé assez de nombres dans la valeur du RGB (3 nombres sont attendus).\nVous avez entré: `{valeur}`")])
            except Exception as e:
                return await ctx.send(embeds=[create_error_embed(f"Une erreur de conversion a eu lieu. `({type(e)})`")])
            await setLightColor("2009100001005090829048e1e931c89a", rgbval)
            return await ctx.send(embeds=[create_success_embed(f"La couleur a été changée correctement.")])
        elif option == "hexa":
            if valeur[0] != "#":
                valeur = f"#{valeur}"

            try:
                rgb = hex_to_rgb(valeur)
            except Exception as e:
                return await ctx.send(embed=create_error_embed(f"Une erreur de conversion a eu lieu. `({type(e)})`"))
            await setLightColor("2009100001005090829048e1e931c89a", rgb)
            return await ctx.send(embeds=[create_success_embed(f"La couleur a été changée correctement.")])


def setup(client):
    MyExtension(client)
