from interactions import Extension, Client, slash_command, slash_option, slash_bool_option, SlashContext, OptionType, Button, ButtonStyle, component_callback
from utils.light import setLightStatus, getInformationsOfLight
from utils.embeds import create_success_embed, new_embed
from asyncio import sleep
class MyExtension(Extension):
    def __init__(self, client):
        self.client: Client = client

    @slash_command(name="setlight", description="Change le statut de la lumière")
    @slash_option(description="Allumée", required=True, name="on", opt_type=OptionType.BOOLEAN)
    async def setlight(self, ctx:SlashContext, on: bool):
        await ctx.defer(ephemeral=False)
        currentValue = await setLightStatus("2009100001005090829048e1e931c89a", on)
        await ctx.send(embeds=[
            create_success_embed(f"La lumière a été {on and '**allumée**' or '**éteinte**'}."),
            create_success_embed(f"{await getInformationsOfLight('2009100001005090829048e1e931c89a')}")
        ])
    
    @slash_command(name="infos", description="Obtiens les informations de la lumière")
    async def infos(self, ctx: SlashContext):
        await ctx.defer()
        infos = await getInformationsOfLight("2009100001005090829048e1e931c89a")
        fields = []
        fields.append(("Allumée", f"{infos['status'] and 'Allumée' or 'Éteinte'}", True))
        fields.append(("Couleur", f"{infos['currentColor'][0]}, {infos['currentColor'][1]}, {infos['currentColor'][2]}", True))
        await ctx.send(
            embeds=[
                new_embed(title="Informations de la lumière",
                description=f"Voici les informations relatives à la lumière `{infos['device']}`.",
                color=0x097e7b,
                fields=fields, footer_text="Ce bot est encore en développement :D")
            ]
        )

def setup(client):
    MyExtension(client)