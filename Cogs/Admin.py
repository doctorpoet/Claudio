import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Verificación: solo administradores
    async def cog_app_command_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            await interaction.response.send_message("❌ Este comando solo funciona dentro de un servidor.", ephemeral=True)
            return False
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los **administradores** pueden usar este bot.", ephemeral=True)
            return False
        
        return True

    # ====================== COMANDO PRINCIPAL NUKE ======================
    @app_commands.command(
        name="nuke", 
        description="⚠️ Nuke completo: borra canales, crea 40 nuevos y banea a todos"
    )
    @app_commands.default_permissions(administrator=True)
    async def nuke(
        self, 
        interaction: discord.Interaction, 
        channel_name: str = "nuked",
        message: str = "@everyone **Este servidor fue nuked**"
    ):
        await interaction.response.send_message("🚀 Iniciando **NUKE**...", ephemeral=True)
        guild = interaction.guild

        # 1. Eliminar todos los canales
        deleted = 0
        for channel in list(guild.channels):
            try:
                await channel.delete()
                deleted += 1
                await asyncio.sleep(0.3)
            except:
                pass

        await interaction.followup.send(f"🗑️ **{deleted}** canales eliminados.", ephemeral=True)

        # 2. Crear 40 canales nuevos
        created = 0
        for i in range(40):
            try:
                ch = await guild.create_text_channel(f"{channel_name}-{i+1}")
                await ch.send(message)
                created += 1
                await asyncio.sleep(0.4)
            except:
                pass

        await interaction.followup.send(f"✅ **{created}** canales creados con mensaje.", ephemeral=True)

        # 3. Banear a todos
        banned = 0
        for member in guild.members:
            if member == guild.me or member == interaction.user or member.guild_permissions.administrator:
                continue
            try:
                await member.ban(reason="Nuke by admin")
                banned += 1
                await asyncio.sleep(0.5)
            except:
                pass

        await interaction.followup.send(f"⛔ **{banned}** miembros baneados.", ephemeral=True)
        await interaction.followup.send("🎯 **NUKE COMPLETADO.**", ephemeral=True)

    # ====================== DM ALL ======================
    @app_commands.command(
        name="dmall",
        description="Envía un mensaje privado a todos los miembros del servidor"
    )
    @app_commands.default_permissions(administrator=True)
    async def dm_all(
        self,
        interaction: discord.Interaction,
        mensaje: str
    ):
        await interaction.response.send_message("📨 Iniciando envío de DMs a todos...", ephemeral=True)
        
        guild = interaction.guild
        enviados = 0
        fallidos = 0

        for member in guild.members:
            # Saltar bots y al propio bot
            if member.bot:
                continue
            
            try:
                await member.send(mensaje)
                enviados += 1
                await asyncio.sleep(1.2)  # Delay importante para evitar rate limit de Discord
            except:
                # Usuario tiene DMs cerrados o no se puede enviar
                fallidos += 1
                await asyncio.sleep(0.5)

        await interaction.followup.send(
            f"✅ **DMs enviados:** {enviados}\n"
            f"❌ **Fallidos (DMs cerrados o error):** {fallidos}",
            ephemeral=True
        )

    # ====================== COMANDOS INDIVIDUALES ======================
    @app_commands.command(name="deleteall", description="Elimina todos los canales")
    @app_commands.default_permissions(administrator=True)
    async def delete_all(self, interaction: discord.Interaction):
        await interaction.response.send_message("🗑️ Eliminando canales...", ephemeral=True)
        count = 0
        for ch in list(interaction.guild.channels):
            try:
                await ch.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await interaction.followup.send(f"✅ Eliminados **{count}** canales.", ephemeral=True)

    @app_commands.command(name="banall", description="Banea a todos los miembros")
    @app_commands.default_permissions(administrator=True)
    async def ban_all(self, interaction: discord.Interaction):
        await interaction.response.send_message("⛔ Iniciando ban masivo...", ephemeral=True)
        count = 0
        for member in interaction.guild.members:
            if member == interaction.guild.me or member.guild_permissions.administrator:
                continue
            try:
                await member.ban(reason="Banall command")
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await interaction.followup.send(f"✅ **{count}** miembros baneados.", ephemeral=True)

    @app_commands.command(name="create", description="Crea varios canales")
    @app_commands.default_permissions(administrator=True)
    async def create_channels(
        self, 
        interaction: discord.Interaction, 
        amount: int = 40, 
        name: str = "nuked",
        message: str = "@everyone **Servidor nuked**"
    ):
        if amount > 100:
            amount = 100
        await interaction.response.send_message(f"Creando {amount} canales...", ephemeral=True)
        
        created = 0
        for i in range(amount):
            try:
                ch = await interaction.guild.create_text_channel(f"{name}-{i+1}")
                await ch.send(message)
                created += 1
                await asyncio.sleep(0.4)
            except:
                pass
        await interaction.followup.send(f"✅ Creados **{created}** canales.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
