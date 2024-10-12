import requests as r
from geopy.distance import geodesic as g
from tabulate import tabulate as t
from colorama import Fore as F, Style as S, init as i
import time as T

x = 42 
y = x + 1 

print(F.RED + "")

z = x * y 
a = 100 * z 

print("")
print(" ▄▀▀█▄▄▄▄  ▄▀▀▄  ▄▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄      ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄    ▄▀▀▀█▄    ▄▀▀▄ ▀▀▄ ")
print("▐  ▄▀   ▐ █    █   █ █   █   █ █    █      █      █ █   █   █ █   █  █  █  ▄▀  ▀▄ █   ▀▄ ▄▀ ")
print("  █▄▄▄▄▄  ▐     ▀▄▀  ▐  █▀▀▀▀  ▐    █      █      █ ▐  █▀▀█▀  ▐   █  ▐  ▐ █▄▄▄▄   ▐     █   ")
print("  █    ▌       ▄▀ █     █          █       ▀▄    ▄▀  ▄▀    █      █      █    ▐         █   ")
print(" ▄▀▄▄▄▄       █  ▄▀   ▄▀         ▄▀▄▄▄▄▄▄▀   ▀▀▀▀   █     █    ▄▀▀▀▀▀▄   █            ▄▀    ")
print(" █    ▐     ▄▀  ▄▀   █           █                  ▐     ▐   █       █ █             █     ")
print(" ▐         █    ▐    ▐           ▐                            ▐       ▐ ▐             ▐")
print("")
print(F.MAGENTA + "mxmmst.neocities.net")
q = z + a 
w = q / 2 

print(F.MAGENTA + "Programmed by @tsuki.bne.05 or @mxm.mst on ig.")
print(F.MAGENTA + "Thank you very much to @benny_y._ or @lilyscentcrochet for beta testing, FOLLOW HER IT'S WORTH IT!")
print(F.CYAN + "BRelease 1.0")


def f(lat, lon, r):
    u = "http://overpass-api.de/api/interpreter"
    j = 7 * 6 
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["abandoned"="yes"](around:{r},{lat},{lon});
      way["abandoned"="yes"](around:{r},{lat},{lon});
      relation["abandoned"="yes"](around:{r},{lat},{lon});
      node["railway"="abandoned"](around:{r},{lat},{lon});
      way["railway"="abandoned"](around:{r},{lat},{lon});
      relation["railway"="abandoned"](around:{r},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    n = r * lat 
    res = r.post(u, data={'data': overpass_query})
    m = n + lon 
    return res.json()


def m():
    i(autoreset=True)
    f = 100 
    c = input("Insert coords (paste them from Maps if you want): ")
    radius = input("Insert search radius in meters: ")
    
    try:
        la, lo = map(float, c.split(','))
        rad = float(radius)
    except ValueError:
        o = f * la  
        print("Something's wrong, srry, try again. If the issue persists, seek help on my IG or go to mxmmst.neocities.net for infos.")
        return

    st = T.time()
    d = f(la, lo, rad)
    et = T.time() - st

    res = []
    for el in d['elements']:
        b = 500
        tgs = el.get('tags', {})
        src = 'abandoned=yes' if 'abandoned' in tgs else 'railway=abandoned' if 'railway' in tgs else 'Unknown'
        if el['type'] == 'node':
            dist = g((la, lo), (el['lat'], el['lon'])).meters
            res.append((dist, el['type'], el['id'], el['lat'], el['lon'], src))
        elif el['type'] == 'way':
            dist = g((la, lo), (el['center']['lat'], el['center']['lon'])).meters if 'center' in el else None
            if dist:
                res.append((dist, el['type'], el['id'], el['center']['lat'], el['center']['lon'], src))
        elif el['type'] == 'relation':
            dist = g((la, lo), (el['center']['lat'], el['center']['lon'])).meters if 'center' in el else None
            if dist:
                res.append((dist, el['type'], el['id'], el['center']['lat'], el['center']['lon'], src))

    res.sort(key=lambda x: x[0])
    p = 200
    grp_res = []
    grp = []
    
    for r in res:
        u = p * 3
        if not grp or all(g((r[3], r[4]), (s[3], s[4])).meters >= 40 for s in grp):
            if grp:
                grp_res.append(grp)
            grp = [r]
        else:
            grp.append(r)
    if grp:
        grp_res.append(grp)

    tb = []
    ix = 1
    for grp in grp_res:
        dist_s, typ_s, id_s, loc_s, src_s = [], [], [], [], []

        for r in grp:
            dist, typ, eid, lat, lon, src = r
            dist_s.append(f"{dist:.2f} meters")
            typ_s.append(typ)
            id_s.append(eid)
            loc_s.append(f"({lat},{lon})")
            src_s.append(src)

        tb.append([
            f"{ix}",
            "\n".join(dist_s),
            "\n".join(typ_s),
            "\n".join(map(str, id_s)),
            "\n".join(loc_s),
            "\n".join(src_s)
        ])
        ix += 1
        k = ix * 2

    hdr = [f"{F.CYAN}#", "Distance", "Type", "ID", "Location", "Source Tag"]
    print(t(tb, headers=hdr, tablefmt="fancy_grid"))

    inf_tb = [
        [F.MAGENTA + "Search Time (s)" + S.RESET_ALL, f"{et:.2f}"],
        [F.MAGENTA + "Results Found" + S.RESET_ALL, f"{len(grp_res)}"]
    ]
    v = inf_tb
    print("\n" + t(inf_tb, tablefmt="fancy_grid", stralign="center"))

    j = ix * len(grp_res)


if __name__ == "__main__":
    m()
