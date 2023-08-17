import os
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox
import nltk
import tokenize
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.probability import FreqDist
from nltk import pos_tag
import PyPDF2 
from termcolor import colored, cprint
from nltk.tag import tnt
from urdu_pos_tags import urdu_pos_tags

master = tk.Tk()
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
master.geometry('%dx%d+0+0' % (screen_width,screen_height))
master.configure(bg="#857E78")

class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        #self.func = Functionality.functionality()
        
        # Initialize the Urdu POS Tagger
        self.tagger = tnt.TnT()
          # Load the tagger model
    

    urdu_administration = [
                
                'batti gate',
                'Landa Bazar',
                'gurdwaras',
                'makan',
                'jhuggees',
                'haveli',
                'madrasa',
                'police-thana',
                'paisa',
                'General Sahib',
                'Zina',
                'Raj',
                'tongas',
                'rickshaws'
            ]

    urdu_socio_cultural = [

                'ghazal',
                'ghazals',
                'izzat',
                'khandan',
                'easop-gol',
                'atash',
                'feta',
                'lathi'
            ]

    urdu_Clothing = [

                'choli',
                'lungi',
                'kurta',
                'dhoti',
                'dhotis',
                'kurta',
                'kurtas',
                'sari',
                'saris',
                'sari-blouse',
                'sari-set',
                'palu',
                'shawl',
                'shawls',
                'shalwars',
                'shalwar-kamize',
                'dopattas',
                'Kamiz',
                'burqas',
                'Kapra',
                'doria',
                'thaan',
                'thaans',
                'cummerbund',
                'caftan',
            ]

    urdu_people_label = [

                'Bibi',
                'ayah',
                'kaki',
                'begum',
                'memsahib',
                'boochimai',
                'betiyan',
                'bai jee',
                'mai',
                'badmash',
                'guru',
                'lesson-walla',
                'Gin walla',
                'Jungle walla',
                'Mujahadeen',
                'baba',
                'kaka',
                'mullah',
                'mullahs',
                'maulvi',
                'sufi',
                'sher',
                'yaar',
                'Sala ',
                'heejras',
                'afeemi',
                'goonda',
                'goondas',
                'haramzada',
                'pathan',
                'paindoo',
                'Kalay Khan',
                'Lahori Parsees',
                'nawabs',
                'gujrati',
                'qawals',
                'Punjabi',
                'Data Sahib',
                'Pakis',
                'gora',
                'Kashmiri'
            ]

    urdu_food = [

                'pakoras',
                'Roti',
                'paans',
                'pora',
                'dal',
                'whiskypani',
                'chutney'
            ]

    urdu_gathering = [

                'gup-shup',
                'Anjuman', 
                'anjumans',
                'mushairas',
                'mehfil',
                'Tandarosti prayer',
                'khutba',
                'kusti',
                'panchayat',
                'quawali'
            ]

    verbs = [

                'khoos-poosing',
                'salaamed',
                'salaaming', 
                'salaam',
                'Choop kar',
                'bus kar',
                'ghoor ghoor ke',

            ]

    adjective = [

                'desi', 
                'desis',
                'khaki',
                'khush',
                'khandani',
                'Basmati',
                'fakir like',
                'caftaned',
                'mullahish',
                'Badshahi',
                'chitta',
                'gora',
                'gora chitta',
                'pajamaed',
                'tanchoi',
                'cashmere',
                'banarsi'
            ]
    
    def highlight_words(self):
            # Clear existing tags
            self.text_widget.tag_remove("highlight", "1.0", tk.END)
    
            # Get the text content from the Text widget
            content = self.text_widget.get("1.0", tk.END)

            word_lists = [self.urdu_administration, self.urdu_socio_cultural, self.urdu_Clothing, self.urdu_people_label, self.urdu_food, self.urdu_gathering, self.verbs, self.adjective]

            # Create a dictionary that maps each word to its category
            word_category = {}
            for category, words in zip(["urdu_administration", "urdu_socio_cultural", "urdu_Clothing", "urdu_people_label", "urdu_food", "urdu_gathering", "verbs", "adjective"], word_lists):
                for word in words:
                    word_category[word] = category

            # Create a tooltip function
            def show_tooltip(event):
                word = self.text_widget.get("current wordstart", "current wordend")
                category = word_category.get(word, "NAN")
                messagebox.showinfo("Tooltip", f"This is a {category} word: {word}")

            # Bind tooltip function to mouse hover event for highlighted words
            self.text_widget.tag_bind("highlight", "<Enter>", show_tooltip)


            # Iterate over each word list and highlight the words
            for word_list in word_lists:
                for word in word_list:
                    start = "1.0"
                    while True:
                        # Search for the word from the current position
                        index = self.text_widget.search(word, start, stopindex=tk.END)
                        if not index:
                            break
                        end = f"{index}+{len(word)}c"
                        self.text_widget.tag_add("highlight", index, end)
                        start = end

            # Configure the appearance of the "highlight" tag
            self.text_widget.tag_configure("highlight", foreground="red")
            
    def tag_paragraph_and_count(self, paragraph):
        words = word_tokenize(paragraph.lower())
        tagged_words = []
        tagged_word_count = 0

        for word in words:
            # Look for matches in the imported dictionary
            if word in urdu_pos_tags:
                tagged_words.append((word, urdu_pos_tags[word]))
                tagged_word_count += 1

        return tagged_words, tagged_word_count


    #UI components.....
    def createWidgets(self):
    
    #Menu Bar- File 
        self.menubar = Menu(master)
    #filemenu 
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Open File', command=self.load_files)
        self.filemenu.add_command(label='Open Corpus', command=self.load_corpus)
        self.filemenu.add_command(label='Exit', command=master.quit)
        self.menubar.add_cascade(label='File', menu = self.filemenu)
        
        # Edit Menu
        self.edit_menu = Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Add Urdu Words', command=self.open_add_urdu_words_form)
        self.edit_menu.add_command(label='Delete Urdu Words', command=self.load_corpus)
        self.edit_menu.add_command(label='Exit', command=master.quit)
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu)


        master.config(menu = self.menubar);
        
         # Main Frame
        self.main_frame = Frame(master, bg="#90ee91")  # Create the main_frame as a child of the master window
        self.main_frame.pack(side=RIGHT, anchor=NE, fill='both', padx=1, pady=1)

        #FRAME 1 
        self.frame_1 = Frame(master, bg="#90ee91")
        self.frame_1.pack(side= LEFT, anchor= NW,fill='y', padx=1, pady=1)

        self.target_corpus = Label(self.frame_1, text="Target Corpus", bg="#90ee91", fg="#000000", font=('Helvetica', 9, 'bold'))
        self.target_corpus.pack(anchor= NW)
        corpus_file = Label(self.frame_1, text="Files:", bg="#90ee91", fg="#000000")
        corpus_file.pack(anchor= NW)
        tokenss = Label(self.frame_1, text="Tokens:",bg="#90ee91", fg="#000000")
        tokenss.pack(anchor= NW)
        Wrd_frq = Label(self.frame_1, text="Word Freq:",bg="#90ee91", fg="#000000")
        Wrd_frq.pack(anchor= NW)
        
        #listbox
        self.Lbox = Listbox(self.frame_1, selectmode=MULTIPLE, bg="#e5f6df", width=30)
        self.Lbox.pack(anchor=NW, expand=True, fill='y')

        self.notebook_frame = Frame(master)
        self.notebook_frame.pack(anchor=N, expand=True, fill='both')
        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack( anchor=N, expand=True, fill='both')

        #TAB's FRAME
        self.KWIC_tab = Frame(self.notebook, bg="#90ee91")
        self.KWIC_tab.columnconfigure(0, weight=1)

        #TAB's FRAME
        self.roman_urdu_tab = Frame(self.notebook, bg="#90ee91")
        self.roman_urdu_tab.columnconfigure(0, weight=1)

        #TAB's FRAME
        self.pos_tag = Frame(self.notebook, bg="#90ee91")
        self.pos_tag.columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background="#90ee91")

        # Create a frame to hold the text widget and scrollbar
        self.frame_2 = ttk.Frame(self.KWIC_tab, style="My.TFrame", padding=2, height=30, width=145)
        self.frame_2.grid(row=0, column=0, sticky="nsew")

        # Create a text widget and add it to the frame
        self.text_widget = tk.Text(self.frame_2,bg="#e5f6df", wrap="word", height=20, width=147)
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the frame and link it to the text widget
        self.scrollbar = ttk.Scrollbar(self.frame_2, orient="vertical", command= self.text_widget.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        
    # Input Box
        self.input_box_label = Label(self.main_frame, text="Enter Your Text:", bg="#90ee91", fg="#000000",
                                     font=('Helvetica', 9, 'bold'))
        self.input_box_label.pack(anchor=NE)
        self.input_box = Entry(self.main_frame, width=30)
        self.input_box.pack(anchor=SW, fill='x')
        
          # Find Button
        self.find_button = Button(self.main_frame, text='Find', command=self.find_text, font=('Helvetica', 9))
        self.find_button.pack(anchor=NE, padx=5, pady=5)

        # Clear Button
        self.clear_button = Button(self.main_frame, text='Clear', command=self.clear_text, font=('Helvetica', 9))
        self.clear_button.pack(anchor=NE, padx=5, pady=5)

        # Delete Button
        self.delete_button = Button(self.main_frame, text='Delete', command=self.delete_text, font=('Helvetica', 9))
        self.delete_button.pack(anchor=NE, padx=5, pady=5)

        # ... Existing code ...

        # Make the frame resizable with the window
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        def open_file():
            file_contents = ''
            for i in self.Lbox.curselection():
                file_path = self.Lbox.get(i)
                self.file_name.config(text=f"{file_path}")
                with open(file_path, "rt", encoding="utf-8") as f:
                    if file_path.endswith(".txt"):
                        file_contents = f.read()
                    elif file_path.endswith(".pdf"):
                        with open(file_path, "rb") as pdf:
                            pdf_rdr = PyPDF2.PdfFileReader(pdf)
                            pdf_page_nums = len(pdf_rdr.pages)
                        for pag_nm in range(pdf_page_nums):
                            try:
                                pg = pdf_rdr.getPage(pag_nm)
                                pg_txt = pg.extractText()
                                pg_txt = pg_txt.replace('\n',' ')
                                file_contents += pg_txt
                            except KeyError:
                                print("Error: Page {} does not contain the '/Contents' key".format(pag_nm))
                            continue
                    else:
                        file_contents = f.read()

            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", file_contents)
            self.highlight_words()

            return file_contents
        
        ######################## corpus
        def read_selected_files():
        
            corpus = []
        
            selected_path = self.Lbox.curselection()
            #print("selected_path: ", selected_path)
            #self.file_name.config(text=f"{self.file}")
            for index in selected_path:
                #getting file path from listbox
                path = self.Lbox.get(index)
                #getting file extension
                file_extension = os.path.splitext(path)[1].lower()
            
                # Read file content based on the file extension
                if file_extension == ".txt":
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        content = content.replace("\n", "")  # Remove newline characters
                        corpus.append(content)
                    
                elif file_extension == ".pdf":
                    with open(path, "rb", encoding="utf-8") as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        content = ""
                        for page in pdf_reader.pages:
                            content += page.extract_text()
                            content = content.replace("\n", "")  # Remove newline characters
                        corpus.append(content)
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", corpus)
            self.highlight_words()
            
            return corpus
    

        
        def get_value():
            value = self.search_box.get().lower()
            frequency = {}
            file_contents = None

            if file_contents == open_file():
                file_contents = open_file()
            else:
                file_contents = read_selected_files()

            if isinstance(file_contents, str):
                file_contents = file_contents.lower()
            else:
                file_contents = " ".join(file_contents).lower()

            # Perform POS tagging
            tagged_words = pos_tag(file_contents.split())
            treee.delete(*treee.get_children())
            for word, pos in tagged_words:
                treee.insert("", tk.END, values=(pos, word))

            for word in file_contents.split(): #.lower() yahan tha split sy phely
                count = frequency.get(word, 0)
                frequency[word] = count + 1
    
            frequency_value = frequency.get(value, 0)
            self.word_occurence.config(text=f"{frequency_value}")
    
            words = nltk.word_tokenize(file_contents)
            fdist = FreqDist(words)
            tokens = len(words)
            self.token_count.config(text=f"{tokens}")

            texts = Text(words)
            concordance = texts.concordance_list(value, width=22)
            selected_number = int(self.selected_value.get())
            tree.delete(*tree.get_children())

            for line in concordance:
                left_context = ' '.join(line.left[:selected_number])
                right_context = ' '.join(line.right[:selected_number])
                concordance_value = value
                tree.insert("", tk.END, values=(left_context, concordance_value, right_context))
            
            self.text_widget.configure(state="normal")
            self.text_widget.delete("1.0", tk.END)
            self.highlight_words()

        urdised_word_tree = ttk.Treeview(self.roman_urdu_tab, columns=("urdu_administration",
                "urdu_socio_cultural",
                "urdu_Clothing",
                "urdu_people",
                "urdu_food",
                "urdu_gathering",
                "verbs",
                "adjective"), height= 25)
        urdised_word_tree.grid(row=0, column=0, columnspan=8)

        urdised_word_tree.column("#0",width=50, anchor=W, stretch=NO)
        urdised_word_tree.column("#1", anchor=W, stretch=NO)
        urdised_word_tree.column("#2", anchor=W, stretch=NO)
        urdised_word_tree.column("#3", anchor=W, stretch=NO)
        urdised_word_tree.column("#4", anchor=W, stretch=NO)
        urdised_word_tree.column("#5", anchor=W, stretch=NO)
        urdised_word_tree.column("#6", anchor=W, stretch=NO)
        urdised_word_tree.column("#7", anchor=W, stretch=NO)

        urdised_word_tree.heading("#0", text="urdu_administration")
        urdised_word_tree.heading("#1", text="urdu_socio_cultural")
        urdised_word_tree.heading("#2", text="urdu_Clothing")
        urdised_word_tree.heading("#3", text="urdu_people")
        urdised_word_tree.heading("#4", text="urdu_food")
        urdised_word_tree.heading("#5", text="urdu_gathering")
        urdised_word_tree.heading("#6", text="verbs")
        urdised_word_tree.heading("#7", text="adjective")

        urdu_administration = [
                
                'batti gate',
                'Landa Bazar',
                'gurdwaras',
                'makan',
                'jhuggees',
                'haveli',
                'madrasa',
                'police-thana',
                'paisa',
                'General Sahib',
                'Zina',
                'Raj',
                'tongas',
                'rickshaws'
            ]

        urdu_socio_cultural = [

                'ghazal',
                'ghazals',
                'izzat',
                'khandan',
                'easop-gol',
                'atash',
                'feta',
                'lathi'
            ]

        urdu_Clothing = [

                'choli',
                'lungi',
                'kurta',
                'dhoti',
                'dhotis',
                'kurta',
                'kurtas',
                'sari',
                'saris',
                'sari-blouse',
                'sari-set',
                'palu',
                'shawl',
                'shawls',
                'shalwars',
                'shalwar-kamize',
                'dopattas',
                'Kamiz',
                'burqas',
                'Kapra',
                'doria',
                'thaan',
                'thaans',
                'cummerbund',
                'caftan',
            ]

        urdu_people_label = [

                'Bibi',
                'ayah',
                'kaki',
                'begum',
                'memsahib',
                'boochimai',
                'betiyan',
                'bai jee',
                'mai',
                'badmash',
                'guru',
                'lesson-walla',
                'Gin walla',
                'Jungle walla',
                'Mujahadeen',
                'baba',
                'kaka',
                'mullah',
                'mullahs',
                'maulvi',
                'sufi',
                'sher',
                'yaar',
                'Sala ',
                'heejras',
                'afeemi',
                'goonda',
                'goondas',
                'haramzada',
                'pathan',
                'paindoo',
                'Kalay Khan',
                'Lahori Parsees',
                'nawabs',
                'gujrati',
                'qawals',
                'Punjabi',
                'Data Sahib',
                'Pakis',
                'gora',
                'Kashmiri'
            ]

        urdu_food = [

                'pakoras',
                'Roti',
                'paans',
                'pora',
                'dal',
                'whiskypani',
                'chutney'
            ]

        urdu_gathering = [

                'gup-shup',
                'Anjuman', 
                'anjumans',
                'mushairas',
                'mehfil',
                'Tandarosti prayer',
                'khutba',
                'kusti',
                'panchayat',
                'quawali'
            ]

        verbs = [

                'khoos-poosing',
                'salaamed',
                'salaaming', 
                'salaam',
                'Choop kar',
                'bus kar',
                'ghoor ghoor ke',

            ]

        adjective = [

                'desi', 
                'desis',
                'khaki',
                'khush',
                'khandani',
                'Basmati',
                'fakir like',
                'caftaned',
                'mullahish',
                'Badshahi',
                'chitta',
                'gora',
                'gora chitta',
                'pajamaed',
                'tanchoi',
                'cashmere',
                'banarsi'
            ]
        
    
            # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_admin in urdu_administration:
            urdised_word_tree.insert("", tk.END, values=(urdu_admin))
            
        # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_socio in urdu_socio_cultural:
            urdised_word_tree.insert("", tk.END, values=(urdu_socio))

        # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_clothing in urdu_Clothing:
            urdised_word_tree.insert("", tk.END, values=(urdu_clothing))
            
        # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_people in urdu_people_label:
            urdised_word_tree.insert("", tk.END, values=(urdu_people))
            
        # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_foods in urdu_food:
            urdised_word_tree.insert("", tk.END, values=(urdu_foods))

        # Clear any existing items in the listbox
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for urdu_gatherings in urdu_gathering:
            urdised_word_tree.insert("", tk.END, values=(urdu_gatherings))

            
        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for verb in verbs:
            urdised_word_tree.insert("", tk.END, values=(verb))

        urdised_word_tree.delete(*urdised_word_tree.get_children())

        for adj in adjective:
            urdised_word_tree.insert("", tk.END, values=(adj))

        # Define the available values for the dropdown menu
        self.dropdown_values = list(range(1, 12))
        # Create a Tkinter StringVar to store the selected dropdown value
        self.selected_value = tk.StringVar()
        self.selected_value.set(1)
        # Create the dropdown menu
        self.dropdown_menu = tk.OptionMenu(self.KWIC_tab, self.selected_value, *self.dropdown_values)
        self.dropdown_menu.grid(row=3, column=0, sticky=NW, padx=540, ipadx=5)

        # File Name
        self.file_name = Label(self.frame_1 , bg="#90ee91", text="" ,padx=10)
        self.file_name.place(x=28, y=20)
        # token_count
        self.token_count = Label(self.frame_1 , bg="#90ee91", text="" ,padx=10)
        self.token_count.place(x=50, y=43)
        #Word Occurence
        self.word_occurence = Label(self.frame_1 , bg="#90ee91", text="" ,padx=5)
        self.word_occurence.place(x=67, y=64)

        #search boxx
        self.search_box = tk.Entry(self.KWIC_tab, width=50)
        self.search_box.grid(row=3, column=0, sticky=NW, padx=4, pady=3)
        self.kwic_btn = Button(self.KWIC_tab, text='Start', relief=GROOVE, background="#2aed2d", command=get_value)
        self.kwic_btn.grid(row=3, column=0, sticky=NW, padx=320, ipadx=5)
        self.kwic_open_file_btn = Button(self.KWIC_tab, text='Open File', command=open_file, relief=GROOVE, background="#2aed2d")
        self.kwic_open_file_btn.grid(row=3, column=0, sticky=NW, padx=370, ipadx=5)
        self.kwic_open_corpus_btn = Button(self.KWIC_tab, text='Open Corpus', command=read_selected_files, relief=GROOVE, background="#2aed2d")
        self.kwic_open_corpus_btn.grid(row=3, column=0, sticky=NW, padx=445, ipadx=5)

        # Create a Treeview widget
        tree = ttk.Treeview(self.KWIC_tab ,columns=("left", "value", "right"), show="headings")

        # Define column headings
        tree.heading("left", text="Left Context")
        tree.heading("value", text="Concordance Value")
        tree.heading("right", text="Right Context")

        # Set column widths
        tree.column("left", width=300)
        tree.column("value", width=300)
        tree.column("right", width=300)

        # Position the Treeview widget
        tree.grid(pady=15)

        # Create a Treeview widget
        treee = ttk.Treeview(self.pos_tag ,columns=("pos-tag", "value"), show="headings")

        # Define column headings
        treee.heading("pos-tag", text="pos")
        treee.heading("value", text="word")

        # Set column widths
        treee.column("pos-tag", width=300)
        treee.column("value", width=300)

        # Position the Treeview widget
        treee.pack(fill=BOTH, expand = 1, padx=5, pady= 5)

        self.KWIC_tab.pack(fill="both", expand=True)

        #adding tab to tab controller
        self.notebook.add(self.KWIC_tab, text='KWIC')
        self.notebook.add(self.roman_urdu_tab, text='Urdu Word Categories')
        self.notebook.add(self.pos_tag, text='POS TAG')

    def load_files(self):
        load_one_file = fd.askopenfilename(initialdir="/",title="Select an File",filetypes=[("TXT","*.txt"),("PDF","*.pdf"),("ALL Files","*.*")])
        self.Lbox.insert(tk.END, os.path.join(load_one_file, load_one_file))

    def load_corpus(self):
        self.load_corpus_files = fd.askopenfiles(initialdir="/",title="Select Multiple Files", filetypes=[("TXT","*.txt"),("PDF","*.pdf"),("ALL Files","*.*")])
        for file in self.load_corpus_files:
            self.file = file.name
            self.Lbox.insert(END, self.file)
            
    
    def find_text(self):
        # Get the text from the input box
        text_to_display = self.input_box.get()

        # Clear any existing content in the text widget
        self.text_widget.delete("1.0", tk.END)

        # Insert the text from the input box into the text widget
        self.text_widget.insert("1.0", text_to_display)

        # Tag the paragraph and count tagged words
        tagged_words, tagged_word_count = self.tag_paragraph_and_count(text_to_display)

        # Display the tagged words in the text widget
        for word, tag in tagged_words:
            self.text_widget.insert(tk.END, f"\n{word}: {tag}")

        # Display the total number of tagged words
        self.text_widget.insert(tk.END, f"\n\nTotal Tagged Words: {tagged_word_count}")

        # Highlight Roman Urduized or Urdu words
        self.highlight_words()
        
    def open_add_urdu_words_form(self):
        # Create a new form window
        add_word_form = tk.Toplevel(self.master)
        add_word_form.title("Add Urdu Word")
        
        # Set the size and position of the form
        form_width = 400
        form_height = 200
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - form_width) // 2
        y = (screen_height - form_height) // 2
        add_word_form.geometry(f"{form_width}x{form_height}+{x}+{y}")

        # Create labels, entry fields, and buttons for the form
        self.word_label = tk.Label(add_word_form, text="Urdu Word:", font=('Helvetica', 12))
        self.word_label.pack(pady=10)
        self.word_entry = tk.Entry(add_word_form, font=('Helvetica', 12))
        self.word_entry.pack()

        self.pos_label = tk.Label(add_word_form, text="Part of Speech:", font=('Helvetica', 12))
        self.pos_label.pack(pady=10)
        self.pos_entry = tk.Entry(add_word_form, font=('Helvetica', 12))
        self.pos_entry.pack()

        submit_button = tk.Button(add_word_form, text="Submit", font=('Helvetica', 12), command=lambda: self.submit_urdu_word(add_word_form))
        submit_button.pack(pady=20)
    
    def submit_urdu_word(self, form_window):
        # Get the entered word and part of speech
        word = self.word_entry.get()
        pos = self.pos_entry.get()

        if word and pos:
            # Add the word and its part of speech to the dictionary
            urdu_pos_tags[word] = pos

            # Update the urdu_pos_tags.py file with the new entry
            with open('urdu_pos_tags.py', 'w') as f:
                f.write('urdu_pos_tags = {\n')
                for key, value in urdu_pos_tags.items():
                    f.write(f'    "{key}": "{value}",\n')
                f.write('}\n')

            # Update the highlighting in the text widget
            self.highlight_words()

            # Close the form window
            form_window.destroy()
        else:
            messagebox.showerror("Error", "Both Urdu Word and Part of Speech are required.")

    
    def update_tagged_results_in_text_widget(self):
        # Clear existing tags
        self.text_widget.tag_remove("highlight", "1.0", tk.END)

        # Get the text content from the Text widget
        content = self.text_widget.get("1.0", tk.END)

        # Iterate over each word in the dictionary and highlight them
        for word in self.urdu_pos_tags:
            start = "1.0"
            while True:
                # Search for the word from the current position
                index = self.text_widget.search(word, start, stopindex=tk.END)
                if not index:
                    break
                end = f"{index}+{len(word)}c"
                self.text_widget.tag_add("highlight", index, end)
                start = end

        # Configure the appearance of the "highlight" tag
        self.text_widget.tag_configure("highlight", foreground="red")

    def clear_text(self):
        # Clear the text inside the input box
        self.input_box.delete(0, tk.END)

    def delete_text(self):
        # Delete the text from the input box
        self.input_box.delete(0, tk.END)

    # ... Existing code ...
            
def main():
    openconc = GUI(master)
    openconc.master.title("Open Concordance")
    openconc.mainloop()

if __name__ == "__main__":
    main()

