import curses
import sqlite3
import csv


class termCRM:

  def __init__(self):
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    self.stdscr.keypad(True)
    self.stdscr.clear()

    self.contacts_db = sqlite3.connect('contacts.db')
    self.contacts_db.execute('''CREATE TABLE IF NOT EXISTS contacts
                             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                             NAME TEXT NOT NULL,
                             PHONE INT NOT NULL,
                             EMAIL CHAR(50),
                             NOTE TEXT NOT NULL);''')

  def print_menu(self, selected_idx):
    self.stdscr.clear()
    self.stdscr.addstr(0, 2, "TermBase CRM")
    menu_items = [
      'View Contacts', 'Add Contact', 'Delete Contact', 'Search Contacts',
      'Export Contacts', 'Exit'
    ]
    for i, item in enumerate(menu_items):
      if i == selected_idx:
        mode = curses.A_REVERSE
      else:
        mode = curses.A_NORMAL

      self.stdscr.addstr(2 + i, 2, item, mode)

    self.stdscr.refresh()

  def view_contacts(self):
    self.stdscr.clear()
    contacts = self.contacts_db.execute("SELECT * FROM contacts")
    for i, contact in enumerate(contacts):
      contact_str = f"{contact[0]}. {contact[1]} ({contact[2]}, {contact[3]}) Notes: {contact[4]}"
      self.stdscr.addstr(2 + i, 2, contact_str)

    self.stdscr.addstr(2 + i + 1, 2, "Press any key to continue...")
    self.stdscr.refresh()
    self.stdscr.getch()

  def add_contact(self):
    self.stdscr.clear()
    curses.echo()
    self.stdscr.addstr(2, 2, "Enter contact name:")
    name = self.stdscr.getstr(3, 2).decode('utf-8')
    self.stdscr.addstr(4, 2, "Enter contact phone number:")
    phone = int(self.stdscr.getstr(5, 2).decode('utf-8'))
    self.stdscr.addstr(6, 2, "Enter contact email:")
    email = self.stdscr.getstr(7, 2).decode('utf-8')
    self.stdscr.addstr(8, 2, "Enter client notes:")
    note = self.stdscr.getstr(9, 2).decode('utf-8')

    self.contacts_db.execute(
      "INSERT INTO contacts (NAME, PHONE, NOTE, EMAIL) VALUES (?, ?, ?, ?)",
      (name, phone, note, email))
    self.contacts_db.commit()

    self.stdscr.addstr(11, 2, "Contact added successfully.")
    self.stdscr.addstr(12, 2, "Press any key to continue...")
    self.stdscr.refresh()
    self.stdscr.getch()

  def delete_contact(self):
    self.stdscr.clear()
    curses.echo()
    self.stdscr.addstr(2, 2, "Enter ID of the contact to delete:")
    contact_id = int(self.stdscr.getstr(3, 2).decode('utf-8'))
    self.contacts_db.execute(f"DELETE FROM contacts WHERE ID={contact_id}")
    self.contacts_db.commit()

    self.stdscr.addstr(5, 2, "Contact deleted successfully.")
    self.stdscr.addstr(6, 2, "Press any key to continue...")
    self.stdscr.refresh()
    self.stdscr.getch()

  def search_contacts(self):
    self.stdscr.clear()
    curses.echo()
    self.stdscr.addstr(2, 2, "Enter search query:")
    query = self.stdscr.getstr(3, 2).decode('utf-8')

    contacts = self.contacts_db.execute(
      f"SELECT * FROM contacts WHERE NAME LIKE '%{query}%' OR NOTE LIKE '%{query}%' OR EMAIL LIKE '%{query}%'"
    )
    for i, contact in enumerate(contacts):
      contact_str = f"{contact[0]}. {contact[1]} ({contact[2]}, {contact[4]}) Notes: {contact[3]}"
      self.stdscr.addstr(5 + i, 2, contact_str)

    self.stdscr.addstr(5 + i + 1, 2, "Press any key to continue...")
    self.stdscr.refresh()
    self.stdscr.getch()

  def export_contacts_csv(self):
    filename = 'contacts.csv'
    with open(filename, mode='w', newline='') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(['ID', 'Name', 'Phone', 'Note', 'Email'])
      contacts = self.contacts_db.execute("SELECT * FROM contacts")
      for contact in contacts:
        writer.writerow(contact)

    self.stdscr.clear()
    self.stdscr.addstr(2, 2, f"Contacts exported to {filename} successfully.")
    self.stdscr.addstr(3, 2, "Press any key to continue...")
    self.stdscr.refresh()
    self.stdscr.getch()

  def run(self):
    menu_items = [
      'View Contacts', 'Add Contact', 'Delete Contact', 'Search Contacts',
      'Export Contacts', 'Exit'
    ]
    current_idx = 0

    while True:
      self.print_menu(current_idx)

      key = self.stdscr.getch()
      if key == curses.KEY_UP:
        current_idx = (current_idx - 1) % len(menu_items)
      elif key == curses.KEY_DOWN:
        current_idx = (current_idx + 1) % len(menu_items)
      elif key == curses.KEY_ENTER or key in [10, 13]:
        if current_idx == len(menu_items) - 1:
          break
        elif current_idx == 0:
          self.view_contacts()
        elif current_idx == 1:
          self.add_contact()
        elif current_idx == 2:
          self.delete_contact()
        elif current_idx == 3:
          self.search_contacts()
        elif current_idx == 4:
          self.export_contacts_csv()
        elif current_idx == 5:
          break

    curses.endwin()

    self.stdscr.clear()
    self.stdscr.addstr(2, 2, "Goodbye!")
    self.stdscr.refresh()
    self.stdscr.getch()


if __name__ == '__main__':
  crm = termCRM()
  crm.run()
