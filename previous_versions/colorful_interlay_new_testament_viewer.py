from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.core.window import Window
import os

# Register the Greek font (ensure 'greek.ttf' is in your application directory)
LabelBase.register(name='Greek', fn_regular='greek.ttf')

# Set the background color of the window
Window.clearcolor = (0.95, 0.95, 1, 1)  # Soft light blue background

class NewTestamentViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Spinner for selecting the book
        self.book_spinner = Spinner(
            text='1John',
            values=('1Cor', '1John', '1Pet', '1Thess', '1Tim', '2Cor', '2John', '2Pet', '2Thess', '2Tim', '3John', 'Acts', 'Col', 'Eph', 'Gal', 'Heb', 'James', 'Jude', 'John', 'Luke', 'Mark', 'Matt', 'Phil', 'Phlm', 'Rev', 'Rom', 'Titus'),
            size_hint=(None, None),
            size=(220, 44),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.1, 0.1, 1),
            color=(1, 1, 1, 1)
        )

        # Input fields for chapter and verse
        self.chapter_input = TextInput(hint_text='Chapter', size_hint=(1, None), height=40, background_color=(0.8, 0.8, 0.8, 1))
        self.verse_input = TextInput(hint_text='Verse', size_hint=(1, None), height=40, background_color=(0.8, 0.8, 0.8, 1))

        # Button to load the Greek text
        self.load_button = Button(text='Load Greek Text', size_hint=(1, None), height=50, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        self.load_button.bind(on_press=self.load_greek_text)

        # Greek text display
        self.greek_text_display = TextInput(
            readonly=True,
            size_hint_y=None,
            height=500,
            font_name='Greek',
            font_size=32,
            background_color=(0.9, 0.9, 0.9, 1)
        )

        # Translation input
        self.translation_input = TextInput(
            hint_text='Type your translation here',
            size_hint_y=None,
            height=150,
            background_color=(1, 1, 1, 1)
        )

        # Button to save the translation
        self.save_button = Button(text='Save Translation', size_hint=(1, None), height=50, background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        self.save_button.bind(on_press=self.save_translation)

        # Assemble the main layout
        self.layout.add_widget(self.book_spinner)
        self.layout.add_widget(self.chapter_input)
        self.layout.add_widget(self.verse_input)
        self.layout.add_widget(self.load_button)
        self.layout.add_widget(self.greek_text_display)
        self.layout.add_widget(self.translation_input)
        self.layout.add_widget(self.save_button)

        return self.layout

    def load_greek_text(self, instance):
        book = self.book_spinner.text
        chapter = self.chapter_input.text.strip()
        verse_range = self.verse_input.text.strip()
        file_path = f"SBLGNT/data/sblgnt/text/{book}.txt"
        scripture_text = ""

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            if '-' in verse_range:
                start_verse, end_verse = map(int, verse_range.split('-'))
                verses_to_load = range(start_verse, end_verse + 1)
            else:
                verses_to_load = [int(verse_range)]

            for line in lines:
                line_parts = line.strip().split('\t')
                if len(line_parts) < 2:
                    continue
                ref, verse_text = line_parts[0], line_parts[1]
                ref_parts = ref.split()
                ref_book, ref_chapter_verse = ref_parts[0], ref_parts[1]
                ref_chapter, ref_verse = ref_chapter_verse.split(':')
                if ref_book == book and ref_chapter == chapter and int(ref_verse) in verses_to_load:
                    scripture_text += verse_text + '\n'

            self.greek_text_display.text = scripture_text.rstrip('\n')

        except FileNotFoundError:
            self.greek_text_display.text = "The specified text file does not exist."
        except Exception as e:
            self.greek_text_display.text = f"An unexpected error occurred: {e}"

    def save_translation(self, instance):
        book = self.book_spinner.text.replace(" ", "")
        chapter = self.chapter_input.text.strip()
        verse = self.verse_input.text.strip()
        translation = self.translation_input.text
        filename = f"translations/{book}.{chapter}_{verse}.translated.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(translation)

if __name__ == '__main__':
    NewTestamentViewerApp().run()

