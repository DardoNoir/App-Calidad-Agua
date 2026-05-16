from src.ui.windows import App


def bootstarp():
    print("Conectando a Supabase...")
    app = App()
    app.mainloop()

if __name__ == "__main__":    
    bootstarp()