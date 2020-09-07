import rumps
from datetime import datetime
import sys

class PomodoroApp(object):
    def __init__(self):
        self.config = {
            "app_name": "Pomodoro",
            "start": "Start Pomodoro",
            "pause": "Pause Timer",
            "continue": "Continue Timer",
            "stop": "Stop Timer",
            "break_message": "Time is up! Take a break :)",
            'buttons': {"ok": 1, "cancel": 2}
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = 1500
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=self.stop_timer)        
        self.app.menu = [self.start_pause_button, self.stop_button]
        self.set_up_menu()
        self.user_goals = ''

    def set_up_menu(self, show_end_message=False):
        self.timer.stop()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]
        self.timer.count = 0
        self.app.title = "🍅"
        if(show_end_message): 
            self.closing_statements()

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            self.set_up_menu(show_end_message=True)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

    def start_timer(self, sender):
        if sender.title.lower().startswith("start"): 
            window = rumps.Window(message='What would you like to accomplish in this session?', title='Set Your Goals')
            window.add_buttons('Cancel')
            response = window.run()
            if response.clicked == self.config['buttons']['cancel']:
                rumps.quit_application()
            self.user_goals = response.text
            window = rumps.Window(message='How many minutes would you like to focus?', title='Set Your Timer', dimensions=(60, 25))
            window.add_buttons('Cancel')
            response = window.run()
            if response.clicked == self.config['buttons']['cancel']:
                rumps.quit_application()
            self.interval = int(response.text)*60
            start_timer = rumps.alert(title="Get Ready!", message='Awesome! Don\'t forget to put your distractions away and let\'s get started.', ok="Start Timer", cancel=True)
            if(not start_timer): 
                rumps.quit_application()
        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    def stop_timer(self, sender):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]

    def closing_statements(self): 
        window = rumps.Window(message='Congratulations! What did you accomplish in this session? We filled out your goals below to remind you of what you set out to focus on.', 
            title='Reflect On Your Goals', 
            default_text="Accomplished: \nOriginal goals: " + self.user_goals)
        response = window.run()
        self.user_reflection = response.text
        try: 
            with open("pomodoro_logs.txt", 'a') as file: 
                file.write(str(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")) + ": \n")
                lines_in_reflection = self.user_reflection.split("\n")
                file.write("\t" + "\n\t".join(lines_in_reflection) + "\n")
                file.write("\n")
        except: 
            print("Unexpected error:", sys.exc_info()[0])
            print("Oops, couldn't find logs! Oh well!")   
            

    def run(self):
        self.app.run()
        
        
        # window.run()

        

if __name__ == '__main__':
    app = PomodoroApp()
    app.run()