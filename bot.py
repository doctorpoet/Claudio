import discord
from discord.ext import commands
import os

# ==================== CONFIGURACIÓN ====================
intents = discord.Intents.default()
intents.guilds = True
intents.members = True      # Necesario para banear miembros

class AdminBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  # Prefijo por si acaso (no principal)
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Carga los cogs al iniciar"""
        await self.load_extension("cogs.admin")
        print(f"✅ Cogs cargados correctamente.")

bot = AdminBot()

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    print(f"🤖 Bot conectado como {bot.user} (ID: {bot.user.id})")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Se sincronizaron {len(synced)} comandos slash globales.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

# ==================== INICIO DEL BOT ====================
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if not TOKEN:
        raise ValueError("❌ No se encontró DISCORD_TOKEN en las variables de entorno.")
    
    print("🚀 Iniciando bot...")
    bot.run(TOKEN)
