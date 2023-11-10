from PIL import Image, ImageDraw, ImageFont
from internal.models.SQLite_db.get_fight import get_fight_num_by_m
from internal.models.SQLite_db.get_category_setka import get_state_by_id

font_path = ".\storage\\fonts\Hero.ttf"

name_font_size = 16
tur_name_font_size = 32
cat_font_size = 24

padding = 4
up_padding = 10
left_padding = 20

between_boxes = 5
between_rounds = 10
min_box_width = 100
min_box_height = 10

def draw_setka(tur_id, tur_name, cat_id, cat, members):
    wt, ht = h_w(tur_name, font_path, tur_name_font_size)
    wc, hc = h_w(cat, font_path, cat_font_size)
    wb, hb = h_w(members[0]["fio"], font_path, name_font_size)
    pust_mas = []
    mas_setka = get_mas_setka(members, pust_mas)
    boxes, lines, texts = get_boxes_setka(mas_setka, hb)
    mw, mh = min_boxes_w_h(boxes)

    img = Image.new('RGB', (int(mw), int(mh+ht+hc+4*up_padding)), 'white')
    draw_texts(img, [[left_padding, up_padding, tur_name]], font_path, tur_name_font_size, mh+up_padding)
    draw_texts(img, [[left_padding, up_padding, cat]], font_path, cat_font_size, mh+ht+up_padding*2)
    draw_boxes(img, boxes, 0)
    draw_lines(img, lines, 0)
    draw_texts(img, texts, font_path, name_font_size, 0)
    state_cat = get_state_by_id(cat_id)
    img_path = str(tur_id)+"_"+str(cat_id)+"_"+str(state_cat)+".jpg"
    img.save(".\storage\img_setka\setka_"+img_path)
    return img_path

def draw_boxes(img, boxes, plush):
    imgd = ImageDraw.Draw(img)
    for b in boxes:
        imgd.rectangle(b, fill ="#ffffff", width = 2 ,outline = "black")

def draw_lines(img, lines, plush):
    imgd = ImageDraw.Draw(img)
    for l in lines:
        imgd.line(l, width=2, fill = "black")

def draw_texts(img, texts, font_path, font_size, plush):
    imgd = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    for t in texts:
        imgd.text([t[0], t[1]+plush], t[2], font = font, fill="black")

def min_boxes_w_h(boxes):
    mw, mh = 0, 0 
    for b in boxes:
        if mw<b[2]:
            mw = b[2]
        if mh<b[3]:
            mh = b[3]
    mw = mw + left_padding
    mh = mh + up_padding
    return mw, mh


def max_fights(members):
    mf = 0
    for i in members:
        if mf<i["n_fights"]:
            mf = i["n_fights"]
    return mf

def get_mas_setka(members, mas = []):
    masn = []
    new_members=[]
    l = len(members)
    mf = max_fights(members)   

    i = 0
    while i in range(l-1):
        if members[i]["n_fights"] == members[i+1]["n_fights"] and members[i]["n_fights"] == mf:
            masn.append({"fio":members[i]["fio"], "id": members[i]["id"]})
            masn.append({"fio": members[i+1]["fio"], "id": members[i+1]["id"]})

            if members[i]["n_wons"] == 0 and members[i+1]["n_wons"] == 0:
                new_members.append({"id": -1, "fio": "", "n_fights": members[i]["n_fights"]-1, "n_wons": 0})
            elif members[i]["n_wons"] == 0:
                m = dict(members[i+1])
                m["n_fights"] = m["n_fights"] -1
                m["n_wons"] = m["n_wons"] - 1
                new_members.append(m)
            elif members[i+1]["n_wons"] == 0:
                m = dict(members[i])
                m["n_fights"] = m["n_fights"] -1
                m["n_wons"] = m["n_wons"] - 1
                new_members.append(m)
            else:
                new_members.append({"id": -1, "fio": "", "n_fights": members[i]["n_fights"]-1, "n_wons": 0})
            i = i + 1
        else:
            masn.append(None)
            new_members.append(members[i])
        i = i + 1

    if len(masn) != l:
        masn.append(None)
        new_members.append(members[l-1])

    if len(masn) < 2**mf:
        for i in range(2**mf - len(masn)):
            masn.append(None)

    mas.append(masn)
    if len(new_members) == 1:
        mas.append([{"fio": new_members[0]["fio"], "id": new_members[0]["id"]}])
        return mas
    else:
        return get_mas_setka(new_members, mas)

def get_boxes_setka(mas_setka, height):

    height = height + padding*2
    boxes = []
    lines = []
    texts = []
    mw = [left_padding]

    for r in range(len(mas_setka)-1):
        mw.append(max(min_w(mas_setka[r], name_font_size, font_path)+padding*2,min_box_width))
        for b in range(0,len(mas_setka[r]),2):
            if not mas_setka[r][b] is None:

                sdvig_w = between_rounds * r
                for i in range(len(mw)-1):
                    sdvig_w = sdvig_w + mw[i] 
                sdvig_h = b*(2**r)*(height+between_boxes)+(r!=0)*((2**abs(r-1))*(height+between_boxes)-height/2)+(r==0)*(between_boxes/2)+up_padding
                box1 = [sdvig_w, sdvig_h, sdvig_w+mw[r+1], sdvig_h+height]
                sdvig_h = (b+1)*(2**r)*(height+between_boxes)+(r!=0)*((2**abs(r-1))*(height+between_boxes)-height/2)+(r==0)*(between_boxes/2)+up_padding
                box2 = [sdvig_w, sdvig_h, sdvig_w+mw[r+1], sdvig_h+height]
                boxes.append(box1)
                boxes.append(box2)

                if mas_setka[r][b]["fio"] == "":
                    num = get_fight_num_by_m(mas_setka[r-1][b*2]["id"], mas_setka[r-1][b*2+1]["id"])
                    mas_setka[r][b]["id"] = -num["id"]
                    num_f = "Бой "+str(num["fio"])
                else: 
                    num_f = mas_setka[r][b]["fio"]      
                texts.append([box1[0]+padding, box1[1]+padding, num_f])

                if mas_setka[r][b+1]["fio"] == "":
                    num = get_fight_num_by_m(mas_setka[r-1][(b+1)*2]["id"], mas_setka[r-1][(b+1)*2+1]["id"])
                    mas_setka[r][b+1]["id"] = -num["id"]
                    num_f = "Бой "+str(num["fio"])
                else: 
                    num_f = mas_setka[r][b+1]["fio"] 
                texts.append([box2[0]+padding, box2[1]+padding, num_f])
                
                line1 = [box1[2], (box1[1]+box1[3])/2, box1[2]+between_rounds/2, (box1[1]+box1[3])/2]
                line2 = [box2[2], (box2[1]+box2[3])/2, box2[2]+between_rounds/2, (box2[1]+box2[3])/2]
                line3 = [line1[2],line1[3], line2[2],line2[3]]
                line4 = [line3[0],(line3[1]+line3[3])/2,line3[0]+between_rounds/2,(line3[1]+line3[3])/2]

                lines.append(line1)
                lines.append(line2)
                lines.append(line3)
                lines.append(line4)
    
    last = lines[len(lines)-1]
    num = get_fight_num_by_m(mas_setka[len(mas_setka)-2][0]["id"], mas_setka[len(mas_setka)-2][1]["id"])
    
    if mas_setka[len(mas_setka)-1][0]["fio"] == "":
        lbox = "Бой "+str(num["fio"])
    else: 
        lbox = mas_setka[len(mas_setka)-1][0]["fio"]
    w, _ = h_w(lbox, font_path, name_font_size)
    if w < min_box_width:
        w = min_box_width
    box = [last[2],last[3]-height/2, last[2]+w+padding*2, last[3]+height/2]

    boxes.append(box)

    texts.append([box[0]+padding, box[1]+padding, lbox])    

    return boxes, lines, texts

def min_w(fios, font_size, font_path):
    ttf = ImageFont.truetype(font_path, font_size)
    widths = []
    for i in fios:
        if not i is None:
            w, _ =ttf.getsize(i["fio"])
            widths.append(w)
    if len(widths) == 0:
        return min_box_width
    return max(widths)

def h_w(text, font_path, font_size):
    w = 0
    h = 0
    ttf = ImageFont.truetype(font_path, font_size, encoding="unic")
    for c in text:
        w += ttf.getsize(c)[0]
    h = ttf.getsize(text)[1]
    return w, h