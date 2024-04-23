from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase
import os

# Register the Greek font (ensure 'greek.ttf' is in your application directory)
LabelBase.register(name='Greek', fn_regular='greek.ttf')

class NewTestamentViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Dropdown for selecting the book
        self.book_spinner = Spinner(
            text='1John',
            values=('1Cor', '1John', '1Pet', '1Thess', '1Tim', '2Cor', '2John', '2Pet', '2Thess', '2Tim', '3John', 'Acts', 'Col', 'Eph', 'Gal', 'Heb', 'James', 'Jude', 'John', 'Luke', 'Mark', 'Matt', 'Phil', 'Phlm', 'Rev', 'Rom', 'Titus'),
            size_hint=(None, None),
            size=(220, 44),
            pos_hint={'center_x': 0.5}
        )

        # Input fields for chapter and verse
        self.chapter_input = TextInput(hint_text='Chapter', size_hint=(1, None), height=30)
        self.verse_input = TextInput(hint_text='Verse', size_hint=(1, None), height=30)

        # Button to load the Greek text
        self.load_button = Button(text='Load Greek Text', size_hint=(1, None), height=50)
        self.load_button.bind(on_press=self.load_greek_text)

        # Button to save the translation
        self.save_button = Button(text='Save Translation', size_hint=(1, None), height=50)
        self.save_button.bind(on_press=self.save_translation)

        # Greek text display
        self.greek_text_display = TextInput(
            readonly=True,
            size_hint_y=None,
            height=400,
            font_name='Greek'
        )

        # English translation input
        self.translation_input = TextInput(
            hint_text='Type your translation here',
            size_hint_y=None,
            height=120
        )

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
        except ValueError as e:
            self.greek_text_display.text = f"An error occurred with the verse range: {e}"
        except Exception as e:
            self.greek_text_display.text = f"An unexpected error occurred: {e}"

    def save_translation(self, instance):
        book = self.book_spinner.text
        chapter = self.chapter_input.text.strip()
        verse_range = self.verse_input.text.strip()
        translation_text = self.translation_input.text
        # Formatting the filename to include book, chapter, and verse range, followed by '.translated.txt'
        filename = f"{book}.{chapter}_{verse_range}.translated.txt"
        directory = 'translations'
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(directory, filename)
    
        # Writing the translation to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(translation_text)
        self.translation_input.text = ''  # Optionally clear the text input after saving
        print(f"Translation saved successfully to {file_path}")

if __name__ == '__main__':
    NewTestamentViewerApp().run()

