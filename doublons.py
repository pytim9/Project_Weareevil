# Get weevil names
with open("data/names_model_has_seen.txt", "r", encoding="utf-8") as f:
    known_names = f.read().splitlines()

# Get unknonwn weevil names
with open("data/unknown_names.txt", "r", encoding="utf-8") as f:
    unknown_names = f.read().splitlines()

def find_doublons(known_names, unknown_names):
    doublons = []
    for name in known_names:
        if name in unknown_names:
            doublons.append(name)
    return doublons, len(doublons)

print(find_doublons(known_names, unknown_names))