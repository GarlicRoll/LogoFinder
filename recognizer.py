import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
from warnings import filterwarnings

filterwarnings("ignore")


def recognizer(path):
    nn = tf.keras.models.load_model("models/nn128.keras")
    #nn.load_weights("models/model_fast_food_big.weights.h5")
    '''
    op = cv2.imread(path)
    op = cv2.resize(op, (30, 30))
    op = np.array(op)
    op = op.reshape(1, 30, 30, 3)
    model = nn.predict(op)

    store_name = ['burger king', 'mcdonalds', 'starbucks', 'subway']

    # Convert to DataFrame
    val = []
    for i in model:
        val.append(i)
    data_fram = pd.DataFrame([store_name, val[0]]).T
    data_fram.columns = ["Outlate", "Output"]

    # Final Output
    op_final = data_fram.groupby('Output').max().tail(1).values[0][0]

    # Get the index of the predicted class
    predicted_class_index = np.argmax(model)

    # Get the predicted class associated probability
    probability = model.squeeze()[predicted_class_index] * 100  # Convert to percentage
    print(f"Given Image is {op_final} Store with a probability of {probability:.2f}%")
    '''
    store_names = ['piltti',
 "Arthur Treacher's Fish & Chips",
 'xiangeqing',
 'lion cereal',
 'true coffee',
 'violet crumble',
 "Camille's Sidewalk Cafe",
 'ConAgra Foods',
 'puffa puffa rice',
 'CoCo Wheats',
 'wuyutai',
 'ganningpai',
 'mcdonalds',
 'rice honeys nabisco',
 'real ale',
 'Bertie Beetle',
 'quaker steak & lube',
 'Cinna-Crunch Pebbles',
 'Fruit Selection',
 "stephen's gourmet",
 'Fruco',
 'Brugal',
 'taco cabana',
 'Jumbo Krispies',
 'Cinnabon',
 'Calistoga',
 'Ito En',
 'spizzico',
 'Fruit Selection Yogurt',
 'Costa Coffee',
 'California Pizza Kitchen',
 'Marble Slab Creamery',
 'Honey Nut Clusters',
 "Bullwinkle's Restaurant",
 "Coco's Bakery",
 'Blue State Coffee',
 'square one organic',
 'HuiShan',
 'Blackjack Pizza',
 'Cerelac',
 'Blimpie',
 'pronutro',
 'nutren',
 'Blavod',
 'secret recipe',
 'Indomie Mi goreng',
 'chandelle',
 "panarotti's",
 'lost coast',
 'swensons',
 'quality street',
 'Appleton Estate',
 'slim fast',
 "mother's pride",
 'ribena',
 'la cocinera',
 'Budget Gourmet',
 'planet cola',
 'cookie crisp brownie',
 'Celestial Seasonings',
 'Highland Toffee',
 'new zealand natural-3',
 "Carl's Jr",
 'rum-bar',
 'Maille',
 'vapiano',
 "Adrian's",
 "Auntie Anne's-1",
 "Lady's Choice",
 "cheddar's casual cafe",
 'lupicia',
 'svedka',
 'Bovril',
 'A. Marinelli',
 "Fox's Biscuits",
 'Bubba Gump Shrimp Company',
 'Henri Lloyd',
 'cheesecake factory',
 'sixpoint',
 'Berry Bones Scooby-Doo',
 'Belvita',
 'calfee design',
 'Poulain',
 'Arehucas',
 'pacific coffee company',
 'jixiangju',
 'red robin',
 'Hebrew National',
 "Homer's Cinnamon Donut",
 'chicken out rotisserie',
 'Beacon Drive In',
 'Cocoa Pebbles',
 'Gobstoppers',
 'Lucky Charms',
 'lindt',
 'sweetened wheat-fuls',
 'Berry Berry Kix',
 'poppycock',
 'Cocoa Puffs Combos',
 'Fruit2O',
 'cheeburger cheeburger',
 'Blue Bottle Coffee Company',
 'Maxwell House',
 'Maynards',
 'screaming yellow zonkers',
 'toasties',
 'Hard Rock Cafe',
 'moutai',
 'El Paso',
 'showmars',
 'nairobi java house',
 'pizza 73',
 'rooibee',
 'Cinnamon Jacks',
 'lollo',
 'zephyrhills',
 'Hudsons Coffee-2',
 'wangzhihe',
 'sweet tomatoes',
 'Cinnamon Toasters',
 'Chocolate liqueur',
 'Frosted Mini Spooners',
 "Herrell's Ice Cream",
 'biostime-1',
 'wangs',
 "Bird's Custard",
 "Graeter's",
 'Maizena',
 "Breakstone's",
 'Casa Dragones',
 'Burger Street',
 'Allagash',
 'Country Crock',
 'Chronic Tacos-2',
 'Loacker',
 'Corn Pops',
 'holy cow casino',
 'yonho-1',
 "Aurelio's Pizza",
 'Eristoff',
 'Kraft Ramek',
 "wrigley's",
 'royal farms',
 'Club Social',
 'GuanShengYuan',
 'Ketel One',
 "Colman's",
 'Honey Bunches of Oats',
 'Colossal Crunch',
 'reddi-wip',
 'zoegas',
 'Highlands Coffee',
 "Hershey's Cookies 'n' Creme",
 'Adnams',
 'Coco Roos',
 'oatmeal crisp',
 'Burrow Hill Cider',
 "moe's southwest grill",
 'Breyers',
 'Chocolate Flakes',
 'waffle crisp',
 'r.whites',
 'Mecca Cola',
 "Buddy's Pizza",
 'chef-mate',
 'cookie crisp sprinkles',
 'strawberry rice krispies',
 'yesmywine',
 'Honey Kix',
 'La Laitiere',
 'Huddle House',
 'nabob',
 'Honey Nut Shredded Wheat',
 'contrex',
 'Koskenkorva',
 'mikado',
 "Gritty McDuff's",
 "zatarain's",
 'Iams',
 'Bacon soda',
 "Angelo Brocato's",
 'rogue ales',
 'montesierpe',
 'new zealand natural-1',
 'tired hands',
 'sveltesse',
 'tealuxe',
 'biostime-2',
 'wilton',
 'laimao',
 'smart bran',
 'Berry Lucky Charms',
 'kichesippi-1',
 'Blueberry Morning',
 'Bazooka',
 'Frosty Jack Cider',
 'merrydown',
 'sandford orchards',
 'wudeli',
 'Chick-fil-A',
 'tres generaciones',
 'pizza my heart',
 'Chiclets',
 "Hale's Ales",
 'raisin wheats',
 'ommegang',
 'Chocolate Toast Crunch',
 'pop weavei',
 'lolly gobble bliss',
 "wyder's",
 'wolf brand chili',
 'Caffe Ritazza',
 'great lakes',
 'Huiyuan',
 'Heinz Tomato Ketchup',
 "Hungry Howie's Pizza",
 'Cream of Wheat',
 'ro-tel',
 'rock bottom',
 "romano's macaroni grill",
 'Cafe Coffee Day',
 'Conimex',
 'Lacta',
 'pop mie',
 "Chocolate D'Onofrio",
 'pisco horcon quemado',
 'Hungry Hungry Hippos',
 'Candy Land',
 'Juan Valdez Cafe',
 'Bridgehead Coffee',
 'old style pilsner',
 'liwayway',
 'Hot chocolate',
 'Charmin',
 '1519 Tequila',
 "charlie brown's steakhouse",
 'Margherita',
 'pop-tarts crunch',
 'Golden Grahams',
 'Ijml',
 'three olives',
 "Cap'n Crunch",
 'Infacare',
 'sariwangi',
 'weetos',
 'Coffee Crisp',
 'sanka',
 'milk-bone',
 'Bear Republic',
 'Hula Hoops',
 'Bellywashers',
 'pianyifang',
 'Bold Rock Hard Cider',
 'Lunchables',
 'Crush',
 "Cameron's",
 'tacama demonio',
 'Creemore',
 'Buc Wheats',
 'tres agaves',
 'pizza schmizza',
 'coffeeheaven',
 'robust',
 'BiFi',
 'snot shots',
 'Angry Orchard',
 'Harvest Crunch',
 'nestle corn flakes',
 'Bran Flakes',
 "Cheader's",
 'pucko',
 'ucc ueshima coffee co',
 'luzhoulaojiao-2',
 'Johnny Rockets',
 'Arette',
 'newport creamery-1',
 'rj rockers',
 'sarris candies',
 "robin's donuts",
 'papa guiseppi',
 'taco bueno',
 'BARSOL',
 'the melting pot',
 'Baja Fresh',
 'Blenz Coffee-2',
 'Anglo Bubbly',
 'Crispin Cider',
 'Becel',
 'wiesmann',
 "rickard's dark",
 'Ginger Ale',
 'Honey Smacks',
 'Cocosette',
 'Cheerios',
 "Carino's Italian Grill",
 'san pellegrino',
 'chenkeming-2',
 "papa murphy's take 'n' bake pizza",
 'Franconia',
 'peptamen',
 'weight watchers',
 "nut 'n honey",
 'la saltena',
 'pepsi lime',
 'yurun',
 "McDonald's",
 'Bisquick',
 'red rose tea',
 'texan bar',
 'sasini',
 'Giolitti',
 'Cocoa Puffs',
 'Lamb Weston',
 'Frosted Shredded Wheat',
 "Joe's Crab Shack",
 'Kleiner Feigling',
 'stumptown coffee roasters',
 'tart n tinys',
 "Cassano's Pizza King",
 "steak 'n shake",
 'Aroma Espresso Bar',
 "mountain mike's pizza",
 'old el paso',
 'pick up stix',
 "marco's pizza",
 'Cailler',
 'Count Chocula',
 'popeyes chicken & biscuits',
 'qdoba mexican grill',
 'Cape Cod Potato Chips',
 'saimaza',
 "Cap'n Crunch Crunch Berries",
 'haagen-dazs',
 'Apple Zings',
 'Carling Black Label',
 'Bucanero',
 'Bubbaloo',
 'Lucozade',
 'cheezels',
 'tignanello',
 'El Chico',
 'mr. pizza',
 'russian river',
 'chicken in a biskit',
 'Erikli',
 'wandashan',
 "Brigham's Ice Cream",
 "charley's grilled subs",
 'chicken express',
 'Cha Dao',
 'Cafe HAG',
 'Cigar City',
 "raising cane's chicken fingers",
 'suerdieck',
 'H. P. Bulmer-2',
 "tully's coffee",
 'swiss miss',
 'Cavalier',
 'Big Turk',
 'van houtte',
 'Berthillon',
 'Chocomel',
 'Beaulieu',
 'Henniez',
 'Maxibon',
 'rohrbach',
 "Bruster's Ice Cream",
 'Hav-A-Tampa',
 'mauds ice cream',
 'cheddarie',
 'Bully Boy Distillers',
 'Fruit Brute',
 'peppes pizza',
 'Carupano',
 'smint',
 'pepsi jazz',
 'xifeng',
 'wienerschnitzel',
 "Hardee's",
 'le viennois',
 "Gino's Pizza and Spaghetti",
 "portillo's",
 'Berry Burst Cheerios',
 'nandos',
 '85C Bakery Cafe',
 'galak',
 "Benedetti's Pizza",
 'Ingman Ice Cream',
 "Bearno's",
 'st arnou',
 "ray's pizza",
 'straw hat pizza',
 'toxic waste',
 'champps americana',
 'Caribou Coffee',
 'Cachantun',
 'port city java',
 'Big Mama Sausage',
 'copella',
 'pipsqueak',
 'cornnuts',
 'California Free Former',
 "It's a Grind Coffee House",
 'mulata',
 'the capital grille',
 'Boston Pizza',
 'Cruz Tequila',
 'El Taco Tote',
 'Frank Pepe Pizzeria Napoletana',
 'warburtons',
 '241 Pizza',
 'sabra liqueur',
 'wolverine',
 'Chipsmore',
 'Cocoa Krispies',
 'Carte Noire',
 "Bennigan's",
 'smokey bones',
 'stroh',
 'McCoys Crisps',
 'chenkeming-1',
 "Horniman's",
 'sheetz',
 'Angela Mia',
 'Bakers Square',
 "I Can't Believe It's Not Butter",
 'sanquan',
 'ristretto',
 'Gerber',
 'skyy',
 'rice chex',
 'Chocolate Chex',
 "milo's hamburgers",
 'slotts',
 'Apple Cinnamon Chex',
 'Fruity Cheerios',
 'Crunch',
 'pizza pizza',
 'Lagunitas',
 'Caffe Umbria',
 'Cinnamon Mini-Buns',
 'newport creamery-2',
 'Freihofers',
 'humdinger',
 'Laffy Taffy',
 'penn station (restaurant)',
 'Berry Krispies',
 'East of Chicago Pizza',
 'mondaine',
 'supligen',
 'minties',
 "lender's",
 'zjs express',
 'Brummel & Brown',
 'California Tortilla',
 'H. J. Heinz',
 'Eukanuba',
 'Cows',
 'taoranju',
 'Kibon',
 'maarud',
 'Chocolate Cheerios',
 'Caffe Luxxe',
 'La Lechera',
 'Canada Dry',
 'Krupnik',
 'BaMa',
 'Homey',
 'Captain Morgan',
 "weston's cider",
 'zhoujunji',
 'cheesybite',
 'Certs',
 'viru valge',
 'matusalem',
 'toppers pizza',
 'the original pancake house',
 'Furst Bismarck',
 'gladiator cycle',
 'Marmite',
 "Carrabba's Italian Grill",
 'penguin mints',
 'Egg Beaters',
 'Carvel Ice Cream',
 'Coco Pops',
 'chatime',
 'winiary',
 'oberweis dairy-2',
 'oberweis dairy-1',
 "Bewley's",
 'widmer brothers',
 'LongHorn Steakhouse',
 'nesvita',
 'Arrowroot biscuits',
 'philadelphia',
 'Bear Naked',
 "Cadwalader's Ice Cream",
 'Imperial Margarine',
 'El Dorado',
 'Biggby Coffee',
 'Chocapic',
 'Fudgee-O',
 'Chronic Tacos-1',
 "tony roma's",
 'Cinnamon Grahams',
 "lee's famous recipe chicken",
 "montana mike's",
 "Hunt's Snack Pack",
 'Caffe Bene',
 'prezzo',
 'marshmallow mateys',
 'Eden Cheese',
 "EatZi's",
 'Market Pantry',
 'In-N-Out Burger',
 'Apple Jacks',
 'pollo campero',
 'pizzeria venti',
 'pomegreat',
 'Cili',
 'Bacardi',
 'ready brek',
 'Bundaberg',
 'smirnoff',
 'yili',
 'General Mills',
 'Chex',
 'nestle',
 "timothy's world coffee",
 'Hell Pizza',
 'AN JI WHITE TEA',
 'luzhoulaojiao-1',
 'Gimme! Coffee',
 'Half Pints',
 "CiCi's Pizza",
 "tito's",
 'Eco de los Andes',
 'Coffee Republic',
 "wayne's coffee",
 'Fudgsicle',
 'mutong',
 'hengshui laobaigan',
 'which wich',
 'wheat stax',
 'on the border mexican grill & cantina',
 'Cinnamon Toast Crunch',
 'APEROL',
 'CoverGirl',
 'Choc-Ola',
 'new zealand natural-2',
 'chex mix',
 'Coffee Beanery',
 'chewits',
 'Crunchy Nut',
 'queirolo',
 'Bushells',
 'runts',
 'taco time',
 'xiao nan guo',
 'Bravo!, Cucina Italiana',
 'tassimo',
 'ron zacapa',
 'Chips Ahoy!',
 "papa gino's",
 'luhua',
 'Cheese Nips',
 'Ashridge Cider',
 "John's Incredible Pizza",
 'svelty',
 'Frosted Cheerios',
 'lunazul',
 'shmaltz',
 "Bojangles' Famous Chicken 'n Biscuits",
 'AMT Coffee',
 'Coffee-Mate',
 "Marie Callender's",
 '7-Up',
 'Appletiser',
 'quorn',
 'Carrows',
 'Arcaffe',
 'cheeseburger in paradise',
 'thomy',
 'miracoli',
 'Cabo Wabo',
 'viladrau',
 'IHOP',
 'Honey Nut Cheerios',
 'Glider Cider',
 'Cafe Hillel',
 'montecruz',
 'tudor crisps',
 'Kotipizza',
 'Chef Boyardee',
 'Bigg Mixx',
 'CHIVAS REGAL',
 'Krave',
 'port of subs',
 'walkers lites',
 'puffs',
 "Hellmann's",
 'chiffon margarine',
 'Boo Berry',
 'silver gulch',
 'Hunt Brothers Pizza',
 "Friendly's",
 'Cascadian Farm',
 'ledo pizza',
 'upslope',
 'ragu',
 'Candyman',
 "taco john's",
 'Chocolate Lucky Charms',
 'Gabriel Pizza',
 'phileas fogg',
 'Espresso Vivace',
 'Keglevich',
 'tenwowfood',
 "lappert's",
 'Chuck-A-Rama',
 'Honey Maid',
 'vladivar',
 'molson exel',
 'wufangzhai',
 "rosati's",
 'trung nguyen',
 'la porchetta',
 'huntkey',
 'Aqua Carpatica',
 'lan-choo',
 'the coffee bean & tea leaf',
 'Maggi Masala noodles',
 'ricoffy',
 'Colectivo Coffee Roasters',
 "Gale's",
 'Espolon',
 'round table pizza',
 'Buzz Blasts',
 'Coffee Time',
 'Aroma Cafe',
 'Beers of Stone',
 'CHIVAS',
 'Heinz Baked Beans',
 "Amy's Ice Creams",
 "Mazzio's",
 'Maggi',
 'GuiFaXiangShiBaJie',
 'Au Bon Pain',
 'Breath Savers',
 'Honey Graham',
 'GUINNESS',
 'teavana',
 "russo's new york pizzeria",
 'rosarita',
 'joe muggs',
 'Hubba Bubba',
 'Grapette',
 'Cracker Jack',
 'nestle milk chocolate',
 'nemiroff',
 'quickchek',
 'ruby tuesday',
 'Cinnamon Chex',
 "rutter's",
 'Bon Pari',
 'skyline chili',
 "steve's ice cream",
 'rhum barbancourt',
 'sahne nuss',
 "toscanini's",
 'pei wei asian diner',
 "plochman's",
 'Boston Market',
 'Hot Pockets',
 'pisco porton',
 'pisco capel',
 "miller's ale house",
 "Auntie Anne's-2",
 'Cola Cao',
 'Hollys Coffee',
 'shuijingfang',
 "Gardetto's",
 'penpont',
 'Act II',
 'manwich',
 'waffle house',
 'taza chocolate',
 'Cibo Espresso',
 'Brothers Cider',
 'Bubblicious',
 'yonho-2',
 'Black Angus Steakhouse',
 'Cool Whip',
 'youyou',
 'Guigoz',
 'Bicerin',
 'Caffe Cova',
 'mars muffin',
 'lizano',
 'Glee Gum',
 'smuttynose',
 'Chocolate Surpresa',
 'Irn Bru Bar',
 "Handel's Homemade Ice Cream & Yogurt",
 'molson brador',
 "Anthony's Pizza",
 'Hudsons Coffee-1',
 'Apple Jacks Gliders',
 "Eegee's",
 'mikel coffee company',
 'Four Star Pizza',
 "luby's",
 'Bulls-Eye Barbecue',
 'kichesippi-2',
 'frigor',
 'tequila don weber',
 'chicken tonight',
 'chamyto',
 'El Jimador',
 'Bournvita',
 'Holgate',
 'valiojaatelo',
 'sugar wafers',
 'Horlicks',
 "rickard's red",
 'Cat Chow',
 "Freddy's Frozen Custard & Steakburgers",
 'Better Cheddars',
 'Chocos',
 "mactarnahan's",
 "mcalister's deli",
 'Beneful',
 'lollicup coffee & tea',
 'lightlife',
 'oh henry',
 'French Toast Crunch',
 'Breakfast with Barbie',
 'Cafe A Brasileira',
 'maggi noodles',
 'ruffles',
 'chevys fresh mex',
 'coca cola',
 'Bawls',
 'Insomnia Coffee Company',
 'Caffe Pascucci',
 'chewy louie',
 'razzle dazzle rice krispies',
 'pizza corner',
 'mellow mushroom',
 'Hamburger Helper',
 'rolo',
 'perkins restaurant and bakery',
 'HobNobs',
 'powdered donutz',
 'Corn Flakes',
 'showbiz pizza place',
 'Magners Irish',
 "Captain D's",
 'Carlos V',
 'Jus-Rol',
 'wanchai ferry',
 'Carnation',
 'Honey Nut Corn Flakes',
 'treets',
 'taixiang',
 'Heineken',
 'sprinkle spangles',
 "Long John Silver's",
 'Carling',
 "Braum's",
 'raisin nut bran',
 'toasted cinnamon squares',
 'Maltesers',
 'la barberie',
 'peter piper pizza',
 'xinghualou',
 'Boca Burger',
 'H. P. Bulmer-1',
 'Back Yard Burgers',
 'Cherry 7Up',
 'robeks',
 'vikingfjord',
 'FruChocs',
 "Honey Nut Toasty O's",
 'Cheez Whiz',
 'vascolet',
 'raisin bran crunch',
 "Eat'n Park",
 'Growers Direct',
 'Cocio',
 "Frosty O's",
 'wheat chex',
 'luzhoulaojiao-3',
 'williams fresh cafe',
 'pop secret',
 'Gevalia',
 'Caffe Nero',
 'lobethal bierhaus',
 'regina pizzeria',
 'Highland Spring',
 'waffelos',
 "Baker's Dozen Donuts",
 'Juicy Fruit',
 'national coney island',
 'Blenz Coffee-1',
 'qingmei',
 'Kissan',
 'shuanghui',
 'Casa Noble',
 "Cote d'Or",
 "pusser's",
 'Cinnzeo',
 'chicago town',
 "Gatti's Pizza",
 'Hornitos',
 'Alete',
 'chiffon',
 'Galaxy Counters',
 'tooty footies',
 'Handi-Snacks',
 'Batchelors',
 'Crunchy Corn Bran',
 'Ice Breakers',
 'shengfeng',
 'Ciego Montero',
 "wall's",
 "logan's roadhouse",
 "rubio's fresh mexican grill",
 'Cafe du Monde',
 'Cafe Rio',
 'La Choy',
 'second cup',
 'mr. noodles',
 "rickard's white",
 "Carl's Ice Cream",
 'yorkshire tea',
 "Maker's Mark",
 'mallow oats',
 'mccafe',
 'Atlanta Bread Company',
 'Coca-Cola Zero',
 'Capri Sun',
 'punch crunch',
 'Buondi',
 'LAVAZZA',
 "Gloria Jean's Coffees",
 "margie's candies",
 'HP Sauce',
 'AktaVite',
 'the old spaghetti factory',
 'wild berry skittles',
 'mueslix',
 'Eggo',
 'potbelly sandwich works',
 "noble roman's",
 'teekampagne',
 'Four Seas Ice Cream',
 'plancoet',
 'Argus Cider',
 'stadium mustard',
 'nong shim ltd',
 'Honey Stars',
 'Kola Shaler',
 'cheese flavoured moments',
 'Amora',
 'Caramac',
 "maggiano's little italy",
 'Best Foods',
 'raisinets',
 'Futurelife SmartFood',
 'Intelligentsia Coffee & Tea',
 "larosa's pizzeria",
 "Mario's Pizzeria",
 'glad wrap',
 "Kwality Wall's",
 'stolichnaya',
 "whitey's ice cream",
 '42 Below',
 'red lobster',
 "Angie's Kettle",
 'Buca di Beppo',
 "mellow bird's",
 'turun sinappi',
 'Carling Cider',
 'Benihana',
 'Cinnamon Burst Cheerios',
 '10 Cane',
 'Ginsters',
 'Good Humor',
 'chicza',
 'BigBabol',
 'toblerone',
 'royco',
 'Freia',
 "Bruegger's",
 'Caffe Trieste',
 "Imo's Pizza",
 'jack in the box',
 'pizza ranch',
 "ching's secret",
 'royal crown cola',
 'Ice Mountain',
 'cookie crisp',
 'zoladkowa gorzka',
 'Ballast Point',
 'Half Acre',
 'Coors',
 'Burgerville',
 'Cold Stone Creamery',
 "Baker's",
 "Applebee's",
 'Corona',
 'Maestro Dobel',
 'Ciao Bella Gelato Company',
 "Fox's Pizza Den",
 'roy rogers restaurants',
 'rice bubbles',
 "MaggieMoo's Ice Cream and Treatery",
 'Claussen',
 'Marshmallow',
 "Aoki's Pizza",
 "jittery joe's",
 'rowntree',
 'Blue Riband',
 "michel's patisserie",
 'vico',
 'Cini Minis',
 "Giordano's Pizzeria",
 "smokin' joes",
 'scottish blend',
 'Campbells',
 'laura secord chocolates']
    op = cv2.imread(path)
    op = cv2.resize(op, (128, 128))
    op = np.array(op)
    # op = op.reshape(1,30,30,3)

    x_min, y_min = 4, 4
    x_max, y_max = 124, 124
    op_xml = np.array([x_min, x_max, y_min, y_max])
    op_image = np.array(op).reshape(1, *op.shape)
    op_xml = np.array(op_xml).reshape(1, *op_xml.shape)

    model = nn.predict([op_image, op_xml])

    # Convert to DataFrame
    val = []
    for i in model:
        val.append(i)
    data_fram = pd.DataFrame([store_names, val[0]]).T
    data_fram.columns = ["Outlate", "Output"]

    # Final Output
    op_final = data_fram.groupby('Output').max().tail(1).values[0][0]

    # Get the indices of the top 5 classes sorted by probability
    top_5_indices = np.argsort(model.squeeze())[-5:][::-1]

    # Get the top 5 probabilities
    top_5_probabilities = model.squeeze()[top_5_indices] * 100

    # Get the corresponding class labels for the top 5 indices
    top_5_classes = [store_names[i] for i in top_5_indices]

    # Print the top 5 most possible classes and their probabilities
    for class_name, probability in zip(top_5_classes, top_5_probabilities):
     print(f"Class: {class_name}, Probability: {probability:.2f}%")
    return op_final