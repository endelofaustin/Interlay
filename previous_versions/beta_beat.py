import os
import xml.etree.ElementTree as ET
import requests
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.popup import Popup
from plyer import email
import logging


class AppConfig:
    @staticmethod
    def setup():
        # Kivy configuration
        Config.set('kivy', 'log_level', 'debug')
        Config.set('kivy', 'log_enable', 1)

        # Register the Greek font
        LabelBase.register(name='Greek', fn_regular='greek.ttf')

        # Set the background color of the window
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

        # Configure logging to a common logging directory
        downloads_folder = '/sdcard/Download'
        log_file = os.path.join(downloads_folder, 'new_testament_viewer_log.txt')

        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        return logger


class NewTestamentViewerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = AppConfig.setup()

    def build(self):
        # Log build start
        self.logger.debug("Building the app interface")

        # Set the app icon
        self.icon = 'greek_bible_icon.png'

        # Main layout
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(content_layout)

        self.greek_text_display = self.create_text_input(font_name='Greek', font_size=36, height=400)
        self.translated_text_display = self.create_text_input(height=200)
        self.translation_input = self.create_text_input(hint_text='Type your translation here', height=100)

        self.book_spinner = self.create_spinner(
            text='1John',
            values=('1Cor', '1John', '1Pet', '1Thess', '1Tim', '2Cor', '2John', '2Pet', '2Thess', '2Tim', '3John', 
                    'Acts', 'Col', 'Eph', 'Gal', 'Heb', 'James', 'Jude', 'John', 'Luke', 'Mark', 'Matt', 'Phil', 
                    'Phlm', 'Rev', 'Rom', 'Titus'),
            height=44
        )

        self.chapter_input = self.create_text_input(hint_text='Chapter', height=40)
        self.verse_input = self.create_text_input(hint_text='Verse', height=40)

        self.load_button = self.create_button(text='Load Greek Text', on_press=self.load_greek_text)
        self.save_button = self.create_button(text='Save Translation', on_press=self.save_translation)
        self.translate_button = self.create_button(text='Translate It', on_press=self.translate_text)
        self.email_button = self.create_button(text='Email Translation', on_press=self.email_translation)

        self.definition_label = self.create_label()

        elements = [
            self.greek_text_display, self.book_spinner, self.chapter_input, self.verse_input, 
            self.load_button, self.translated_text_display, self.translation_input, 
            self.save_button, self.translate_button, self.email_button, self.definition_label
        ]

        for element in elements:
            content_layout.add_widget(element)

        root_layout.add_widget(scroll_view)
        self.logger.debug("App interface built successfully")
        return root_layout

    def create_text_input(self, hint_text='', font_name=None, font_size=24, height=40):
        return TextInput(
            hint_text=hint_text,
            size_hint_y=None,
            height=height,
            font_size=font_size,
            font_name=font_name,
            readonly=hint_text == '',  # Allow only copying if hint_text is empty
            background_color=(0.1, 0.1, 0.1, 1) if hint_text else (0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1) if hint_text else (1, 1, 1, 1),
            multiline=True
        )

    def create_button(self, text, on_press, height=50):
        button = Button(
            text=text,
            size_hint=(1, None),
            height=height,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        button.bind(on_press=on_press)
        return button

    def create_spinner(self, text, values, height=44):
        return Spinner(
            text=text,
            values=values,
            size_hint=(1, None),
            height=height,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )

    def create_label(self, text='', height=50):
        return Label(
            text=text,
            size_hint=(1, None),
            height=height,
            font_size=24,
            color=(1, 1, 1, 1),
            text_size=(Window.width, None)
        )

    def load_greek_text(self, instance):
        book, chapter, verse_range = self.book_spinner.text, self.chapter_input.text.strip(), self.verse_input.text.strip()
        file_path = f"SBLGNT/data/sblgnt/text/{book}.txt"
        scripture_text = ""
        self.logger.info(f"Loading Greek text for {book} {chapter}:{verse_range}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            verses_to_load = self.parse_verse_range(verse_range)
            scripture_text = self.extract_scripture_text(book, chapter, lines, verses_to_load)

            self.greek_text_display.text = scripture_text.rstrip('\n')
            self.logger.info("Greek text loaded successfully")

        except FileNotFoundError:
            self.handle_error("The specified text file does not exist.", f"FileNotFoundError: {file_path} not found")
        except ValueError as ve:
            self.handle_error(f"An error occurred with the verse range: {ve}", f"ValueError: Invalid verse range - {ve}")
        except Exception as e:
            self.handle_error(f"An unexpected error occurred: {e}", f"Exception: {e}")

    def parse_verse_range(self, verse_range):
        if '-' in verse_range:
            start_verse, end_verse = map(int, map(str.strip, verse_range.split('-')))
            return range(start_verse, end_verse + 1)
        return [int(verse_range.strip())]

    def extract_scripture_text(self, book, chapter, lines, verses_to_load):
        scripture_text = ""
        for line in lines:
            line_parts = line.strip().split('\t')
            if len(line_parts) < 2:
                continue
            ref, verse_text = line_parts[0], line_parts[1]
            ref_book, ref_chapter, ref_verse = self.parse_reference(ref)
            if ref_book == book and ref_chapter == chapter and int(ref_verse.strip()) in verses_to_load:
                scripture_text += verse_text + '\n'
        return scripture_text

    def parse_reference(self, ref):
        ref_parts = ref.split()
        ref_book, ref_chapter_verse = ref_parts[0], ref_parts[1]
        ref_chapter, ref_verse = ref_chapter_verse.split(':')
        return ref_book, ref_chapter, ref_verse

    def save_translation(self, instance):
        book, chapter, verse, translation = self.get_translation_details()
        filename = f"translations/{book}.{chapter}_{verse}.translated.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        self.logger.info(f"Saving translation to {filename}")

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(translation)
            self.logger.info("Translation saved successfully")
            self.show_popup("Success", "Translation saved successfully.")
        except Exception as e:
            self.handle_error(f"Error saving translation: {e}", f"Error saving translation: {e}")

    def translate_text(self, instance):
        greek_text = self.greek_text_display.text

        if not greek_text:
            self.handle_error("Please load Greek text first.", "Translate error: Greek text not loaded")
            return

        url = "https://api-free.deepl.com/v2/translate"
        headers = {"Authorization": "DeepL-Auth-Key 60e6e163-10eb-4b49-bf99-8bda5bfe29c4:fx"}
        payload = {"text": greek_text, "target_lang": "EN"}

        self.logger.info("Translating Greek text using DeepL API")

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            translated_text = response.json()["translations"][0]["text"]
            self.translated_text_display.text = translated_text
            self.logger.info("Translation successful")

        except requests.exceptions.RequestException as e:
            self.handle_error(f"Translation error: {e}", f"Translation error: {e}")

    def email_translation(self, instance):
        book, chapter, verse, translation = self.get_translation_details()

        if not translation:
            self.handle_error("No translation to email.", "Email error: No translation available")
            return

        subject = f"Translation of {book} {chapter}:{verse}"
        body = f"Here is the translation:\n\n{translation}"

        self.logger.info(f"Emailing translation: {subject}")

        try:
            email.send(recipient="endelofaustin@gmail.com", subject=subject, text=body)
            self.show_popup("Success", "Email sent successfully.")
            self.logger.info("Email sent successfully")
        except Exception as e:
            self.handle_error(f"Email error: {e}", f"Email error: {e}")

    def get_translation_details(self):
        book = self.book_spinner.text.replace(" ", "")
        chapter = self.chapter_input.text.strip()
        verse = self.verse_input.text.strip()
        translation = self.translation_input.text
        return book, chapter, verse, translation

    def handle_error(self, user_message, log_message):
        self.greek_text_display.text = user_message
        self.logger.error(log_message)
        self.show_popup("Error", user_message)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = self.create_label(text=message, height=40)
        close_button = self.create_button(text='Close', on_press=lambda *args: popup.dismiss(), height=40)
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.75, 0.5))
        popup.open()
        self.logger.info(f"Popup shown: {title} - {message}")

if __name__ == '__main__':
    NewTestamentViewerApp().run()   
