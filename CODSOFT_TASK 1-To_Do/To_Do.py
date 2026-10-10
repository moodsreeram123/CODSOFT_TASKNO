"""A small, dependency-free desktop to-do list application.

Run with: python todo_app.py
Tasks are stored beside this file in todo_tasks.json.
"""

from __future__ import annotations

import json
import tkinter as tk
from datetime import date, datetime
from pathlib import Path
from tkinter import messagebox, ttk
from uuid import uuid4


DATA_FILE = Path(__file__).with_name("todo_tasks.json")
PRIORITIES = ("High", "Medium", "Low")


class TodoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Focus List")
        self.geometry("850x570")
        self.minsize(720, 480)
        self.configure(bg="#f7f8fc")
        self.tasks = self.load_tasks()
        self.current_filter = "All"
        self.selected_id: str | None = None
        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10), background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10), background="#e9ecf5")
        style.map("Treeview", background=[("selected", "#dce7ff")], foreground=[("selected", "#172554")])

        header = tk.Frame(self, bg="#172554", padx=25, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="Focus List", font=("Segoe UI Semibold", 22), fg="white", bg="#172554").pack(anchor="w")
        self.summary = tk.Label(header, font=("Segoe UI", 10), fg="#cbd5e1", bg="#172554")
        self.summary.pack(anchor="w", pady=(3, 0))

        entry = tk.Frame(self, bg="#f7f8fc", padx=25, pady=18)
        entry.pack(fill="x")
        self.title_var = tk.StringVar()
        self.due_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        tk.Entry(entry, textvariable=self.title_var, font=("Segoe UI", 11), relief="solid", bd=1).grid(row=0, column=0, sticky="ew", ipady=8)
        ttk.Combobox(entry, textvariable=self.priority_var, values=PRIORITIES, state="readonly", width=10).grid(row=0, column=1, padx=(10, 0), ipady=5)
        tk.Entry(entry, textvariable=self.due_var, width=15, font=("Segoe UI", 10), relief="solid", bd=1).grid(row=0, column=2, padx=(10, 0), ipady=8)
        tk.Button(entry, text="Add task", command=self.add_task, bg="#2563eb", fg="white", activebackground="#1d4ed8", relief="flat", font=("Segoe UI Semibold", 10), padx=18, pady=8, cursor="hand2").grid(row=0, column=3, padx=(10, 0))
        tk.Label(entry, text="Due date: YYYY-MM-DD (optional)", bg="#f7f8fc", fg="#64748b", font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", pady=(5, 0))
        entry.columnconfigure(0, weight=1)
        self.title_var.trace_add("write", lambda *_: None)

        tools = tk.Frame(self, bg="#f7f8fc", padx=25)
        tools.pack(fill="x", pady=(0, 10))
        for name in ("All", "Active", "Completed"):
            tk.Button(tools, text=name, command=lambda n=name: self.set_filter(n), relief="flat", bg="#e2e8f0", fg="#334155", font=("Segoe UI", 9), padx=12, pady=5, cursor="hand2").pack(side="left", padx=(0, 7))
        tk.Button(tools, text="Mark done / active", command=self.toggle_selected, relief="flat", bg="#dcfce7", fg="#166534", font=("Segoe UI", 9), padx=12, pady=5, cursor="hand2").pack(side="right", padx=(7, 0))
        tk.Button(tools, text="Delete", command=self.delete_selected, relief="flat", bg="#fee2e2", fg="#991b1b", font=("Segoe UI", 9), padx=12, pady=5, cursor="hand2").pack(side="right")

        table_wrap = tk.Frame(self, bg="#f7f8fc", padx=25, pady=5)
        table_wrap.pack(fill="both", expand=True)
        columns = ("status", "title", "priority", "due")
        self.tree = ttk.Treeview(table_wrap, columns=columns, show="headings", selectmode="browse")
        for key, label, width, anchor in (("status", "Status", 105, "center"), ("title", "Task", 390, "w"), ("priority", "Priority", 110, "center"), ("due", "Due date", 130, "center")):
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, anchor=anchor, stretch=key == "title")
        scrollbar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda _: self.toggle_selected())

        footer = tk.Label(self, text="Double-click a task to change its status.", bg="#f7f8fc", fg="#64748b", font=("Segoe UI", 9), padx=25, pady=12)
        footer.pack(fill="x")
        self.bind("<Return>", lambda _: self.add_task())

    def load_tasks(self) -> list[dict]:
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2, ensure_ascii=False)

    def add_task(self) -> None:
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title before adding it.")
            return

        due = self.due_var.get().strip()
        if due:
            try:
                date.fromisoformat(due)
            except ValueError:
                messagebox.showerror("Invalid date", "Please use YYYY-MM-DD format for due dates.")
                return

        task = {
            "id": str(uuid4()),
            "title": title,
            "priority": self.priority_var.get(),
            "due": due,
            "completed": False,
        }
        self.tasks.append(task)
        self.save_tasks()
        self.title_var.set("")
        self.due_var.set("")
        self.priority_var.set("Medium")
        self.selected_id = None



    def set_filter(self, filter_name: str) -> None:
        self.current_filter = filter_name
        self.refresh()

    def on_select(self, _event=None) -> None:
        selected = self.tree.selection()
        self.selected_id = selected[0] if selected else None

    def toggle_selected(self) -> None:
        if not self.selected_id:
            messagebox.showwarning("No task selected", "Select a task before toggling its status.")
            return

        for task in self.tasks:
            if task["id"] == self.selected_id:
                task["completed"] = not task.get("completed", False)
                break
        self.save_tasks()
        self.refresh()

    def delete_selected(self) -> None:
        if not self.selected_id:
            messagebox.showwarning("No task selected", "Select a task before deleting it.")
            return

        for task in self.tasks:
            if task["id"] == self.selected_id:
                self.tasks.remove(task)
                break

        self.save_tasks()
        self.selected_id = None
        self.refresh()

    def refresh(self) -> None:
        self.tree.selection_remove(self.tree.selection())
        self.tree.delete(*self.tree.get_children())

        visible_tasks = []
        for task in self.tasks:
            if self.current_filter == "Active" and task.get("completed"):
                continue
            if self.current_filter == "Completed" and not task.get("completed"):
                continue
            visible_tasks.append(task)

        for task in visible_tasks:
            values = (
                "Done" if task.get("completed") else "Active",
                task.get("title", ""),
                task.get("priority", "Medium"),
                task.get("due", ""),
            )
            iid = task["id"]
            self.tree.insert("", "end", iid=iid, values=values)
            if self.selected_id == iid:
                self.tree.selection_set(iid)

        completed = sum(1 for task in self.tasks if task.get("completed"))
        active = len(self.tasks) - completed
        if self.current_filter == "All":
            summary_text = f"{len(self.tasks)} total tasks • {active} active • {completed} completed"
        elif self.current_filter == "Active":
            summary_text = f"{active} active task(s) shown"
        else:
            summary_text = f"{completed} completed task(s) shown"
        self.summary.configure(text=summary_text)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()