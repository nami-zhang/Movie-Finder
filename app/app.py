from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
import os, subprocess

# Initialize Flask app
app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
DATABASE_NAME = "imdb"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Language and Region mappings
LANGUAGE_MAP = {
    'af': 'Afrikaans',
    'am': 'አማርኛ',
    'ar': 'العربية',
    'az': 'azərbaycan dili',
    'be': 'беларуская мова',
    'bg': 'български език',
    'bn': 'বাংলা',
    'br': 'brezhoneg',
    'bs': 'bosanski jezik',
    'ca': 'Català',
    'cr': 'ᓀᐦᐃᔭᐍᐏᐣ (Cree)',
    'cs': 'čeština',
    'cy': 'Cymraeg',
    'da': 'dansk',
    'de': 'Deutsch',
    'eka': 'Ekajuk',
    'el': 'Ελληνικά',
    'en': 'English',
    'es': 'Español',
    'et': 'eesti',
    'eu': 'euskara',
    'fa': 'فارسی',
    'fi': 'suomi',
    'fr': 'français',
    'fro': 'ancien français',
    'ga': 'Gaeilge',
    'gd': 'Gàidhlig',
    'gl': 'galego',
    'gsw': 'Schwiizertüütsch',
    'gu': 'ગુજરાતી',
    'haw': 'ʻŌlelo Hawaiʻi',
    'he': 'עברית',
    'hi': 'हिन्दी',
    'hil': 'Ilonggo',
    'hr': 'Hrvatski',
    'hu': 'magyar',
    'hy': 'Հայերեն',
    'id': 'Bahasa Indonesia',
    'is': 'Íslenska',
    'it': 'Italiano',
    'iu': 'ᐃᓄᒃᑎᑐᑦ (Inuktitut)',
    'ja': '日本語',
    'jsl': '日本手話',
    'jv': 'basa Jawa',
    'ka': 'ქართული',
    'kk': 'қазақ тілі',
    'kn': 'ಕನ್ನಡ',
    'ko': '한국어',
    'ku': 'Kurdî',
    'ky': 'Кыргызча',
    'la': 'latine',
    'lb': 'Lëtzebuergesch',
    'lo': 'ພາສາລາວ',
    'lt': 'lietuvių kalba',
    'lv': 'latviešu valoda',
    'mi': 'te reo Māori',
    'mk': 'македонски јазик',
    'ml': 'മലയാളം',
    'mn': 'Монгол хэл',
    'mr': 'मराठी',
    'ms': 'Bahasa Malaysia',
    'my': 'ဗမာစာ',
    'myv': 'эрзянь кель',
    'ne': 'नेपाली',
    'nl': 'Nederlands',
    'no': 'Norsk',
    'pa': 'ਪੰਜਾਬੀ',
    'pl': 'Polski',
    'prs': 'دری',
    'ps': 'پښتو',
    'pt': 'Português',
    'qac': 'Qac (Unclassified)',
    'qal': 'Qal (Unclassified)',
    'qbn': 'Qbn (Unclassified)',
    'qbo': 'Qbo (Unclassified)',
    'qbp': 'Qbp (Unclassified)',
    'rm': 'rumantsch grischun',
    'rn': 'Ikirundi',
    'ro': 'Română',
    'roa': 'roa (Unclassified)',
    'ru': 'Русский',
    'sd': 'सिन्धी',
    'sk': 'slovenčina',
    'sl': 'slovenščina',
    'sq': 'Shqip',
    'sr': 'српски језик',
    'st': 'Sesotho',
    'su': 'Basa Sunda',
    'sv': 'Svenska',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'tg': 'тоҷикӣ',
    'th': 'ไทย',
    'tk': 'Türkmen',
    'tl': 'Wikang Tagalog',
    'tn': 'Setswana',
    'tr': 'Türkçe',
    'uk': 'Українська',
    'ur': 'اردو',
    'uz': 'Ўзбек',
    'vi': 'Tiếng Việt',
    'wo': 'Wollof',
    'xh': 'isiXhosa',
    'yi': 'ייִדיש',
    'yue': '粵語',
    'zh': '中文',
    'zu': 'isiZulu'
}

REGION_MAP = {
    'AD': 'Andorra',
    'AE': 'United Arab Emirates',
    'AF': 'Afghanistan',
    'AG': 'Antigua and Barbuda',
    'AI': 'Anguilla',
    'AL': 'Albania',
    'AM': 'Armenia',
    'AN': 'Netherlands Antilles',
    'AO': 'Angola',
    'AQ': 'Antarctica',
    'AR': 'Argentina',
    'AS': 'American Samoa',
    'AT': 'Austria',
    'AU': 'Australia',
    'AW': 'Aruba',
    'AZ': 'Azerbaijan',
    'BA': 'Bosnia and Herzegovina',
    'BB': 'Barbados',
    'BD': 'Bangladesh',
    'BE': 'Belgium',
    'BF': 'Burkina Faso',
    'BG': 'Bulgaria',
    'BH': 'Bahrain',
    'BI': 'Burundi',
    'BJ': 'Benin',
    'BM': 'Bermuda',
    'BN': 'Brunei Darussalam',
    'BO': 'Bolivia',
    'BR': 'Brazil',
    'BS': 'Bahamas',
    'BT': 'Bhutan',
    'BW': 'Botswana',
    'BY': 'Belarus',
    'BZ': 'Belize',
    'BUMM': 'Myanmar (Burma) (Historic)',
    'CA': 'Canada',
    'CC': 'Cocos (Keeling) Islands',
    'CD': 'Democratic Republic of the Congo',
    'CF': 'Central African Republic',
    'CG': 'Republic of the Congo',
    'CH': 'Switzerland',
    'CI': 'Côte d\'Ivoire',
    'CK': 'Cook Islands',
    'CL': 'Chile',
    'CM': 'Cameroon',
    'CN': 'China',
    'CO': 'Colombia',
    'CR': 'Costa Rica',
    'CSHH': 'Czechoslovakia (Historic)',
    'CSXX': 'Czechoslovakia (Unknown Specific)',
    'CU': 'Cuba',
    'CV': 'Cabo Verde',
    'CW': 'Curaçao',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DDDE': 'East Germany (GDR)',
    'DE': 'Germany',
    'DJ': 'Djibouti',
    'DK': 'Denmark',
    'DM': 'Dominica',
    'DO': 'Dominican Republic',
    'DZ': 'Algeria',
    'EH': 'Western Sahara',
    'EC': 'Ecuador',
    'EE': 'Estonia',
    'EG': 'Egypt',
    'ER': 'Eritrea',
    'ES': 'Spain',
    'ET': 'Ethiopia',
    'FI': 'Finland',
    'FJ': 'Fiji',
    'FM': 'Micronesia',
    'FO': 'Faroe Islands',
    'FR': 'France',
    'GA': 'Gabon',
    'GB': 'United Kingdom',
    'GD': 'Grenada',
    'GE': 'Georgia',
    'GF': 'French Guiana',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GL': 'Greenland',
    'GM': 'Gambia',
    'GN': 'Guinea',
    'GP': 'Guadeloupe',
    'GQ': 'Equatorial Guinea',
    'GR': 'Greece',
    'GT': 'Guatemala',
    'GU': 'Guam',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HK': 'Hong Kong',
    'HN': 'Honduras',
    'HR': 'Croatia',
    'HT': 'Haiti',
    'HU': 'Hungary',
    'ID': 'Indonesia',
    'IE': 'Ireland',
    'IL': 'Israel',
    'IM': 'Isle of Man',
    'IN': 'India',
    'IQ': 'Iraq',
    'IR': 'Iran',
    'IS': 'Iceland',
    'IT': 'Italy',
    'JE': 'Jersey',
    'JM': 'Jamaica',
    'JO': 'Jordan',
    'JP': 'Japan',
    'KE': 'Kenya',
    'KG': 'Kyrgyzstan',
    'KH': 'Cambodia',
    'KI': 'Kiribati',
    'KM': 'Comoros',
    'KN': 'Saint Kitts and Nevis',
    'KP': 'North Korea',
    'KR': 'South Korea',
    'KW': 'Kuwait',
    'KY': 'Cayman Islands',
    'KZ': 'Kazakhstan',
    'LA': 'Laos',
    'LB': 'Lebanon',
    'LC': 'Saint Lucia',
    'LI': 'Liechtenstein',
    'LK': 'Sri Lanka',
    'LR': 'Liberia',
    'LS': 'Lesotho',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'LY': 'Libya',
    'MA': 'Morocco',
    'MC': 'Monaco',
    'MD': 'Moldova',
    'ME': 'Montenegro',
    'MG': 'Madagascar',
    'MH': 'Marshall Islands',
    'MK': 'North Macedonia',
    'ML': 'Mali',
    'MM': 'Myanmar',
    'MN': 'Mongolia',
    'MO': 'Macau',
    'MP': 'Northern Mariana Islands',
    'MQ': 'Martinique',
    'MR': 'Mauritania',
    'MS': 'Montserrat',
    'MT': 'Malta',
    'MU': 'Mauritius',
    'MV': 'Maldives',
    'MW': 'Malawi',
    'MX': 'Mexico',
    'MY': 'Malaysia',
    'MZ': 'Mozambique',
    'NA': 'Namibia',
    'NC': 'New Caledonia',
    'NE': 'Niger',
    'NG': 'Nigeria',
    'NI': 'Nicaragua',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'NP': 'Nepal',
    'NR': 'Nauru',
    'NU': 'Niue',
    'NZ': 'New Zealand',
    'OM': 'Oman',
    'PA': 'Panama',
    'PE': 'Peru',
    'PF': 'French Polynesia',
    'PG': 'Papua New Guinea',
    'PH': 'Philippines',
    'PK': 'Pakistan',
    'PL': 'Poland',
    'PR': 'Puerto Rico',
    'PS': 'Palestine',
    'PT': 'Portugal',
    'PW': 'Palau',
    'PY': 'Paraguay',
    'QA': 'Qatar',
    'RE': 'Réunion',
    'RO': 'Romania',
    'RS': 'Serbia',
    'RU': 'Russia',
    'RW': 'Rwanda',
    'SA': 'Saudi Arabia',
    'SB': 'Solomon Islands',
    'SC': 'Seychelles',
    'SD': 'Sudan',
    'SE': 'Sweden',
    'SG': 'Singapore',
    'SH': 'Saint Helena',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'SL': 'Sierra Leone',
    'SM': 'San Marino',
    'SN': 'Senegal',
    'SO': 'Somalia',
    'SR': 'Suriname',
    'ST': 'São Tomé and Príncipe',
    'SUHH': 'Soviet Union (Historic)',
    'SV': 'El Salvador',
    'SY': 'Syria',
    'SZ': 'Eswatini',
    'TC': 'Turks and Caicos Islands',
    'TD': 'Chad',
    'TG': 'Togo',
    'TH': 'Thailand',
    'TJ': 'Tajikistan',
    'TL': 'Timor-Leste',
    'TM': 'Turkmenistan',
    'TN': 'Tunisia',
    'TO': 'Tonga',
    'TR': 'Turkey',
    'TT': 'Trinidad and Tobago',
    'TV': 'Tuvalu',
    'TW': 'Taiwan',
    'TZ': 'Tanzania',
    'UA': 'Ukraine',
    'UG': 'Uganda',
    'US': 'United States',
    'UY': 'Uruguay',
    'UZ': 'Uzbekistan',
    'VA': 'Vatican City',
    'VC': 'Saint Vincent and the Grenadines',
    'VE': 'Venezuela',
    'VG': 'British Virgin Islands',
    'VI': 'United States Virgin Islands',
    'VN': 'Vietnam',
    'VU': 'Vanuatu',
    'WS': 'Samoa',
    'XAS': 'Asia (Generic)',
    'XAU': 'Australia (Generic)',
    'XEU': 'Europe (Generic)',
    'XKO': 'Kosovo',
    'XKV': 'Kosovo Variant',
    'XNA': 'North America (Generic)',
    'XPI': 'Pacific Islands',
    'XSA': 'South America (Generic)',
    'XSI': 'South Asia (Generic)',
    'XWG': 'West Germany',
    'XWW': 'Worldwide',
    'XYU': 'Yugoslavia (Historic)',
    'YUCS': 'Yugoslavia (Country Split)',
    'YE': 'Yemen',
    'ZA': 'South Africa',
    'ZM': 'Zambia',
    'ZW': 'Zimbabwe',
    'ZRCD': 'Zaire (Now DRC)'
}

def fetch_movies(search_params, page, per_page):
    """Helper function to fetch movies with filters and pagination."""
    query = {}

    # Title filter
    if search_params.get("title"):
        query["primaryTitle"] = {"$regex": search_params["title"], "$options": "i"}

    # Year filter
    if search_params.get("startYear"):
        query["startYear"] = {"$gte": int(search_params["startYear"])}
    if search_params.get("endYear"):
        query["startYear"] = query.get("startYear", {})
        query["startYear"]["$lte"] = int(search_params["endYear"])

    # Genre filter
    if search_params.get("genre"):
        query["genres"] = search_params["genre"]

    # Rating filter
    if search_params.get("minRating"):
        query["averageRating"] = {"$gte": float(search_params["minRating"])}
    if search_params.get("maxRating"):
        query["averageRating"] = query.get("averageRating", {})
        query["averageRating"]["$lte"] = float(search_params["maxRating"])

    # Votes filter
    if search_params.get("minVotes"):
        query["numVotes"] = {"$gte": int(search_params["minVotes"])}

    # Search by Director
    if search_params.get("director"):
        director_name = search_params["director"]
        director = db.name_basics.find_one(
            {"primaryName": {"$regex": director_name, "$options": "i"}},
            {"nconst": 1}
        )
        if director:
            query["directors"] = {"$in": [director["nconst"]]}
        else:
            return []  # No matching director, return empty list

    # Search by Writer
    if search_params.get("writer"):
        writer_name = search_params["writer"]
        writer = db.name_basics.find_one(
            {"primaryName": {"$regex": writer_name, "$options": "i"}},
            {"nconst": 1}
        )
        if writer:
            query["writers"] = {"$in": [writer["nconst"]]}
        else:
            return []  # No matching writer, return empty list

    # Exclude Adult Content
    if search_params.get("isAdult") == "off":
        query["isAdult"] = False  # Exclude adult movies
    elif search_params.get("isAdult") == "on":
        query["isAdult"] = True  # Include only adult movies

    # Pagination logic
    skip = (page - 1) * per_page

    # Fetch from MongoDB
    movies_cursor = db.titles.find(query).skip(skip).limit(per_page)
    movies = list(movies_cursor)

    # Apply localization
    if search_params.get("language"):
        movies = localize_titles(movies, search_params["language"])

    return movies

@app.route('/')
def home():
    """Homepage with a list of movies."""
    return render_template("index.html")

@app.route('/refresh', methods=['GET'])
def refresh_data():
    """Refresh IMDb data by running scripts."""
    app_dir = "/app/"
    import_scripts = [
        "refresh_data.py",
        "import_title.basics.py",
        "import_title.akas.py",
        "import_name.basics.py",
    ]

    # Execute each script in sequence
    for script in import_scripts:
        script_path = os.path.join(app_dir, script)
        process = subprocess.Popen(
            ["python", script_path],
            cwd=app_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Stream stdout and stderr in real-time
        for line in process.stdout:
            print(line, end="")  # Print each line as it appears

        for line in process.stderr:
            print(line, end="")  # Print each error line as it appears

        process.wait()  # Wait for the process to complete

        if process.returncode != 0:
            return f"Error refreshing data: {script} failed.", 500

    return redirect("/")

@app.route('/search', methods=['GET'])
def search():
    """Search route for movies."""
    # Get search parameters
    search_params = {
        "title": request.args.get("title", ""),
        "startYear": request.args.get("startYear", ""),
        "endYear": request.args.get("endYear", ""),
        "minRating": request.args.get("minRating", ""),
        "maxRating": request.args.get("maxRating", ""),
        "minVotes": request.args.get("minVotes", ""),
        "director": request.args.get("director", ""),
        "writer": request.args.get("writer", ""),
        "genre": request.args.get("genre", ""),
        "language": request.args.get("language", ""),
        "isAdult": request.args.get("isAdult", "off"),  # Default to "off" if not in URL
    }

    # Pagination
    page = int(request.args.get("page", 1))
    per_page = 10

    # Fetch movies
    movies = fetch_movies(search_params, page, per_page)

    return render_template("search.html", movies=movies, page=page, search_mode=True, search_params=search_params)

@app.route('/movie/<tconst>')
def movie_details(tconst):
    """Get details of a specific movie."""
    movie = db.titles.find_one({"tconst": tconst}, {"_id": 0})
    if not movie:
        return "Movie not found", 404

    # Fetch and replace director names
    if "directors" in movie:
        movie["directors"] = [
            db.name_basics.find_one({"nconst": nconst}, {"primaryName": 1}).get("primaryName", "")
            for nconst in movie["directors"]
        ]

    # Fetch and replace writer names
    if "writers" in movie:
        movie["writers"] = [
            db.name_basics.find_one({"nconst": nconst}, {"primaryName": 1}).get("primaryName", "")
            for nconst in movie["writers"]
        ]

    # Localize movie title
    language = request.args.get("language")
    if language:
        localized_title = get_localized_title(tconst, language)
        if localized_title:
            movie["primaryTitle"] = localized_title

    return render_template("details.html", movie=movie)

def localize_titles(movies, language):
    """Localize titles for a list of movies."""
    for movie in movies:
        tconst = movie.get("tconst")
        if tconst:
            localized_title = get_localized_title(tconst, language)
            if localized_title:
                movie["primaryTitle"] = localized_title
    return movies

def get_localized_title(tconst, language):
    """Fetch localized title for a movie."""
    query = {"titleId": tconst}
    prioritized_languages = ["cmn", "zh"] if language == "zh" else [language]

    for lang in prioritized_languages:
        query["language"] = lang

        localized_entry = db.akas.find_one(query, {"_id": 0, "title": 1})
        if localized_entry:
            return localized_entry["title"]

    # Fallback to original title
    query = {"titleId": tconst, "isOriginalTitle": 1}
    original_entry = db.akas.find_one(query, {"_id": 0, "title": 1})
    return original_entry["title"] if original_entry else None

@app.context_processor
def inject_filters():
    """Inject genres, languages, and regions into the template context."""
    genres = db.titles.distinct("genres")
    languages = db.akas.distinct("language")
    regions = db.akas.distinct("region")

    # Ensure valid genres
    genres = [genre for genre in genres if genre and isinstance(genre, str)]
    genres.sort()

    # Ensure valid languages, removing 'nan', 'cmn', and 'jsl'
    languages = [
        {"code": lang, "name": LANGUAGE_MAP.get(lang, lang)}
        for lang in languages
        if isinstance(lang, str) and lang.lower() != "nan" and lang != "cmn" and lang != "jsl"
    ]
    languages.sort(key=lambda x: x["name"])

    # Ensure valid regions, removing 'nan'
    regions = [
        {"code": region, "name": REGION_MAP.get(region, region)}
        for region in regions
        if isinstance(region, str) and region.lower() != "nan"
    ]
    regions.sort(key=lambda x: x["name"])

    return {
        "genres": genres,
        "languages": languages,
        "regions": regions,
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)