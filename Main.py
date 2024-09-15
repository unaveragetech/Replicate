import asyncio
import tkinter as tk
from helper import Helper

class ControlApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Script Control Panel")
        self.log_text = tk.Text(master, height=20, width=60)
        self.log_text.pack()

        self.control_var = tk.IntVar(value=1)  # 1 for Full Control, 0 for Admin Approval

        self.full_control_radio = tk.Radiobutton(master, text="Full Control", variable=self.control_var, value=1)
        self.admin_mode_radio = tk.Radiobutton(master, text="Admin Approval Mode", variable=self.control_var, value=0)

        self.full_control_radio.pack()
        self.admin_mode_radio.pack()

        self.approve_button = tk.Button(master, text="Approve Change", command=self.approve_change, state=tk.DISABLED)
        self.approve_button.pack()

        self.helper = Helper("main.py", "test_script.py", self.log_text)
        self.approve_event = asyncio.Event()

    def approve_change(self):
        """Manually approve a change in admin mode."""
        self.log("Admin approval granted.")
        self.approve_event.set()

    def log(self, message):
        """Log messages in the UI."""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    async def main_loop(self):
        """Main loop for running and suggesting code."""
        while True:
            await self.helper.log_to_gui("Running code...")
            new_code = self.helper.suggest_new_code()
            
            await self.helper.inject_code_async(new_code)

            # If in admin mode, wait for approval
            if self.control_var.get() == 0:  # Admin mode
                self.approve_button.config(state=tk.NORMAL)
                await self.helper.log_to_gui("Waiting for admin approval...")
                await self.approve_event.wait()  # Wait until user approves
                self.approve_event.clear()
                self.approve_button.config(state=tk.DISABLED)

            await asyncio.sleep(5)  # Simulate waiting period between cycles


def run_gui():
    root = tk.Tk()
    app = ControlApp(root)
    asyncio.run(app.main_loop())
    root.mainloop()


if __name__ == "__main__":
    run_gui()
