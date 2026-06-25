import requests
from geopy.distance import geodesic
from tabulate import tabulate
from colorama import Fore, Style, init
import time

print(Fore.RED + "")

print("")
print(" ▄▀▀█▄▄▄▄  ▄▀▀▄  ▄▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄      ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄    ▄▀▀▀█▄    ▄▀▀▄ ▀▀▄ ")
print("▐  ▄▀   ▐ █    █   █ █   █   █ █    █      █      █ █   █   █ █   █  █  █  ▄▀  ▀▄ █   ▀▄ ▄▀ ")
print("  █▄▄▄▄▄  ▐     ▀▄▀  ▐  █▀▀▀▀  ▐    █      █      █ ▐  █▀▀█▀  ▐   █  ▐  ▐ █▄▄▄▄   ▐     █   ")
print("  █    ▌       ▄▀ █     █          █       ▀▄    ▄▀  ▄▀    █      █      █    ▐         █   ")
print(" ▄▀▄▄▄▄       █  ▄▀   ▄▀         ▄▀▄▄▄▄▄▄▀   ▀▀▀▀   █     █    ▄▀▀▀▀▀▄   █            ▄▀    ")
print(" █    ▐     ▄▀  ▄▀   █           █                  ▐     ▐   █       █ █             █     ")
print(" ▐         █    ▐    ▐           ▐                            ▐       ▐ ▐             ▐")
print("")
print(Fore.MAGENTA + "Scans for abandoned railways and buildings, runes and everything urbex.")
print(Fore.YELLOW + "made with <3 by @tsuki.bne.05 on ig")
print(Fore.RED + "Beta 0.8.3")

def find_abandoned_places(lat, lon, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["abandoned"="yes"](around:{radius},{lat},{lon});
      way["abandoned"="yes"](around:{radius},{lat},{lon});
      relation["abandoned"="yes"](around:{radius},{lat},{lon});
      node["railway"="abandoned"](around:{radius},{lat},{lon});
      way["railway"="abandoned"](around:{radius},{lat},{lon});
      relation["railway"="abandoned"](around:{radius},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.post(overpass_url, data={'data': overpass_query})
    return response.json()

def main():
    init(autoreset=True)
    coordinates = input("Insert coords (lat, long): ")
    radius = input("Insert radius:  ")
    
    try:
        lat, lon = map(float, coordinates.split(','))
        radius = float(radius)
    except ValueError:
        print("Coords and ray must be numbers, retry.")
        return

    start_time = time.time()
    data = find_abandoned_places(lat, lon, radius)
    search_time = time.time() - start_time

    results = []
    for element in data['elements']:
        tags = element.get('tags', {})
        source_tag = 'abandoned=yes' if 'abandoned' in tags else 'railway=abandoned' if 'railway' in tags else 'unknown'
        if element['type'] == 'node':
            distance = geodesic((lat, lon), (element['lat'], element['lon'])).meters
            results.append((distance, element['lat'], element['lon'], source_tag))
        elif element['type'] == 'way':
            distance = geodesic((lat, lon), (element['center']['lat'], element['center']['lon'])).meters if 'center' in element else None
            if distance:
                results.append((distance, element['center']['lat'], element['center']['lon'], source_tag))
        elif element['type'] == 'relation':
            distance = geodesic((lat, lon), (element['center']['lat'], element['center']['lon'])).meters if 'center' in element else None
            if distance:
                results.append((distance, element['center']['lat'], element['center']['lon'], source_tag))

    results.sort(key=lambda x: x[0])
    grouped_results = []
    group = []
    
    for result in results:
        if not group or all(geodesic((result[1], result[2]), (r[1], r[2])).meters >= 40 for r in group):
            if group:
                grouped_results.append(group)
            group = [result]
        else:
            group.append(result)
    if group:
        grouped_results.append(group)
    
    table = []
    idx = 1
    for group in grouped_results:
        distance_strs = []
        location_strs = []
        source_tags_strs = []

        for result in group:
            distance, lat, lon, source_tag = result
            distance_strs.append(f"{distance:.2f} meters")
            location_strs.append(f"({lat},{lon})")
            if source_tag != 'unknown':
                source_tags_strs.append(source_tag)

        table.append([
            f"{idx}",
            "\n".join(distance_strs),
            "\n".join(location_strs),
            "\n".join(source_tags_strs)
        ])
        idx += 1

    headers = [f"{Fore.CYAN}#", "Distance", "Coordinates", "Tag"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    info_table = [
        [Fore.MAGENTA + "Search Time (s)" + Style.RESET_ALL, f"{search_time:.2f}"],
        [Fore.MAGENTA + "Results Found" + Style.RESET_ALL, f"{len(grouped_results)}"]
    ]
    print("\n" + tabulate(info_table, tablefmt="fancy_grid", stralign="center"))

if __name__ == "__main__":
    main()
