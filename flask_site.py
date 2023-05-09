import pandas as pd
from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap
import json
import os

base_path = os.path.dirname(os.path.abspath(__file__))
material_path = os.path.normpath(
    os.path.join(base_path, './dataset/dishes.csv'))
shop_path = os.path.normpath(os.path.join(
    base_path, './dataset/restaurants.csv'))

material = pd.read_csv(material_path, usecols=['料理名', '素材', '写真', 'dish'])
restaurant = pd.read_csv(
    shop_path, usecols=['店名', 'サイト', 'メニュー', 'lat', 'lng'])  # データにNaNがあるとエラーになる

nc = Flask(__name__)
nc.config['JSON_AS_ASCII'] = False
Bootstrap(nc)

cui = {"豚丼": "buta_don", "鮭のちゃんちゃん焼き": "sake_no_Chanchan_yaki", "いももち": "imo_mochi", "ニシン漬け": "nishin_zuke", "石狩鍋": "ishikari_nabe", "いかめし": "ika_meshi", "ラーメン": "ramen",
       "赤飯": "sekihan", "昆布巻き": "konbu_maki", "美唄のとりめし": "Bibai_no_tori_meshi", "美唄やきとり": "Bibai_no_yakitori", "室蘭焼き鳥": "Muroran_yakitori", "鯨汁": "kujira_jiru", "ルイベ": "ruibe",
       "ニシン蕎麦": "nishin_soba", "ザンギ": "zangi", "シシャモの甘露煮": "shishamo_no_kanroni", "カスべの煮つけ": "kasube_no_nitsuke", "トキシラズの焼漬け": "tokishirazu_no_yaki_zuke", "いくらの醤油漬け": "ikura_no_shoyu_zuke",
       "たちの味噌汁": "tachi_no_misoshiru", "べこ餅": "beko_mochi", "飯寿司": "meshi_sushi", "松前漬": "Matsumae_zuke", "てっぽう汁": "teppo_jiru", "三平汁": "sanpei_jiru", "ジンギスカン": "zingisukan"}


@nc.route("/", methods=["get"])
def check():
    mat = {"豚肉": "butaniku", "鶏肉": "toriniku", "羊肉": "hitsujiniku", "サケ": "sake", "ニシン": "nishin", "ホッケ": "hokke",
           "じゃがいも": "jagaimo", "キャベツ": "kyabetsu", "人参": "ninjin", "中華そば": "chukasoba", "辛い": "karai", "しょっぱい": "syoppai"}
    # templates内のhtmlを渡す
    return render_template('home.html', material=mat)
    # 文字埋め込みが可能だから、おすすめを表示できるように（将来）


@nc.route('/search', methods=['POST'])
def search():
    foods = dish_find()
    return render_template("cuisine_list.html", foods=foods)


def dish_find():  # return dish list
    ingre_name_list = request.form.getlist('example')  # 選択したチェックボックスのname属性
    return_list = []
    return_img = []
    skip = {}
    # ingre_nameの各文字に応じたずらす分を設定
    for l in range(len(ingre_name_list)):
        ingre_name = ingre_name_list[l]

        if len(ingre_name) == 1:  # ingre_nameが一文字だったら1文字だけずらす
            skip[ingre_name[0]] = 1
        else:
            for i in range(len(ingre_name) - 1):
                skip[ingre_name[i]] = len(ingre_name) - 1 - i

            ingre = {}
            Dish_name = {}
            img = {}
            for k in range(len(material.iloc[:, 0])):  # materialの行数が範囲
                ingre[k] = material.iloc[k, 1]
                Data = ingre[k]  # 素材列の各行をテキストと見なす
                Dish_name[k] = material.iloc[k, 0]
                img[k] = material.iloc[k, 2]

                # 探索初期値は, dataとdish_nameの先頭が合うようにしたとき末尾になるように設定
                i = len(ingre_name) - 1
                while i < len(Data):
                    match = True

                    for l in range(len(ingre_name)):
                        # dish_nameを順に1文字ずつ比較する
                        if Data[i - l] != ingre_name[-1-l]:
                            match = False  # 不一致
                            break  # 探索箇所を次に移行するため，これ以上の探索はしない
                    if match:  # すべて一致した ⇒ 探索終了
                        return_list.append(Dish_name[k])  # 料理名を返す
                        return_img.append(img[k])
                        break
                    if Data[i] in skip:
                        # 先ほど探索した中、ingre_nameと同じ文字があったらその文字に定めた文字数だけずらす
                        i += skip[Data[i]]
                    else:
                        # ずらす対象がとくに見当たらなければ，ingre_nameの文字数だけずらす
                        i += len(ingre_name)

    # return_list内重複のものを削除
    result = sorted(set(return_list), key=return_list.index)
    foods = []
    for i in result:
        num = str(material[material["料理名"] == i].index[0]+1).zfill(2)
        img = "static/img/cuisine/btn_cuisine_" + num + "@2x.png"
        name_tag = material[material["料理名"] == i].dish.item()
        name_tag_en = cui[name_tag].replace("_", " ")
        food_tile = {
            "dish": i,
            "img": img,
            "name_tag": name_tag,
            "name_tag_en": name_tag_en
        }
        foods.append(food_tile)
    print(foods)
    return foods


# 料理名から、レストランのリストを返す


def res_find(restaurants_area, dish_name):    # 選択されたdish_nameを引数として実行
    return_list = []
    return_link = []
    skip = {}

    for i in range(len(dish_name) - 1):  # dish_nameが1文字だったらエラー出る
        skip[dish_name[i]] = len(dish_name) - 1 - i

        res_name = {}
        link = {}
        menu = {}

        for k in range(len(restaurants_area.iloc[:, 1])):  # restaurantの行数が範囲
            menu[k] = restaurants_area.iloc[k, 2]
            data = menu[k]
            res_name[k] = restaurants_area.iloc[k, 0]
            # res_name[k] = restaurant.iloc[k,0] + " " + restaurant.iloc[k,1]  # 店名とサイトを１行になるようにする
            link[k] = restaurants_area.iloc[k, 1]

            i = len(dish_name) - 1
            while i < len(data):
                match = True

                for j in range(len(dish_name)):
                    # dish_nameを後ろから順に1文字ずつ比較する
                    if data[i - j] != dish_name[-1-j]:
                        match = False
                        break  # 探索箇所を次に移行するため，これ以上の探索はしない
                if match:  # すべて一致した ⇒ 探索終了
                    return_list.append(res_name[k])  # 店名を返す
                    return_link.append(link[k])  # リンクを返す
                    break
                if data[i] in skip:
                    i += skip[data[i]]
                else:
                    i += len(dish_name)

    # return_list内元の順序を保ちながら重複したものを削除
    result = sorted(set(return_list), key=return_list.index)
    result_link = sorted(set(return_link), key=return_link.index)
    return result


@nc.route('/output', methods=['POST'])
def output():
    dish = request.form.get("dish")
    print(dish)
    print(request.form.get("lat"))
    print(request.form.get("lng"))
    lat = float(request.form.get('lat'))
    lng = float(request.form.get('lng'))
    # ここまでが、post通信で取得された情報
    # ここで、検索と、gmapリンクづくり
    restaurants_aread = srch_place(restaurant, lat, lng)
    target_restaurant = res_find(restaurants_aread, dish)

    # map_data[0] = current position
    map_data = [
        {
            "name": "current position",
            "lat": lat,
            "lng": lng
        }]

    for i in range(min(5, len(target_restaurant))):
        each_restrant = restaurant[restaurant["店名"] == target_restaurant[i]]
        each_restrant_data = {
            "name": each_restrant["店名"].item(),
            "lat": each_restrant["lat"].item(),
            "lng": each_restrant["lng"].item(),
            "url": each_restrant["サイト"].item(),
            "menu": each_restrant["メニュー"].item()[:18]
        }
        map_data.append(each_restrant_data)
        # map_dataを渡す
        print(map_data)
    return render_template('return_page.html', map_data=map_data)


# data search
def srch_place(res, lat, lon):  # 経度、緯度から近くの場所を絞り込み
    return res[(res["lat"] >= lat-0.05) & (res["lat"] <= lat+0.05) & (res["lng"] >= lon-0.05) & (res["lng"] <= lon+0.05)]

# map show -- can send part of html or rewrite all
# apiを使わないものーーリンクにするものとして使えるか


def show_map(lat, lon):
    return "https://maps.google.co.jp/maps?output=embed&q=" + str(lat) + "," + str(lon) + "&t=m&z=14"


if __name__ == '__main__':
    nc.run(debug=False, host="localhost", port=8888)
