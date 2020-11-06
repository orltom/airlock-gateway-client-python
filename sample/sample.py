from src.resourceclient import *
from src.httpclient import *

token = "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiZGlyIn0..gae_uBITEwOzFNq54BJBww.IBSY-TDvpktMCTF6KgRCHTebiYyNuSVOVbOw6XVkF-ek7eG-OJ7B7Q5CoYLZEZFju-74LQLWSO0P8js4eiegGufYFLqqJQmoH-p1cT_m2Mv808ZzR9TfoTDDLKb9SXXSlnpWFnF9BwYIptFVKXICVF_8uU1FlGz9Eyi5zu6arXZ7tQXi-06M3T_ei7G0rTnMQ29MkjgxxjWtNn2MOgj4M27bPC-9wiLHniONF4av54tehe9cAeut_7dsfXo139Qvh6WZp8j6QdqO3NCSCl-UlUYIwHY_YeBooTyT2q0AiTGOQgztj-fa8NoenhG0dycrWwPha5gCHkwM7wPYu5Gxf3_IhjKesSnoTCwEQzrjUUj4RaIZ3VuuseXr-j-sx_9YyX2--pnLJ16KkeEojy4Rp3y0fdkzmlIL5lo6yTQSfBwjYf2kJcL_rIfb3DpA_o36U2E6mYN3oHAPWQW1mOhqnPAxbtuvJ9kG2Sfds3ozinuXzcj-lPCmWY-vEui_32xIBi1mYAmzbxFzM2dQRUl_Y1fCP8lC7gCdV7V0D1icOeo.Jfw7wqqC60bz_kR0XNHMGYGJYN69OtpKEyQ-gET2NOQ	"
http_client = HttpClient("http://al-waf-docker-local-stack:8080")
session = SessionClient(http_client, token)

try:
    session.create()
    config_client = ConfigurationClient(http_client)
    config_client.load_current_active()
    virtual_host_client = VirtualHostClient(http_client)
    vh = virtual_host_client.create(data="""
    {
      "data" : {
        "type" : "virtual-host",
        "attributes" : {
          "name" : "hugo",
          "hostName" : "hugo.example.com",
          "networkInterface" : {
            "externalLogicalInterfaceName" : "NIC0",
            "ipV4Address" : "87.239.214.12/24",
            "http" : {
              "enabled" : true,
              "port" : 80,
              "httpsRedirectEnforced" : false
            }
          }
        }
      }
    }
    """)
    vhId = vh.json()['data']['id']
    mapping_client = MappingClient(http_client)
    m = mapping_client.create(data="""
    {
        "data" : {
            "type" : "mapping",
            "attributes" : {
              "name" : "hugo",
              "entryPath" : {
                "value" : "/"
              },
              "backendPath" : "/"
            }
        }
    }
    """)
    mId = m.json()['data']['id']
    mapping_client.connect_virtual_host(mId, vhId)
    config_client.save("hugo")
except Exception as e:
    print("unexpected error occurs.", e)
    exit(1)
finally:
    session.terminate()
