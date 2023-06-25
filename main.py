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
intent = discord.Intents.all()
client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)
out_msg = None
log = []
timestamp = datetime.datetime.now().strftime("%Y%m%d")
isCreating = False
chara = Literal['Flandre Scarlet', 'Cirno', 'Sakuya Izayoi', 'Reimu Hakurei']
load_dotenv()

@client.event
async def on_ready():
  global tree
  await tree.sync()
  print("already!")

@tree.command(name="img-normal",description="東方キャラの画像を出力します。")
async def img_command(interaction: discord.Interaction, character: chara = 'Flandre Scarlet'):
  await interaction.response.defer()
  try:
    global out_msg
    task = asyncio.create_task(img_command_main(interaction, character))
    await task
  except:
    await interaction.followup.send("ERROR! : An internal error has occurred. Please pass this information on to the author.")
  
async def img_command_main(interaction, character):
    global out_msg
    out_msg = await interaction.followup.send('Bot is creating image...')
    img_get_task = asyncio.create_task(get_img(interaction, False, character))
    res = await img_get_task
    if(res != 0):
      await interaction.followup.send(f"ERROR : {res}")


@tree.command(name="img-nsfw",description="東方キャラのNSFW画像を出力します。")
async def nsfw_img_command(interaction: discord.Interaction, character : chara = 'Flandre Scarlet'):
  global out_msg
  await interaction.response.defer()
  try:
    if interaction.channel_id == 1089087674066940027 or interaction.channel.is_nsfw == True or interaction.channel_id == 1118874768423264368 or interaction.channel_id == 1122044968605859891:
      out_msg = await interaction.followup.send("Bot is creating **NSFW** image...")
      img_get_task = asyncio.create_task(get_img(interaction, True, character))
      res = await img_get_task
      if(res != 0):
        await interaction.followup.send(f"ERROR : {res}")
    else:
      await interaction.followup.send("ERROR! : CAN'T CREATE **NSFW** IMAGE IN NOT R18 SPACE!", ephemeral=True)
  except:
    await interaction.followup.send("ERROR! : An internal error has occurred. Please pass this information on to the author.")

@tree.command(name="logs", description="このチャンネルのimg-normal, img-nsfwコマンドログを表示します。")
async def send_log(interaction: discord.Interaction):
  global timestamp
  await interaction.response.defer()
  try:
    try:
      with open(str(timestamp[:8] + ".log"), "r") as file:
        text = file.read()
    except :
      await interaction.followup.send("Nothing here :)")
      return
    logs = text.split("\n")
    Notsend = True
    data = {}
    for JsonStr in logs:
      print(JsonStr)
      if JsonStr:
        data = json.loads(JsonStr)
      if data["channel_id"] == str(interaction.channel_id):
        await interaction.channel.send(JsonStr)
        Notsend = False
    await interaction.followup.send("(END)")
    if Notsend:
      await interaction.followup.send("Nothing here :)")
  except:
    await interaction.followup.send("ERROR! : An internal error has occurred. Line 88 Please pass this information on to the author.")

  
@tree.command(name="shutdown", description="For debug(Only author can use this command)")
async def shutdown(interaction: discord.Interaction):
  try:
    if interaction.user.id == 1059732895473868820:
      await interaction.response.send_message("Bot is Shutting down....", ephemeral=True)
      await client.close()    
  except:
    await interaction.response.send_message("ERROR! : An internal error has occurred. Please pass this information on to the author.")

async def get_img(interaction : discord.Interaction, nsfw : bool, character : chara):
  try:
    global out_msg  
    global log
    global timestamp
    try:
      if nsfw == True:
        params = {
          "restore_faces": False,
          "face_restorer": "CodeFormer",
          "codeformer_weight": 0.5,
          "sd_model": "yden-v30.safetensors",
          "prompt": "nsfw, pussy, tits",
          "negative_prompt": "lbad anatomy, long_neck, long_body, longbody, deformed mutated disfigured, missing arms, extra_arms, mutated hands, extra_legs, bad hands, poorly_drawn_hands, malformed_hands, missing_limb, floating_limbs, disconnected_limbs, extra_fingers, bad fingers, liquid fingers, poorly drawn fingers, missing fingers, extra digit, fewer digits, ugly face, deformed eyes, partial face, partial head, bad face, inaccurate limb, cropped, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh",
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
      else:
        params = {
          "restore_faces": False,
          "face_restorer": "CodeFormer",
          "codeformer_weight": 0.5,
          "sd_model": "yden-v30.safetensors",
          "prompt": "anime character, japanese, high quolity, 8k, very cute girl, simple background",
          "negative_prompt": "lbad anatomy, long_neck, long_body, longbody, deformed mutated disfigured, missing arms, extra_arms, mutated hands, extra_legs, bad hands, poorly_drawn_hands, malformed_hands, missing_limb, floating_limbs, disconnected_limbs, extra_fingers, bad fingers, liquid fingers, poorly drawn fingers, missing fingers, extra digit, fewer digits, ugly face, deformed eyes, partial face, partial head, bad face, inaccurate limb, cropped, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh",
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
      await client.get_channel(interaction.channel_id).typing()
      params["prompt"] += str(', ' + character)
      r = requests.post(url="http://127.0.0.1:7860/sdapi/v1/txt2img", json=params).json()
      info_json = r["info"]
      with open("./test.json", "w") as file:
        file.write(info_json)
      with open("./test.json") as file:
        info = json.load(file)
      timestamp = info["job_timestamp"]
      img_bs64 = str(r['images'])
      img_binary = base64.b64decode(img_bs64)
      jpg=np.frombuffer(img_binary,dtype=np.uint8)
      img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
      cv2.imwrite('./img.png',img)
      if nsfw == True:
        outfile = discord.File('./img.png', str(timestamp + ".png"), spoiler=True)
      else:
        outfile = discord.File('./img.png', str(timestamp + ".png"), spoiler=False)
      await client.get_channel(interaction.channel_id).send('OutPut Image', file=outfile)
      print(f'Create Image : {{"nsfw" : "{nsfw}", "timestamp": "{timestamp}", "guild_id" : "{interaction.guild_id}", "channel_id" : "{interaction.channel_id}", "user.name":{interaction.user.name}}}')
      log = str(f'{{"nsfw" : "{nsfw}", "timestamp": "{timestamp}", "guild_id" : "{interaction.guild_id}", "channel_id" : "{interaction.channel_id}", "user.name": "{interaction.user.name}"}}')
      with open(str(timestamp[:8] + ".log") , "a") as file:
        file.write(log + "\n")
        file.close()
      return 0
    except ConnectionError as e:
      return e
    except FileNotFoundError as e:
      await client.get_channel(interaction.channel_id).send('ERROR : FileNotFoundError : ')
      await client.get_channel(interaction.channel_id).send(e)
  except:
    await interaction.followup.send("ERROR! : An internal error has occurred. Please pass this information on to the author.")
client.run(os.environ["TOKEN"])