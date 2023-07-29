from typing import Literal
import requests
import discord
from discord import app_commands
import base64
import cv2
import json
import numpy as np
import asyncio
from dotenv import load_dotenv
import os
import datetime
import time
import math
import aiohttp
intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)
out_msg = None
nsfw_channels = [1089087674066940027, 1118874768423264368, 1122044968605859891, 1129201326660780155, 1133399681649623091, 1133398633279127623]
log = []
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
isCreating = False
chara = Literal['Flandre Scarlet', 'Cirno', 'Sakuya Izayoi', 'Reimu Hakurei']
model = Literal['yden_v30.ckpt', 'wd-v1-3-full.safetensors']
user_timeouts = {}
paid_users = {}
load_dotenv()
loop = asyncio.get_event_loop()

@client.event
async def on_ready():
  global user_timeouts
  global tree
  global paid_users
  await tree.sync()
  print("already!")
  with open("paid_user.json") as f:
    paid_users = json.load(f)['users']
  member_count = 0
  for guild in client.guilds:
    for member in guild.members:
      member_count += 1
      if str(member.id) in paid_users:
        user_timeouts[str(member.id)] = -1
      else:
        user_timeouts[str(member.id)] = int(datetime.datetime.now().strftime('%H%M%S'))
  print(f"{member_count=}")
@client.event
async def on_member_join(member):
  global user_timeouts
  if str(member.id) not in user_timeouts.items():
    user_timeouts[str(member.id)] = int(datetime.datetime.now().strftime('%H%M%S'))

@tree.command(name="img-normal",description="東方キャラの画像を出力します。")
async def img_command(interaction: discord.Interaction, character: chara = 'Flandre Scarlet', model_name : model = 'yden_v30'):
    global user_timeouts
    global loop

    try:
      if user_timeouts[str(interaction.user.id)] is None:
        return
    except KeyError:
      embed = discord.Embed(title=':warning: ERROR', description='Botの起動中もしくはKeyが追加されていません。もしBotの起動中でない場合は、 @0266stにDMもしくはサポートサーバでバグ報告を行なってください。', color=0xFFFF00)
      interaction.response.send_message(embed=embed)
      return
    
    print(str(str(user_timeouts[str(interaction.user.id)]) + ' >= ' + str(datetime.datetime.now().strftime('%H%M%S'))))
    
    if user_timeouts[str(interaction.user.id)] >= int(datetime.datetime.now().strftime('%H%M%S')) and user_timeouts[str(interaction.user.id)] >= 0:
      msg_embed = discord.Embed(title=":warning: ERROR", description="You can't create image. please retry at 10 seconds after or upgrade your plan.", color=0xFF0000)
      msg_embed.set_footer(text='- フランドールスカーレット写真Bot')
      await interaction.response.send_message(embed=msg_embed, ephemeral=True)
      return
    
    await interaction.response.defer() 
    
    msg_embed = discord.Embed(title='Bot is creating image...', description='Waiting in the queue.... please wait', color= 0x0000ff)
    msg_embed.set_footer(text=str('Request from ' + str(interaction.user.name)))
    out_msg = await interaction.followup.send(embed=msg_embed)
    await interaction.channel.typing()
    await get_img(interaction, False, character, model_name, out_msg)


@tree.command(name="img-nsfw",description="東方キャラのNSFW画像を出力します。")
async def nsfw_img_command(interaction: discord.Interaction, character : chara = 'Flandre Scarlet', model_name : model = 'yden_v30'):
    
    global user_timeouts
    try:
      if user_timeouts[str(interaction.user.id)] is None:
        return
    except KeyError:
      embed = discord.Embed(title=':warning: ERROR', description='Botの起動中もしくはKeyが追加されていません。もしBotの起動中でない場合は、 @0266stにDMもしくはサポートサーバでバグ報告を行なってください。', color=0xFFFF00)
      interaction.response.send_message(embed=embed)
      return
    
    print(str(user_timeouts[str(interaction.user.id)]) + ' >= ' + str(datetime.datetime.now().strftime('%H%M%S')))
    
    if user_timeouts[str(interaction.user.id)] >= int(datetime.datetime.now().strftime('%H%M%S')) and user_timeouts[str(interaction.user.id)] >= 0:
      msg_embed = discord.Embed(title=":warning: ERROR", description="You can't create image. please retry at 10 seconds after or upgrade your plan.", color=0xFF0000)
      msg_embed.set_footer(text='Request from ' + interaction.user.name)
      await interaction.response.send_message(embed=msg_embed, ephemeral=True)
      return
    
    await interaction.response.defer()
    
    try:
      if interaction.channel_id in nsfw_channels:
        msg_embed = discord.Embed(title='Bot is creating **NSFW** image...', description='Waiting in the queue... please wait', color= 0x0000ff)
        msg_embed.set_footer(text=str('Request from ' + interaction.user.name))
        out_msg = await interaction.followup.send(embed=msg_embed)
        await get_img(interaction, True, character, model_name, out_msg)
      
      else:
        embed = discord.Embed(title=':warning: ERROR', description="CAN'T CREATE **NSFW** IMAGE IN NOT R18 SPACE!", color=0xff0000)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    except:
      await interaction.followup.send("ERROR! : An internal error has occurred. Line 80. Please pass this information on to the author.")


@tree.command(name="logs", description="このチャンネルのimg-normal, img-nsfwコマンドログを表示します。")
async def send_log(interaction: discord.Interaction):
  global timestamp
  
  await interaction.response.defer()
  
  try:
  
    try:
      print(timestamp[:8])
      with open(str("./logs/" + timestamp[:8] + ".log"), "r") as file:
        text = file.read()
        print(text)
  
    except :
      await interaction.followup.send("Error : Nothing here :)")
      return
    logs = text.split("\n")
    Notsend = True
    data = {}
  
    for JsonStr in logs:
      print(JsonStr)
  
      if not JsonStr == "":
        data = json.loads(JsonStr)
  
        if data["channel_id"] == str(interaction.channel_id):
          await interaction.channel.send(JsonStr)
          Notsend = False
    
    await interaction.followup.send("(END)")
    
    if Notsend:
      await interaction.followup.send("Nothing here :)")
  
  except json.JSONDecodeError as e:
    await interaction.followup.send("ERROR! : An internal error has occurred. Line 88 Please pass this information on to the author. Error : " + e.msg)

  
@tree.command(name="shutdown", description="For debug(Only author can use this command)")
async def shutdown(interaction: discord.Interaction):
  try:
    if interaction.user.id == 1059732895473868820:
      await interaction.response.send_message("Bot is Shutting down....", ephemeral=True)
      await client.close()
    else:
      await interaction.response.send_message("You can't shutting down this bot : You don't have permission to use this command.", ephemeral=True)
  
  except:
    await interaction.response.send_message("ERROR! : An internal error has occurred. Please pass this information on to the author.")


async def get_img(interaction : discord.Interaction, nsfw : bool, character : chara, model_name : str, out_msg : discord.WebhookMessage):
      try:
        global log
        global timestamp
        global user_timeouts
        await out_msg.channel.typing()
        if nsfw == True:
          params = {
            "restore_faces": False,
            "face_restorer": "CodeFormer",
            "codeformer_weight": 0.5,
            "prompt": "erotic, nsfw, pussy, tits, 8k, very cute girl",
            "negative_prompt": "horror, icon, lbad anatomy, long_neck, long_body, longbody, deformed mutated disfigured, missing arms, extra_arms, mutated hands, extra_legs, bad hands, poorly_drawn_hands, malformed_hands, missing_limb, floating_limbs, disconnected_limbs, extra_fingers, bad fingers, liquid fingers, poorly drawn fingers, missing fingers, extra digit, fewer digits, ugly face, deformed eyes, partial face, partial head, bad face, inaccurate limb, cropped, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh",
            "seed": -1,
            "seed_enable_extras": False,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": 0,
            "seed_resize_from_w": 0,
            "sampler_name": "Euler a",
            "steps": 30,
            "cfg_scale": 7.5,
            "denoising_strength": 0.35,
            "batch_count": 1,
            "batch_size": 1,
            "base_size": 512,
            "max_size": 768,
            "tiling": False,
            "highres_fix": 'enable_hr',
            "firstphase_height": 512,
            "firstphase_width": 512,
            "upscaler_name": "None",
            "filter_nsfw": False,
            "include_grid": False,
            "sample_path": "outputs/krita-out",
            "orig_width": 512,
            "orig_height": 512
          }
        
        else:
          params = {
            "restore_faces": False,
            "face_restorer": "CodeFormer",
            "codeformer_weight": 0.5,
            "prompt": "very cute girl, one girl, cowboy shots,  super fine illustration, (color body), simple white background",
            "negative_prompt": "horror, nsfw, icon, lbad anatomy, long_neck, long_body, longbody, deformed mutated disfigured, missing arms, extra_arms, mutated hands, extra_legs, bad hands, poorly_drawn_hands, malformed_hands, missing_limb, floating_limbs, disconnected_limbs, extra_fingers, bad fingers, liquid fingers, poorly drawn fingers, missing fingers, extra digit, fewer digits, ugly face, deformed eyes, partial face, partial head, bad face, inaccurate limb, cropped, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh",
            "seed": -1,
            "seed_enable_extras": False,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": 0,
            "seed_resize_from_w": 0,
            "sampler_name": "Euler a",
            "steps": 30,
            "cfg_scale": 7.5,
            "denoising_strength": 0.35,
            "batch_count": 1,
            "batch_size": 1,
            "base_size": 512,
            "max_size": 768,
            "tiling": False,
            "highres_fix": False,
            "firstphase_height": 512,
            "firstphase_width": 512,
            "upscaler_name": "None",
            "filter_nsfw": False,
            "include_grid": False,
            "sample_path": "outputs/krita-out",
            "orig_width": 512,
            "orig_height": 512
          }
        
        params["prompt"] += str(', ' + character)
        
        r = await post_data('http://127.0.0.1:7860/sdapi/v1/txt2img', params)
        
        if r['ERROR'] is True:
          msg_embed = discord.Embed(':warning: An internal Error has Occureted.', description='Failed to request Stable Diffusion WebUI API. Please pass to the author.', color=0xFF0000)
          out_msg.edit(embed=msg_embed)
          return

        info_json = r["info"]
        with open("./test.json", "w") as file:
          file.write(info_json)
        
        with open("./test.json") as file:
          info = json.load(file)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        prompt = info["prompt"]
        img_bs64 = str(r['images'])
        img_binary = base64.b64decode(img_bs64)
        jpg=np.frombuffer(img_binary,dtype=np.uint8)
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        cv2.imwrite(str('./log_images/' + timestamp + '.png'),img)
        
        with open(str("./log_images/" + timestamp + ".png"), "br") as f:
          embed = discord.Embed(title='Image Task Complete.', description='', color=0x00ffff)
          if nsfw:
            embed.add_field(name='This is nsfw image', value='')
          outfile = discord.File(fp=f, filename="image.png", spoiler=False)
          embed.set_image(url=f'attachment://image.png')
          embed.set_footer(text=f'Request from {interaction.user.name}')
        await out_msg.edit(attachments=[outfile], embed=embed)
        print(f'Create Image : {{"nsfw" : "{nsfw}", "timestamp": "{timestamp}", "guild_id" : "{interaction.guild_id}", "channel_id" : "{interaction.channel_id}", "user.id":{interaction.user.id}, "user.name":{interaction.user.name}}}')
        log = str(f'{{"nsfw" : "{nsfw}", "timestamp": "{timestamp}", "guild_id" : "{interaction.guild_id}", "channel_id" : "{interaction.channel_id}", "user.id": "{interaction.user.id}"}}')
        with open(str("./logs/" + timestamp[:8] + ".log") , "a") as file:
          file.write(log + "\n")
          file.close()
        if user_timeouts[str(interaction.user.id)] != -1:
          user_timeouts[str(interaction.user.id)] = int(datetime.datetime.now().strftime('%H%M%S')) + 10
      except ConnectionError as e:
        return e

def ispaidUser(target):
  global paid_users
  if target in paid_users:
    return True
  return False

async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
      try:
        async with session.post(url, json=data) as response:
          return_dict = await response.json()
          return_dict['ERROR'] = False
          return return_dict
      except:
        return_dict = []
        return_dict['ERROR'] = True
        return return_dict

client.run(os.environ["TOKEN"])