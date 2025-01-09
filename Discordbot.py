import discord
from discord.ext import commands, tasks
import random
import asyncio

# Your bot's token
TOKEN = ''

# Create the bot instance
intents = discord.Intents.default()
intents.members = True  # Enable access to member events
intents.message_content = True  # Enable access to message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Quiz questions and answers
quiz_data = [
    {"question": "Koji je glavni grad Srbije?", "options": ["Beograd", "Niš", "Kragujevac", "Novosad"], "answer": "Beograd"},
    {"question": "Koja je najveća reka u Srbiji?", "options": ["Sava", "Morava", "Drina", "Dunav"], "answer": "Dunav"},
    {"question": "Ko je pisac 'Na Drini ćuprija'?", "options": ["Ivo Andrić", "Miloš Crnjanski", "Danilo Kiš", "Borislav Pekić"], "answer": "Ivo Andrić"},
    {"question": "Koja je najviša planina u Srbiji?", "options": ["Kopaonik", "Tara", "Stara planina", "Radan"], "answer": "Stara planina"},
    {"question": "Ko je bio prvi predsednik Jugoslavije?", "options": ["Josip Broz Tito", "Ivan Stambolić", "Slobodan Milošević", "Vojislav Koštunica"], "answer": "Josip Broz Tito"},
    {"question": "Koja država se graniči sa Srbijom na zapadu?", "options": ["Mađarska", "Hrvatska", "Bugarska", "Rumunija"], "answer": "Hrvatska"},
    {"question": "Ko je napisao pesmu 'Tamo daleko'?", "options": ["Jovan Dučić", "Milan Jovanović", "Aleksa Šantić", "Vladislav Petković Dis"], "answer": "Aleksa Šantić"},
    {"question": "Koja životinja je simbol Srbije?", "options": ["Beli orao", "Lav", "Kengur", "Soko"], "answer": "Beli orao"},
    {"question": "Ko je najpoznatiji srpski teniser?", "options": ["Novak Đoković", "Viktor Troicki", "Janko Tipsarević", "Nenad Zimonjić"], "answer": "Novak Đoković"},
    {"question": "Koja reka prolazi kroz Beograd?", "options": ["Sava", "Morava", "Tisa", "Dunav"], "answer": "Sava"},
    {"question": "Ko je otkrio Srbu električnu energiju?", "options": ["Nikola Tesla", "Mihajlo Pupin", "Vuk Stefanović Karadžić", "Jovan Cvijić"], "answer": "Nikola Tesla"},
    {"question": "Koja hrana je tradicionalna za Srbiju?", "options": ["Sarma", "Pizza", "Pasta", "Sushi"], "answer": "Sarma"},
    {"question": "Koji je najpoznatiji srpski film?", "options": ["Underground", "Ko to tamo peva", "Maratonci trče počasni krug", "Balkanski špijun"], "answer": "Underground"},
    {"question": "Koji je najpoznatiji srpski rukometaš?", "options": ["Milenko Vuković", "Nikola Karabatić", "Božidar Jović", "Nemanja Zelenović"], "answer": "Milenko Vuković"},
    {"question": "Koji je najviši vrh na Kopaoniku?", "options": ["Pančićev vrh", "Jankov kamen", "Suvovršje", "Veliki Kopaonik"], "answer": "Pančićev vrh"},
    {"question": "Koja država se nalazi na jugu Srbije?", "options": ["Makedonija", "Hrvatska", "Rumunija", "Albanija"], "answer": "Makedonija"},
    {"question": "Ko je napisao pesmu 'Boj na Kosovu'?", "options": ["Njegoš", "Jovan Jovanović Zmaj", "Desanka Maksimović", "Branislav Nušić"], "answer": "Njegoš"},
    {"question": "Koja srpska pesma je najpoznatija u svetu?", "options": ["Tamo daleko", "Marš na Drinu", "Bojna Čavoglave", "Vidovdan"], "answer": "Marš na Drinu"},
    {"question": "Ko je otkrio da je Zemlja okrugla?", "options": ["Nikola Tesla", "Jovan Cvijić", "Mihajlo Pupin", "Aristotel"], "answer": "Aristotel"},
    {"question": "Koji je najpoznatiji srpski pesnik?", "options": ["Ivo Andrić", "Miloš Crnjanski", "Vuk Stefanović Karadžić", "Branislav Nušić"], "answer": "Ivo Andrić"},
    {"question": "Koja srpska planina je poznata po ski centrima?", "options": ["Kopaonik", "Stara planina", "Tara", "Javor"], "answer": "Kopaonik"},
    {"question": "Koja srpska ekipa je najuspešnija u fudbalu?", "options": ["Partizan", "Crvena zvezda", "Vojvodina", "Rad"], "answer": "Crvena zvezda"},
    {"question": "Koji srpski vladar je poznat po reformama?", "options": ["Miloš Obrenović", "Petar II Petrović Njegoš", "Aleksandar Karađorđević", "Dušan Silni"], "answer": "Miloš Obrenović"},
    {"question": "Koji je najpoznatiji srpski film?", "options": ["Underground", "Ko to tamo peva", "Maratonci trče počasni krug", "Balkanski špijun"], "answer": "Underground"},
    {"question": "Ko je bio prvi srpski kralj?", "options": ["Miloš Obrenović", "Karađorđe Petrović", "Petar I Karađorđević", "Dušan Silni"], "answer": "Petar I Karađorđević"},
    {"question": "Koji je najveći grad u Srbiji?", "options": ["Beograd", "Novi Sad", "Kragujevac", "Niš"], "answer": "Beograd"},
    {"question": "Koji srpski naučnik je izumeo radio?", "options": ["Nikola Tesla", "Mihajlo Pupin", "Vuk Stefanović Karadžić", "Jovan Cvijić"], "answer": "Nikola Tesla"},
    {"question": "Koji grad je najpoznatiji po filmovima?", "options": ["Beograd", "Novi Sad", "Niš", "Kragujevac"], "answer": "Beograd"},
    {"question": "Koja je najpoznatija srpska pesma?", "options": ["Marš na Drinu", "Tamo daleko", "Boj na Kosovu", "Vidovdan"], "answer": "Marš na Drinu"},
    {"question": "Koji je najpoznatiji srpski pesnik?", "options": ["Branislav Nušić", "Ivo Andrić", "Desanka Maksimović", "Jovan Jovanović Zmaj"], "answer": "Ivo Andrić"},
    {"question": "Ko je najpoznatiji srpski pisac?", "options": ["Ivo Andrić", "Miloš Crnjanski", "Danilo Kiš", "Vladislav Petković Dis"], "answer": "Ivo Andrić"},
    {"question": "Koji je najpoznatiji srpski sportista?", "options": ["Novak Đoković", "Miloš Teodosić", "Nenad Milijaš", "Dušan Tadić"], "answer": "Novak Đoković"},
    {"question": "Ko je bio najmlađi predsednik Republike Srbije?", "options": ["Slobodan Milošević", "Vojislav Koštunica", "Boris Tadić", "Aleksandar Vučić"], "answer": "Aleksandar Vučić"},
    {"question": "Koji srpski fudbaler je igrao za Real Madrid?", "options": ["Nemanja Bjelica", "Dejan Stanković", "Dušan Lajović", "Luka Jovic"], "answer": "Luka Jovic"},
    {"question": "Koji je najpoznatiji srpski pjevač?", "options": ["Željko Joksimović", "Aca Lukas", "Ceca Ražnatović", "Bojan Tomović"], "answer": "Željko Joksimović"},
    {"question": "Koji grad je domaćin Exit festivala?", "options": ["Beograd", "Niš", "Novi Sad", "Kragujevac"], "answer": "Novi Sad"},
    {"question": "Koji je najpoznatiji srpski film?", "options": ["Ko to tamo peva", "Balkanski špijun", "Maratonci trče počasni krug", "Underground"], "answer": "Ko to tamo peva"},
    {"question": "Koji je najviši vrh Srbije?", "options": ["Pančićev vrh", "Stara planina", "Veliki Kopaonik", "Jankov kamen"], "answer": "Pančićev vrh"},
    {"question": "Koji srpski sportista je osvojio najviše medalja na Olimpijadi?", "options": ["Nenad Milijaš", "Novak Đoković", "Aleksandar Kolarov", "Dušan Tadić"], "answer": "Novak Đoković"},
    {"question": "Ko je bio prvi vladar dinastije Karađorđević?", "options": ["Karađorđe Petrović", "Miloš Obrenović", "Petar II Petrović Njegoš", "Aleksandar Karađorđević"], "answer": "Karađorđe Petrović"},
    {"question": "Koji je najpoznatiji srpski pisac u svetu?", "options": ["Ivo Andrić", "Miloš Crnjanski", "Danilo Kiš", "Branislav Nušić"], "answer": "Ivo Andrić"},
    {"question": "Koji je najlepši grad u Srbiji?", "options": ["Beograd", "Novi Sad", "Niš", "Kragujevac"], "answer": "Beograd"},
    {"question": "Koji je najveći grad u Jugoslaviji?", "options": ["Zagreb", "Beograd", "Sarajevo", "Podgorica"], "answer": "Beograd"},
    {"question": "Koji je najpoznatiji srpski jelo?", "options": ["Sarma", "Pasta", "Pizza", "Sushi"], "answer": "Sarma"},
    {"question": "Ko je otkrio prvi telefon?", "options": ["Nikola Tesla", "Thomas Edison", "Alexander Graham Bell", "Mihajlo Pupin"], "answer": "Alexander Graham Bell"},
    {"question": "Koji je najlepši srpski park?", "options": ["Kalemegdan", "Tasmajdan", "Ada Ciganlija", "Parcović"], "answer": "Kalemegdan"},
]

# Variable to store the current question index
current_question = 0
randomized_questions = []
quiz_channel_id = None
quiz_active = False
welcomer_channel_id = None
inactivity_task = None

# Command to setup the quiz channel
@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup_quiz(ctx):
    global quiz_channel_id
    quiz_channel_id = ctx.channel.id
    embed = discord.Embed(title="Kviz Postavljen", description=f"Kviz je postavljen u kanalu: {ctx.channel.name}", color=discord.Color.green())
    await ctx.send(embed=embed)

# Command to start the quiz
@bot.command(name="zapocni")
async def start_quiz(ctx):
    global quiz_active, current_question, randomized_questions, inactivity_task
    if ctx.channel.id != quiz_channel_id:
        embed = discord.Embed(title="Greška", description="Kviz možete započeti samo u postavljenom kanalu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    quiz_active = True
    current_question = 0
    randomized_questions = random.sample(quiz_data, len(quiz_data))
    
    notes_message = (
        "Kviz počinje! Imate 2 šanse da odgovorite tačno na svako pitanje.\n"
        "Imate 2 minuta da odgovorite na pitanje!\n"
        "Imate opciju !preskoci da preskočite pitanje."
    )
    embed = discord.Embed(title="Početak Kviza", description=notes_message, color=discord.Color.green())
    notes_msg = await ctx.send(embed=embed)
    await asyncio.sleep(10)  # Wait for 10 seconds before deleting the notes
    await notes_msg.delete()
    
    if inactivity_task:
        inactivity_task.cancel()
    inactivity_task = bot.loop.create_task(inactivity_timer(ctx))
    
    await ask_question(ctx)

# Function to ask the next question
async def ask_question(ctx):
    global current_question, quiz_active, inactivity_task

    if not quiz_active or current_question >= len(randomized_questions):
        return

    # Get the current question
    question_data = randomized_questions[current_question]
    question_text = question_data["question"]
    options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question_data["options"])])

    # Send the question and options
    embed = discord.Embed(title="Pitanje", description=f"{question_text}\n\nOpcije:\n{options_text}", color=discord.Color.green())
    await ctx.send(embed=embed)

    # Wait for 2 minutes for an answer
    attempts = 0
    answered = False
    while attempts < 2 and not answered:
        try:
            msg = await bot.wait_for('message', timeout=120.0, check=lambda message: message.channel.id == quiz_channel_id)
            if not quiz_active:
                return
            if msg.content.isdigit():
                option = int(msg.content)
                if 1 <= option <= len(question_data["options"]):
                    if await check_answer(ctx, option):
                        answered = True
                    else:
                        attempts += 1
                        if attempts < 2 and quiz_active:
                            embed = discord.Embed(title="Netačno", description="Netačno. Pokušajte ponovo.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Greška", description="Pogrešan unos.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Greška", description="Pogrešan unos.", color=discord.Color.red())
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            if quiz_active:
                embed = discord.Embed(title="Vreme je isteklo", description="Vreme je isteklo! Prelazimo na sledeće pitanje.", color=discord.Color.red())
                await ctx.send(embed=embed)
            break

    if quiz_active and not answered:
        current_question += 1
        if current_question < len(randomized_questions):
            await ask_question(ctx)
        else:
            await finish_quiz(ctx)

# Function to check the answer
async def check_answer(ctx, option):
    global current_question, quiz_active, inactivity_task

    if not quiz_active:
        return False

    # Get the current question
    question_data = randomized_questions[current_question]

    # Check if the answer is correct
    if question_data["options"][option - 1] == question_data["answer"]:
        embed = discord.Embed(title="Tačno", description="Tačno!", color=discord.Color.green())
        await ctx.send(embed=embed)
        current_question += 1

        # Check if there are more questions
        if current_question < len(randomized_questions):
            await ask_question(ctx)
        else:
            await finish_quiz(ctx)
        return True
    return False

# Command to skip the current question
@bot.command(name="preskoci")
async def skip_question(ctx):
    global quiz_active, current_question, inactivity_task
    if ctx.channel.id != quiz_channel_id:
        embed = discord.Embed(title="Greška", description="Kviz možete igrati samo u postavljenom kanalu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if not quiz_active:
        return

    current_question += 1
    embed = discord.Embed(title="Preskočeno", description="Preskačemo pitanje.", color=discord.Color.green())
    await ctx.send(embed=embed)
    if current_question < len(randomized_questions):
        await ask_question(ctx)
    else:
        await finish_quiz(ctx)

# Command to end the quiz
@bot.command(name="zavrsi")
async def end_quiz(ctx):
    global quiz_active, inactivity_task
    if ctx.channel.id != quiz_channel_id:
        embed = discord.Embed(title="Greška", description="Kviz možete završiti samo u postavljenom kanalu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    await finish_quiz(ctx)

# Function to finish the quiz
async def finish_quiz(ctx):
    global quiz_active, current_question, inactivity_task
    quiz_active = False
    current_question = 0
    embed = discord.Embed(title="Kraj Kviza", description="Kviz je završen.", color=discord.Color.green())
    await ctx.send(embed=embed)
    await clear_quiz_messages(ctx)
    if inactivity_task:
        inactivity_task.cancel()

# Function to clear quiz messages
async def clear_quiz_messages(ctx):
    await ctx.send("Brisanje poruka...")
    async for message in ctx.channel.history(limit=100):
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass
    await quiz_commands(ctx)

# Command to display all quiz commands
@bot.command(name="komande_kviz")
async def quiz_commands(ctx):
    commands_text = (
        "Komande za kviz:\n"
        "!setup - Postavite kanal za kviz\n"
        "!zapocni - Započnite kviz\n"
        "Odgovorite na pitanje tako što ćete uneti broj opcije\n"
        "!preskoci - Preskočite trenutno pitanje\n"
        "!zavrsi - Završite kviz\n"
    )
    embed = discord.Embed(title="Komande za Kviz", description=commands_text, color=discord.Color.green())
    await ctx.send(embed=embed)

# Command to display all bot commands
@bot.command(name="komande_bota")
async def bot_commands(ctx):
    commands_text = (
        "Komande za bota:\n"
        "!setup - Postavite kanal za kviz (samo administratori)\n"
        "!zapocni - Započnite kviz\n"
        "!preskoci - Preskočite trenutno pitanje\n"
        "!zavrsi - Završite kviz\n"
        "!socials - Prikaz društvenih mreža\n"
        "!deki - Prikaz poruke 'deki kraljina'\n"
        "!setup_welcomer - Postavite kanal za dobrodošlicu (samo administratori)\n"
    )
    embed = discord.Embed(title="Komande za Bota", description=commands_text, color=discord.Color.green())
    await ctx.send(embed=embed)
# Command to say "Hana"
@bot.command(name="Hana")
async def deki(ctx):
    embed = discord.Embed(title="Hana", description="Hana cold", color=discord.Color.green())
    await ctx.send(embed=embed)
# Command to say "deki kraljina"
@bot.command(name="Deki")
async def deki(ctx):
    embed = discord.Embed(title="Deki", description="Deki kraljina", color=discord.Color.green())
    await ctx.send(embed=embed)
# Command to say "Foxara"
@bot.command(name="Foxara")
async def deki(ctx):
    embed = discord.Embed(title="Foxara", description="Foxara npc", color=discord.Color.green())
    await ctx.send(embed=embed)
# Command to setup the welcomer channel
@bot.command(name="setup_welcomer")
@commands.has_permissions(administrator=True)
async def setup_welcomer(ctx):
    global welcomer_channel_id
    welcomer_channel_id = ctx.channel.id
    await ctx.send(f"Welcomer je postavljen u kanalu: {ctx.channel.name}")

# Command to display social links
@bot.command(name="socials")
async def socials(ctx):
    embed_foxara = discord.Embed(title="Foxara", description="## Linkovi : https://linktr.ee/foxara", color=discord.Color.green())
    await ctx.send(embed=embed_foxara)
    
    embed_max471 = discord.Embed(title="Max471", description="## Linkovi : https://linktr.ee/max471", color=discord.Color.green())
    await ctx.send(embed=embed_max471)

# Event to welcome new members
@bot.event
async def on_member_join(member):
    if welcomer_channel_id is not None:
        channel = bot.get_channel(welcomer_channel_id)
        role = discord.Object(id=1194014169159180338)
        await member.add_roles(role)
        await channel.send(f"Dobrodošao na Lotus community, {member.mention}!")

# Function to start the inactivity timer
def start_inactivity_timer(ctx):
    global inactivity_task
    if inactivity_task:
        inactivity_task.cancel()
    inactivity_task = bot.loop.create_task(inactivity_timer(ctx))

# Function to handle inactivity
async def inactivity_timer(ctx):
    await asyncio.sleep(180)  # Wait for 3 minutes
    if quiz_active:
        embed = discord.Embed(title="Kviz Zavrsen", description="Kviz se zavrsio posto niko nije odgovrio.", color=discord.Color.red())
        await ctx.send(embed=embed)
        await finish_quiz(ctx)
    else:
        await clear_quiz_messages(ctx)

# Run the bot
bot.run(TOKEN)