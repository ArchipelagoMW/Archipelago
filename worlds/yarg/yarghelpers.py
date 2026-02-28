def instnamechange(input):
    #Swaps between the 2 formats of intsrument names
    if input == "guitar5F":
        return "Guitar"
    if input == "bass5F":
        return "Bass"
    if input == "rhythm5F":
        return "Rhythm"
    if input == "drums":
        return "Drums"
    if input == "keys5F":
        return "Keys"
    if input == "keysPro":
        return "Pro Keys"
    if input == "vocals":
        return "Vocals"
    if input == "harmony2":
        return "2 Part Harmony"
    if input == "harmony3":
        return "3 Part Harmony"
    
    
    if input == "Guitar":
        return "guitar5F"
    if input == "Bass":
        return "bass5f"
    if input == "Rhythm":
        return "rhythm5F"
    if input == "Drums":
        return "drums"
    if input == "Keys":
        return "keys5F"
    if input == "Pro Keys":
        return "keysPro"
    if input == "Vocals":
        return "vocals"
    if input == "2 Part Harmony":
        return "harmony2"
    if input == "3 Part Harmony":
        return "harmony3"

def itemnamefromindex(index):
    from .songinfo import Songs
    longnames = False

    if longnames == False:
        return f'"{(Songs.get(index)).songname}" by {(Songs.get(index)).artistname}'

    if longnames == True:
        return f'"{(Songs.get(index)).songname}" by {(Songs.get(index)).artistname} from {(Songs.get(index)).source}'