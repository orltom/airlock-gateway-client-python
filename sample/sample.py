from client.resourceclient import VirtualHostClient, MappingClient, BackendGroupClient, ConfigurationClient, \
    AuthenticationClient
from client.httpclient import DefaultHttpClient

token = "...."
host_url = "http://localhost:8080"
http_client = DefaultHttpClient(host_url)


def integrate_application():
    try:
        auth_client = AuthenticationClient(
            http_client=http_client,
            token=token
        )
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
