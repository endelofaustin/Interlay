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

Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_enable', 1)

# Register the Greek font
LabelBase.register(name='Greek', fn_regular='greek.ttf')

# Set the background color of the window
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

# Configure logging
downloads_folder = '/sdcard/Download'
log_file = os.path.join(downloads_folder, 'new_testament_viewer_log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewTestamentViewerApp(App):
    def build(self):
        # Log build start
        logger.debug("Building the app interface")

        # Set the app icon
        self.icon = 'greek_bible_icon.png'

        # Main layout
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scrollable content layout
        scroll_view = ScrollView(size_hint=(1, 1))
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Scrollable Greek text display
        greek_text_scroll = ScrollView(size_hint=(1, None), height=400)  # Increased height for better visibility
        self.greek_text_display = TextInput(
            readonly=True,  # Allow only copying
            font_name='Greek',
            font_size=36,  # Larger text
            background_color=(0.1, 0.1, 0.1, 1),  # Dark background
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=400,
            multiline=True  # Allow multiline text
        )
        self.greek_text_display.bind(minimum_height=self.greek_text_display.setter('height'))
        greek_text_scroll.add_widget(self.greek_text_display)

        # Spinner for selecting the book
        self.book_spinner = Spinner(
            text='1John',
            values=('1Cor', '1John', '1Pet', '1Thess', '1Tim', '2Cor', '2John', '2Pet', '2Thess', '2Tim', '3John', 'Acts', 'Col', 'Eph', 'Gal', 'Heb', 'James', 'Jude', 'John', 'Luke', 'Mark', 'Matt', 'Phil', 'Phlm', 'Rev', 'Rom', 'Titus'),
            size_hint=(1, None),
            height=44,
            background_color=(0.2, 0.6, 0.8, 1),  # Modern blue
            color=(1, 1, 1, 1)
        )

        # Input fields for chapter and verse
        self.chapter_input = TextInput(
            hint_text='Chapter',
            size_hint=(1, None),
            height=40,
            font_size=24,  # Larger text
            background_color=(0.2, 0.2, 0.2, 1),  # Dark input field
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1)
        )
        self.verse_input = TextInput(
            hint_text='Verse',
            size_hint=(1, None),
            height=40,
            font_size=24,  # Larger text
            background_color=(0.2, 0.2, 0.2, 1),  # Dark input field
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1)
        )

        # Button to load the Greek text
        self.load_button = Button(
            text='Load Greek Text',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),  # Modern blue
            color=(1, 1, 1, 1)
        )
        self.load_button.bind(on_press=self.load_greek_text)

        # Translated text display
        self.translated_text_display = TextInput(
            readonly=True,
            size_hint_y=None,
            height=200,
            font_size=24,  # Larger text
            background_color=(0.1, 0.1, 0.1, 1),  # Dark background
            foreground_color=(1, 1, 1, 1)
        )

        # Translation input
        self.translation_input = TextInput(
            hint_text='Type your translation here',
            size_hint_y=None,
            height=100,
            font_size=24,  # Larger text
            background_color=(0.2, 0.2, 0.2, 1),  # Dark input field
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1)
        )

        # Button to save the translation
        self.save_button = Button(
            text='Save Translation',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),  # Modern blue
            color=(1, 1, 1, 1)
        )
        self.save_button.bind(on_press=self.save_translation)

        # Button to translate the Greek text
        self.translate_button = Button(
            text='Translate It',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),  # Modern blue
            color=(1, 1, 1, 1)
        )
        self.translate_button.bind(on_press=self.translate_text)

        # Button to email the translation
        self.email_button = Button(
            text='Email Translation',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),
            # Modern blue
            color=(1, 1, 1, 1)
        )
        
        self.email_button.bind(on_press=self.email_translation)

        # Label to display the Greek word definition
        self.definition_label = Label(
            text='',
            size_hint=(1, None),
            height=50,
            font_size=24,
            color=(1, 1, 1, 1),
            text_size=(Window.width, None)
        )

        # Assemble the content layout
        content_layout.add_widget(greek_text_scroll)
        content_layout.add_widget(self.book_spinner)
        content_layout.add_widget(self.chapter_input)
        content_layout.add_widget(self.verse_input)
        content_layout.add_widget(self.load_button)
        content_layout.add_widget(self.translated_text_display)
        content_layout.add_widget(self.translation_input)
        content_layout.add_widget(self.save_button)
        content_layout.add_widget(self.translate_button)
        content_layout.add_widget(self.email_button)
        content_layout.add_widget(self.definition_label)

        # Add content layout to the scroll view
        scroll_view.add_widget(content_layout)

        # Add scroll view to the root layout
        root_layout.add_widget(scroll_view)

        logger.debug("App interface built successfully")
        return root_layout

    def load_greek_text(self, instance):
        book = self.book_spinner.text
        chapter = self.chapter_input.text.strip()
        verse_range = self.verse_input.text.strip()
        file_path = f"SBLGNT/data/sblgnt/text/{book}.txt"
        scripture_text = ""
        logger.info(f"Loading Greek text for {book} {chapter}:{verse_range}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            if '-' in verse_range:
                start_verse, end_verse = map(int, map(str.strip, verse_range.split('-')))
                verses_to_load = range(start_verse, end_verse + 1)
            else:
                verses_to_load = [int(verse_range.strip())]

            for line in lines:
                line_parts = line.strip().split('\t')
                if len(line_parts) < 2:
                    continue
                ref, verse_text = line_parts[0], line_parts[1]
                ref_parts = ref.split()
                ref_book, ref_chapter_verse = ref_parts[0], ref_parts[1]
                ref_chapter, ref_verse = ref_chapter_verse.split(':')
                if ref_book == book and ref_chapter == chapter and int(ref_verse.strip()) in verses_to_load:
                    scripture_text += verse_text + '\n'

            self.greek_text_display.text = scripture_text.rstrip('\n')
            logger.info("Greek text loaded successfully")

        except FileNotFoundError:
            self.greek_text_display.text = "The specified text file does not exist."
            logger.error(f"FileNotFoundError: {file_path} not found")
        except ValueError as ve:
            self.greek_text_display.text = f"An error occurred with the verse range: {ve}"
            logger.error(f"ValueError: Invalid verse range - {ve}")
        except Exception as e:
            self.greek_text_display.text = f"An unexpected error occurred: {e}"
            logger.error(f"Exception: {e}")

    def save_translation(self, instance):
        book = self.book_spinner.text.replace(" ", "")
        chapter = self.chapter_input.text.strip()
        verse = self.verse_input.text.strip()
        translation = self.translation_input.text
        filename = f"translations/{book}.{chapter}_{verse}.translated.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        logger.info(f"Saving translation to {filename}")

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(translation)
            logger.info("Translation saved successfully")
            self.show_popup("Success", "Translation saved successfully.")
        except Exception as e:
            logger.error(f"Error saving translation: {e}")
            self.show_popup("Error", f"Error saving translation: {e}")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, size_hint_y=None, height=40, color=(1, 1, 1, 1))
        close_button = Button(text='Close', size_hint_y=None, height=40, background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        close_button.bind(on_press=lambda *args: popup.dismiss())

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.75, 0.5))
        popup.open()
        logger.info(f"Popup shown: {title} - {message}")

    def translate_text(self, instance):
        greek_text = self.greek_text_display.text
        if not greek_text:
            self.show_popup("Error", "Please load Greek text first.")
            logger.error("Translate error: Greek text not loaded")
            return

        # DeepL API URL and headers
        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": "DeepL-Auth-Key 60e6e163-10eb-4b49-bf99-8bda5bfe29c4:fx"
        }

        # Payload for DeepL API
        payload = {
            "text": greek_text,
            "target_lang": "EN"
        }

        logger.info("Translating Greek text using DeepL API")

        try:
            # Make the API request
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the translated text from the response
            translated_text = response.json()["translations"][0]["text"]

            # Set the translated text in the translated text display field
            self.translated_text_display.text = translated_text
            logger.info("Translation successful")

        except requests.exceptions.RequestException as e:
            logger.error(f"Translation error: {e}")
            self.show_popup("Error", f"An error occurred: {e}")

    def email_translation(self, instance):
        book = self.book_spinner.text.replace(" ", "")
        chapter = self.chapter_input.text.strip()
        verse = self.verse_input.text.strip()
        translation = self.translation_input.text

        if not translation:
            self.show_popup("Error", "No translation to email.")
            logger.error("Email error: No translation available")
            return

        subject = f"Translation of {book} {chapter}:{verse}"
        body = f"Here is the translation:\n\n{translation}"

        logger.info(f"Emailing translation: {subject}")

        try:
            email.send(recipient="endelofaustin@gmail.com", subject=subject, text=body)
            self.show_popup("Success", "Email sent successfully.")
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Email error: {e}")
            self.show_popup("Error", f"An error occurred: {e}")

if __name__ == '__main__':
    NewTestamentViewerApp().run()

