import os
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.popup import Popup
import logging

Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_enable', 1)

# Register the Greek font
LabelBase.register(name='Greek', fn_regular='greek.ttf')

# Set the background color of the window
Window.clearcolor = (1.0, 0.97, 0.88, 1)  # Light cream background

# Configure logging
downloads_folder = '/sdcard/Download'
log_file = os.path.join(downloads_folder, 'new_testament_viewer_log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def build_layout(app_instance):
    # Main layout
    root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    # Greek text display
    app_instance.greek_text_display = TextInput(
        readonly=True,  # Allow only copying
        font_name='Greek',
        font_size=36,  # Larger text
        background_color=(1.0, 0.97, 0.88, 1),  # Light cream background
        foreground_color=(0.26, 0.26, 0.26, 1),  # Dark gray text
        size_hint=(1, 0.4),  # Use 40% of the available height
        multiline=True  # Allow multiline text
    )

    # Spinner for selecting the book
    app_instance.book_spinner = Spinner(
        text='1John',
        values=('1Cor', '1John', '1Pet', '1Thess', '1Tim', '2Cor', '2John', '2Pet', '2Thess', '2Tim', '3John', 'Acts', 'Col', 'Eph', 'Gal', 'Heb', 'James', 'Jude', 'John', 'Luke', 'Mark', 'Matt', 'Phil', 'Phlm', 'Rev', 'Rom', 'Titus'),
        size_hint=(1, 0.1),
        background_color=(0.15, 0.65, 0.60, 1),  # Soft teal
        color=(1, 1, 1, 1)  # White text
    )

    # ScrollView for input fields and translation
    input_scrollview = ScrollView(size_hint=(1, 0.5))

    # Vertical layout inside the ScrollView
    input_layout = BoxLayout(orientation='vertical', size_hint_y=None)
    input_layout.bind(minimum_height=input_layout.setter('height'))

    # Input fields for chapter and verse
    app_instance.chapter_input = TextInput(
        hint_text='Chapter',
        size_hint=(1, None),
        height=50,
        font_size=24,  # Larger text
        background_color=(0.95, 0.95, 0.95, 1),  # Light gray input field
        foreground_color=(0.26, 0.26, 0.26, 1),  # Dark gray text
        hint_text_color=(0.6, 0.6, 0.6, 1)  # Gray hint text
    )
    app_instance.verse_input = TextInput(
        hint_text='Verse',
        size_hint=(1, None),
        height=50,
        font_size=24,  # Larger text
        background_color=(0.95, 0.95, 0.95, 1),  # Light gray input field
        foreground_color=(0.26, 0.26, 0.26, 1),  # Dark gray text
        hint_text_color=(0.6, 0.6, 0.6, 1)  # Gray hint text
    )

    # Button to load the Greek text
    app_instance.load_button = Button(
        text='Load Greek Text',
        size_hint=(1, None),
        height=50,
        background_color=(0.15, 0.65, 0.60, 1),  # Soft teal
        color=(1, 1, 1, 1),  # White text
        background_normal='',
        background_down='',
        border=(20, 20, 20, 20)
    )
    app_instance.load_button.bind(on_press=app_instance.load_greek_text)

    # Translated text display
    app_instance.translated_text_display = TextInput(
        readonly=True,
        size_hint=(1, None),
        height=100,
        font_size=24,  # Larger text
        background_color=(1.0, 0.97, 0.88, 1),  # Light cream background
        foreground_color=(0.26, 0.26, 0.26, 1)  # Dark gray text
    )

    # Translation input
    app_instance.translation_input = TextInput(
        hint_text='Type your translation here',
        size_hint=(1, None),
        height=100,
        font_size=24,  # Larger text
        background_color=(0.95, 0.95, 0.95, 1),  # Light gray input field
        foreground_color=(0.26, 0.26, 0.26, 1),  # Dark gray text
        hint_text_color=(0.6, 0.6, 0.6, 1)  # Gray hint text
    )

    # Add inputs and translation fields to the input layout
    input_layout.add_widget(app_instance.chapter_input)
    input_layout.add_widget(app_instance.verse_input)
    input_layout.add_widget(app_instance.load_button)
    input_layout.add_widget(app_instance.translated_text_display)
    input_layout.add_widget(app_instance.translation_input)

    # Add input layout to the ScrollView
    input_scrollview.add_widget(input_layout)

    # Horizontal layout for the bottom buttons
    bottom_buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

    # Button to save the translation
    app_instance.save_button = Button(
        text='Save Translation',
        size_hint=(1, 1),  # Use all available space
        background_color=(0.15, 0.65, 0.60, 1),  # Soft teal
        color=(1, 1, 1, 1),  # White text
        background_normal='',
        background_down='',
        border=(20, 20, 20, 20)
    )
    app_instance.save_button.bind(on_press=app_instance.save_translation)

    # Button to translate the Greek text
    app_instance.translate_button = Button(
        text='Translate It',
        size_hint=(1, 1),  # Use all available space
        background_color=(0.15, 0.65, 0.60, 1),  # Soft teal
        color=(1, 1, 1, 1),  # White text
        background_normal='',
        background_down='',
        border=(20, 20, 20, 20)
    )
    app_instance.translate_button.bind(on_press=app_instance.translate_text)

    # Button to email the translation
    app_instance.email_button = Button(
        text='Email Translation',
        size_hint=(1, 1),  # Use all available space
        background_color=(0.15, 0.65, 0.60, 1),  # Soft teal
        color=(1, 1, 1, 1),  # White text
        background_normal='',
        background_down='',
        border=(20, 20, 20, 20)
    )
    app_instance.email_button.bind(on_press=app_instance.email_translation)

    # Add buttons to the horizontal layout
    bottom_buttons_layout.add_widget(app_instance.save_button)
    bottom_buttons_layout.add_widget(app_instance.translate_button)
    bottom_buttons_layout.add_widget(app_instance.email_button)

    # Label to display the Greek word definition
    app_instance.definition_label = Label(
        text='',
        size_hint=(1, 0.05),
        font_size=24,
        color=(0.26, 0.26, 0.26, 1),  # Dark gray text
        text_size=(Window.width, None)
    )

    # Assemble the content layout
    content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    content_layout.add_widget(app_instance.greek_text_display)
    content_layout.add_widget(app_instance.book_spinner)
    content_layout.add_widget(input_scrollview)
    content_layout.add_widget(bottom_buttons_layout)  # Add the horizontal button layout
    content_layout.add_widget(app_instance.definition_label)

    # Add content layout to the root layout
    root_layout.add_widget(content_layout)

    # Bind keyboard visibility changes to a function
    Window.bind(on_keyboard_height=app_instance.on_keyboard_height)

    logger.debug("App interface built successfully")
    return root_layout

