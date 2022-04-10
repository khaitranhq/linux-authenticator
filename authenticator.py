#!/usr/bin/python3

import gi
import datetime
import time

from src.authenticator import AuthenticatorDomain

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

global application


class AccountBox:
    def __init__(self, name_label: Gtk.Label, code_label: Gtk.Label):
        self.name_label = name_label
        self.code_label = code_label


class Application(Gtk.Window):
    def __init__(self):
        super().__init__(title="Authenticator")

        self.authenticator = AuthenticatorDomain()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        root_box.set_margin_start(20)
        root_box.set_margin_end(20)
        root_box.set_margin_top(20)
        root_box.set_margin_bottom(20)

        self.account_boxes = []
        for account in self.authenticator.accounts:
            code_box = Gtk.Box()
            account_name = account["name"]
            if not isinstance(account_name, str):
                continue

            labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            account_name_arr = account_name.split(":")
            name_text = f"{account_name_arr[0]} ({account_name_arr[1]})"

            if len(name_text) > 42:
                name_text = name_text[:40] + "..."

            name_label = Gtk.Label(label=name_text)
            name_label.set_name(account_name)
            name_label.set_xalign(0)

            code_label = Gtk.Label(label=self.authenticator.get_code(account["name"]))
            code_label.set_xalign(0)
            code_label.set_margin_start(0)
            labels_box.set_size_request(300, -1)
            labels_box.pack_start(name_label, True, True, 0)
            labels_box.pack_start(code_label, True, True, 0)

            button_box = Gtk.Box()
            copy_button = Gtk.Button(label="Copy")
            copy_button.set_property("width-request", 20)
            copy_button.connect("clicked", self.copy_text, account_name)
            button_box.set_size_request(50, -1)
            button_box.add(copy_button)

            code_box.pack_start(labels_box, True, True, 0)
            code_box.pack_start(button_box, True, True, 0)
            root_box.add(code_box)
            self.account_boxes.append(AccountBox(name_label, code_label))

        form_box = Gtk.Box()

        entry_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.site_input = Gtk.Entry()
        self.site_input.set_placeholder_text("Website")
        self.account_input = Gtk.Entry()
        self.account_input.set_placeholder_text("Account")
        self.code_input = Gtk.Entry()
        self.code_input.set_placeholder_text("Secret key")
        entry_box.pack_start(self.site_input, True, True, 0)
        entry_box.pack_start(self.account_input, True, True, 0)
        entry_box.pack_start(self.code_input, True, True, 0)

        form_box.pack_start(entry_box, True, True, 0)

        button_box = Gtk.Box()
        self.button = Gtk.Button(label="Add")
        self.button.connect("clicked", self.on_click_button)
        button_box.pack_start(self.button, True, True, 0)
        button_box.set_margin_start(20)
        button_box.set_size_request(90, 20)

        form_box.pack_start(button_box, False, True, 0)

        root_box.add(form_box)
        self.add(root_box)

    def copy_text(self, button, name):
        for account in self.account_boxes:
            if account.name_label.get_text() == name:
                print(account.code_label.get_text())
                self.clipboard.set_text(account.code_label.get_text(), -1)

    def on_click_button(self, button):
        account = self.account_input.get_text()
        website = self.site_input.get_text()
        secret_code = self.code_input.get_text()
        self.authenticator.save_secret(website + ":" + account, secret_code)
        self.queue_draw()

    def update_code(self):
        #  print("executed")
        for i in range(len(self.account_boxes)):
            account_name = self.account_boxes[i].name_label.get_name()
            code = self.authenticator.get_code(account_name)
            self.account_boxes[i].code_label.set_text(code)


global cnt
cnt = 0


def run_schedule(cnt, application, timeout_id):
    application.update_code()

    if cnt == 0:
        cnt = 1
        print("update")
        GLib.source_remove(timeout_id)
        GLib.timeout_add(30 * 1000, lambda: run_schedule(1, application, timeout_id))
    return True


def main():
    application = Application()
    application.connect("destroy", Gtk.main_quit)
    application.show_all()

    timeout_id = 0
    current_second = datetime.datetime.now().second
    timeout_interval = (
        30 - current_second if current_second <= 30 else 60 - current_second
    )
    #      print(current_second)
    #  print(timeout_interval)

    timeout_id = GLib.timeout_add(
        timeout_interval * 1000, lambda: run_schedule(cnt, application, timeout_id)
    )

    Gtk.main()


if __name__ == "__main__":
    main()
