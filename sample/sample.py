from client.resourceclient import VirtualHostClient, MappingClient, BackendGroupClient, ConfigurationClient, AuthenticationClient
from client.httpclient import DefaultHttpClient

token = "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiZGlyIn0..gae_uBITEwOzFNq54BJBww.IBSY" \
        "-TDvpktMCTF6KgRCHTebiYyNuSVOVbOw6XVkF-ek7eG-OJ7B7Q5CoYLZEZFju-74LQLWSO0P8js4eiegGufYFLqqJQmoH" \
        "-p1cT_m2Mv808ZzR9TfoTDDLKb9SXXSlnpWFnF9BwYIptFVKXICVF_8uU1FlGz9Eyi5zu6arXZ7tQXi" \
        "-06M3T_ei7G0rTnMQ29MkjgxxjWtNn2MOgj4M27bPC-9wiLHniONF4av54tehe9cAeut_7dsfXo139Qvh6WZp8j6QdqO3NCSCl" \
        "-UlUYIwHY_YeBooTyT2q0AiTGOQgztj-fa8NoenhG0dycrWwPha5gCHkwM7wPYu5Gxf3_IhjKesSnoTCwEQzrjUUj4RaIZ3VuuseXr-j" \
        "-sx_9YyX2--pnLJ16KkeEojy4Rp3y0fdkzmlIL5lo6yTQSfBwjYf2kJcL_rIfb3DpA_o36U2E6mYN3oHAPWQW1mOhqnPAxbtuvJ9k" \
        "G2Sfds3ozinuXzcj-lPCmWY-vEui_32xIBi1mYAmzbxFzM2dQRUl_Y1fCP8lC7gCdV7V0D1icOeo.Jfw7wqqC60bz_kR0XNHMGYGJ" \
        "YN69OtpKEyQ-gET2NOQ "
http_client = DefaultHttpClient("http://al-waf-docker-local-stack:8080")


def main():
    try:
        auth_client = AuthenticationClient(http_client=http_client, token=token)
        session = auth_client.create()
        config_client = ConfigurationClient(session)
        config_client.load_current_active()
        virtual_host_client = VirtualHostClient(session)
        vh = virtual_host_client.create("""
        {
          "data" : {
            "type" : "virtual-host",
            "attributes" : {
              "name" : "example.cm",
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
        vh_id = vh.json()['data']['id']
        mapping_client = MappingClient(session)
        m = mapping_client.create("""
        {
            "data" : {
                "type" : "mapping",
                "attributes" : {
                  "name" : "auth",
                  "entryPath" : {
                    "value" : "/"
                  },
                  "backendPath" : "/"
                }
            }
        }
        """)
        m_id = m.json()['data']['id']
        mapping_client.connect_virtual_host(m_id, vh_id)
        backend_group_client = BackendGroupClient(session)
        b = backend_group_client.create("""
        {
          "data" : {
            "type" : "back-end-group",
            "attributes" : {
              "name" : "tomcat",
              "backendHosts" : [ {
                "protocol" : "HTTP",
                "hostName" : "example.com",
                "port" : 80,
                "mode" : "ENABLED",
                "spare" : false,
                "weight" : 200
              } ]
            }
          }
        }
        """)
        b_id = b.json()['data']['id']
        mapping_client.connect_back_end_group(m_id, b_id)
        config_client.activate("sample: actvate")
    except Exception as e:
        print("unexpected error occurs.", e)
        exit(1)
    finally:
        if session:
            session.terminate()


main()
