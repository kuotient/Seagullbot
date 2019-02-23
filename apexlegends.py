from apex_legends import ApexLegends

apex = ApexLegends("f1b30488-6b83-4295-9659-d9ef2a15c2fb")

def search(id):
    try:
        player = apex.player(id)
        return str(player)

    except:
        return -1