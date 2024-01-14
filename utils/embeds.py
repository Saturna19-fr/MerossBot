import interactions

def new_embed(
    title: str = "",
    description: str = "",
    color: int = 0x3b7873,
    image:str = None,
    thumb:str = None,
    fields: list[tuple[str, str, bool]] = [],
    footer_text:str = None,
) -> interactions.Embed:
    embed = interactions.Embed(
        title=title,
        description=description,
        color=color
    )
    if image:
        embed.set_image(url=image)
    if thumb:
        embed.set_thumbnail(url=thumb)
    if footer_text:
        embed.set_footer(text=footer_text)
    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2] or False)
    return embed


def create_error_embed(text: str) -> interactions.Embed:
    return new_embed(
        title="Quelque chose s'est mal passé.",
        description=text,
        color=0xFF0000
    )

def create_success_embed(text: str) -> interactions.Embed:
    return new_embed(
        title="Succès !",
        description=text,
        color=0x00FF00
    )

def new_notify_embed(text: str) -> interactions.Embed:
    return new_embed(
        title="Information",
        description=text,
        color=0x00e5ff
    )

def progression_embed(step:str, maxstep:str, text: str) -> interactions.Embed:
    return new_embed(
        title=f"En cours de chargement [{str(step)} / {str(maxstep)}]",
        description=text,
        color=0x00e5ff
    )

def non_responded() -> interactions.Embed:
    return new_embed(
        description="💡 Vous n'avez pas répondu à temps."
    )