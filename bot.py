import discord  # Discord API ile çalışmak için Discord kütüphanesini içe aktarma
from discord.ext import commands  # Bot komutları oluşturmak için discord.ext'den commands modülünün içe aktarılması
from config import token  # Botun tokenini config.py dosyasından içe aktarma

intents = discord.Intents.default()  # Botun yetkilerini belirlemek için bir intents nesnesi oluşturma
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları yasaklamasına izin veren bayrağı ayarlama
intents.message_content = True  # Botun mesajların içeriğiyle çalışmasına izin veren bayrağın ayarlanması

bot = commands.Bot(command_prefix='!', intents=intents)  # "!" komut önekiyle bir bot örneği oluşturun ve intents nesnesini ona aktarın

@bot.event  # Bot başarıyla başlatıldığında tetiklenecek olayı tanımlama
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Discord'da başarılı oturum açma hakkında konsolda bir mesaj görüntüleyin

@bot.command()  # Kullanıcı "!start" girdiğinde çağrılacak "start" komutunu tanımlayın
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")  # Sohbet odasına geri mesaj gönderme

@bot.command()  # Kullanıcının yasaklama haklarına sahip olmasını gerektiren "ban" komutunun tanımlanması
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:  # Komutun yasaklanması gereken kullanıcıyı belirtip belirtmediğinin kontrol edilmesi
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı yasaklamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)  # Bir kullanıcıyı sunucudan yasaklama
            await ctx.send(f" Kullanıcı {member.name} banlandı.")  # Başarılı bir yasaklama hakkında mesaj gönderme
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error  # "ban" komutu için bir hata işleyicisi/handler tanımlayın
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")  # Kullanıcıyı erişim hakları hatası hakkında bilgilendiren bir mesaj gönderme
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı.")  # Belirtilen kullanıcı bulunamazsa bir hata mesajı gönderme

bot.run(token)  # Kimlik doğrulama için token kullanarak botu başlatma