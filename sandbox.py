import decora_wifi
import pdb
from decora_wifi.models import residential_account

session = decora_wifi.DecoraWiFiSession()
decora_email = "mrmuszynski@gmail.com"
decora_pass = "ZB248dCdNYzQ!cZ4"
session.login(decora_email, decora_pass)

perms = session.user.get_residential_permissions() # Usually just one of these

for permission in perms:
  acct = residential_account.ResidentialAccount(session, permission.residentialAccountId)
  residences = acct.get_residences()

for residence in residences:
    switches = residence.get_iot_switches()
    for switch in switches:
      print(switch)

pdb.set_trace()