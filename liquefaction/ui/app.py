from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ..engine import LiquefactionEngine
from ..io.storage import load_project


class LiquefactionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Liquefaction Analysis Dashboard")
        self.geometry("980x620")
        self.engine = LiquefactionEngine()

        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(toolbar, text="Open Project", command=self.open_project).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Run Analysis", command=self.run_analysis).pack(side=tk.LEFT, padx=6)

        self.summary = tk.Text(self, height=8)
        self.summary.pack(fill=tk.X, padx=8)

        tabs = ttk.Notebook(self)
        tabs.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.spt_tree = self._build_table(tabs, "SPT Results")
        self.cpt_tree = self._build_table(tabs, "CPT Results")

        self.project_path: str | None = None
        self.project = None

    def _build_table(self, tabs: ttk.Notebook, label: str) -> ttk.Treeview:
        frame = ttk.Frame(tabs)
        tabs.add(frame, text=label)
        tree = ttk.Treeview(frame, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def open_project(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        self.project = load_project(path)
        self.project_path = path
        self.summary.delete("1.0", tk.END)
        self.summary.insert(tk.END, json.dumps(self.project.to_dict()["info"], indent=2))

    def _fill_tree(self, tree: ttk.Treeview, rows: list[dict]) -> None:
        tree.delete(*tree.get_children())
        if not rows:
            return
        cols = list(rows[0].keys())
        tree["columns"] = cols
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        for row in rows:
            tree.insert("", tk.END, values=[row.get(c, "") for c in cols])

    def run_analysis(self) -> None:
        if not self.project:
            messagebox.showerror("No project", "Please open a project file first")
            return
        out = self.engine.analyze(self.project)
        self._fill_tree(self.spt_tree, out.spt_results.to_dict("records"))
        self._fill_tree(self.cpt_tree, out.cpt_results.to_dict("records"))
        msg = [f"Loaded project: {Path(self.project_path or '').name}"]
        if out.errors:
            msg.extend(["Errors:", *out.errors])
        if out.warnings:
            msg.extend(["Warnings:", *out.warnings])
        self.summary.delete("1.0", tk.END)
        self.summary.insert(tk.END, "\n".join(msg))


def main() -> None:
    app = LiquefactionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
