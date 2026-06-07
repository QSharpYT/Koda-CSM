import tkinter as tk
from core.storage import load_snippets,save_snippets
from core.search import filter_snippets
from core.clipboard import copy

class MainWindow:
    def __init__(self,root):
        self.root=root
        root.title('Koda')
        root.geometry('1200x750')
        root.configure(bg='black')
        self.data=load_snippets()

        tk.Label(root,text='Koda',bg='black',fg='white',font=('Segoe UI',24,'bold')).pack(pady=8)

        self.search=tk.StringVar()
        self.search.trace_add('write',lambda *_:self.refresh())
        tk.Entry(root,textvariable=self.search,bg='white',fg='black').pack(fill='x',padx=10)

        body=tk.Frame(root,bg='black'); body.pack(fill='both',expand=True,padx=10,pady=10)

        self.list=tk.Listbox(body,bg='#00ffff',fg='black',width=30)
        self.list.pack(side='left',fill='y')
        self.list.bind('<<ListboxSelect>>',self.select)

        right=tk.Frame(body,bg='black'); right.pack(side='left',fill='both',expand=True,padx=10)

        self.title_e=tk.Entry(right,bg='white',fg='black'); self.title_e.pack(fill='x')
        self.tags_e=tk.Entry(right,bg='white',fg='black'); self.tags_e.pack(fill='x',pady=5)

        self.code=tk.Text(right,bg='#00ffff',fg='black'); self.code.pack(fill='both',expand=True)

        btns=tk.Frame(right,bg='black'); btns.pack(fill='x')
        for t,c in [('New',self.new),('Save',self.save),('Copy',self.copy_code),('Delete',self.delete)]:
            tk.Button(btns,text=t,bg='white',fg='black',command=c).pack(side='left',padx=2,pady=4)

        self.refresh()

    def refresh(self):
        self.filtered=filter_snippets(self.data,self.search.get())
        self.list.delete(0,'end')
        for s in self.filtered: self.list.insert('end',s['title'])

    def select(self,e=None):
        if not self.list.curselection(): return
        s=self.filtered[self.list.curselection()[0]]
        self.title_e.delete(0,'end'); self.title_e.insert(0,s['title'])
        self.tags_e.delete(0,'end'); self.tags_e.insert(0,s['tags'])
        self.code.delete('1.0','end'); self.code.insert('1.0',s['code'])

    def new(self):
        self.title_e.delete(0,'end'); self.tags_e.delete(0,'end'); self.code.delete('1.0','end')

    def save(self):
        item={'title':self.title_e.get(),'tags':self.tags_e.get(),'code':self.code.get('1.0','end').strip()}
        found=False
        for i,s in enumerate(self.data):
            if s['title']==item['title']:
                self.data[i]=item; found=True
        if not found: self.data.append(item)
        save_snippets(self.data); self.refresh()

    def copy_code(self):
        copy(self.root,self.code.get('1.0','end'))

    def delete(self):
        title=self.title_e.get()
        self.data=[s for s in self.data if s['title']!=title]
        save_snippets(self.data); self.refresh(); self.new()
