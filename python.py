import tweepy
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

# Helper function to create hoverable tooltips for the credential fields
def create_tooltip(widget, text):
    # Create a tooltip window and hide it initially
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()  # Hide by default
    tooltip.overrideredirect(True)  # Remove window borders
    tooltip_label = tk.Label(tooltip, text=text, background="lightyellow", wraplength=200)
    tooltip_label.pack()

    # Show the tooltip near the mouse pointer when hovered over the widget
    def show_tooltip(event):
        tooltip.deiconify()  # Make tooltip visible
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")  # Position tooltip

    # Hide the tooltip when the mouse leaves the widget
    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)  # Bind hover event to show the tooltip
    widget.bind("<Leave>", hide_tooltip)  # Bind leave event to hide the tooltip

# Function to authenticate with Twitter API and fetch user info
def authenticate_and_fetch():
    # Grab API credentials entered by the user
    consumer_key = consumer_key_entry.get()
    consumer_secret = consumer_secret_entry.get()
    access_token = access_token_entry.get()
    access_token_secret = access_token_secret_entry.get()

    # Simple check to ensure all fields are filled before proceeding
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        messagebox.showwarning("Missing Information", "Please fill in all API credentials.")
        return

    # Try to authenticate using the provided credentials
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Verify if the credentials are valid
        user = api.verify_credentials()

        if user:
            # Construct a detailed message showing key information about the authenticated user
            user_info = (
                f"Authenticated as: {user.screen_name}\n"
                f"Name: {user.name}\n"
                f"Location: {user.location}\n"
                f"Followers: {user.followers_count}\n"
                f"Friends: {user.friends_count}\n"
                f"Statuses Count: {user.statuses_count}\n"
                f"Favorites Count: {user.favourites_count}\n"
                f"Account Creation Date: {user.created_at}\n"
                f"Verified: {'Yes' if user.verified else 'No'}"
            )

            # Display the user info in a new window with a scrollable text box
            info_window = tk.Toplevel(root)
            info_window.title("User Information")

            text_area = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, width=50, height=15)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, user_info)
            text_area.configure(state='disabled')  # Make the text box read-only
        else:
            messagebox.showwarning("Authentication Failed", "Failed to authenticate. Please check your credentials.")
    
    # Handle any errors that may occur during the authentication process
    except tweepy.TweepError as e:
        messagebox.showerror("Error", f"Failed to authenticate: {e}")

# Create the main application window for user interaction
root = tk.Tk()
root.title("Twitter API Credentials")

# Create labels and input fields for each Twitter API credential
tk.Label(root, text="Twitter Consumer Key").grid(row=0, column=0, padx=10, pady=5)
consumer_key_entry = tk.Entry(root, width=50)
consumer_key_entry.grid(row=0, column=1, padx=10, pady=5)

# Add help tooltip for Consumer Key
consumer_key_help = tk.Label(root, text="?", fg="blue", cursor="hand2")
consumer_key_help.grid(row=0, column=2)
create_tooltip(consumer_key_help, "You can find your Consumer Key in the 'Keys and Tokens' section of your Twitter Developer dashboard.")

tk.Label(root, text="Twitter Consumer Secret").grid(row=1, column=0, padx=10, pady=5)
consumer_secret_entry = tk.Entry(root, width=50)
consumer_secret_entry.grid(row=1, column=1, padx=10, pady=5)

# Add help tooltip for Consumer Secret
consumer_secret_help = tk.Label(root, text="?", fg="blue", cursor="hand2")
consumer_secret_help.grid(row=1, column=2)
create_tooltip(consumer_secret_help, "You can find your Consumer Secret in the 'Keys and Tokens' section of your Twitter Developer dashboard.")

tk.Label(root, text="Access Token").grid(row=2, column=0, padx=10, pady=5)
access_token_entry = tk.Entry(root, width=50)
access_token_entry.grid(row=2, column=1, padx=10, pady=5)

# Add help tooltip for Access Token
access_token_help = tk.Label(root, text="?", fg="blue", cursor="hand2")
access_token_help.grid(row=2, column=2)
create_tooltip(access_token_help, "You can generate your Access Token in the 'Keys and Tokens' section of your Twitter Developer dashboard.")

tk.Label(root, text="Access Token Secret").grid(row=3, column=0, padx=10, pady=5)
access_token_secret_entry = tk.Entry(root, width=50)
access_token_secret_entry.grid(row=3, column=1, padx=10, pady=5)

# Add help tooltip for Access Token Secret
access_token_secret_help = tk.Label(root, text="?", fg="blue", cursor="hand2")
access_token_secret_help.grid(row=3, column=2)
create_tooltip(access_token_secret_help, "You can generate your Access Token Secret in the 'Keys and Tokens' section of your Twitter Developer dashboard.")

# Add the Authenticate button to trigger the authentication process
submit_button = tk.Button(root, text="Authenticate", command=authenticate_and_fetch)
submit_button.grid(row=4, column=1, pady=10)

# Start the Tkinter event loop to keep the window running
root.mainloop()
