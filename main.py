from opensea import OpenseaAPI
import discord
from discord.ext import commands, tasks
import asyncio
import json
import time

SLUG = "azuki"

bot = commands.Bot(command_prefix='.')

api = OpenseaAPI(apikey='')



#print('NFT Collection: ',result['collection']['name'])

#print('IMG URL: ',result['collection']['image_url'])

    
    



@bot.event
async def on_ready():

    print(f'{bot.user} has connected to Discord')

'''@bot.command()
async def nft(ctx):
    embed = discord.Embed(title=result['collection']['name'], description='desc', color=0x00ff00)
    embed.set_image(url=result['collection']['image_url'])
    await ctx.channel.send(embed=embed)'''

@tasks.loop(minutes=5)
async def get_results(ctx):

    with open('data.json') as w:
        json_data = json.loads(w.read())

    global result 
    result = api.collection(collection_slug=SLUG)

    category_id = json_data['category']
    daily_id = json_data['daily']
    channel_floor_price_id = json_data['floor']
    channel_sales_id = json_data['sales']
    channel_24havg_id = json_data['avg']
    channel_24hourvol_id = json_data['volume']

    w.close()


    floor_price = result['collection']['stats']['floor_price']
    daily_sales = int(result['collection']['stats']['one_day_sales'])
    daily_avg_price = result['collection']['stats']['one_day_average_price']
    daily_volume = result['collection']['stats']['one_day_volume']
    name = result['collection']['name']

    try:
        floor_price = result['collection']['stats']['floor_price']
        daily_sales = int(result['collection']['stats']['one_day_sales'])
        daily_avg_price = result['collection']['stats']['one_day_average_price']
        daily_volume = result['collection']['stats']['one_day_volume']
        name = result['collection']['name']

        await discord.utils.get(ctx.guild.channels, id=daily_id).edit(name='Daily')
        await discord.utils.get(ctx.guild.channels, id=category_id).edit(name=f'{name} Statistics')
        await discord.utils.get(ctx.guild.channels, id=channel_floor_price_id).edit(name=f'Floor Price: {floor_price:.2f} ETH')
        await discord.utils.get(ctx.guild.channels, id=channel_sales_id).edit(name=f'Sales: {daily_sales}')
        await discord.utils.get(ctx.guild.channels, id=channel_24havg_id).edit(name=f'avg Price: {daily_avg_price:.2f} ETH')
        await discord.utils.get(ctx.guild.channels, id=channel_24hourvol_id).edit(name=f'Volume: {daily_volume:.2f} ETH')

        
    except:
        print('An Error occured')
    '''
    elif  rotation == 2:
        try:
            floor_price = result['collection']['stats']['floor_price']
            weekly_sales = int(result['collection']['stats']['seven_day_sales'])
            weekly_avg_price = result['collection']['stats']['seven_day_average_price']
            weekly_volume = result['collection']['stats']['seven_day_volume']
            name = result['collection']['name']

            await discord.utils.get(ctx.guild.channels, id=daily_id).edit(name='Weekly')
            await discord.utils.get(ctx.guild.channels, id=category_id).edit(name=f'{name} Statistics')
            await discord.utils.get(ctx.guild.channels, id=channel_floor_price_id).edit(name=f'Floor Price: {floor_price:.2f} ETH')
            await discord.utils.get(ctx.guild.channels, id=channel_sales_id).edit(name=f'Sales: {weekly_sales}')
            await discord.utils.get(ctx.guild.channels, id=channel_24havg_id).edit(name=f'avg Price: {weekly_avg_price:.2f} ETH')
            await discord.utils.get(ctx.guild.channels, id=channel_24hourvol_id).edit(name=f'Volume: {weekly_volume:.2f} ETH')

            rotation+=1
        except:
            print(f'An error occured on rotation {rotation}')
 
    elif  rotation == 3:
        try:
            floor_price = result['collection']['stats']['floor_price']
            monthly_sales = int(result['collection']['stats']['thirty_day_sales'])
            monthly_avg_price = result['collection']['stats']['thirty_day_average_price']
            monthly_volume = result['collection']['stats']['thirty_day_volume']
            name = result['collection']['name']

            await discord.utils.get(ctx.guild.channels, id=daily_id).edit(name='Monthly')
            await discord.utils.get(ctx.guild.channels, id=category_id).edit(name=f'{name} Statistics')
            await discord.utils.get(ctx.guild.channels, id=channel_floor_price_id).edit(name=f'Floor Price: {floor_price:.2f} ETH')
            await discord.utils.get(ctx.guild.channels, id=channel_sales_id).edit(name=f'Sales: {monthly_sales}')
            await discord.utils.get(ctx.guild.channels, id=channel_24havg_id).edit(name=f'avg Price: {monthly_avg_price:.2f} ETH')
            await discord.utils.get(ctx.guild.channels, id=channel_24hourvol_id).edit(name=f'Volume: {monthly_volume:.2f} ETH')

            rotation=1
        except:
            print(f'An error occured on rotation {rotation}')
    '''

@bot.command()
async def setup(ctx):
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
    }
    await ctx.guild.create_category("Nft Stuff", overwrites=overwrites)
    category = discord.utils.get(ctx.guild.categories, name="Nft Stuff")
    await ctx.guild.create_voice_channel("Daily", category=category)
    await ctx.guild.create_voice_channel("Floor Price", category=category)
    await ctx.guild.create_voice_channel("Sales Today", category=category)
    await ctx.guild.create_voice_channel("24h avg price", category=category)
    await ctx.guild.create_voice_channel("24h volume", category=category)

    category_id = discord.utils.get(ctx.guild.channels, name='Nft Stuff').id
    daily_id = discord.utils.get(ctx.guild.channels, name='Daily').id
    channel_floor_price_id = discord.utils.get(ctx.guild.channels, name='Floor Price').id
    channel_sales_id = discord.utils.get(ctx.guild.channels, name='Sales Today').id
    channel_24havg_id = discord.utils.get(ctx.guild.channels, name='24h avg price').id
    channel_24hourvol_id = discord.utils.get(ctx.guild.channels, name='24h volume').id

    json_data = {
        'category' : category_id,
        'daily': daily_id,
        'floor': channel_floor_price_id,
        'sales': channel_sales_id,
        'avg': channel_24havg_id,
        'volume': channel_24hourvol_id
    }

    with open("data.json", 'w') as w:
        json.dump(json_data, w)
    
    w.close()

    get_results.start(ctx)


@bot.command()
async def delete(ctx):
    with open('data.json') as w:
        json_data = json.loads(w.read())

    for key in json_data:
        await discord.utils.get(ctx.guild.channels, id=json_data[key]).delete()
    

    w.close()

    get_results.stop()

bot.run('OTM3NDg4OTE2ODcxNzc4MzA0.Yfcelw.Dfuv78twgFRa1mW10ZeapTxXJ2Q')

