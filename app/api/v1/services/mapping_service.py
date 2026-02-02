import os
from app.config.settings import get_settings
from sqlalchemy import text
import mysql.connector
import unicodedata

settings = get_settings()

class MappingService:
    def __init__(self):

        self.host = settings.db_host
        self.user = settings.db_user
        self.password = settings.db_password
        self.database = settings.db_name

        # --- Aryabhatta numeration mappings ---
        self.consonant_values = {}
        self.vowel_multipliers = {}

        # Latin ↔ Devanagari mappings
        self.consonant_devanagari = {}
        self.vowel_devanagari = {}
        self.devanagari_to_latin_consonant_map = {}
        self.devanagari_to_latin_vowel_map = {}

        # Devanagari matras/modifiers
        self.DEVANAGARI_MATRA_TO_LATIN_VOWEL = {}
        self.DEVANAGARI_MODIFIERS_TO_LATIN = {}

        self.DEVANAGARI_MATRAS_SET = set([
            'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'े', 'ै', 'ो', 'ौ'
        ])

        self.MATRA_TO_FULL_VOWEL = {
            'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
            'ृ': 'ऋ', 'ॄ': 'ॠ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
        }

        # Kannada mappings
        self.kannada_to_latin_consonant_map = {}
        self.kannada_to_latin_vowel_map = {}
        self.kannada_MATRAS_SET = set()
        self.kannada_MATRA_TO_LATIN_VOWEL = {}
        self.kannada_MODIFIERS_TO_LATIN = {}

        # Cross-language mappings for Kannada
        self.latin_to_kannada_consonant = {}  # This was missing
        self.latin_to_kannada_vowel = {}      # This was missing
        self.devanagari_to_kannada_matra = {}
        self.devanagari_to_kannada_modifier = {}

        # Telugu mappings
        self.telugu_to_latin_consonant_map = {}
        self.telugu_to_latin_vowel_map = {}
        self.telugu_MATRAS_SET = set()
        self.telugu_MATRA_TO_LATIN_VOWEL = {}
        self.telugu_MODIFIERS_TO_LATIN = {}

        # Cross-language mappings - comment Tamil ones
        # self.latin_to_tamil_consonant = {}
        # self.latin_to_tamil_vowel = {}
        # self.devanagari_to_tamil_matra = {}
        # self.devanagari_to_tamil_modifier = {}
        self.latin_to_telugu_consonant = {}
        self.latin_to_telugu_vowel = {}
        self.devanagari_to_telugu_matra = {}
        self.devanagari_to_telugu_modifier = {}

        # Malayalam mappings
        self.malayalam_to_latin_consonant_map = {}
        self.malayalam_to_latin_vowel_map = {}
        self.malayalam_MATRAS_SET = set()
        self.malayalam_MATRA_TO_LATIN_VOWEL = {}
        self.malayalam_MODIFIERS_TO_LATIN = {}
        self.latin_to_malayalam_consonant = {}
        self.latin_to_malayalam_vowel = {}
        self.devanagari_to_malayalam_matra = {}
        self.devanagari_to_malayalam_modifier = {}

        self.KANNADA_MATRA_TO_FULL_VOWEL = {
            'ಾ': 'ಆ', 'ಿ': 'ಇ', 'ೀ': 'ಈ', 'ು': 'ಉ', 'ೂ': 'ಊ',
            'ೃ': 'ಋ', 'ೄ': 'ೠ', 'ೆ': 'ಎ', 'ೇ': 'ಏ', 'ೈ': 'ಐ',
            'ೊ': 'ಒ', 'ೋ': 'ಓ', 'ೌ': 'ಔ'
        }

        # Comment out Tamil matra map
        # self.TAMIL_MATRA_TO_FULL_VOWEL = {
        #     'ா': 'ஆ',   # aa
        #     'ி': 'இ',   # i
        #     'ீ': 'ஈ',   # ii
        #     'ு': 'உ',   # u
        #     'ூ': 'ஊ',   # uu
        #     'ெ': 'எ',   # e
        #     'ே': 'ஏ',   # ee
        #     'ை': 'ஐ',   # ai
        #     'ொ': 'ஒ',   # o
        #     'ோ': 'ஓ',   # oo
        #     'ௌ': 'ஔ'    # au
        # }

        self.TELUGU_MATRA_TO_FULL_VOWEL = {
            'ా': 'ఆ',   # aa
            'ి': 'ఇ',   # i
            'ీ': 'ఈ',   # ii
            'ు': 'ఉ',   # u
            'ూ': 'ఊ',   # uu
            'ృ': 'ఋ',   # r
            'ె': 'ఎ',   # e
            'ే': 'ఏ',   # ee
            'ై': 'ఐ',   # ai
            'ొ': 'ఒ',   # o
            'ో': 'ఓ',   # oo
            'ౌ': 'ఔ'    # au
        }

        self.MALAYALAM_MATRA_TO_FULL_VOWEL = {
            'ാ': 'ആ',   # aa
            'ി': 'ഇ',   # i
            'ീ': 'ഈ',   # ii
            'ു': 'ഉ',   # u
            'ൂ': 'ഊ',   # uu
            'ൃ': 'ഋ',   # r
            'െ': 'എ',   # e
            'േ': 'ഏ',   # ee
            'ൈ': 'ഐ',   # ai
            'ൊ': 'ഒ',   # o
            'ോ': 'ഓ',   # oo
            'ൌ': 'ഔ'    # au
        }

        # Add placeholder for Tamil mappings (to prevent errors in case referenced elsewhere)
        self.tamil_MATRAS_SET = set()
        self.tamil_MODIFIERS_TO_LATIN = {}
        self.tamil_to_latin_consonant_map = {}
        self.tamil_to_latin_vowel_map = {}
        self.TAMIL_MATRA_TO_FULL_VOWEL = {}

        # Stores Dev/Kann/Latin char -> hex color
        self.character_colors_map = {}

    # -------- Initialization Methods --------
    def load_character_colors_from_db(self, db_config=None):


        config = db_config or {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "database": self.database
        }

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            # Update query to include telugu_char
            cursor.execute("""
                SELECT devanagari_char, latin_char, kannada_char,
                       telugu_char,malayalam_char, color_hex
                FROM colour_mapping
            """)
            self.character_colors_map.clear()
            for dev, lat, kan, tel, mal, hexcol in cursor.fetchall():
                if dev: self.character_colors_map[dev] = hexcol
                if lat: self.character_colors_map[lat] = hexcol
                if kan: self.character_colors_map[kan] = hexcol
                if tel: self.character_colors_map[tel] = hexcol  # Add Telugu character colors
                if mal: self.character_colors_map[mal] = hexcol  # Add Malayalam character colors
        except Exception as e:
            print(f"[ERROR] Loading character colors failed: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()



    def get_db_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_color_mappings(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    id,
                    devanagari_char,
                    latin_char,
                    kannada_char,
                    telugu_char,
                    malayalam_char,
                    category,
                    place_of_articulation,
                    sthana,
                    numeric_value,
                    color_hex,
                    color_r,
                    color_g,
                    color_b,
                    colour_shade
                FROM colour_mapping
                ORDER BY id ASC
            """)
            rows = cursor.fetchall()
            return rows or []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()




    def closest_character(self, r: int, g: int, b: int):
        """
        Find the closest character given an RGB input.
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT devanagari_char, color_r, color_g, color_b, colour_shade, sthana
                FROM colour_mapping
            """)
            mappings = cursor.fetchall()

            closest_char, closest_shade, closest_sthana = None, None, None
            min_dist = float("inf")

            for row in mappings:
                dist = ((row["color_r"] - r) ** 2 +
                        (row["color_g"] - g) ** 2 +
                        (row["color_b"] - b) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest_char = row["devanagari_char"]
                    closest_shade = row["colour_shade"]
                    closest_sthana = row["sthana"]

            cursor.close(); conn.close()

            if closest_char:
                return {
                    "closest_character": closest_char,
                    "colour_shade": closest_shade,
                    "sthana": closest_sthana
                }
            else:
                return {"error": "No characters found"}
        except Exception as e:
            return {"error": str(e)}

    def get_colors(self):
        """
        Returns all character colors, including implicit mappings if needed.
        """
        colors_with_implicit = self.character_colors_map.copy()

        implicit_map = {
            "अ (implicit)": "अ",
            "ಆ (implicit)": "ಆ",
            "a (implicit)": "a",
            "അ (implicit)": "അ",  # Malayalam implicit vowel
            # add more implicit → explicit mappings as required
        }

        for implicit_char, explicit_char in implicit_map.items():
            if explicit_char in colors_with_implicit:
                colors_with_implicit[implicit_char] = colors_with_implicit[explicit_char]

        return colors_with_implicit


    def load_initial_values_from_db(self):
        """Loads all mappings from DB into memory."""
        try:
            print("[INFO] Loading mappings from DB...")
            conn = self.get_db_connection()
            cursor = conn.cursor()  # optional: dictionary rows

            # Load consonant mappings
            cursor.execute("SELECT latin_character, char_id, devanagari_character FROM consonants_latin")

            for latin_char, code, dev_char in cursor.fetchall():

                if not dev_char or not latin_char:
                    continue
                self.consonant_values[latin_char] = int(code)
                self.consonant_devanagari[latin_char] = dev_char
                if dev_char:
                    self.devanagari_to_latin_consonant_map[
                        unicodedata.normalize('NFC', dev_char)
                    ] = latin_char

            # Load vowel mappings
            cursor.execute("SELECT latin_character, char_id, devanagari_character FROM vowels_latin")
            for latin_char, code, dev_char in cursor.fetchall():

                self.vowel_multipliers[latin_char] = int(code)
                self.vowel_devanagari[latin_char] = dev_char
                if dev_char:
                    self.devanagari_to_latin_vowel_map[
                        unicodedata.normalize('NFC', dev_char)
                    ] = latin_char


            # Load Devanagari matras
            cursor.execute("SELECT devanagari_char, latin_equivalent_vowel FROM devanagari_matras_map")
            for dev_matra_char, latin_vowel_eq in cursor.fetchall():
                self.DEVANAGARI_MATRA_TO_LATIN_VOWEL[
                    unicodedata.normalize('NFC', dev_matra_char)
                ] = latin_vowel_eq

            # Load Devanagari modifiers
            cursor.execute("SELECT devanagari_char, latin_equivalent_modifier FROM devanagari_modifiers_map")
            for dev_mod_char, latin_mod_eq in cursor.fetchall():
                self.DEVANAGARI_MODIFIERS_TO_LATIN[
                    unicodedata.normalize('NFC', dev_mod_char)
                ] = latin_mod_eq

            # Load Kannada mappings (reusing same connection)
            self._load_kannada_mappings_from_db(conn)

            # Comment out Tamil loading
            # self._load_tamil_mappings_from_db(conn)

            # Load Telugu mappings
            self._load_telugu_mappings_from_db(conn)

            # Load Malayalam mappings
            self._load_malayalam_mappings_from_db(conn)

        except mysql.connector.Error as err:
            print(f"[ERROR] DB load failed: {err}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def _load_kannada_mappings_from_db(self, db_conn):
        """Loads Kannada-specific mappings."""
        try:
            cursor = db_conn.cursor()

            # Consonants
            cursor.execute("SELECT kannada_character, devanagari_character FROM consonants_kannada")
            for kannada_char, dev_char in cursor.fetchall():
                latin_equiv = self.devanagari_to_latin_consonant_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.kannada_to_latin_consonant_map[
                        unicodedata.normalize('NFC', kannada_char)
                    ] = latin_equiv
                    self.latin_to_kannada_consonant[latin_equiv] = unicodedata.normalize('NFC', kannada_char)

            # Vowels
            cursor.execute("SELECT kannada_character, devanagari_character FROM vowels_kannada")
            for kannada_char, dev_char in cursor.fetchall():
                latin_equiv = self.devanagari_to_latin_vowel_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.kannada_to_latin_vowel_map[
                        unicodedata.normalize('NFC', kannada_char)
                    ] = latin_equiv
                    self.latin_to_kannada_vowel[latin_equiv] = unicodedata.normalize('NFC', kannada_char)

            # Matras
            cursor.execute("SELECT kannada_char, devanagari_char FROM kannada_matras_map")
            for kannada_matra, dev_matra in cursor.fetchall():
                dev_latin_equiv = self.DEVANAGARI_MATRA_TO_LATIN_VOWEL.get(
                    unicodedata.normalize('NFC', dev_matra)
                )
                if dev_latin_equiv:
                    kannada_norm = unicodedata.normalize('NFC', kannada_matra)
                    self.kannada_MATRAS_SET.add(kannada_norm)
                    self.kannada_MATRA_TO_LATIN_VOWEL[kannada_norm] = dev_latin_equiv
                    self.devanagari_to_kannada_matra[unicodedata.normalize('NFC', dev_matra)] = kannada_norm

            # Modifiers
            cursor.execute("SELECT kannada_char, devanagari_char FROM kannada_modifiers_map")
            for kannada_mod, dev_mod in cursor.fetchall():
                dev_latin_equiv = self.DEVANAGARI_MODIFIERS_TO_LATIN.get(
                    unicodedata.normalize('NFC', dev_mod or "")
                )
                if dev_latin_equiv:
                    kannada_norm = unicodedata.normalize('NFC', kannada_mod)
                    self.kannada_MODIFIERS_TO_LATIN[kannada_norm] = dev_latin_equiv
                    self.devanagari_to_kannada_modifier[unicodedata.normalize('NFC', dev_mod)] = kannada_norm

        except mysql.connector.Error as err:
            print(f"[ERROR] Kannada load failed: {err}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()


    def _load_tamil_mappings_from_db(self, db_conn):
        """Loads Tamil-specific mappings."""
        pass  # Commented out as per instructions

    def _load_telugu_mappings_from_db(self, db_conn):
        """Loads Telugu-specific mappings."""
        try:
            cursor = db_conn.cursor()

            # Load Telugu consonants
            cursor.execute("SELECT telugu_character, devanagari_character FROM consonants_telugu")
            for teluguChar, dev_char in cursor.fetchall():
                latin_equiv = self.devanagari_to_latin_consonant_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.telugu_to_latin_consonant_map[
                        unicodedata.normalize('NFC', teluguChar)
                    ] = latin_equiv
                    self.latin_to_telugu_consonant[latin_equiv] = unicodedata.normalize('NFC', teluguChar)

            # Load Telugu vowels
            cursor.execute("SELECT telugu_character, devanagari_character FROM vowels_telugu")
            for teluguChar, dev_char in cursor.fetchall():
                latin_equiv = self.devanagari_to_latin_vowel_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.telugu_to_latin_vowel_map[
                        unicodedata.normalize('NFC', teluguChar)
                    ] = latin_equiv
                    self.latin_to_telugu_vowel[latin_equiv] = unicodedata.normalize('NFC', teluguChar)

            # Load Telugu matras
            cursor.execute("SELECT telugu_char, devanagari_char FROM telugu_matras_map")
            for telugu_matra, dev_matra in cursor.fetchall():
                dev_latin_equiv = self.DEVANAGARI_MATRA_TO_LATIN_VOWEL.get(
                    unicodedata.normalize('NFC', dev_matra)
                )
                if dev_latin_equiv:
                    telugu_norm = unicodedata.normalize('NFC', telugu_matra)
                    self.telugu_MATRAS_SET.add(telugu_norm)
                    self.telugu_MATRA_TO_LATIN_VOWEL[telugu_norm] = dev_latin_equiv
                    self.devanagari_to_telugu_matra[unicodedata.normalize('NFC', dev_matra)] = telugu_norm

            # Load Telugu modifiers
            cursor.execute("SELECT telugu_char, devanagari_char FROM telugu_modifiers_map")
            for telugu_mod, dev_mod in cursor.fetchall():
                dev_latin_equiv = self.DEVANAGARI_MODIFIERS_TO_LATIN.get(
                    unicodedata.normalize('NFC', dev_mod or "")
                )
                if dev_latin_equiv:
                    telugu_norm = unicodedata.normalize('NFC', telugu_mod)
                    self.telugu_MODIFIERS_TO_LATIN[telugu_norm] = dev_latin_equiv
                    self.devanagari_to_telugu_modifier[unicodedata.normalize('NFC', dev_mod)] = telugu_norm

        except mysql.connector.Error as err:
            print(f"[ERROR] Telugu load failed: {err}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def _load_malayalam_mappings_from_db(self, db_conn):
        """Loads Malayalam-specific mappings."""
        try:
            cursor = db_conn.cursor()

            # Load Malayalam consonants
            cursor.execute("SELECT malayalam_character, devanagari_character FROM consonants_malayalam")
            for malayalamChar, dev_char in cursor.fetchall():
                if not malayalamChar or not dev_char:
                    continue
                latin_equiv = self.devanagari_to_latin_consonant_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.malayalam_to_latin_consonant_map[
                        unicodedata.normalize('NFC', malayalamChar)
                    ] = latin_equiv
                    self.latin_to_malayalam_consonant[latin_equiv] = unicodedata.normalize('NFC', malayalamChar)

            # Load Malayalam vowels
            cursor.execute("SELECT malayalam_character, devanagari_character FROM vowels_malayalam")
            for malayalamChar, dev_char in cursor.fetchall():
                if not malayalamChar or not dev_char:
                    continue
                latin_equiv = self.devanagari_to_latin_vowel_map.get(
                    unicodedata.normalize('NFC', dev_char)
                )
                if latin_equiv:
                    self.malayalam_to_latin_vowel_map[
                        unicodedata.normalize('NFC', malayalamChar)
                    ] = latin_equiv
                    self.latin_to_malayalam_vowel[latin_equiv] = unicodedata.normalize('NFC', malayalamChar)

            # Load Malayalam matras
            cursor.execute("SELECT malayalam_char, devanagari_char FROM malayalam_matras_map")
            for malayalam_matra, dev_matra in cursor.fetchall():
                if not malayalam_matra or not dev_matra:
                    continue
                dev_latin_equiv = self.DEVANAGARI_MATRA_TO_LATIN_VOWEL.get(
                    unicodedata.normalize('NFC', dev_matra)
                )
                if dev_latin_equiv:
                    malayalam_norm = unicodedata.normalize('NFC', malayalam_matra)
                    self.malayalam_MATRAS_SET.add(malayalam_norm)
                    self.malayalam_MATRA_TO_LATIN_VOWEL[malayalam_norm] = dev_latin_equiv
                    self.devanagari_to_malayalam_matra[unicodedata.normalize('NFC', dev_matra)] = malayalam_norm

            # Load Malayalam modifiers
            cursor.execute("SELECT malayalam_char, devanagari_char FROM malayalam_modifiers_map")
            for malayalam_mod, dev_mod in cursor.fetchall():
                if not malayalam_mod or not dev_mod:
                    continue
                dev_latin_equiv = self.DEVANAGARI_MODIFIERS_TO_LATIN.get(
                    unicodedata.normalize('NFC', dev_mod)
                )
                if dev_latin_equiv:
                    malayalam_norm = unicodedata.normalize('NFC', malayalam_mod)
                    self.malayalam_MODIFIERS_TO_LATIN[malayalam_norm] = dev_latin_equiv
                    self.devanagari_to_malayalam_modifier[unicodedata.normalize('NFC', dev_mod)] = malayalam_norm

        except mysql.connector.Error as err:
            print(f"[ERROR] Malayalam load failed: {err}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()





    # -------- Utilities --------
    @staticmethod
    def get_digits(number: int):
        """Converts a number into list of its digits."""
        return [int(d) for d in str(abs(number)) if d.isdigit()]

    def expand_matras_to_vowels(self, input_text, script_matras_set, matra_to_full_vowel_map):
        """Expands Devanagari/Kannada matras into full vowels."""
        output_text = ''
        i = 0
        while i < len(input_text):
            current_char = input_text[i]
            if current_char not in script_matras_set and (i + 1) < len(input_text) and input_text[i + 1] in script_matras_set:
                next_char = input_text[i + 1]
                expanded_vowel = matra_to_full_vowel_map.get(next_char, '')
                output_text += current_char + expanded_vowel
                i += 2
            else:
                output_text += current_char
                i += 1
        return output_text

    def calculate_digit_sum(self, number):
        """Calculates the sum of digits of a given number."""
        digits = self.get_digits(number)
        return sum(digits)

    def calculate_digit_product(self, number):
        """Calculates the product of digits of a given number."""
        digits = self.get_digits(number)
        if not digits:
            return 0
        product = 1
        for d in digits:
            product *= d
        return product

    def calculate_digit_difference_fd(self,number):
        """Calculates the difference of digits from left to right: (d1 - d2 - d3 ...)."""
        digits = self.get_digits(number)
        if not digits:
            return 0
        if len(digits) == 1:
            return digits[0]
        result = digits[0]
        for d in digits[1:]:
            result -= d
        return result

    def calculate_digit_difference_bd(self,number):
        """Calculates the difference of digits from right to left: (dn - dn-1 - ... - d1)."""
        digits = self.get_digits(number)
        if not digits:
            return 0
        if len(digits) == 1:
            return digits[0]
        result = digits[-1]
        for d in reversed(digits[:-1]):
            result -= d
        return result

    def calculate_digit_quotient_fd(self,number):
        """
        Calculates the quotient of digits from left to right: ((d1 / d2) / d3 ...).
        Returns 'Infinity' on division by zero.
        """
        digits = self.get_digits(number)
        if not digits:
            return 0
        if len(digits) == 1:
            return digits[0]

        result = float(digits[0])
        for d in digits[1:]:
            if d == 0:
                if result == 0.0:
                    return "Error: Indeterminate (0/0)"
                return "Infinity" if result >= 0 else "-Infinity"
            result /= d
        return result

    def calculate_digit_quotient_bd(self,number):
        """
        Calculates the quotient of digits from right to left: ((dn / dn-1) / ... / d1).
        Returns 'Infinity' on division by zero.
        """
        digits = self.get_digits(number)
        if not digits:
            return 0
        if len(digits) == 1:
            return digits[0]

        result = float(digits[-1])
        for d in reversed(digits[:-1]):
            if d == 0:
                if result == 0.0:
                    return "Error: Indeterminate (0/0)"
                return "Infinity" if result >= 0 else "-Infinity"
            result /= d
        return result

    # -------- Tokenizer Logic for Aryabhatta Numeration --------
    def tokenize_sentence(self, text, input_script):
        """
        Tokenizes a single word into its Aryabhatta numerical value and a breakdown.
        Handles Latin transliteration, Devanagari script, and Kannada script.
        """
        # Normalize input text to NFC for consistent character matching
        text = unicodedata.normalize('NFC', text)

        if input_script == 'latin':
            cleaned_word = ''.join(
                unicodedata.normalize('NFC', char.lower()) for char in text
                if not unicodedata.category(char).startswith('P')
            )
        elif input_script in ['devanagari', 'kannada', 'tamil', 'telugu', 'malayalam']:
            cleaned_word = ''.join(
                unicodedata.normalize('NFC', char) for char in text
                if not unicodedata.category(char).startswith('P') and not unicodedata.category(char).startswith('Z')
            ).strip()

            # Expand matras to full vowels based on the script
            if input_script == 'devanagari':
                cleaned_word = self.expand_matras_to_vowels(cleaned_word, self.DEVANAGARI_MATRAS_SET, self.MATRA_TO_FULL_VOWEL)
            elif input_script == 'kannada':
                cleaned_word = self.expand_matras_to_vowels(
                    cleaned_word,
                    self.kannada_MATRAS_SET,
                    self.KANNADA_MATRA_TO_FULL_VOWEL
                )
            elif input_script == 'tamil':
                cleaned_word = self.expand_matras_to_vowels(cleaned_word, self.tamil_MATRAS_SET, self.TAMIL_MATRA_TO_FULL_VOWEL)
            elif input_script == 'telugu':
                cleaned_word = self.expand_matras_to_vowels(cleaned_word, self.telugu_MATRAS_SET, self.TELUGU_MATRA_TO_FULL_VOWEL)
            elif input_script == 'malayalam':
                cleaned_word = self.expand_matras_to_vowels(cleaned_word, self.malayalam_MATRAS_SET, self.MALAYALAM_MATRA_TO_FULL_VOWEL)
        else:
            return [], []

        word_to_process = cleaned_word.split()[0] if cleaned_word else ""

        tokens = []
        all_numbers_in_word = []

        if not word_to_process:
            return [], []

        current_word_aryabhatta_value = 0
        current_consonant_sum = 0
        processed_letters_data = []

        i = 0
        while i < len(word_to_process):
            char_processed_in_this_iteration = False  # Reset at start of each iteration

            # --- Determine script-specific maps ---
            if input_script == 'latin':
                sorted_consonant_keys = sorted(self.consonant_values.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.vowel_multipliers.keys(), key=len, reverse=True)
                map_consonant_to_latin = lambda k: k
                map_vowel_to_latin = lambda k: k
            elif input_script == 'devanagari':
                sorted_consonant_keys = sorted(self.devanagari_to_latin_consonant_map.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.devanagari_to_latin_vowel_map.keys(), key=len, reverse=True)
                map_consonant_to_latin = self.devanagari_to_latin_consonant_map.get
                map_vowel_to_latin = self.devanagari_to_latin_vowel_map.get
            elif input_script == 'kannada':
                sorted_consonant_keys = sorted(self.kannada_to_latin_consonant_map.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.kannada_to_latin_vowel_map.keys(), key=len, reverse=True)
                map_consonant_to_latin = self.kannada_to_latin_consonant_map.get
                map_vowel_to_latin = self.kannada_to_latin_vowel_map.get

            elif input_script == 'tamil':
                sorted_consonant_keys = sorted(self.tamil_to_latin_consonant_map.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.tamil_to_latin_vowel_map.keys(), key=len, reverse=True)
                map_consonant_to_latin = self.tamil_to_latin_consonant_map.get
                map_vowel_to_latin = self.tamil_to_latin_vowel_map.get
            elif input_script == 'telugu':
                sorted_consonant_keys = sorted(self.telugu_to_latin_consonant_map.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.telugu_to_latin_vowel_map.keys(), key=len, reverse=True)
                map_consonant_to_latin = self.telugu_to_latin_consonant_map.get
                map_vowel_to_latin = self.telugu_to_latin_vowel_map.get
            elif input_script == 'malayalam':
                sorted_consonant_keys = sorted(self.malayalam_to_latin_consonant_map.keys(), key=len, reverse=True)
                sorted_vowel_keys = sorted(self.malayalam_to_latin_vowel_map.keys(), key=len, reverse=True)
                map_consonant_to_latin = self.malayalam_to_latin_consonant_map.get
                map_vowel_to_latin = self.malayalam_to_latin_vowel_map.get
            else:
                break


            matched_consonant_char = None
            consonant_len = 0
            for key in sorted_consonant_keys:
                if word_to_process[i:].startswith(key):
                    matched_consonant_char = key
                    consonant_len = len(key)
                    break

            if matched_consonant_char:
                latin_equivalent_cons = map_consonant_to_latin(matched_consonant_char)
                numerical_value_cons = self.consonant_values.get(latin_equivalent_cons, 0) if latin_equivalent_cons else 0

                current_consonant_sum = numerical_value_cons

                processed_letters_data.append({
                    "type": "consonant",
                    "char": matched_consonant_char,
                    "latin_equivalent": latin_equivalent_cons,
                    "value": numerical_value_cons
                })
                i += consonant_len

                # Handle halant clusters and consecutive consonants
                while i < len(word_to_process):
                    next_char = word_to_process[i]

                    is_explicit_halant = (
                        (input_script == 'devanagari' and next_char == '्') or
                        (input_script == 'kannada' and next_char == '್') or
                        (input_script == 'telugu' and next_char == '్') or
                        (input_script == 'malayalam' and next_char == '്') or
                        (input_script == 'latin' and next_char == '-')  # Latin explicit halant
                    )

                    # For Latin script, also check for implicit halant (consecutive consonants)
                    is_implicit_halant_latin = False
                    if input_script == 'latin' and not is_explicit_halant:
                        # Check if current position starts with another consonant
                        for key in sorted_consonant_keys:
                            if word_to_process[i:].startswith(key):
                                is_implicit_halant_latin = True
                                break

                    if not is_explicit_halant and not is_implicit_halant_latin:
                        break

                    # Add explicit halant to processed data
                    if is_explicit_halant:

                        processed_letters_data.append({
                            "type": "modifier_halant",
                            "char": next_char,
                            "latin_equivalent": None,
                            "value": 0
                        })

                        i += 1
                    elif is_implicit_halant_latin:
                        # For Latin implicit halant, add a note but don't increment i

                        processed_letters_data.append({
                            "type": "modifier_halant",
                            "char": "- (implicit)",
                            "latin_equivalent": None,
                            "value": 0
                        })


                    # Look for the next consonant
                    next_consonant = None
                    for key in sorted_consonant_keys:
                        if word_to_process[i:].startswith(key):
                            next_consonant = key
                            latin_equiv = map_consonant_to_latin(next_consonant)
                            next_value = self.consonant_values.get(latin_equiv, 0)
                            current_consonant_sum += next_value
                            processed_letters_data.append({
                                "type": "consonant",
                                "char": next_consonant,
                                "latin_equivalent": latin_equiv,
                                "value": next_value
                            })
                            i += len(key)
                            break
                    if not next_consonant:
                        break

                # Check for vowel after consonant/cluster
                found_vowel = False
                if i < len(word_to_process):
                    for key in sorted_vowel_keys:
                        if word_to_process[i:].startswith(key):
                            found_vowel = True
                            matched_vowel = key
                            latin_vowel = map_vowel_to_latin(matched_vowel)
                            vowel_multiplier = self.vowel_multipliers.get(latin_vowel, 0)
                            term_value = current_consonant_sum * vowel_multiplier
                            current_word_aryabhatta_value += term_value
                            processed_letters_data.append({
                                "type": "vowel_for_consonant",
                                "char": matched_vowel,
                                "latin_equivalent": latin_vowel,
                                "value": vowel_multiplier,
                                "term_value": term_value,
                                "consonant_sum_at_vowel": current_consonant_sum
                            })
                            i += len(key)
                            current_consonant_sum = 0
                            break

                if not found_vowel and current_consonant_sum > 0:

                    implicit_a_multiplier = self.vowel_multipliers.get('a', 1)
                    term_value = current_consonant_sum * implicit_a_multiplier
                    current_word_aryabhatta_value += term_value
                    processed_letters_data.append({
                        "type": "implicit_vowel",
                        "char": "अ (implicit)" if input_script == 'devanagari' else (
                            "ಅ (implicit)" if input_script == 'kannada' else (
                            "అ (implicit)" if input_script == 'telugu' else "a (implicit)")
                        ),
                        "latin_equivalent": "a",
                        "value": implicit_a_multiplier,
                        "term_value": term_value,
                        "consonant_sum_at_vowel": current_consonant_sum
                    })
                    current_consonant_sum = 0


                char_processed_in_this_iteration = True
                continue  # Consonant processed


            # --- Block B: Standalone Vowel ---
            matched_vowel_char = None
            for key in sorted_vowel_keys:
                if word_to_process[i:].startswith(key):
                    matched_vowel_char = key
                    vowel_len = len(key)
                    break

            if matched_vowel_char:
                latin_equivalent_vowel = map_vowel_to_latin(matched_vowel_char)
                term_value = 0
                breakdown_type = "standalone_vowel"

                processed_letters_data.append({
                    "type": breakdown_type,
                    "char": matched_vowel_char,
                    "latin_equivalent": latin_equivalent_vowel,
                    "value": self.vowel_multipliers.get(latin_equivalent_vowel, 0),
                    "term_value": term_value,
                    "consonant_sum_at_vowel": None
                })
                current_consonant_sum = 0
                i += vowel_len
                char_processed_in_this_iteration = True


                continue

            # --- Block C: Modifiers ---
            modifiers_map = None
            if input_script == 'devanagari':
                modifiers_map = self.DEVANAGARI_MODIFIERS_TO_LATIN
            elif input_script == 'kannada':
                modifiers_map = self.kannada_MODIFIERS_TO_LATIN
            elif input_script == 'tamil':
                modifiers_map = self.tamil_MODIFIERS_TO_LATIN
            elif input_script == 'telugu':
                modifiers_map = self.telugu_MODIFIERS_TO_LATIN

            if modifiers_map and word_to_process[i] in modifiers_map:
                matched_modifier_char = word_to_process[i]
                mod_latin_equiv = modifiers_map[matched_modifier_char]
                mod_type = "modifier_other"
                if matched_modifier_char in ['ं','ಂ','ம்','ం']: mod_type = "modifier_anusvara"
                elif matched_modifier_char in ['ः','ಃ']: mod_type = "modifier_visarga"
                elif matched_modifier_char in ['्','್','்','్']: mod_type = "modifier_halant"
                processed_letters_data.append({
                    "type": mod_type,
                    "char": matched_modifier_char,
                    "latin_equivalent": mod_latin_equiv,
                    "value": 0
                })
                i += 1
                char_processed_in_this_iteration = True
                continue

            # --- Block D: Unknown Character ---
            if not char_processed_in_this_iteration:
                processed_letters_data.append({
                    "type": "unknown",
                    "char": word_to_process[i],
                    "latin_equivalent": None,
                    "value": 0,
                    "term_value": 0
                })
                i += 1

        # --- Final check for lingering consonant sum ---
        if current_consonant_sum > 0:
            implicit_a_multiplier = self.vowel_multipliers.get('a', 1)
            term_value = current_consonant_sum * implicit_a_multiplier
            current_word_aryabhatta_value += term_value
            processed_letters_data.append({
                "type": "implicit_vowel",
                "char": "अ (implicit)" if input_script == 'devanagari' else ("ಅ (implicit)" if input_script == 'kannada' else "a (implicit)"),
                "latin_equivalent": "a",
                "value": implicit_a_multiplier,
                "term_value": term_value,
                "consonant_sum_at_vowel": current_consonant_sum
            })
            current_consonant_sum = 0



        tokens.append({
            word_to_process: {
                "length": len(processed_letters_data),
                "letters_breakdown": processed_letters_data,
                "value": current_word_aryabhatta_value,
            }
        })
        all_numbers_in_word.append(current_word_aryabhatta_value)

        return tokens, all_numbers_in_word

    def get_mappings(self, db=None):
        """Return all mappings in a structured format."""

        # --- Consonants ---
        consonants_data = []
        for latin_char, number in sorted(self.consonant_values.items(), key=lambda x: x[1]):
            devanagari_char = self.consonant_devanagari.get(latin_char, "")
            kannada_char = self.latin_to_kannada_consonant.get(latin_char, "")
            telugu_char = self.latin_to_telugu_consonant.get(latin_char, "")
            malayalam_char = self.latin_to_malayalam_consonant.get(latin_char, "")
            consonants_data.append({
                "latinChar": latin_char,
                "number": number,
                "devanagariChar": devanagari_char,
                "kannadaChar": kannada_char,
                "teluguChar": telugu_char,
                "malayalamChar": malayalam_char
            })

        # --- Vowels ---
        vowels_data = []
        for latin_char, number in sorted(self.vowel_multipliers.items(), key=lambda item: item[1]):
            vowels_data.append({
                "latinChar": latin_char,
                "number": number,
                "devanagariChar": self.vowel_devanagari.get(latin_char, ""),
                "kannadaChar": self.latin_to_kannada_vowel.get(latin_char, ""),
                "teluguChar": self.latin_to_telugu_vowel.get(latin_char, ""),
                "malayalamChar": self.latin_to_malayalam_vowel.get(latin_char, "")
            })

        # --- Devanagari Matras & Modifiers ---
        matras_data = []
        for dev_matra, latin_equiv in self.DEVANAGARI_MATRA_TO_LATIN_VOWEL.items():
            matras_data.append({
                "devanagariChar": dev_matra,
                "latinEquivalent": latin_equiv,
                "kannadaChar": self.devanagari_to_kannada_matra.get(dev_matra, ""),
                "teluguChar": self.devanagari_to_telugu_matra.get(dev_matra, ""),
                "malayalamChar": self.devanagari_to_malayalam_matra.get(dev_matra, "")
            })

        modifiers_data = []
        for dev_mod, latin_equiv in self.DEVANAGARI_MODIFIERS_TO_LATIN.items():
            modifiers_data.append({
                "devanagariChar": dev_mod,
                "latinEquivalent": latin_equiv,
                "kannadaChar": self.devanagari_to_kannada_modifier.get(dev_mod, ""),
                "teluguChar": self.devanagari_to_telugu_modifier.get(dev_mod, ""),
                "malayalamChar": self.devanagari_to_malayalam_modifier.get(dev_mod, "")
            })

        # --- Kannada Matras & Modifiers ---
        kannada_matras_data = [
            {"kannadaChar": k, "latinEquivalent": v}
            for k, v in self.kannada_MATRA_TO_LATIN_VOWEL.items()
        ]

        kannada_modifiers_data = [
            {"kannadaChar": k, "latinEquivalent": v}
            for k, v in self.kannada_MODIFIERS_TO_LATIN.items()
        ]

        # --- Telugu Matras & Modifiers ---
        telugu_matras_data = [
            {"teluguChar": k, "latinEquivalent": v}
            for k, v in self.telugu_MATRA_TO_LATIN_VOWEL.items()
        ]

        telugu_modifiers_data = [
            {"teluguChar": k, "latinEquivalent": v}
            for k, v in self.telugu_MODIFIERS_TO_LATIN.items()
        ]

        # --- Malayalam Matras & Modifiers ---
        malayalam_matras_data = [
            {"malayalamChar": k, "latinEquivalent": v}
            for k, v in self.malayalam_MATRA_TO_LATIN_VOWEL.items()
        ]

        malayalam_modifiers_data = [
            {"malayalamChar": k, "latinEquivalent": v}
            for k, v in self.malayalam_MODIFIERS_TO_LATIN.items()
        ]

        return {
            "consonants": consonants_data,
            "vowels": vowels_data,
            "devanagari_matras_map": matras_data,
            "devanagari_modifiers_map": modifiers_data,
            "kannada_matras_map": kannada_matras_data,
            "kannada_modifiers_map": kannada_modifiers_data,
            "telugu_matras_map": telugu_matras_data,
            "telugu_modifiers_map": telugu_modifiers_data,
            "malayalam_matras_map": malayalam_matras_data,
            "malayalam_modifiers_map": malayalam_modifiers_data
        }

    def calculate_logic(self, tokens: list, operation: str):

        """
        Apply the selected digit-wise operation to a list of tokens (numbers).
        """
        results = []

        for token in tokens:
            number = int(token)  # ensure it's an int

            if operation in ["sum", "addition"]:
                results.append(self.calculate_digit_sum(number))
            elif operation in ["product", "multiplication"]:
                results.append(self.calculate_digit_product(number))
            elif operation in ["subtract_fd", "subtraction_fd"]:
                results.append(self.calculate_digit_difference_fd(number))
            elif operation in ["subtract_bd", "subtraction_bd"]:
                results.append(self.calculate_digit_difference_bd(number))
            elif operation in ["divide_fd", "division_fd"]:
                results.append(self.calculate_digit_quotient_fd(number))
            elif operation in ["divide_bd", "division_bd"]:
                results.append(self.calculate_digit_quotient_bd(number))
            else:
                raise ValueError(f"Unsupported operation: {operation}")


        return results



    def add_mapping(self, db, latin_char, insert_at, mapping_type, devanagari_char="", kannada_char="", telugu_char="", malayalam_char="", color_hex=""):

        if mapping_type == "consonant":
            # Check if exists in consonants_latin
            existing = db.execute(
                text("SELECT latin_character FROM consonants_latin WHERE latin_character = :latinChar"),
                {"latinChar": latin_char}
            ).fetchone()
            if existing:
                raise ValueError(f"Consonant Latin character '{latin_char}' already exists.")

            # Insert into consonants_latin
            db.execute(
                text("INSERT INTO consonants_latin (latin_character, char_id, devanagari_character) VALUES (:latin, :id, :dev)"),
                {"latin": latin_char, "id": insert_at, "dev": devanagari_char}
            )

            # If Kannada char provided → check duplicate and insert
            if kannada_char and devanagari_char:
                existing_kan = db.execute(
                    text("SELECT kannada_character FROM consonants_kannada WHERE kannada_character = :kan"),
                    {"kan": kannada_char}
                ).fetchone()
                if not existing_kan:
                    db.execute(
                        text("INSERT INTO consonants_kannada (char_id, kannada_character, devanagari_character) VALUES (:id, :kan, :dev)"),
                        {"id": insert_at, "kan": kannada_char, "dev": devanagari_char}
                    )

            # If Telugu char provided → check duplicate and insert
            if telugu_char and devanagari_char:
                existing_tel = db.execute(
                    text("SELECT telugu_character FROM consonants_telugu WHERE telugu_character = :tel"),
                    {"tel": telugu_char}
                ).fetchone()
                if not existing_tel:
                    db.execute(
                        text("INSERT INTO consonants_telugu (char_id, telugu_character, devanagari_character) VALUES (:id, :tel, :dev)"),
                        {"id": insert_at, "tel": telugu_char, "dev": devanagari_char}
                    )

            # If Malayalam char provided → check duplicate and insert
            if malayalam_char and devanagari_char:
                existing_mal = db.execute(
                    text("SELECT malayalam_character FROM consonants_malayalam WHERE malayalam_character = :mal"),
                    {"mal": malayalam_char}
                ).fetchone()
                if not existing_mal:
                    db.execute(
                        text("INSERT INTO consonants_malayalam (char_id, malayalam_character, devanagari_character) VALUES (:id, :mal, :dev)"),
                        {"id": insert_at, "mal": malayalam_char, "dev": devanagari_char}
                    )

            # Insert into colour_mapping if color provided
            if color_hex and devanagari_char:
                existing_color = db.execute(
                    text("SELECT id FROM colour_mapping WHERE devanagari_char = :dev"),
                    {"dev": devanagari_char}
                ).fetchone()
                if not existing_color:
                    db.execute(
                        text("""INSERT INTO colour_mapping (devanagari_char, latin_char, kannada_char, telugu_char, malayalam_char, color_hex) 
                                VALUES (:dev, :lat, :kan, :tel, :mal, :color)"""),
                        {"dev": devanagari_char, "lat": latin_char, "kan": kannada_char, 
                         "tel": telugu_char, "mal": malayalam_char, "color": color_hex}
                    )

            # Update memory
            self.consonant_values[latin_char] = insert_at
            self.consonant_devanagari[latin_char] = devanagari_char
            if devanagari_char:
                self.devanagari_to_latin_consonant_map[devanagari_char] = latin_char
            if kannada_char:
                self.latin_to_kannada_consonant[latin_char] = kannada_char
                self.kannada_to_latin_consonant_map[kannada_char] = latin_char
            if telugu_char:
                self.latin_to_telugu_consonant[latin_char] = telugu_char
                self.telugu_to_latin_consonant_map[telugu_char] = latin_char
            if malayalam_char:
                self.latin_to_malayalam_consonant[latin_char] = malayalam_char
                self.malayalam_to_latin_consonant_map[malayalam_char] = latin_char
            # Update color map if provided
            if color_hex:
                if devanagari_char:
                    self.character_colors_map[devanagari_char] = color_hex
                if latin_char:
                    self.character_colors_map[latin_char] = color_hex
                if kannada_char:
                    self.character_colors_map[kannada_char] = color_hex
                if telugu_char:
                    self.character_colors_map[telugu_char] = color_hex
                if malayalam_char:
                    self.character_colors_map[malayalam_char] = color_hex

        elif mapping_type == "vowel":
            # Check if exists in vowels_latin
            existing = db.execute(
                text("SELECT latin_character FROM vowels_latin WHERE latin_character = :char"),
                {"char": latin_char}
            ).fetchone()
            if existing:
                raise ValueError(f"Vowel Latin character '{latin_char}' already exists.")

            # Insert into vowels_latin
            db.execute(
                text("INSERT INTO vowels_latin (latin_character, char_id, devanagari_character) VALUES (:latin, :id, :dev)"),
                {"latin": latin_char, "id": insert_at, "dev": devanagari_char}
            )

            # If Kannada char provided → check duplicate and insert into vowels_kannada
            if kannada_char and devanagari_char:
                existing_kan = db.execute(
                    text("SELECT kannada_character FROM vowels_kannada WHERE kannada_character = :kan"),
                    {"kan": kannada_char}
                ).fetchone()
                if not existing_kan:
                    db.execute(
                        text("INSERT INTO vowels_kannada (char_id, kannada_character, devanagari_character) VALUES (:id, :kan, :dev)"),
                        {"id": insert_at, "kan": kannada_char, "dev": devanagari_char}
                    )

            # If Telugu char provided → check duplicate and insert into vowels_telugu
            if telugu_char and devanagari_char:
                existing_tel = db.execute(
                    text("SELECT telugu_character FROM vowels_telugu WHERE telugu_character = :tel"),
                    {"tel": telugu_char}
                ).fetchone()
                if not existing_tel:
                    db.execute(
                        text("INSERT INTO vowels_telugu (char_id, telugu_character, devanagari_character) VALUES (:id, :tel, :dev)"),
                        {"id": insert_at, "tel": telugu_char, "dev": devanagari_char}
                    )

            # If Malayalam char provided → check duplicate and insert into vowels_malayalam
            if malayalam_char and devanagari_char:
                existing_mal = db.execute(
                    text("SELECT malayalam_character FROM vowels_malayalam WHERE malayalam_character = :mal"),
                    {"mal": malayalam_char}
                ).fetchone()
                if not existing_mal:
                    db.execute(
                        text("INSERT INTO vowels_malayalam (char_id, malayalam_character, devanagari_character) VALUES (:id, :mal, :dev)"),
                        {"id": insert_at, "mal": malayalam_char, "dev": devanagari_char}
                    )

            # Insert into colour_mapping if color provided
            if color_hex and devanagari_char:
                existing_color = db.execute(
                    text("SELECT id FROM colour_mapping WHERE devanagari_char = :dev"),
                    {"dev": devanagari_char}
                ).fetchone()
                if not existing_color:
                    db.execute(
                        text("""INSERT INTO colour_mapping (devanagari_char, latin_char, kannada_char, telugu_char, malayalam_char, color_hex) 
                                VALUES (:dev, :lat, :kan, :tel, :mal, :color)"""),
                        {"dev": devanagari_char, "lat": latin_char, "kan": kannada_char, 
                         "tel": telugu_char, "mal": malayalam_char, "color": color_hex}
                    )

            # Update memory
            self.vowel_multipliers[latin_char] = insert_at
            self.vowel_devanagari[latin_char] = devanagari_char
            if devanagari_char:
                self.devanagari_to_latin_vowel_map[devanagari_char] = latin_char
            if kannada_char:
                self.latin_to_kannada_vowel[latin_char] = kannada_char
                self.kannada_to_latin_vowel_map[kannada_char] = latin_char
            if telugu_char:
                self.latin_to_telugu_vowel[latin_char] = telugu_char
                self.telugu_to_latin_vowel_map[telugu_char] = latin_char
            if malayalam_char:
                self.latin_to_malayalam_vowel[latin_char] = malayalam_char
                self.malayalam_to_latin_vowel_map[malayalam_char] = latin_char
            # Update color map if provided
            if color_hex:
                if devanagari_char:
                    self.character_colors_map[devanagari_char] = color_hex
                if latin_char:
                    self.character_colors_map[latin_char] = color_hex
                if kannada_char:
                    self.character_colors_map[kannada_char] = color_hex
                if telugu_char:
                    self.character_colors_map[telugu_char] = color_hex
                if malayalam_char:
                    self.character_colors_map[malayalam_char] = color_hex

        else:
            raise ValueError("Invalid mapping type")

        db.commit()
