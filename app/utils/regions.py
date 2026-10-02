from enum import Enum


REGIONS = {
    "Afghanistan": "AF",
    "Angola": "AO",
    "Albania": "AL",
    "Andorra": "AD",
    "United Arab Emirates": "AE",
    "Argentina": "AR",
    "Armenia": "AM",
    "Antigua and Barbuda": "AG",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Burundi": "BI",
    "Belgium": "BE",
    "Benin": "BJ",
    "Burkina Faso": "BF",
    "Bangladesh": "BD",
    "Bulgaria": "BG",
    "Bahrain": "BH",
    "Bahamas": "BS",
    "Bosnia and Herzegovina": "BA",
    "Belarus": "BY",
    "Belize": "BZ",
    "Bolivia": "BO",
    "Brazil": "BR",
    "Barbados": "BB",
    "Brunei": "BN",
    "Bhutan": "BT",
    "Botswana": "BW",
    "Central African Republic": "CF",
    "Canada": "CA",
    "Switzerland": "CH",
    "Chile": "CL",
    "China": "CN",
    "Côte d'Ivoire": "CI",
    "Cameroon": "CM",
    "Democratic Republic of the Congo": "CD",
    "Republic of the Congo": "CG",
    "Colombia": "CO",
    "Comoros": "KM",
    "Cape Verde": "CV",
    "Costa Rica": "CR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Germany": "DE",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Denmark": "DK",
    "Dominican Republic": "DO",
    "Algeria": "DZ",
    "Ecuador": "EC",
    "Egypt": "EG",
    "Eritrea": "ER",
    "Spain": "ES",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Finland": "FI",
    "Fiji": "FJ",
    "France": "FR",
    "Micronesia": "FM",
    "Gabon": "GA",
    "United Kingdom": "GB",
    "Georgia": "GE",
    "Ghana": "GH",
    "Guinea": "GN",
    "Gambia": "GM",
    "Guinea-Bissau": "GW",
    "Equatorial Guinea": "GQ",
    "Greece": "GR",
    "Grenada": "GD",
    "Guatemala": "GT",
    "Guyana": "GY",
    "Honduras": "HN",
    "Croatia": "HR",
    "Haiti": "HT",
    "Hungary": "HU",
    "Indonesia": "ID",
    "India": "IN",
    "Ireland": "IE",
    "Iran": "IR",
    "Iraq": "IQ",
    "Iceland": "IS",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Jordan": "JO",
    "Japan": "JP",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kyrgyzstan": "KG",
    "Cambodia": "KH",
    "Kiribati": "KI",
    "Saint Kitts and Nevis": "KN",
    "South Korea": "KR",
    "Kuwait": "KW",
    "Laos": "LA",
    "Lebanon": "LB",
    "Liberia": "LR",
    "Libya": "LY",
    "Saint Lucia": "LC",
    "Liechtenstein": "LI",
    "Sri Lanka": "LK",
    "Lesotho": "LS",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Latvia": "LV",
    "Morocco": "MA",
    "Monaco": "MC",
    "Moldova": "MD",
    "Madagascar": "MG",
    "Maldives": "MV",
    "Mexico": "MX",
    "Marshall Islands": "MH",
    "North Macedonia": "MK",
    "Mali": "ML",
    "Malta": "MT",
    "Myanmar": "MM",
    "Montenegro": "ME",
    "Mongolia": "MN",
    "Mozambique": "MZ",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Namibia": "NA",
    "Niger": "NE",
    "Nigeria": "NG",
    "Nicaragua": "NI",
    "Netherlands": "NL",
    "Norway": "NO",
    "Nepal": "NP",
    "Nauru": "NR",
    "New Zealand": "NZ",
    "Oman": "OM",
    "Pakistan": "PK",
    "Panama": "PA",
    "Peru": "PE",
    "Philippines": "PH",
    "Palau": "PW",
    "Papua New Guinea": "PG",
    "Poland": "PL",
    "North Korea": "KP",
    "Portugal": "PT",
    "Paraguay": "PY",
    "Palestine": "PS",
    "Qatar": "QA",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saudi Arabia": "SA",
    "Sudan": "SD",
    "Senegal": "SN",
    "Singapore": "SG",
    "Solomon Islands": "SB",
    "Sierra Leone": "SL",
    "El Salvador": "SV",
    "San Marino": "SM",
    "Somalia": "SO",
    "Serbia": "RS",
    "South Sudan": "SS",
    "São Tomé and Príncipe": "ST",
    "Suriname": "SR",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Sweden": "SE",
    "Taiwan": "TW",
    "Eswatini": "SZ",
    "Seychelles": "SC",
    "Syria": "SY",
    "Chad": "TD",
    "Togo": "TG",
    "Thailand": "TH",
    "Tajikistan": "TJ",
    "Turkmenistan": "TM",
    "Timor-Leste": "TL",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Türkiye": "TR",
    "Tuvalu": "TV",
    "Tanzania": "TZ",
    "Uganda": "UG",
    "Ukraine": "UA",
    "Uruguay": "UY",
    "United States": "US",
    "Uzbekistan": "UZ",
    "Vatican City": "VA",
    "Saint Vincent and the Grenadines": "VC",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Vanuatu": "VU",
    "Samoa": "WS",
    "Yemen": "YE",
    "South Africa": "ZA",
    "Zambia": "ZM",
    "Zimbabwe": "ZW",
    "NO": "NO"
}

class Regions(str, Enum):
    # 193 члена ООН + наблюдатели (VA, PS) + TW = 196
    # TW — де-факто юрисдикция, включена практических ради (как у Stripe/Google)
    AFGHANISTAN = "AF"
    ANGOLA = "AO"
    ALBANIA = "AL"
    ANDORRA = "AD"
    UNITED_ARAB_EMIRATES = "AE"
    ARGENTINA = "AR"
    ARMENIA = "AM"
    ANTIGUA_AND_BARBUDA = "AG"
    AUSTRALIA = "AU"
    AUSTRIA = "AT"
    AZERBAIJAN = "AZ"
    BURUNDI = "BI"
    BELGIUM = "BE"
    BENIN = "BJ"
    BURKINA_FASO = "BF"
    BANGLADESH = "BD"
    BULGARIA = "BG"
    BAHRAIN = "BH"
    BAHAMAS = "BS"
    BOSNIA_AND_HERZEGOVINA = "BA"
    BELARUS = "BY"
    BELIZE = "BZ"
    BOLIVIA = "BO"
    BRAZIL = "BR"
    BARBADOS = "BB"
    BRUNEI = "BN"
    BHUTAN = "BT"
    BOTSWANA = "BW"
    CENTRAL_AFRICAN_REPUBLIC = "CF"
    CANADA = "CA"
    SWITZERLAND = "CH"
    CHILE = "CL"
    CHINA = "CN"
    COTE_D_IVOIRE = "CI"
    CAMEROON = "CM"
    DEMOCRATIC_REPUBLIC_OF_CONGO = "CD"
    CONGO = "CG"
    COLOMBIA = "CO"
    COMOROS = "KM"
    CAPE_VERDE = "CV"
    COSTA_RICA = "CR"
    CUBA = "CU"
    CYPRUS = "CY"
    CZECHIA = "CZ"
    GERMANY = "DE"
    DJIBOUTI = "DJ"
    DOMINICA = "DM"
    DENMARK = "DK"
    DOMINICAN_REPUBLIC = "DO"
    ALGERIA = "DZ"
    ECUADOR = "EC"
    EGYPT = "EG"
    ERITREA = "ER"
    SPAIN = "ES"
    ESTONIA = "EE"
    ETHIOPIA = "ET"
    FINLAND = "FI"
    FIJI = "FJ"
    FRANCE = "FR"
    MICRONESIA = "FM"
    GABON = "GA"
    UNITED_KINGDOM = "GB"
    GEORGIA = "GE"
    GHANA = "GH"
    GUINEA = "GN"
    GAMBIA = "GM"
    GUINEA_BISSAU = "GW"
    EQUATORIAL_GUINEA = "GQ"
    GREECE = "GR"
    GRENADA = "GD"
    GUATEMALA = "GT"
    GUYANA = "GY"
    HONDURAS = "HN"
    CROATIA = "HR"
    HAITI = "HT"
    HUNGARY = "HU"
    INDONESIA = "ID"
    INDIA = "IN"
    IRELAND = "IE"
    IRAN = "IR"
    IRAQ = "IQ"
    ICELAND = "IS"
    ISRAEL = "IL"
    ITALY = "IT"
    JAMAICA = "JM"
    JORDAN = "JO"
    JAPAN = "JP"
    KAZAKHSTAN = "KZ"
    KENYA = "KE"
    KYRGYZSTAN = "KG"
    CAMBODIA = "KH"
    KIRIBATI = "KI"
    SAINT_KITTS_AND_NEVIS = "KN"
    SOUTH_KOREA = "KR"
    KUWAIT = "KW"
    LAOS = "LA"
    LEBANON = "LB"
    LIBERIA = "LR"
    LIBYA = "LY"
    SAINT_LUCIA = "LC"
    LIECHTENSTEIN = "LI"
    SRI_LANKA = "LK"
    LESOTHO = "LS"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    LATVIA = "LV"
    MOROCCO = "MA"
    MONACO = "MC"
    MOLDOVA = "MD"
    MADAGASCAR = "MG"
    MALDIVES = "MV"
    MEXICO = "MX"
    MARSHALL_ISLANDS = "MH"
    NORTH_MACEDONIA = "MK"
    MALI = "ML"
    MALTA = "MT"
    MYANMAR = "MM"
    MONTENEGRO = "ME"
    MONGOLIA = "MN"
    MOZAMBIQUE = "MZ"
    MAURITANIA = "MR"
    MAURITIUS = "MU"
    MALAWI = "MW"
    MALAYSIA = "MY"
    NAMIBIA = "NA"
    NIGER = "NE"
    NIGERIA = "NG"
    NICARAGUA = "NI"
    NETHERLANDS = "NL"
    NORWAY = "NO"
    NEPAL = "NP"
    NAURU = "NR"
    NEW_ZEALAND = "NZ"
    OMAN = "OM"
    PAKISTAN = "PK"
    PANAMA = "PA"
    PERU = "PE"
    PHILIPPINES = "PH"
    PALAU = "PW"
    PAPUA_NEW_GUINEA = "PG"
    POLAND = "PL"
    NORTH_KOREA = "KP"
    PORTUGAL = "PT"
    PARAGUAY = "PY"
    PALESTINE = "PS"
    QATAR = "QA"
    ROMANIA = "RO"
    RUSSIA = "RU"
    RWANDA = "RW"
    SAUDI_ARABIA = "SA"
    SUDAN = "SD"
    SENEGAL = "SN"
    SINGAPORE = "SG"
    SOLOMON_ISLANDS = "SB"
    SIERRA_LEONE = "SL"
    EL_SALVADOR = "SV"
    SAN_MARINO = "SM"
    SOMALIA = "SO"
    SERBIA = "RS"
    SOUTH_SUDAN = "SS"
    SAO_TOME_AND_PRINCIPE = "ST"
    SURINAME = "SR"
    SLOVAKIA = "SK"
    SLOVENIA = "SI"
    SWEDEN = "SE"
    TAIWAN = "TW"
    ESWATINI = "SZ"
    SEYCHELLES = "SC"
    SYRIA = "SY"
    CHAD = "TD"
    TOGO = "TG"
    THAILAND = "TH"
    TAJIKISTAN = "TJ"
    TURKMENISTAN = "TM"
    TIMOR_LESTE = "TL"
    TONGA = "TO"
    TRINIDAD_AND_TOBAGO = "TT"
    TUNISIA = "TN"
    TURKEY = "TR"
    TUVALU = "TV"
    TANZANIA = "TZ"
    UGANDA = "UG"
    UKRAINE = "UA"
    URUGUAY = "UY"
    UNITED_STATES = "US"
    UZBEKISTAN = "UZ"
    VATICAN_CITY = "VA"
    SAINT_VINCENT_AND_THE_GRENADINES = "VC"
    VENEZUELA = "VE"
    VIETNAM = "VN"
    VANUATU = "VU"
    SAMOA = "WS"
    YEMEN = "YE"
    SOUTH_AFRICA = "ZA"
    ZAMBIA = "ZM"
    ZIMBABWE = "ZW"
    NO = "NO"