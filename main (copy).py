from fortnitepy import party
import nextcord
from nextcord.application_command import SlashOption
from nextcord.ext import commands
import requests
import aiohttp
import json
import os
from nextcord.ui import View, Button
import asyncio
from nextcord import Interaction, ButtonStyle, Embed
import copy

serverid = 1249026688470225037
footertext = "Ramirez"  # Footer text to be used in all embeds
os.system("pip install git+https://github.com/notxivyy/fortnitepy")
import fortnitepy
from fortnitepy.ext import commands as FortniteCommands

os.system('cls' if os.name == 'nt' else 'clear')
ac = nextcord.Game('sumtingshit')
intents = nextcord.Intents.all()
bot = commands.Bot(activity=ac, command_prefix="!", intents=intents)


async def get_avatar(auths):
  print(str(auths))
  url = 'https://avatar-service-prod.identity.live.on.epicgames.com/v1/avatar/fortnite/ids?accountIds=' + auths.get(
      'account_id')
  headers = {
      "Authorization": "Bearer " + await Epic.authsToBearer(auths),
      "Content-Type": "application/json"
  }
  responce = await Request.get(url, headers=headers)
  #print(str(headers))
  #print(str(responce))
  try:
    return (await
            Cosmetics.find_async(
                responce[0]['avatarId'].removeprefix("ATHENACHARACTER:"),
                type='id'))['images']['icon']
  except:
    return "https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png"


@bot.event
async def on_ready():
  print(f"Bot running as {bot.user}")


"""
Classes
"""
cosmetics_data = []
Banners = []


async def initProfileForMM(cient):
  url = f'https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{cient.user.id}/client/QueryProfile?profileId=athena&rvn=-1'
  headers = {
      "Authorization": cient.http.get_auth('FORTNITE_ACCESS_TOKEN'),
      "Content-Type": 'application/json'
  }

  response = await Request.post(url, headers=headers, json={})

  resp1 = await Request.post(url.replace('=athena', '=common_core'),
                             headers=headers,
                             json={})

  return response, resp1


class Cosmetics:

  @staticmethod
  def get_cosmetics():
    global cosmetics_data
    global Banners
    if len(cosmetics_data) == 0:
      cosmetics_data = requests.get(
          "https://fortnite-api.com/v2/cosmetics/br").json()['data']
    if len(Banners) == 0:
      Banners = requests.get(
          'https://fortnite-api.com/v1/banners').json()['data']
    return cosmetics_data

  @staticmethod
  def gather_skins():
    data = Cosmetics.get_cosmetics()
    skins = []
    for i in data:
      if i["type"]["value"] == "outfit":
        skins.append(i)
    return skins

  @staticmethod
  def gather_banners():
    global Banners
    data = copy.deepcopy(Banners)
    return data

  @staticmethod
  def gather_backpacks():
    data = Cosmetics.get_cosmetics()
    backpacks = []
    for i in data:
      if i["type"]["value"] == "backpack":
        backpacks.append(i)
    return backpacks

  @staticmethod
  def gather_pickaxes():
    data = Cosmetics.get_cosmetics()
    pickaxes = []
    for i in data:
      if i["type"]["value"] == "pickaxe":
        pickaxes.append(i)
    return pickaxes

  @staticmethod
  def gather_emotes():
    data = Cosmetics.get_cosmetics()
    emotes = []
    for i in data:
      if i["type"]["value"] == "emote":
        emotes.append(i)
    return emotes

  @staticmethod
  async def check_updates():
    while True:
      await asyncio.sleep(60 * 10)
      # Will Be Added Later

  @staticmethod
  def reinterpret_path(path):
    if path.startswith(
        'FortniteGame/Plugins/GameFeatures/BRCosmetics/Content'):
      path = path.replace(
          'FortniteGame/Plugins/GameFeatures/BRCosmetics/Content',
          '/BRCosmetics', 1)
    elif path.startswith('FortniteGame/Content'):
      path = path.replace('FortniteGame/Content', '/Game', 1)

    path_parts = path.split('/')

    filename = path_parts[-1]

    new_path = '/'.join(path_parts) + '.' + filename

    return new_path

  @staticmethod
  async def find_async(cosmetic_name, type='name'):
    data = Cosmetics.get_cosmetics()
    for i in data:
      if i[type].lower() == cosmetic_name.lower():
        return i
    return None

  @staticmethod
  async def banner_async(banner_id):
    global Banners
    for i in Banners:
      if i['id'] == banner_id:
        return i
    return None

  @staticmethod
  def Initiate():
    Cosmetics.get_cosmetics()
    bot.loop.create_task(Cosmetics.check_updates())
    print(
        'Successfully Created Cosmetics. Found ' +
        str(len(Cosmetics.gather_skins())) + ' Skins, ' +
        str(len(Cosmetics.gather_backpacks())) + ' Backpacks, ' +
        str(len(Cosmetics.gather_pickaxes())) + ' Pickaxes, ' +
        str(len(Cosmetics.gather_emotes())) + ' Emotes.',
        'Overall: ' + str(len(Cosmetics.get_cosmetics())))


class Vars:
  NEW_SWITCH_TOKEN = "Basic OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
  #IOSTOKEN = Vars.LAUNCHERTOKEN#IOSTOKEN = "Basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
  LAUNCHERTOKEN = "Basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="
  IOSTOKEN = NEW_SWITCH_TOKEN # idk why they disabled that client


class Epic:

  @staticmethod
  async def get_exchange(bearerToken):
    async with aiohttp.ClientSession() as session:
      async with session.get(
          url=
          "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange",
          headers={
              "Authorization": "Bearer " + bearerToken,
              'Content-Type': 'application/x-www-form-urlencoded'
          }) as request:
        data = await request.json()

    exchangeCode = data['code']
    return exchangeCode

  @staticmethod
  async def authsToBearer(auths):
    async with aiohttp.ClientSession() as session:
      async with session.post(
          url=
          "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
          headers={
              "Authorization": Vars.IOSTOKEN,
              "Content-Type": "application/x-www-form-urlencoded"
          },
          data=
          f"grant_type=device_auth&account_id={auths['account_id']}&device_id={auths['device_id']}&secret={auths['secret']}&token_type=eg1"
      ) as request:
        data = await request.json()

    bearerToken = data['access_token']
    return bearerToken

  @staticmethod
  async def get_device_code(bearer_token, account_id):
    async with aiohttp.ClientSession() as session:
      async with session.post(
          url=
          "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/"
          + account_id + "/deviceAuth",
          headers={
              "Authorization": "Bearer " + bearer_token,
              'Content-Type': 'application/json'
          }) as response:
        newResponse = await response.json()
        data = newResponse

    try:
      auths = {
          "account_id": account_id,
          "device_id": data["deviceId"],
          "secret": data["secret"]
      }
      return auths
    except KeyError:
      return None

  @staticmethod
  async def create_login(device_code):
    """Creates Login From Device Code"""

    async with aiohttp.ClientSession() as session:
      async with session.post(
          url=
          "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
          headers={
              "Authorization": Vars.NEW_SWITCH_TOKEN,
              "Content-Type": "application/x-www-form-urlencoded"
          },
          data=f"grant_type=device_code&device_code={device_code}",
          ssl=False) as request:
        if request.status != 200:
          return None
        data = await request.json()

        device_auth = await Epic.get_device_code(data["access_token"],
                                             data["account_id"])
        return {"device_auth": device_auth, "displayName": data["displayName"]}

  @staticmethod
  async def get_client_credentials_token():
    """Generates A Client Credentials Token For Auth"""
    async with aiohttp.ClientSession() as session:
      async with session.post(
          url=
          "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
          headers={
              "Authorization": Vars.NEW_SWITCH_TOKEN,
              "Content-Type": "application/x-www-form-urlencoded"
          },
          data="grant_type=client_credentials",
      ) as response:
        data = await response.json()

    return data["access_token"]

  @staticmethod
  async def create_device_authorization(access_token: str):
    """Generates A Device Authorization Code For Auth"""
    async with aiohttp.ClientSession() as session:
      async with session.post(
          url=
          "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization",
          headers={
              "Authorization": f"bearer {access_token}",
              "Content-Type": 'application/x-www-form-urlencoded'
          },
          data="prompt=login") as response:
        data = await response.json()

    return data["device_code"], data['verification_uri_complete']

  @staticmethod
  async def get_party_id(account_id, bearer_token):
    url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}"
    headers = {
        "Authorization": "Bearer " + bearer_token,
    }
    response = await Request.get(url=url, headers=headers)
    member = None
    if len(response['current']) == 0: return 122, None
    for memb in response["current"][0]["members"]:
      if memb["account_id"] == account_id:
        member = memb
        break
    return response["current"][0]["id"], member


class colors:
  default = 0
  teal = 0x1abc9c
  dark_teal = 0x11806a
  green = 0x2ecc71
  dark_green = 0x1f8b4c
  blue = 0x3498db
  dark_blue = 0x206694
  purple = 0x9b59b6
  dark_purple = 0x71368a
  magenta = 0xe91e63
  dark_magenta = 0xad1457
  gold = 0xf1c40f
  dark_gold = 0xc27c0e
  orange = 0xe67e22
  dark_orange = 0xa84300
  red = 0xe74c3c
  dark_red = 0x992d22
  lighter_grey = 0x95a5a6
  dark_grey = 0x607d8b
  light_grey = 0x979c9f
  darker_grey = 0x546e7a
  blurple = 0x7289da
  greyple = 0x99aab5


class Users:
  file_path = "Accounts.json"

  @staticmethod
  def load_users():
    if os.path.exists(Users.file_path):
      with open(Users.file_path, "r") as f:
        return json.load(f)
    return {}

  @staticmethod
  def save_users(users):
    with open(Users.file_path, "w") as f:
      json.dump(users, f, indent=4)

  @staticmethod
  def save(userid, newauth, selectedIdx):
    users = Users.load_users()
    userid = str(userid)  # Ensure the user ID is a string
    if userid not in users:
      users[userid] = {'auths': [], 'selectedIdx': 0}
    if newauth['account_id'] not in [
        auth['account_id'] for auth in users[userid]['auths']
    ]:
      users[userid]['auths'].append(newauth)
      users[userid]['selectedIdx'] = int(selectedIdx)
    else:
      for index, value in enumerate(users[userid]['auths']):
        if value['account_id'] == newauth['account_id']:
          users[userid]['auths'][index] = newauth
    Users.save_users(users)

  @staticmethod
  def set_selected(userid, selectedIdx):
    users = Users.load_users()
    userid = str(userid)  # Ensure the user ID is a string
    if userid in users:
      users[userid]['selectedIdx'] = int(selectedIdx)
      Users.save_users(users)
    else:
      raise KeyError(f"User ID {userid} not found.")

  @staticmethod
  def get(key: str, returnAuths=False):
    users = Users.load_users()
    key = str(key)  # Ensure the key is a string
    if key not in users:
      return None
    if not returnAuths:
      return users[key]['auths'][users[key]['selectedIdx']]
    return users[key]

  @staticmethod
  def delete(key):
    users = Users.load_users()
    key = str(key)  # Ensure the key is a string
    if key in users:
      del users[key]
      Users.save_users(users)
    else:
      raise KeyError(f"User ID {key} not found.")


class Request:

  @staticmethod
  async def get(url, **kwargs):
    async with aiohttp.ClientSession() as session:
      try:
        async with session.get(url, **kwargs) as response:
          try:
            return await response.json()
          except:
            return await response.text()
      except aiohttp.ClientError as e:
        return str(e)

  @staticmethod
  async def post(url, **kwargs):
    async with aiohttp.ClientSession() as session:
      try:
        async with session.post(url, **kwargs) as response:
          try:
            return await response.json()
          except:
            return await response.text()
      except aiohttp.ClientError as e:
        return str(e)

  @staticmethod
  async def patch(url, **kwargs):
    async with aiohttp.ClientSession() as session:
      try:
        async with session.patch(url, **kwargs) as response:
          try:
            return await response.json()
          except aiohttp.ContentTypeError:
            return await response.text()
      except aiohttp.ClientError as e:
        return str(e)

  @staticmethod
  async def put(url, **kwargs):
    async with aiohttp.ClientSession() as session:
      try:
        async with session.put(url, **kwargs) as response:
          try:
            return await response.json()
          except aiohttp.ContentTypeError:
            return await response.text()
      except aiohttp.ClientError as e:
        return str(e)


class Party:

  def __init__(self, discord_id, use_json=False):
    if use_json:
      data = (discord_id)
      self.account_id = data['account_id']
      self.device_id = data["device_id"]
      self.secret = data['secret']
    else:
      data = Users.get(discord_id)
      self.account_id = data['account_id']
      self.device_id = data["device_id"]
      self.secret = data['secret']
    self.party_id = None
    self.member = None
    self.rvn = None
    self.skin_id = None
    self.backpack_id = None
    self.pickaxe_id = None
    self.contrail_id = None
    self.crowns_wins = None
    self.has_crown = False
    self.progression = None
    self.backpack_styles = None
    self.skin_style = None
    self.skin_styles_chnl = None
    self.backpack_styles_chnl = None

  async def set_emote(self, emote_id):
    bearer_token = await Epic.authsToBearer({
        "account_id": self.account_id,
        "device_id": self.device_id,
        "secret": self.secret
    })
    self.party_id, self.member = await Epic.get_party_id(
        account_id=self.account_id, bearer_token=bearer_token)
    self.rvn = self.member["revision"]

    url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{self.party_id}/members/{self.account_id}/meta"
    headers = {
        "Authorization": "bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    data = {
        "delete": [],
        "revision": self.rvn,
        "update": {
            "Default:FrontendEmote_j":
            json.dumps({
                "FrontendEmote": {
                    "emoteItemDef": emote_id,
                    "emoteSection": -2
                }
            })
        }
    }
    return await Request.patch(url, headers=headers, json=data)

  async def change_level(self, level):
    bearer_token = await Epic.authsToBearer({
        "account_id": self.account_id,
        "device_id": self.device_id,
        "secret": self.secret
    })
    self.party_id, self.member = await Epic.get_party_id(
        account_id=self.account_id, bearer_token=bearer_token)
    self.rvn = self.member["revision"]

    url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{self.party_id}/members/{self.account_id}/meta"
    headers = {
        "Authorization": "bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    data = {
        "delete": [],
        "revision": self.rvn,
        "update": {
            "Default:AthenaBannerInfo_j":
            json.dumps({"AthenaBannerInfo": {
                "seasonLevel": level,
            }})
        }
    }
    return await Request.patch(url, headers=headers, json=data)

  async def change_banner(self, bannericon, bannerColor):
    bearer_token = await Epic.authsToBearer({
        "account_id": self.account_id,
        "device_id": self.device_id,
        "secret": self.secret
    })
    self.party_id, self.member = await Epic.get_party_id(
        account_id=self.account_id, bearer_token=bearer_token)
    self.rvn = self.member["revision"]

    url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{self.party_id}/members/{self.account_id}/meta"
    headers = {
        "Authorization": "bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    data = {
        "delete": [],
        "revision": self.rvn,
        "update": {
            "Default:AthenaBannerInfo_j":
            json.dumps({
                "AthenaBannerInfo": {
                    "bannerIconId": bannericon,
                    "bannerColorId": bannerColor,
                }
            })
        }
    }
    return await Request.patch(url, headers=headers, json=data)

  async def change_skin(self, skin_id, style=None, chnl=None):
    self.skin_style = style
    self.skin_styles_chnl = chnl
    print(self.skin_styles_chnl)
    self.skin_id = skin_id
    return await self.apply()

  async def change_backpack(self, backpack_id, style=None, chnl=None):
    self.backpack_styles = style
    self.backpack_styles_chnl = chnl
    self.backpack_id = backpack_id
    return await self.apply()

  async def change_pickaxe(self, pickaxe_id):
    self.pickaxe_id = pickaxe_id
    return await self.apply()

  async def change_contrail(self, contrail_id):
    self.contrail_id = contrail_id
    return await self.apply()

  async def change_crowns(self, crowns):
    self.crowns_wins = crowns
    return await self.apply()

  async def change_has_crown(self, has_crown):
    self.has_crown = has_crown
    return await self.apply()

  async def change_progression(self, progression):
    self.progression = progression
    return await self.apply()

  async def apply(self):
    bearer_token = await Epic.authsToBearer({
        "account_id": self.account_id,
        "device_id": self.device_id,
        "secret": self.secret
    })
    self.party_id, self.member = await Epic.get_party_id(
        account_id=self.account_id, bearer_token=bearer_token)
    if self.party_id == 122:
      return 122
    self.rvn = self.member["revision"]

    url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{self.party_id}/members/{self.account_id}/meta"
    headers = {
        "Authorization": "bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    vl = {}
    if self.skin_style != None:
      vl['athenaCharacter'] = {
          'i': [{
              'c': self.skin_styles_chnl,
              'v': self.skin_style,
              'dE': 0
          }]
      }
    if self.backpack_styles != None:
      vl["athenaBackpack"] = {
          'i': [{
              'c': self.backpack_styles_chnl,
              'v': self.backpack_styles,
              'dE': 0
          }]
      }
    data = {
        "delete": [],
        "revision": self.rvn,
        "update": {
            "Default:AthenaCosmeticLoadoutVariants_j":
            json.dumps(
                {'AthenaCosmeticLoadoutVariants': {
                    'vL': vl,
                    'fT': False
                }}),
            "Default:AthenaCosmeticLoadout_j":
            json.dumps({
                "AthenaCosmeticLoadout": {
                    "characterPrimaryAssetId":
                    (self.skin_id if self.skin_id != None else ""),
                    "characterEKey":
                    "",
                    "backpackDef":
                    (self.backpack_id if self.backpack_id != None else ""),
                    "backpackEKey":
                    "",
                    "pickaxeDef":
                    (self.pickaxe_id if self.pickaxe_id != None else ""),
                    "pickaxeEKey":
                    "",
                    "contrailDef":
                    (self.contrail_id if self.contrail_id != None else ""),
                    "contrailEKey":
                    "",
                    "scratchpad": [],
                    "cosmeticStats": [{
                        "statName":
                        "HabaneroProgression",
                        "statValue":
                        (self.progression if self.progression != None else 1)
                    }, {
                        "statName":
                        "TotalVictoryCrowns",
                        "statValue":
                        (self.crowns_wins if self.crowns_wins != None else 1)
                    }, {
                        "statName":
                        "TotalRoyalRoyales",
                        "statValue":
                        (self.crowns_wins if self.crowns_wins != None else 1)
                    }, {
                        "statName":
                        "HasCrown",
                        "statValue": (1 if self.has_crown == True else 0)
                    }]
                }
            })
        }
    }
    return await Request.patch(url, headers=headers, json=data)


"""
Slash Commands
"""


class AccountSelect(nextcord.ui.Select):

  def __init__(self, Accounts):
    self.done = False
    self.selected_style = None

    options = [
        nextcord.SelectOption(label=style["displayName"],
                              description=style['account_id'],
                              value=str(idx))
        for idx, style in enumerate(Accounts.get('auths'))
    ]
    super().__init__(placeholder="Select an account", options=options)

  async def callback(self, interaction: nextcord.Interaction):
    self.selected_style = (self.values[0])
    await super().callback(interaction)
    Users.set_selected(interaction.user.id, int(self.selected_style))
    self.done = True
    self.view.stop()


class AccountSelectView(nextcord.ui.View):

  def __init__(self, Accounts):
    super().__init__()
    self.add_item(AccountSelect(Accounts=Accounts))


@bot.slash_command(name="login",
                   description="Login To Your Epic Games Account")
async def slash_device_login(inter):
  """Login To The Epic Account"""
  d = Users.get(inter.user.id, True)
  if d and len(d) != 0:
    embed = nextcord.Embed(
        title="Choose An Account",
        description="Choose an existing account, or add a new one.",
        color=colors.green)
    view = AccountSelectView(Accounts=d)
    button = nextcord.ui.Button(label="Add New Account",
                                style=nextcord.ButtonStyle.green,
                                emoji='✨')
    bContinue = False

    async def clbk(interaction):
      nonlocal bContinue
      bContinue = True
      view.stop()

    button.callback = clbk
    view.add_item(button)
    msgmsg = await inter.send(embed=embed, view=view)
    await view.wait()
    if view.children[0].done:
      return await msgmsg.edit(embed=nextcord.Embed(
          title=
          f'Logged in to {Users.get(inter.user.id, False).get("displayName")}',
          color=colors.green,
          description="Selected the account: `" +
          Users.get(inter.user.id, False).get("displayName") + '`'),
                               view=None)
    if bContinue:
      token = await Epic.get_client_credentials_token()
      device_code, url = await Epic.create_device_authorization(token)
      embed = nextcord.Embed(title="Login To Your Epic Games Account",
                             color=colors.blurple)
      embed.add_field(
          name="Please Login Using The Following Info",
          value=
          "1. Click The Button Below To Login To Your Epic Games Account\n2. Press Confirm\n3. Wait For The Bot To Log You In"
      )

      view = nextcord.ui.View()
      style = nextcord.ButtonStyle.gray
      item = nextcord.ui.Button(style=style, label="Login To Epic", url=url)
      view.add_item(item)

      await msgmsg.edit(embed=embed, view=view)

      logged_in = False
      disp = ""

      async def check_if_logged_in():
        nonlocal logged_in
        nonlocal disp
        attempts = 0
        while not logged_in:
          response = await Epic.create_login(device_code=device_code)

          attempts += 1
          if response:
            auth = response['device_auth']
            disp = response['displayName']
            auth['displayName'] = disp
            Users.save(inter.user.id, auth,
                       (len(Users.get(inter.user.id, True).get('auths', [])))
                       if Users.get(inter.user.id) != None else 0)
            logged_in = True
          else:
            if attempts > 10:
              return
            await asyncio.sleep(3)

      thread = bot.loop.create_task(check_if_logged_in())
      await thread
      if logged_in:
        embed = nextcord.Embed(
            title="Logged In",
            description=f"Successfully logged in as `{disp}`!",
            color=colors.green)
        await msgmsg.edit(embed=embed, view=None)
      else:
        embed = nextcord.Embed(title="Canceled Login",
                               description="You took too long!",
                               color=colors.red)
        await msgmsg.edit(embed=embed, view=None)

  else:
    token = await Epic.get_client_credentials_token()
    device_code, url = await Epic.create_device_authorization(token)
    embed = nextcord.Embed(title="Login To Your Epic Games Account",
                           color=colors.blurple)
    embed.add_field(
        name="Please Login Using The Following Info",
        value=
        "1. Click The Button Below To Login To Your Epic Games Account\n2. Press Confirm\n3. Wait For The Bot To Log You In"
    )

    view = nextcord.ui.View()
    style = nextcord.ButtonStyle.gray
    item = nextcord.ui.Button(style=style, label="Login To Epic", url=url)
    view.add_item(item)

    msgmsg = await inter.send(embed=embed, view=view)

    logged_in = False
    disp = ""

    async def check_if_logged_in():
      nonlocal logged_in
      nonlocal disp
      attempts = 0
      while not logged_in:
        response = await Epic.create_login(device_code=device_code)
        print(str(response))
        attempts += 1
        if response:
          auth = response['device_auth']
          disp = response['displayName']
          auth['displayName'] = disp
          Users.save(inter.user.id, auth,
                     (len(Users.get(inter.user.id, True).get('auths', [])))
                     if Users.get(inter.user.id) != None else 0)
          logged_in = True
        else:
          if attempts > 10:
            return
          await asyncio.sleep(3)

    thread = bot.loop.create_task(check_if_logged_in())
    await thread
    if logged_in:
      embed = nextcord.Embed(
          title="Logged In",
          description=f"Successfully logged in as `{disp}`!",
          color=colors.green)
      await msgmsg.edit(embed=embed, view=None)
    else:
      embed = nextcord.Embed(title="Canceled Login",
                             description="You took too long!",
                             color=colors.red)
      await msgmsg.edit(embed=embed, view=None)


@bot.slash_command(name="logout", description="Logout From Your Epic Account")
async def slash_logout(inter):
  """Logout From The Epic Account"""
  if Users.get(inter.user.id) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  Users.delete(str(inter.user.id))
  embed = nextcord.Embed(title="Logged Out",
                         description=f"Successfully logged out!",
                         color=colors.green)
  await inter.send(embed=embed)


class autocomplete:
  """Subclass For AutoComplete"""

  @staticmethod
  async def Autocomplete_Skin(inter, value):
    return [
        skin['name'] for skin in Cosmetics.gather_skins()
        if skin['name'].lower().startswith(value.lower())
    ][:25]

  @staticmethod
  async def Autocomplete_Backpack(inter, value):
    return [
        skin['name'] for skin in Cosmetics.gather_backpacks()
        if skin['name'].lower().startswith(value.lower())
    ][:25]

  @staticmethod
  async def Autocomplete_Emote(inter, value):
    return [
        skin['name'] for skin in Cosmetics.gather_emotes()
        if skin['name'].lower().startswith(value.lower())
    ][:25]

  @staticmethod
  async def Autocomplete_pickaxe(inter, value):
    return [
        skin['name'] for skin in Cosmetics.gather_pickaxes()
        if skin['name'].lower().startswith(value.lower())
    ][:25]


"""Ghostequip Clients Defintion"""
Clients = {}
"""Ghost Equip"""


@bot.slash_command(name='ghostequip')
async def ghostequip(inter):
  pass


class StyleSelect(nextcord.ui.Select):

  def __init__(self, styles):
    self.done = False
    self.selected_style = None  # Initialize selected style as None
    options = [
        nextcord.SelectOption(label=style["name"].lower().capitalize(),
                              value=str(style["tag"]))
        for style in (styles[0]['options'])[:25]
    ]
    super().__init__(placeholder="Select a style", options=options)

  async def callback(self, interaction: nextcord.Interaction):
    self.selected_style = (self.values[0])
    await super().callback(interaction)
    self.done = True


class StyleSelectView(nextcord.ui.View):

  def __init__(self, styles):
    super().__init__()
    self.add_item(StyleSelect(styles))


@ghostequip.subcommand(name='skin', description="Equips A Skin In Lobby")
async def skin(inter: Interaction,
               item: str = SlashOption(
                   name='item',
                   description='The Item You Want To Equip',
                   autocomplete=True,
                   autocomplete_callback=autocomplete.Autocomplete_Skin)):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  Cosmetic = (await Cosmetics.find_async(item))
  styles = Cosmetic['variants']
  selected_style = None
  chnl = None
  if styles != None:

    view = StyleSelectView(styles)
    msgmsg = await inter.send(
        embed=nextcord.Embed(title="Skin Styles",
                             description="Select a style for the skin:",
                             color=colors.blurple),
        view=view,
    )
    while view.children[0].done != True:
      await asyncio.sleep(0.1)
    selected_style = view.children[0].selected_style
    stylepic = None
    stylename = None
    chnl = styles[0]["channel"]
    for stylee in styles[0]['options']:
      if stylee['tag'] == selected_style:
        stylepic = stylee['image']
        stylename = stylee['name']
        break
    ambad = Embed(title="Selected Style: " + stylename,
                  description="Style ID: " + selected_style,
                  color=colors.green)
    ambad.set_thumbnail(url=stylepic)
    auths = Users.get(str(inter.user.id))

    await msgmsg.edit(embed=ambad, view=None)
  RESULT = await Handler.change_skin("AthenaCharacter:" + Cosmetic['id'],
                                     selected_style, chnl)
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    embed.set_footer(text=footertext)    
    embed.set_author(name=auths['displayName'],
                     icon_url=await get_avatar(auths))
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Equipped",
                         description=f"Successfully Equipped  `{item}`",
                         color=colors.green)
  embed.set_thumbnail(url=Cosmetic['images']['icon'])
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@ghostequip.subcommand(name="backpack",
                       description="Equips A Backpack In Lobby")
async def backpack(
    inter: Interaction,
    item: str = SlashOption(
        name='item',
        autocomplete=True,
        autocomplete_callback=autocomplete.Autocomplete_Backpack)):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  Cosmetic = (await Cosmetics.find_async(item))
  styles = Cosmetic['variants']
  selected_style = None
  chnl = None
  if styles != None:
    view = StyleSelectView(styles)
    msgmsg = await inter.send(
        embed=nextcord.Embed(title="Backpack Styles",
                             description="Select a style for the backpack:",
                             color=colors.blurple),
        view=view,
    )
    while view.children[0].done != True:
      await asyncio.sleep(0.1)
    selected_style = view.children[0].selected_style
    stylepic = None
    stylename = None
    chnl = styles[0]["channel"]
    for stylee in styles[0]['options']:
      if stylee['tag'] == selected_style:
        stylepic = stylee['image']
        stylename = stylee['name']
        break
    ambad = Embed(title="Selected Style: " + stylename,
                  description="Style ID: " + selected_style,
                  color=colors.green)
    ambad.set_thumbnail(url=stylepic)

    await msgmsg.edit(embed=ambad, view=None)

  RESULT = await Handler.change_backpack(
      Cosmetics.reinterpret_path(Cosmetic['path']), selected_style, chnl)
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Equipped",
                         description=f"Successfully Equipped  `{item}`",
                         color=colors.green)
  embed.set_thumbnail(url=Cosmetic['images']['icon'])
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@ghostequip.subcommand(name='emote', description="Equips An Emote In Lobby")
async def emote(inter: Interaction,
                item: str = SlashOption(
                    name='item',
                    autocomplete=True,
                    autocomplete_callback=autocomplete.Autocomplete_Emote)):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    auths = Users.get(str(inter.user.id))
    embed.set_footer(text=footertext)    
    embed.set_author(name=auths['displayName'],
                     icon_url=await get_avatar(auths))
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  Cosmetic = (await Cosmetics.find_async(item))
  RESULT = await Handler.set_emote(Cosmetics.reinterpret_path(Cosmetic['path'])
                                   )
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Equipped",
                         description=f"Successfully Equipped  `{item}`",
                         color=colors.green)
  embed.set_thumbnail(url=Cosmetic['images']['icon'])
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@ghostequip.subcommand(name='pickaxe', description="Equips A Pickaxe In Lobby")
async def pickaxe(
    inter: Interaction,
    item: str = SlashOption(
        name='item',
        autocomplete=True,
        autocomplete_callback=autocomplete.Autocomplete_pickaxe)):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    auths = Users.get(str(inter.user.id))
    embed.set_footer(text=footertext)    
    embed.set_author(name=auths['displayName'],
                     icon_url=await get_avatar(auths))
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  Cosmetic = (await Cosmetics.find_async(item))
  RESULT = await Handler.change_pickaxe(
      Cosmetics.reinterpret_path(Cosmetic['path']))
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Equipped",
                         description=f"Successfully Equipped  `{item}`",
                         color=colors.green)
  embed.set_thumbnail(url=Cosmetic['images']['icon'])
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@ghostequip.subcommand(name='level', description="Sets A Level In Lobby")
async def level(inter: Interaction,
                level: int = SlashOption(name='level',
                                         description='The level you want')):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  RESULT = await Handler.change_level(level)
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    auths = Users.get(str(inter.user.id))
    embed.set_footer(text=footertext)    
    embed.set_author(name=auths['displayName'],
                     icon_url=await get_avatar(auths))
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Set Level",
                         description=f"Successfully Set Level To  `{level}`",
                         color=colors.green)
  embed.set_thumbnail(
      url=
      'https://drive.usercontent.google.com/download?id=17Fv1zbi4lb9xF8jNjGuzJ33eHV9AeffA&export=download&authuser=0'
  )
  await inter.send(embed=embed)


async def Banner_AtoComplete(ctx, calue):
  return [
      skin['id'] for skin in Cosmetics.gather_banners()
      if skin['id'].lower().startswith(calue.lower())
  ][:25]


Banner_Colors = requests.get(
    "https://fortnite-api.com/v1/banners/colors").json()['data']


def get_banner_color(banner_color):
  for i in Banner_Colors:
    if i['color'] == banner_color:
      return i['id']
  return None


async def BannerC_AtoComplete(ctx, calue):
  return [
      skin['color'] for skin in Banner_Colors
      if skin['color'].lower().startswith(calue.lower())
  ][:25]


@ghostequip.subcommand(name='banner', description="Equips A Banner In Lobby")
async def banner(
    inter: Interaction,
    item: str = SlashOption(name='item',
                            description='The Item You Want To Equip',
                            autocomplete_callback=Banner_AtoComplete,
                            autocomplete=True),
    color: str = SlashOption(name='color',
                             description='The Color You Want On The Banner',
                             autocomplete=True,
                             autocomplete_callback=BannerC_AtoComplete)):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    return await inter.send(embed=embed)
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  RESULT = await Handler.change_banner(item, get_banner_color(color))
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Equipped",
                         description=f"Successfully Equipped  `{item}`",
                         color=colors.green)
  Cosmetic = (await Cosmetics.banner_async(item))
  embed.set_thumbnail(url=Cosmetic['images']['icon'])
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@ghostequip.subcommand(name='crowns', description="Sets Crown Wins In Lobby")
async def crowns(inter: Interaction,
                 crowns: int = SlashOption(name='crowns',
                                           description='The crowns you want')):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  RESULT = await Handler.change_crowns(crowns)
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Set Crowns",
                         description=f"Successfully Set Crowns To  `{crowns}`",
                         color=colors.green)
  embed.set_thumbnail(
      url=
      'https://drive.usercontent.google.com/download?id=1-DJJzjIhUa4be-UzYwUzNDYSgxWsiUHn&export=download&authuser=0'
  )
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


rankes = {
    "bronze 1": 0,
    "bronze 2": 1,
    "bronze 3": 2,
    "silver 1": 3,
    "silver 2": 4,
    "silver 3": 5,
    "gold 1": 6,
    "gold 2": 7,
    "gold 3": 8,
    "platinum 1": 9,
    "platinum 2": 10,
    "platinum 3": 11,
    "diamond 1": 12,
    "diamond 2": 13,
    "diamond 3": 14,
    "elite": 15,
    "champion": 16,
    "unreal": 17
}
"""@ghostequip.subcommand(name='rank', description='Sets Your Rank In Lobby')
async def rank(inter,
               rank: str = SlashOption(
                   name='rank',
                   description='The Rank You Want',
                   choices=set([f.capitalize() for f in rankes.keys()]))):
  global Clients
  if Users.get(str(inter.user.id)) == None:
    embed = nextcord.Embed(title="Not Logged In",
                           description="You are not logged in!",
                           color=colors.red)
    await inter.send(embed=embed)
    return
  if Clients.get(str(inter.user.id)) == None:
    Clients[str(inter.user.id)] = Party(inter.user.id)
  Handler = Clients[str(inter.user.id)]
  RESULT = await Handler.change_progression(rankes[rank.lower()])
  if RESULT == 122:
    embed = nextcord.Embed(
        title="Not In A Party",
        description="You Need To Be Online And In A Party To Use This Command",
        color=colors.red)
    return await inter.send(embed=embed)
  embed = nextcord.Embed(title=f"Successfully Set Rank",
                         description=f"Successfully Set Rank To  `{rank}`",
                         color=colors.green)
  embed.set_thumbnail(
      url=
      'https://drive.usercontent.google.com/download?id=1s17aeXGeB87_5QJ2JZarULrgEXu4xs8h&export=download&authuser=0'
  )
  auths = Users.get(str(inter.user.id))
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url = await get_avatar(auths))
  await inter.send(embed=embed)"""

CurrentBots = {}

import hashlib, websockets


async def websocket(serviceUrl: str, MMSAuth: str, client):
  """ws for matchmake"""
  websocket = await websockets.connect(
      uri=serviceUrl, extra_headers={"Authorization": MMSAuth})
  latest_data = None
  while True:

    try:
      latest_data = await websocket.recv()
      print('[MATCHMAKER] Recieved: ' + str(latest_data))
      if 'queuedPlayers' in json.loads(
          latest_data)['payload'] and client.party.me.leader:
        await websocket.send(
            json.dumps({
                "name": "Exec",
                "payload": {
                    "command": "p.StartMatch"
                }
            }))

    except websockets.ConnectionClosed:
      break

  data = json.loads(latest_data)
  try:
    currentSession = data['payload']['sessionId']
    async with aiohttp.ClientSession() as session:
      async with session.get(
          url=
          f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/matchmaking/session/{currentSession}",
          headers={
              "Authorization": client.http.get_auth('FORTNITE_ACCESS_TOKEN')
          },
          data={}) as request:
        return await request.text()
  except KeyError:
    return None


async def matchmake(client, parameters: dict):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        url=
        f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player/{client.user.id}",
        headers={
            'Content-Type': 'application/json',
            "Authorization": client.http.get_auth('FORTNITE_ACCESS_TOKEN'),
            'User-Agent': client.http.user_agent,
        },
        params=parameters) as request:

      response = await request.json()
      if response.__contains__("errorMessage") and (
          response.get("errorMessage", "").__contains__("'PLAY'")
          or response.get("errorMessage", "").__contains__("Banned")):
        return response['errorMessage']

  payload = response['payload']
  signature = response['signature']
  serviceUrl = response['serviceUrl']
  plaintext = payload[10:20] + "Don'tMessWithMMS" + signature[2:10]

  data = plaintext.encode('utf-16le')
  hash_object = hashlib.sha1(data)
  hash_digest = hash_object.digest()

  checksum = __import__("base64").b16encode(hash_digest[2:10]).decode().upper()

  MMSAuth = f"Epic-Signed mms-player {payload} {signature} {checksum}"
  return await websocket(serviceUrl=serviceUrl, MMSAuth=MMSAuth, client=client)


async def getNetCL(client):
  """Returns NetCL for bucket id"""
  async with aiohttp.ClientSession() as session:
    async with session.post(
        url=
        "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/matchmaking/session/matchMakingRequest",
        headers={
            "Authorization": client.http.get_auth('FORTNITE_ACCESS_TOKEN'),
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "criteria": [],
            "openPlayersRequired": 1,
            "buildUniqueId": "",
            "maxResults": 1
        })) as request:
      response = await request.json()
      text = await request.text()
  #logger.info("NetCL Response : "+ text)

  try:
    data = response[0]
    NetCL = data['attributes']['buildUniqueId_s']
    return NetCL
  except:
    print('error netcl ', text)


@bot.slash_command(name='lobbybot')
async def lobbybot(inter: Interaction):
  pass


@lobbybot.subcommand(name='exch', description="Exchange Code")
async def exch(inter: Interaction):
  client = CurrentBots.get(str(inter.user.id))
  return await inter.send(
      embed=Embed(title='Exchange Code',
                  description=await Epic.get_exchange(await Epic.authsToBearer(
                      nsk[str(inter.user.id)]))))


async def BotDefinition(account_id, device_id, secret, user):

  client = FortniteCommands.Bot(command_prefix="!",
                                auth=fortnitepy.DeviceAuth(
                                    device_id=device_id,
                                    account_id=account_id,
                                    secret=secret, fortnite_token=Vars.NEW_SWITCH_TOKEN.removeprefix("Basic "), ios_token=Vars.LAUNCHERTOKEN.removeprefix("Basic ")))

  @client.event
  async def event_ready():
    embed = nextcord.Embed(title="Client Launched!",
                           description=f"Launched {client.user.display_name}!")
    await client.set_presence("Ramirez")
    CurrentBots.update({str(user.id): client})
    await user.send(embed=embed)
    (await initProfileForMM(client))
    print('done Initated profile')

  @client.event
  async def event_friend_request(request):
    count = 0
    accept = nextcord.ui.Button(label="Accept!",
                                style=nextcord.ButtonStyle.green,
                                emoji='✅')

    async def accept_invite(interaction):
      await request.accept()
      await notification.delete()

    async def decline_invite(interaction):
      await request.decline()
      await notification.delete()

    decline = nextcord.ui.Button(label="Decline!",
                                 style=nextcord.ButtonStyle.danger,
                                 emoji='❌')
    accept.callback = accept_invite
    decline.callback = decline_invite
    invite_view = nextcord.ui.View()
    invite_view.add_item(accept)
    invite_view.add_item(decline)
    embed = nextcord.Embed(
        title="Friend Request Recieved",
        description=f"Accept Friend Request From {request.display_name}?",
        color=colors.green)
    notification = await user.send(embed=embed, view=invite_view)

  @client.event
  async def event_party_member_ready_change(member, before, after):
    members = [
        memb.is_ready() for memb in client.party.members
        if memb.id != client.user.id
    ]
    print(str(members))
    if all(members):
      await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    else:
      await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)

  @client.event
  async def event_party_member_join(member):
    """This Code is Only Excecuted When a Member Joins The Bot!"""
    if member.id == client.user.id:
      return

    embed = nextcord.Embed(
        title="Atomic - Lobby Bot",
        description=f"{member.display_name} Joined Your Party",
        color=colors.green)
    embed.add_field(name="Party Size",
                    value=f"{client.party.member_count}/ 16",
                    inline=True)
    embed.add_field(name="Party Leader",
                    value=f"{client.party.leader}",
                    inline=False)
    return await user.send(embed=embed)

  @client.event
  async def event_party_update(party: fortnitepy.Party):
    mmsInfo = client.party.meta.get_prop('Default:PartyState_s')
    print(mmsInfo)
    if mmsInfo == 'BattleRoyalePreloading':
      client.party.meta.set_prop(
          'Default:LobbyState_j',
          json.dumps({"LobbyState": {
              "hasPreloadedAthena": True
          }}))
    if mmsInfo == 'BattleRoyaleMatchmaking':
      party_playlist_info = client.party.meta.get_prop(
          'Default:PartyMatchmakingInfo_j')
      print(str(party_playlist_info))
      playlist_name, region, playlistRvn = party_playlist_info[
          'PartyMatchmakingInfo']['playlistName'].lower(
          ), party_playlist_info['PartyMatchmakingInfo'].get(
              'regionId', 'EU'
          ), party_playlist_info['PartyMatchmakingInfo']['playlistRevision']

      NetCL = await getNetCL(client=client)
      regionDict = {
          "EUROPE": "eu",
          "NA-EAST": "nae",
          "OCEANIA": "oce",
          "NA-WEST": "naw",
          "BRAZIL": "br",
          "MIDDLE EAST": "me",
          "ASIA": "asia",
          "NA-CENTRAL": "nac",
      }
      if region.lower() not in list(regionDict.values()):
        return
      bucket_id = f"{NetCL}:{playlistRvn}:{region}:{playlist_name}"
      party_player_ids = ','.join(
          [member.id for member in client.party.members if member.is_ready])

      print(f"Bucket ID: {bucket_id}")

      query = {
          "partyPlayerIds": party_player_ids,
          "player.platform": "Windows",
          "player.option.partyId": client.party.id,
          "input.KBM": "true",
          "player.input": "KBM",
          "bucketId": bucket_id
      }
      for member in client.party.members:
        platform_data = member.meta.get_prop('Default:PlatformData_j')
        print(str(platform_data))
        if platform_data and not query.get(
            f"party.{platform_data['PlatformData']['platform']['platformDescription']['name']}"
        ):
          query[
              f"party.{platform_data['PlatformData']['platform']['platformDescription']['name']}"] = "true"

      #await client.party.me.set_ready(fortnitepy.ReadyState.READY)
      await matchmake(
          client,
          parameters=query,
      )

    if mmsInfo == 'BattleRoyalePostMatchmaking':
      await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)

  @client.event
  async def event_party_invite(invite):
    """This Code is Only Excecuted When The Bot Gets Launched!"""
    accept = nextcord.ui.Button(label="Accept!",
                                style=nextcord.ButtonStyle.green,
                                emoji='✅')

    async def accept_invite(interaction):
      await invite.accept()
      await notification.delete()

    async def decline_invite(interaction):
      await invite.decline()
      await notification.delete()

    decline = nextcord.ui.Button(label="Decline!",
                                 style=nextcord.ButtonStyle.danger,
                                 emoji='❌')
    accept.callback = accept_invite
    decline.callback = decline_invite
    invite_view = nextcord.ui.View()
    invite_view.add_item(accept)
    invite_view.add_item(decline)
    embed = nextcord.Embed(
        title="Invite Recieved",
        description=f"Accept Invite From {invite.sender.display_name}?")
    notification = await user.send(embed=embed, view=invite_view)

  return client


async def botWaitKill(user):
  await asyncio.sleep(delay=7200)
  klient = CurrentBots.get(user.id)
  await klient.close()
  CurrentBots.pop(user.id)
  await user.send(
      embed=Embed(title="Your Bot Has Been Stopped",
                  description="To Start It Again Use `/lobbybot start`",
                  color=colors.green))


class AccountLSelect(nextcord.ui.Select):

  def __init__(self, Accounts):
    self.done = False
    self.selected_style = None

    options = [
        nextcord.SelectOption(label=style["displayName"],
                              description=style['account_id'],
                              value=str(idx))
        for idx, style in enumerate(Accounts.get('auths'))
    ]
    super().__init__(placeholder="Select an account", options=options)

  async def callback(self, interaction: nextcord.Interaction):
    self.selected_style = (self.values[0])
    await super().callback(interaction)
    self.done = True
    self.view.stop()


class AccountLSelectView(nextcord.ui.View):

  def __init__(self, Accounts):
    super().__init__()
    self.add_item(AccountSelect(Accounts=Accounts))


nsk = {}


@lobbybot.subcommand(name='start', description='Starts The Bot')
async def start(inter: Interaction):
  view = nextcord.ui.View()
  view.add_item(AccountLSelect(Users.get(str(inter.user.id), True)))
  msgmsg = await inter.send(embed=nextcord.Embed(
      title='Choose Your Account',
      description='Do not choose your main account, choose a secondary account.'
  ),
                            view=view)
  await view.wait()
  auths = Users.get(str(inter.user.id),
                    True)['auths'][int(view.children[0].selected_style)]
  nsk[str(inter.user.id)] = auths
  if not auths:
    embed = nextcord.Embed(title="Error",
                           description="Do /login first :)",
                           color=colors.red)
    await inter.send(embed=embed)

  elif CurrentBots.get(str(inter.user.id)):
    embed = nextcord.Embed(title="Error",
                           description="You already have a bot.")
    await inter.send(embed=embed)

  else:
    client = await BotDefinition(
        user=inter.user,
        account_id=auths.get("account_id"),
        device_id=auths.get("device_id"),
        secret=auths.get("secret"),
    )
    bot.loop.create_task(client.start())

    embed = nextcord.Embed(title="Launching The Client...",
                           description="Check Your DMs For More Info",
                           color=colors.green)
    embed.set_footer(text=footertext)    
    embed.set_author(name=auths['displayName'],
                     icon_url=await get_avatar(auths))
    await inter.send(embed=embed)
    bot.loop.create_task(botWaitKill(user=inter.user))


@lobbybot.subcommand(name='stop', description='Stops The Bot')
async def stop(inter: Interaction):
  if CurrentBots.get(str(inter.user.id)):
    await CurrentBots.get(str(inter.user.id)).close()
    CurrentBots.pop(str(inter.user.id))
    embed = nextcord.Embed(title="Stopped",
                           description="Your bot has been stopped",
                           color=colors.green)
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


Current_LB_clients = {}


@lobbybot.subcommand(name='skin', description='Sets Your Skin On Lobby Bot')
async def skinn(inter: Interaction,
                skin: str = SlashOption(
                    name='skin',
                    description='The Skin You Want',
                    autocomplete=True,
                    autocomplete_callback=autocomplete.Autocomplete_Skin)):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    Cosmetic = (await Cosmetics.find_async(skin))
    styles = Cosmetic['variants']
    selected_style = None
    chnl = None
    if styles != None:

      view = StyleSelectView(styles)
      msgmsg = await inter.send(
          embed=nextcord.Embed(title="Skin Styles",
                               description="Select a style for the skin:",
                               color=colors.blurple),
          view=view,
      )
      while view.children[0].done != True:
        await asyncio.sleep(0.1)
      selected_style = view.children[0].selected_style
      stylepic = None
      stylename = None
      chnl = styles[0]["channel"]
      for stylee in styles[0]['options']:
        if stylee['tag'] == selected_style:
          stylepic = stylee['image']
          stylename = stylee['name']
          break
      ambad = Embed(title="Selected Style: " + stylename,
                    description="Style ID: " + selected_style,
                    color=colors.green)
      ambad.set_thumbnail(url=stylepic)
      await msgmsg.edit(embed=ambad, view=None)
    RESULT = await Handler.change_skin("AthenaCharacter:" + Cosmetic['id'],
                                       selected_style, chnl)
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(title=f"Successfully Equipped",
                           description=f"Successfully Equipped  `{skin}`",
                           color=colors.green)
    embed.set_thumbnail(url=Cosmetic['images']['icon'])
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='backpack',
                     description='Sets Your Backpack On Lobby Bot')
async def bkpk(inter: Interaction,
               backpack: str = SlashOption(
                   name='backpack',
                   description='The Backpack You Want',
                   autocomplete=True,
                   autocomplete_callback=autocomplete.Autocomplete_Backpack)):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    Cosmetic = (await Cosmetics.find_async(backpack))
    styles = Cosmetic['variants']
    selected_style = None
    chnl = None
    if styles != None:

      view = StyleSelectView(styles)
      msgmsg = await inter.send(
          embed=nextcord.Embed(title="Skin Styles",
                               description="Select a style for the backpack:",
                               color=colors.blurple),
          view=view,
      )
      while view.children[0].done != True:
        await asyncio.sleep(0.1)
      selected_style = view.children[0].selected_style
      stylepic = None
      stylename = None
      chnl = styles[0]["channel"]
      for stylee in styles[0]['options']:
        if stylee['tag'] == selected_style:
          stylepic = stylee['image']
          stylename = stylee['name']
          break
      ambad = Embed(title="Selected Style: " + stylename,
                    description="Style ID: " + selected_style,
                    color=colors.green)
      ambad.set_thumbnail(url=stylepic)
      await msgmsg.edit(embed=ambad, view=None)
    RESULT = await Handler.change_backpack(
        Cosmetics.reinterpret_path(Cosmetic['path']), selected_style, chnl)
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(title=f"Successfully Equipped",
                           description=f"Successfully Equipped  `{backpack}`",
                           color=colors.green)
    embed.set_thumbnail(url=Cosmetic['images']['icon'])
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='pickaxe',
                     description='Sets Your Pickaxe On Lobby Bot')
async def pkpk(inter: Interaction,
               pickaxe: str = SlashOption(
                   name='pickaxe',
                   description='The Pickaxe You Want',
                   autocomplete=True,
                   autocomplete_callback=autocomplete.Autocomplete_pickaxe)):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    Cosmetic = (await Cosmetics.find_async(pickaxe))
    RESULT = await Handler.change_pickaxe(
        Cosmetics.reinterpret_path(Cosmetic['path']))
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(title=f"Successfully Equipped",
                           description=f"Successfully Equipped  `{pickaxe}`",
                           color=colors.green)
    embed.set_thumbnail(url=Cosmetic['images']['icon'])
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='emote', description='Sets Your Emote On Lobby Bot')
async def emt(inter: Interaction,
              emote: str = SlashOption(
                  name='emote',
                  description='The Emote You Want',
                  autocomplete=True,
                  autocomplete_callback=autocomplete.Autocomplete_Emote)):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    Cosmetic = (await Cosmetics.find_async(emote))
    RESULT = await Handler.set_emote(
        Cosmetics.reinterpret_path(Cosmetic['path']))
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(title=f"Successfully Equipped",
                           description=f"Successfully Equipped  `{emote}`",
                           color=colors.green)
    embed.set_thumbnail(url=Cosmetic['images']['icon'])
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='banner',
                     description='Sets Your Banner On Lobby Bot')
async def bnr(
    inter: Interaction,
    banner: str = SlashOption(name='banner',
                              description='The Banner You Want',
                              autocomplete=True,
                              autocomplete_callback=Banner_AtoComplete),
    bannercolor: str = SlashOption(name='bannercolor',
                                   description='The Banner Color You Want',
                                   autocomplete=True,
                                   autocomplete_callback=BannerC_AtoComplete)):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    Cosmetic = (await Cosmetics.banner_async(banner))
    RESULT = await Handler.change_banner(banner, bannercolor)
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(title=f"Successfully Equipped",
                           description=f"Successfully Equipped  `{banner}`",
                           color=colors.green)
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    embed.set_thumbnail(url=Cosmetic['images']['icon'])
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='level', description='Sets Your Level On Lobby Bot')
async def lvl(inter: Interaction,
              level: int = SlashOption(name='level',
                                       description='The Level You Want')):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    RESULT = await Handler.change_level(level)
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(
        title=f"Successfully Set",
        description=f"Successfully Set Level To  `{str(level)}`",
        color=colors.green)
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    embed.set_thumbnail(
        url=
        'https://drive.usercontent.google.com/download?id=17Fv1zbi4lb9xF8jNjGuzJ33eHV9AeffA&export=download&authuser=0'
    )
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


@lobbybot.subcommand(name='crowns',
                     description='Sets Your Crowns On Lobby Bot')
async def crwns(inter: Interaction,
                crowns: int = SlashOption(name='crowns',
                                          description='The Crowns You Want')):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    if not str(inter.user.id) in Current_LB_clients:
      Current_LB_clients[str(inter.user.id)] = Party(nsk[str(inter.user.id)],
                                                     True)
    Handler = Current_LB_clients[str(inter.user.id)]
    RESULT = await Handler.change_crowns(crowns)
    if RESULT == 122:
      embed = nextcord.Embed(
          title="Not In A Party",
          description=
          "You Need To Be Online And In A Party To Use This Command",
          color=colors.red)
      return await inter.send(embed=embed)
    embed = nextcord.Embed(
        title=f"Successfully Set",
        description=f"Successfully Set Crowns To  `{str(crowns)}`",
        color=colors.green)
    embed.set_footer(text=footertext)
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    embed.set_thumbnail(
        url=
        'https://drive.usercontent.google.com/download?id=1-DJJzjIhUa4be-UzYwUzNDYSgxWsiUHn&export=download&authuser=0'
    )
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


"""@lobbybot.subcommand(name='platform', description='Sets Your Platform On Lobby Bot')
async def plat(inter: Interaction, platform: str = SlashOption(name='platform', description='The Platform You Want', choices={"Windows", "Mac", "Xbox One", "PlayStation 5", "PlayStation 4", "Nintendo Switch", "Ios", "Android"})):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    
    platformget = {
      "Windows": fortnitepy.Platform.WINDOWS,
      "Mac": fortnitepy.Platform.MAC,
      "Xbox One": fortnitepy.Platform.XBOX_ONE,
      "PlayStation 5": fortnitepy.Platform.PLAYSTATION_5,
      "PlayStation 4": fortnitepy.Platform.PLAYSTATION_4,
      "Nintendo Switch": fortnitepy.Platform.SWITCH,
      "Ios": fortnitepy.Platform.IOS,
      "Android": fortnitepy.Platform.ANDROID
    }

    await client.set_platform(platformget[platform])
    
    embed = nextcord.Embed(title=f"Successfully Set",
                           description=f"Successfully Set Platform To  `{platform}`",
                           color=colors.green)
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(
      title="Error",
      description="You don't have a bot.",
      color=colors.red
    )
    await inter.send(embed=embed)"""


@lobbybot.subcommand(name='ready', description='Sets Your Ready On Lobby Bot')
async def ready(inter: Interaction,
                ready: str = SlashOption(
                    name='ready',
                    description='The Ready Status Of The Bot',
                    choices=["Ready", "Not Ready", 'Sitting Out'])):
  if CurrentBots.get(str(inter.user.id)):
    client = CurrentBots.get(str(inter.user.id))
    readyget = {
        "Not Ready": fortnitepy.ReadyState.NOT_READY,
        "Ready": fortnitepy.ReadyState.READY,
        "Sitting Out": fortnitepy.ReadyState.SITTING_OUT
    }
    await client.party.me.set_ready(readyget[ready])
    embed = nextcord.Embed(
        title=f"Successfully Set",
        description=f"Successfully Set Ready To  `{str(ready)}`",
        color=colors.green)
    embed.set_footer(text=footertext)    
    embed.set_author(name=nsk[str(inter.user.id)]['displayName'],
                     icon_url=await get_avatar(nsk[str(inter.user.id)]))
    await inter.send(embed=embed)
  else:
    embed = nextcord.Embed(title="Error",
                           description="You don't have a bot.",
                           color=colors.red)
    await inter.send(embed=embed)


from PIL import Image, ImageDraw, ImageFont
import io

RARITY_BACKGROUNDS = {
    'epic': 'img/Epic Rarity Box Graphic.PNG',
    'rare': 'img/Rare Rarity Box Graphic.PNG',
    'common': 'img/Rarity Box Graphic.PNG',
    'uncommon': 'img/Uncommon Rarity Box Graphic.PNG',
    'legendary': 'img/Legendary Rarity Box Graphic.PNG',
    'mythic': 'img/Mythic Rarity Box Graphic.PNG',
    'exotic': 'img/Exotic Rarity Box Graphic.PNG'
}

RARITY_ORDER = [
    'mythic', 'exotic', 'legendary', 'epic', 'rare', 'uncommon', 'common'
]


class Imaging:

  @staticmethod
  async def fetch_image(session, url):
    async with session.get(url) as response:
      return await response.read()

  @staticmethod
  def fit_text(draw, text, max_width, font_path, initial_font_size):
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)
    while draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox(
        (0, 0), text, font=font)[0] > max_width and font_size > 10:
      font_size -= 1
      font = ImageFont.truetype(font_path, font_size)
    return font

  @staticmethod
  async def generate_skins_image(skins, output_file_path, username):
    try:
      print("Starting to generate the skins image.")
      # Define some constants
      width, height = 1200, 800  # Overall size for better layout
      padding = 20  # Padding between images
      columns = 8  # Number of skins per row

      # Group skins by rarity
      skins_by_rarity = {rarity: [] for rarity in RARITY_ORDER}
      for skin in skins:
        rarity = skin.get('rarity', {}).get('value', 'common').lower()
        if rarity in skins_by_rarity:
          skins_by_rarity[rarity].append(skin)
        else:
          skins_by_rarity['common'].append(
              skin)  # Default to 'common' if the rarity is unrecognized

      # Flatten the list of skins in the specified rarity order
      ordered_skins = [
          skin for rarity in RARITY_ORDER for skin in skins_by_rarity[rarity]
      ]

      # Determine the maximum possible size for the skins
      total_padding_width = padding * (columns - 1)
      max_skin_width = (width - total_padding_width) // columns
      max_skin_height = max_skin_width

      # Calculate the number of rows needed and adjust the skin size if possible
      rows = (len(ordered_skins) + columns - 1) // columns
      available_height = height + (max_skin_height + padding) * rows + 150
      max_skin_height = min(max_skin_height,
                            (available_height - total_padding_width) // rows)
      skin_width = skin_height = max_skin_height  # Ensure skins are square

      print(f"Calculated rows: {rows}, skin size: {skin_width}x{skin_height}")

      # Create a new image with a dark grey background
      img = Image.new('RGB',
                      (width, height + (skin_height + padding) * rows + 150),
                      (25, 25, 25))
      draw = ImageDraw.Draw(img)

      # Load fonts
      font_path = "arial.ttf"
      title_font = ImageFont.truetype(font_path, 40)  # Font size for title
      footer_font = ImageFont.truetype(font_path, 20)  # Font size for footer
      skin_font = ImageFont.truetype(font_path, 20)  # Font size for skin names

      # Draw the title
      title_text = f"Ramirez Skin Checker | {len(skins)} Items"
      title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
      title_width = title_bbox[2] - title_bbox[0]
      title_height = title_bbox[3] - title_bbox[1]
      draw.text(((width - title_width) / 2, 10),
                title_text,
                font=title_font,
                fill='white')

      # Adjust starting height for skins to account for the title
      start_height = 70

      async with aiohttp.ClientSession() as session:
        tasks = [
            Imaging.fetch_image(session,
                                skin.get('images', {}).get('icon'))
            for skin in ordered_skins if skin.get('images', {}).get('icon')
        ]
        images = await asyncio.gather(*tasks)

        # Iterate over the skins and add them to the image
        for i, skin in enumerate(ordered_skins):
          skin_img_url = skin.get('images', {}).get('icon')
          if not skin_img_url:
            print(f"Skin {i} does not have an image URL.")
            continue

          skin_img_data = images.pop(0)
          skin_img = Image.open(io.BytesIO(skin_img_data)).resize(
              (skin_width, skin_height))

          # Convert to RGBA if necessary
          if skin_img.mode != 'RGBA':
            skin_img = skin_img.convert('RGBA')

          x = (i % columns) * (skin_width + padding)
          y = start_height + (i // columns) * (skin_height + padding)

          # Get the appropriate background based on rarity
          rarity = skin.get('rarity', {}).get('value', 'common').lower()
          bg_path = RARITY_BACKGROUNDS.get(rarity,
                                           RARITY_BACKGROUNDS['common'])
          bg_img = Image.open(bg_path).resize((skin_width, skin_height))

          # Paste the background and skin image
          img.paste(bg_img, (x, y))
          img.paste(skin_img, (x, y), skin_img)

          # Draw the text background box
          text_box_height = int(skin_height / 4)
          text_box_y = y + skin_height - text_box_height
          draw.rectangle([(x, text_box_y), (x + skin_width, y + skin_height)],
                         fill=(0, 0, 0, 180))

          # Draw the skin name with dynamically adjusted font size
          skin_name = skin.get('name', 'Unknown')
          font = Imaging.fit_text(draw, skin_name, max_skin_width - 10,
                                  font_path, 20)
          text_x = x + (skin_width / 2)
          text_y = text_box_y + (text_box_height / 2
                                 )  # Center text vertically in the box
          draw.text((text_x, text_y),
                    skin_name,
                    font=font,
                    fill='white',
                    anchor="mm")

      # Draw the footer
      footer_text = f"Ramirez | Submitted by: {username}"
      footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
      footer_width = footer_bbox[2] - footer_bbox[0]
      footer_height = footer_bbox[3] - footer_bbox[1]
      draw.text(((width - footer_width) / 2, height +
                 (skin_height + padding) * rows + 100),
                footer_text,
                font=footer_font,
                fill='white')

      # Save the image to a file
      img.save(output_file_path, format='PNG')
      print(f"Image saved to {output_file_path}")

      return output_file_path
    except Exception as e:
      print(f"An error occurred: {e}")
      raise


# Ensure the export directory exists
if not os.path.exists('export'):
  os.makedirs('export')


async def query_cosmetics(userid, backendType):
  auths = Users.get(str(userid))
  url = f'https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{auths.get("account_id")}/client/QueryProfile?profileId=athena&rvn=-1'
  headers = {
      "Authorization": f"bearer {await Epic.authsToBearer(auths)}",
      "Content-Type": 'application/json'
  }

  response = await Request.post(url, headers=headers, json={})
  pChanges = response.get("profileChanges")[0].get("profile").get("items")
  cos = []
  for item in pChanges:
    if pChanges[item].get("templateId", "").__contains__(backendType):
      cos.append(pChanges[item]['templateId'].split(":")[-1])
  return cos


def Gather_Bulk(cosmeticids):
  cosmetics = []
  skins = Cosmetics.get_cosmetics()
  for cosmeticid in cosmeticids:
    for skin in skins:
      if skin['id'].lower() == cosmeticid.lower():
        cosmetics.append(skin)
        break
  return cosmetics


@bot.slash_command(
    name='skincheck',
    description='Shows You An Image Of Your Owned Cosmetic Items')
async def skincheck(inter: Interaction,
                    type: str = SlashOption(name='type',
                                            description='Type Of Cosmetic',
                                            choices={
                                                "Skins", "Emotes",
                                                "Backblings", "Pickaxes",
                                                "Gliders", "Contrails"
                                            })):
  typeget = {
      "Skins": "AthenaCharacter",
      "Emotes": "AthenaDance",
      "Backblings": "AthenaBackpack",
      "Pickaxes": "AthenaPickaxe",
      "Gliders": "AthenaGlider",
      "Contrails": "AthenaSkyDiveContrail"
  }
  type = typeget.get(type)
  Chnl = inter.channel
  todel = await inter.send("Generating The Image... Please Wait. Please note: If you have just one cosmetic, such as just the default skin, an image won't be sent.")
  print("Gathering skins.")
  skins = Gather_Bulk(await query_cosmetics(inter.user.id, type))
  print(f"Number of skins gathered: {len(skins)}")

  img_path = f'export/{inter.user.name}_skins.png'
  img = await Imaging.generate_skins_image(skins, img_path, inter.user.name)
  print(f"Image generated: {img}")

  file = nextcord.File(img_path, filename=f"{inter.user.name}_skins.png")
  embed = nextcord.Embed(title="Skin Check Result",
                         description="Here Is Your Image",
                         color=nextcord.Color.green())
  embed.set_image(url=f"attachment://{inter.user.name}_skins.png")
  embed.set_footer(text=footertext)    
  embed.set_author(name=Users.get(str(inter.user.id))['displayName'],
                   icon_url=await get_avatar(Users.get(str(inter.user.id))))
  print("Sending the embed.")
  await Chnl.send(embed=embed, file=file)
  await todel.delete()
  print("Embed sent.")

  # Delete the file after sending
  if os.path.exists(img_path):
    os.remove(img_path)
    print(f"Image {img_path} deleted.")


"""General Purpose Commands"""


@bot.slash_command(name='account')
async def account(inter):
  pass


@account.subcommand(name='anticheat',
                    description='View Your AntiCheat Provider')
async def anticheat(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await Epic.authsToBearer(auths)
  exchange_code = await Epic.get_exchange(bearer_token)
  url = "https://caldera-service-prod.ecosec.on.epicgames.com/caldera/api/v1/launcher/racp"
  djson = {
      "account_id": auths['account_id'],
      "exchange_code": exchange_code,
      "test_mode": False,
      "epic_app": "fortnite",
      "nvidia": False,
      "luna": False,
      "salmon": False
  }
  headers = {}
  response = await Request.post(url, headers=headers, json=djson)
  embed = nextcord.Embed(title='AntiCheat Provider',
                         description='Your AntiCheat Provider Is: ' +
                         response.get('provider'),
                         color=colors.green)
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  if response.get('provider') == 'EasyAntiCheatEOS':
    embed.set_thumbnail(url="https://easy.ac/en-US/opengraph-image.png")
  elif response.get("provider") == "BattlEye":
    embed.set_thumbnail(
        url=
        "https://www.battleye.com/wp-content/themes/battleye/images/logo-large.png"
    )
  await inter.send(embed=embed)


@account.subcommand(
    name='page',
    description=
    'Gives You A Link To Epic Games Account Page For The Selected Account')
async def account_page(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  accounturl = 'https://www.epicgames.com/id/exchange?exchangeCode=' + await Epic.get_exchange(
      await Epic.authsToBearer(auths))

  embed = nextcord.Embed(title='Account Page',
                         description='Expires In 5 Minutes',
                         color=colors.green)
  view = nextcord.ui.View()
  view.add_item(
      nextcord.ui.Button(label='Account Page', url=accounturl, emoji='🔗'))
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed, view=view, ephemeral=True)


@account.subcommand(name='summary',
                    description='Shows A Summary Of Your Account')
async def slash_account_summary(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await Epic.authsToBearer(auths)
  url = 'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/' + auths[
      'account_id']

  headers = {"Authorization": f"Bearer {bearer_token}"}

  response = await Request.get(url, headers=headers)
  embed = nextcord.Embed(title='Account Summary',
                         description='Here Is Your Account Summary',
                         color=colors.green)
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  embed.add_field(name='Account ID', value=response.get('id'), inline=False)
  embed.add_field(name='Account Name',
                  value=response.get('displayName'),
                  inline=False)
  embed.add_field(name='Account Email',
                  value=response.get('email'),
                  inline=False)
  embed.add_field(name='Account Country',
                  value=response.get('country'),
                  inline=False)
  embed.add_field(name='Can Update Display Name',
                  value=str(response.get('canUpdateDisplayName')),
                  inline=False)
  embed.add_field(name='Last Display Name Update',
                  value=response.get('lastDisplayNameChange'),
                  inline=False)
  embed.add_field(
      name='Name',
      value=str(response.get('name', 'None')) +
      (" " +
       str(response.get('lastName')) if response.get('lastName') else ''),
      inline=False)
  embed.add_field(name='Phone Number',
                  value='||' + response.get('phoneNumber', 'None') + '||',
                  inline=False)

  await inter.send(embed=embed, ephemeral=True)


async def get_launcher_token(auths: dict):
  bearer = await Epic.authsToBearer(auths)
  exchange_code = await Epic.get_exchange(bearer)
  token_url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
  headers = {
      "Authorization": Vars.LAUNCHERTOKEN,
      "Content-Type": "application/x-www-form-urlencoded"
  }
  data = "grant_type=exchange_code&exchange_code=" + exchange_code + "&token_type=eg1"
  response = await Request.post(token_url, headers=headers, data=data)
  return response.get('access_token')


@account.subcommand(name='view-playtime', description='View Your Playtime')
async def slash_view_playtime(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await get_launcher_token(auths)
  url = f'https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/{auths.get("account_id")}/all'
  headers = {"Authorization": f"Bearer {bearer_token}"}
  response = await Request.get(url, headers=headers)
  fnstats = {}
  for game in response:
    if game.get("artifactId") == "Fortnite":
      fnstats = game
      break

  embed = nextcord.Embed(
      title='Playtime',
      description=
      f'You\'ve Played Fortnite For: {str(round(int(fnstats.get("totalTime")) / 60 / 60))} Hours!',
      color=colors.green)
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


import uuid
from datetime import datetime, timedelta, timezone


@account.subcommand(name='add-playtime',
                    description='Adds Playtime To Your Account')
async def slash_add_playtime(inter: Interaction,
                             hours: int = SlashOption(
                                 name='hours',
                                 description='Amount Of Hours To Add',
                                 required=True)):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await get_launcher_token(auths)
  url = f'https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/{auths["account_id"]}'
  headers = {"Authorization": f"Bearer {bearer_token}"}
  machineId = str(uuid.uuid4())
  duration = hours * 60 * 60 * 1000
  # Get the current time and calculate the start time
  utc_now = datetime.now(timezone.utc)
  endTime = utc_now.isoformat().replace("+00:00", "Z")
  startTime = (utc_now - timedelta(milliseconds=duration)).isoformat().replace(
      "+00:00", "Z")
  body = {
      "machineId": machineId,
      "artifactId": "Fortnite",
      "startTime": startTime,
      "endTime": endTime,
      "startSegment": True,
      "endSegment": True
  }

  response = await Request.put(url, headers=headers, json=body)
  print(str(response))
  embed = nextcord.Embed(
      title='Playtime',
      description=f'You\'ve Added {hours} Hours To Your Playtime!',
      color=colors.green)
  embed.set_footer(text=footertext)
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))

  await inter.send(embed=embed)


@bot.slash_command(name="free_games",
                   description="Get information about free games")
async def free_games(interaction: nextcord.Interaction):
  try:

    response = requests.get(
        'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions'
    )
    jsonData = response.json()['data']['Catalog']['searchStore']['elements']

    freeGamesInfo = [{
        'name':
        game['title'],
        'description':
        game.get('description', 'No description available.'),
        'image':
        game['keyImages'][0]['url'] if game['keyImages'] else '',
    } for game in jsonData]

    embed = nextcord.Embed(
        color=nextcord.Color.yellow(),
        title='Free Games Information',
        description=
        'Simplified information about currently available free games:',
    )

    for game in freeGamesInfo:
      embed.add_field(name=game['name'],
                      value=f"**Description:** {game['description']}",
                      inline=False)

    if freeGamesInfo and freeGamesInfo[0]['image']:
      embed.set_image(url=freeGamesInfo[0]['image'])

    embed.set_footer(text=footertext)    

    
    await interaction.response.send_message(embed=embed)
  except requests.RequestException as e:
    print(f'Failed to fetch free games information: {e}')
    await interaction.response.send_message(
        f'Failed to fetch free games information. {str(e)}')


@bot.slash_command(
    name='fortnite-island',
    description='Fetch information about a Fortnite creative island.')
async def fortnite_island(inter, code: str):
  api_key = 'f3623e49-a9dca4ba-7818244d-329400ae'
  print(f"Command triggered by {inter.user} with code: {code}")

  try:
    async with aiohttp.ClientSession() as session:
      url = f'https://fortniteapi.io/v1/creative/island?code={code}'
      headers = {'Authorization': api_key}
      async with session.get(url, headers=headers) as response:
        print(f"HTTP Status Code: {response.status}")

        if response.status == 200:
          data = await response.json()
          print(f"Response Data: {data}")

          if 'result' in data and data['result']:
            island = data['island']

            embed = nextcord.Embed(color=0x3498DB,
                                   title=island['title'],
                                   description=island['description'])
            embed.add_field(name='Code', value=island['code'], inline=False)
            embed.add_field(name='Type', value=island['type'], inline=False)
            embed.add_field(name='Latest Version',
                            value=island['latestVersion'],
                            inline=False)
            embed.add_field(name='Island Type',
                            value=island.get('islandType', 'Not available'),
                            inline=False)
            embed.add_field(name='Published Date',
                            value=island['publishedDate'],
                            inline=False)
            embed.add_field(name='Created Date',
                            value=island['createdDate'],
                            inline=False)
            embed.add_field(name='Introduction',
                            value=island['introduction'],
                            inline=False)
            embed.add_field(name='Creator',
                            value=island['creator'],
                            inline=False)
            embed.add_field(name='Creator Code',
                            value=island['creatorCode'],
                            inline=False)
            embed.add_field(name='Tags',
                            value=', '.join(island['tags']),
                            inline=False)
            embed.add_field(name='Status',
                            value=island['status'],
                            inline=False)
            embed.add_field(name='Video ID',
                            value=island.get('videoID', 'Not available'),
                            inline=False)
            if island.get('promotion_image'):
              embed.set_image(url=island['promotion_image'])

            await inter.send(embed=embed)
          else:
            await inter.send(
                'Failed to fetch island data. Unexpected response format or no result.'
            )
        else:
          await inter.send(
              f'Failed to fetch island data. HTTP Status Code: {response.status}'
          )
  except Exception as e:
    print(f"Error occurred: {e}")
    await inter.send(f'Failed to fetch island data: {str(e)}')


weaponsAPI = 'https://api-xji1.onrender.com/api/v1/weapons'


@bot.slash_command(description="Search Fortnite weapon by name")
async def search_weapon(interaction: nextcord.Interaction, name: str):
  weaponName = name

  try:

    loading_message = await interaction.response.send_message('**Loading...**',
                                                              ephemeral=True)

    response = requests.get(weaponsAPI)
    data = response.json()

    if data and 'weapons' in data:
      weapons = [
          weapon for weapon in data['weapons']
          if weaponName.lower() in weapon['name'].lower()
      ]

      if not weapons:

        await interaction.edit_original_message(
            content=f'No weapons found with the name "{weaponName}".')
      else:
        weapon = weapons[0]
        embed = nextcord.Embed(title='Fortnite Weapons',
                               description=f'Results for "{weaponName}"',
                               color=nextcord.Color.gold())
        embed.add_field(name=weapon['name'],
                        value=weapon['description'],
                        inline=False)
        embed.add_field(name='Vaulted',
                        value='False' if weapon['enabled'] else 'True',
                        inline=False)
        embed.add_field(name='Rarity', value=weapon['rarity'], inline=False)
        embed.add_field(
            name='Stats',
            value=
            (f"Damage Per Bullet: {weapon['mainStats']['DmgPB']}\n"
             f"Firing Rate: {weapon['mainStats']['FiringRate']}\n"
             f"Clip Size: {weapon['mainStats']['ClipSize']}\n"
             f"DamageZone Critical: {weapon['mainStats']['DamageZone_Critical']}"
             ),
            inline=False)
        embed.add_field(name='Tags',
                        value='\n'.join(weapon['gameplayTags']),
                        inline=False)
        embed.add_field(name='ID', value=weapon['id'], inline=False)
        embed.set_thumbnail(url=weapon['images']['icon'])

        await interaction.edit_original_message(content=None, embed=embed)
    else:
      print('Unexpected response format:', data)
      await interaction.edit_original_message(
          content='Failed to fetch Fortnite weapons. Unexpected response format.'
      )
  except requests.RequestException as error:
    print('Failed to fetch Fortnite weapons:', error)
    await interaction.edit_original_message(
        content='Failed to fetch Fortnite weapons. Please try again later.')


@bot.slash_command(
    description="Get information about a Fortnite player's profile")
async def player_stats(interaction: nextcord.Interaction, player_name: str):
  try:
    response = requests.get(
        f'https://fortnite-api.com/v2/stats/br/v2?name={player_name}',
        headers={'Authorization': '31c0519b-4651-4f74-a991-4e67db6928da'})
    origMsg = await interaction.send("**Loading...**")
    if response.status_code == 200:
      print(response.text)
      data = response.json().get('data')
      account = data.get('account')
      battlePass = data.get('battlePass')
      stats = data.get('stats').get('all').get('overall')

      if battlePass:
        embed = nextcord.Embed(
            title=f'Fortnite Profile - {account.get("name")}',
            description=f'Player ID: {account.get("id")}',
            color=nextcord.Color.blue(),
            timestamp=nextcord.utils.utcnow())
        embed.set_image(url='https://fortnite.gg/img/assets/icons/1924.jpg')
        embed.add_field(name='Battle Pass Level',
                        value=battlePass.get('level'),
                        inline=True)
        embed.add_field(name='Battle Pass Progress',
                        value=f'{battlePass.get("progress")}% ',
                        inline=True)
        embed.add_field(
            name='Overall Stats',
            value=(f"Score: {stats.get('score')}\n"
                   f"Score Per Min: {stats.get('scorePerMin')}\n"
                   f"Score Per Match: {stats.get('scorePerMatch')}\n"
                   f"Wins: {stats.get('wins')}\n"
                   f"Top 3: {stats.get('top3')}\n"
                   f"Top 5: {stats.get('top5')}\n"
                   f"Top 6: {stats.get('top6')}\n"
                   f"Top 10: {stats.get('top10')}\n"
                   f"Top 12: {stats.get('top12')}\n"
                   f"Top 25: {stats.get('top25')}\n"
                   f"Kills: {stats.get('kills')}\n"
                   f"Kills Per Min: {stats.get('killsPerMin')}\n"
                   f"Kills Per Match: {stats.get('killsPerMatch')}\n"
                   f"Deaths: {stats.get('deaths')}\n"
                   f"K/D Ratio: {stats.get('kd')}\n"
                   f"Matches Played: {stats.get('matches')}\n"
                   f"Win Rate: {stats.get('winRate')}%\n"
                   f"Minutes Played: {stats.get('minutesPlayed')}\n"
                   f"Players Outlived: {stats.get('playersOutlived')}\n"))

        await origMsg.edit("", embed=embed)
      else:
        await origMsg.edit(
            content='Battle Pass information not available for this player.')
    else:
      await interaction.response.send_message(
          content='Error retrieving profile information.', ephemeral=False)
  except requests.RequestException as error:
    print('Error:', error)
    await interaction.response.send_message(
        content='An error occurred while processing your request.',
        ephemeral=False)


@account.subcommand(
    name='launch',
    description='Launch Fortnite Windows From Your Current Account')
async def launch(
    inter: Interaction,
    fortnite_path:
    str = "C:\\Program Files\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64",
    additional_args: str = ""):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await Epic.authsToBearer(auths)
  exchange_code = await Epic.get_exchange(bearer_token)

  embed = Embed(
      title=f'Launch Fortnite As {auths.get("displayName")}',
      description=
      'Please copy the command into Command Prompt (cmd.exe) and press enter. Valid for 5 minutes or until it is used.',
      color=colors.green)
  command = f"start /d {fortnite_path} FortniteLauncher.exe -AUTH_LOGIN=unused -AUTH_PASSWORD={exchange_code} -AUTH_TYPE=exchangecode -epicapp=Fortnite -epicenv=Prod -EpicPortal -epicuserid={auths['account_id']} {additional_args}"
  embed.add_field(name='💻 Command', value=f'```bat\n{command}```')
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed, ephemeral=True)


@account.subcommand(
    name='match-info',
    description='Get Match Info Such As Amount Of Real Players')
async def match_info(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await Epic.authsToBearer(auths)
  url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/matchmaking/session/findPlayer/{auths.get('account_id')}"
  headers = {"Authorization": f"Bearer {bearer_token}"}
  response = await Request.get(url, headers=headers)
  print(str(response))
  try:
    response = response[0]
  except:
    return await inter.send(embed=Embed(
        color=colors.red,
        title='Not In A Match',
        description='You Need To Be In A Match To Use This Command!'))
  embed = Embed(title='Match Info',
                description=f'I have successfully found your current session.',
                color=colors.green)
  embed.add_field(name='Real Players',
                  value=str(response.get('totalPlayers')),
                  inline=False)
  embed.add_field(name='Server IP',
                  value=str(response.get('serverAddress')),
                  inline=False)
  embed.add_field(name='Session ID',
                  value=str(response.get('id')),
                  inline=False)
  embed.add_field(name='Bucket ID',
                  value=str(response.get('attributes').get("BUCKET_s")),
                  inline=False)
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


@account.subcommand(name='stats',
                    description='Shows Your Level, Battle Stars, V-Bucks, etc')
async def account_stats(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")
  auths = Users.get(str(inter.user.id))
  bearer_token = await Epic.authsToBearer(auths)
  url = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{auths.get('account_id')}/client/QueryProfile?profileId=athena&rvn=-1"
  headers = {"Authorization": f"Bearer {bearer_token}"}
  response = await Request.post(url, headers=headers, json={})
  rresponse = await Request.post(url.replace('profileId=athena',
                                             'profileId=common_core'),
                                 json={},
                                 headers=headers)

  embed = Embed(title='Account Stats',
                description='Here Is Your Account Stats',
                color=colors.green)
  level = str(
      response["profileChanges"][0]["profile"]["stats"]["attributes"]["level"])
  acountLevel = str(response["profileChanges"][0]["profile"]["stats"]
                    ["attributes"]["accountLevel"])
  battleStar = str(response["profileChanges"][0]["profile"]["stats"]
                   ["attributes"].get("battlestars", "0"))
  vbuck = str(rresponse["profileChanges"][0]['profile']['items'].get(
      "Currency:MtxPurchased", {"quantity": "None"})['quantity'])
  embed.add_field(name="Level", value=level, inline=False)
  embed.add_field(name="Account Level", value=acountLevel, inline=False)
  embed.add_field(name="Battle Stars", value=battleStar, inline=False)
  embed.add_field(name="V-Bucks (Purchased)", value=vbuck, inline=False)
  embed.set_footer(text=footertext)    
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))
  await inter.send(embed=embed)


async def ac_clbk(inter: Interaction, val: str):
  return [
      cosmetic['name'] for cosmetic in Cosmetics.get_cosmetics()
      if val.lower() in cosmetic['name'].lower()
  ][0:25]


@bot.slash_command(name="cosmetic", description="Shows info for a cosmetic")
async def icon(inter,
               item: str = SlashOption(
                   name='item',
                   description='The item you want to search for',
                   required=True,
                   autocomplete=True,
                   autocomplete_callback=ac_clbk)):
  sub_dict = await Cosmetics.find_async(item)
  embed = Embed(title=sub_dict['name'],
                description=sub_dict['description'],
                color=colors.blue)
  embed.add_field(name='ID', value=sub_dict['id'])
  embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
  embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
  #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")

  if sub_dict['introduction'] == None:
    pass
  else:
    embed.add_field(name='Introduction',
                    value=sub_dict['introduction']['text'])
    embed.set_image(
        url=
        f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png"
    )
    embed.set_thumbnail(
        url=
        f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/featured.png"
    )
    embed.set_footer(text=footertext)    
    message = await inter.send(embed=embed)


@account.subcommand(name='playtime-ultra',
                    description='Adds A Lot Of Hours To Your Playtime')
async def playtime_ultra(inter: Interaction):
  if not Users.get(str(inter.user.id)):
    return await inter.send(
        "You Need to Be Logged In!\nPlease Use `/login` To Solve This.")

  auths = Users.get(str(inter.user.id))
  bearer_token = await get_launcher_token(auths)
  url = f'https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/{auths.get("account_id")}'
  headers = {"Authorization": f"Bearer {bearer_token}"}
  currentPlaytime = 0
  increment = 699
  maxPlaytime = 1000000
  await inter.response.defer()
  while (currentPlaytime < maxPlaytime):
    machineId = str(uuid.uuid4())
    utc_now = datetime.now(timezone.utc)
    endTime = utc_now.isoformat().replace("+00:00", "Z")
    duration = increment * 60 * 60000
    startTime = (utc_now -
                 timedelta(milliseconds=duration)).isoformat().replace(
                     "+00:00", "Z")

    body = {
        "machineId": machineId,
        "artifactId": "Fortnite",
        "startTime": startTime,
        "endTime": endTime,
        "startSegment": True,
        "endSegment": True
    }

    response = await Request.put(url, headers=headers, json=body)
    #print(str(response))
    currentPlaytime += increment
  embed = nextcord.Embed(
      title='Playtime',
      description=f'You\'ve Added A Lot Of Hours To Your Playtime!',
      color=colors.green)
  embed.set_footer(text=footertext)
  embed.set_author(name=auths['displayName'], icon_url=await get_avatar(auths))

  await inter.send(embed=embed)

if __name__ == '__main__':
  Cosmetics.Initiate()
  bot.run(str(os.getenv("TOKEN")))
