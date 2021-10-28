from .tuls import flatten

def rect_center(coords):
    x1,y1 = coords[:2]
    x2,y2 = coords[4:-2]
    xt = (x1+x2)/2
    yt = (y1+y2)/2
    return [xt,yt]

def entity_pairing(entity_coords):
    mid_points = [rect_center(coord) for coord in entity_coords]
    levels = []
    for coord in entity_coords:
        b_bawah = (coord[1] + coord[3])/2
        b_atas = (coord[5] + coord[7])/2
        cur_level = [i for i,mid in enumerate(mid_points) if mid[1]>=b_bawah and mid[1]<=b_atas and i not in flatten(levels)]
        if cur_level not in levels and len(cur_level):
            levels.append(cur_level)
    return levels

def get_paired(levels, coord, transcript):
    pairs = []
    for level in levels:
        pair = [[coord[i][0], coord[i], transcript[i]] for i in level]
        pairs.append(pair)
    return pairs

def split_pairs(paired):
    coords = []
    transcripts = []
    for pairs in paired:
        coord = []
        transcript = []
        for pair in pairs:
            _, cpair, tpair = pair
            coord.append(cpair)
            transcript.append(tpair)
        coords.append(coord)
        transcripts.append(transcript)
    return coords, transcripts