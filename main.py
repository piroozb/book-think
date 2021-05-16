from typing import Optional, List
from classes import Publication, Book, Comment
import os

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
import bcrypt
import json
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv

# Constant to define demo mode or non-demo mode
DEMO = True

load_dotenv('.env')
cluster = MongoClient(os.getenv('VAL'))
db = cluster["BookData"]
collection = db["books"]
ERROR = ["Registry failed: passwords doesn't match!",
         'Registry failed: invalid password!',
         'Registry failed: username already taken!',
         'Registry failed: username invalid!',
         'Login failed: invalid username or password.']


# helper function
def fail_popup(retype: bool) -> None:
    show = Pop2() if retype else Pop()

    popup_win = Popup(title='Error', content=show, size_hint=(None, None),
                      size=(350, 100))
    popup_win.open()


class Pop(FloatLayout):
    pass


class Pop2(FloatLayout):
    pass


class LoginPage(Screen):
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)

    def btn_login(self) -> bool:
        user = self.user.text
        password = self.pass1.text.encode()
        data_user = collection.find_one({"_id": user})
        # gets the information from the database.

        # if os.path.getsize('user.json') > 0:
        #     file = open('user.json')
        #     user_dict = json.load(file)
        # else:
        #     fail_popup(False)
        #     return False
        # if user not in user_dict:
        #     fail_popup(False)
        #     return False

        if data_user is None:
            fail_popup(False)
            return False
        else:
            # hashed = user_dict[user][0]
            # currently hashed is a str of the hashed password
            hashed = data_user["password"]
        # clears textbox
        self.pass1.text = self.user.text = ''
        # used to check if hash corresponds with password
        if bcrypt.checkpw(password, hashed.encode()):
            return True
        else:
            fail_popup(True)
            return False


class RegisterPage(Screen):
    # saves the username and password inputted from the .kv file
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def btn_register(self) -> bool:
        if self.pass1.text != self.pass2.text or 40 < len(self.user.text) or\
                len(self.user.text) < 8 or ' ' in self.pass1.text:
            fail_popup(True)
            self.pass1.text = self.user.text = self.pass2.text = ''
            return False
        # converts password to bytes then encrypts it.
        user = self.user.text
        password = self.pass1.text.encode()
        # TODO: maybe add more rounds to make the password take longer to
        #  hash (for more security).
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
        data_user = collection.find_one({"_id": user})

        # if os.path.getsize('user.json') > 0:
        #     file = open('user.json', 'r')
        #     user_dict = json.load(file)
        # else:
        #     user_dict = {}

        self.pass1.text = self.user.text = self.pass2.text = ''
        if data_user is not None or 32 < len(user) or \
                len(user) < 6 or ' ' in user:
            fail_popup(False)
            return False
        else:
            collection.insert_one({"_id": user, "password": hashed.decode(),
                                   "date": str(date.today())})
            return True
        # if user in user_dict.keys() or 6 > len(user) > 32:
        #     fail_popup(False)
        #     return False
        # else:
        #     user_dict[user] = [str(hashed), str(date.today()), '0']
        #     with open('user.json', 'w') as f:
        #         json.dump(user_dict, f)
        #     return True


class UserPage(Screen):
    pass


class HomePage(Screen):
    pass


# class FeedPage(Screen):
#     pass
#
#
# class BookPage(Screen):
#     pass


class WindowManager(ScreenManager):
    pass


class BookApp(MDApp):
    """Class that builds and runs the app"""

    def build(self):
        return Builder.load_file('ui.kv')

    def update_publication_grid(self, search_keywords: Optional[str] = None) -> None:
        buttons = self.get_publication_buttons(search_keywords)
        self.root.screens[3].ids.book_grid.clear_widgets()
        for button in buttons:
            self.root.screens[3].ids.book_grid.add_widget(button)

    def get_publication_buttons(self, search_keywords: Optional[str] = None
                                ) -> List[TwoLineAvatarListItem]:
        buttons = []
        if DEMO:
            img_paths = ['images/Demo/Books/1984.png',
                         'images/Demo/Books/IHaveTheRightToDestroyMyself.png',
                         'images/Demo/Books/NoPlaceLikeHere.png',
                         'images/Demo/Books/OneFlewOverTheCuckoosNest.png',
                         'images/Demo/Books/TheGirlWithTheDragonTattoo.png',
                         'images/Demo/Books/TheHobbit.png',
                         'images/Demo/Books/TheNarrowRoadToTheDeepNorth.png',
                         'images/Demo/Books/ThreeDayRoad.png',
                         'images/Demo/Books/WhyWeSleep.png']
            books = [Book('1984', 'George Orwell', 'Dystopian Fiction', 328,
                          23),
                     Book('I Have The Right To Destroy Myself', 'Young-Ha Kim',
                          'Fiction', 131),
                     Book('No Place Like Here', 'Christina June', 'Fiction', 32,
                          231),
                     Book('One Flew Over The Cuckoos Nest', 'Ken Kesey',
                          'Fiction', 500, 12),
                     Book('The Girl With The Dragon Tattoo', 'Stieg Larsson',
                          'Fiction', 34),
                     Book('The Hobbit', 'J. R. R. Tolkien', 'Fantasy', 300),
                     Book('The Narrow Road To The Deep North',
                          'Richard Flanagan', 'Fantasy', 430),
                     Book('Three Day Road', 'Joseph Boyden', 'Fiction', 223),
                     Book('Why We Sleep', 'Matthew Walker', 'Fiction', 190)
                     ]
            for i in range(9):
                buttons.append(
                    self.build_publication_button(img_paths[i], books[i]), )
            return buttons
        else:
            # access database and based on search, add books from there
            pass

    def build_publication_button(self, img_path: str, publication: Publication
                                 ) -> TwoLineAvatarListItem:
        # box layout
        # layout = BoxLayout(orientation='vertical')
        # # iconbutton at the top (icon will be the book cover)
        # button = MDIconButton(icon=img_path)
        # # underneath it put title and author
        # layout.add_widget(button)
        # title = MDLabel(text=publication.title, font_style='H6')
        # layout.add_widget(title)
        # author = MDLabel(text=f'by {publication.author}', font_style='Caption')
        # layout.add_widget(author)
        button = TwoLineAvatarListItem(text=publication.title,
                                       secondary_text=publication.author,
                                       on_release=self.change_screens)
        button.add_widget(ImageLeftWidget(source=img_path))
        return button

    def change_screens(self, *args) -> None:
        # placeholder for now
        self.root.current = 'login'
        # self.root.current = 'book_info'

    def update_recent_posts(self) -> None:
        pass

    def format_comment_preview(self, img_path: str, publication: Publication,
                               comment: Comment) -> BoxLayout:
        """
        set up a comment for preview (for profile page)
        """
        # container = self.root.screens[3].ids.recent_post1
        # thingies = [self.root.screens[3].ids.recent_post1,
        container = BoxLayout(orientation='vertical')
        container.add_widget(Label(text=publication.title))
        container.add_widget(Label(text=publication.author))
        container.add_widget(Label(text=comment.content))
        container.add_widget(ImageLeftWidget(source=img_path))
        container.add_widget(Button(text='read more'))
        return container


# class PreviousMDIcons(Screen):
#
#     def set_list_md_icons(self, text="", search=False):
#         '''Builds a list of icons for the screen MDIcons.'''
#
#         def add_icon_item(name_icon):
#             self.ids.rv.data.append(
#                 {
#                     "viewclass": "CustomOneLineIconListItem",
#                     "icon": name_icon,
#                     "text": name_icon,
#                     "callback": lambda x: x,
#                 }
#             )
#
#         self.ids.rv.data = []
#         for name_icon in md_icons.keys():
#             if search:
#                 if text in name_icon:
#                     add_icon_item(name_icon)
#             else:
#                 add_icon_item(name_icon)


# class MainApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = PreviousMDIcons()
#
#     def build(self):
#         return self.screen
#
#     def on_start(self):
#         self.screen.set_list_md_icons()


if __name__ == "__main__":
    BookApp().run()