import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class GPA_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Calculator")

        self.student_name_label = tk.Label(root, text="Student Name:")
        self.student_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.student_name_entry = tk.Entry(root)
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.university_name_label = tk.Label(root, text="University Name:")
        self.university_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.university_name_entry = tk.Entry(root)
        self.university_name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.course_name_label = tk.Label(root, text="Course Name:")
        self.course_name_label.grid(row=2, column=0, padx=10, pady=10)

        self.course_name_entry = tk.Entry(root)
        self.course_name_entry.grid(row=2, column=1, padx=10, pady=10)

        self.credit_label = tk.Label(root, text="Credit Hours:")
        self.credit_label.grid(row=3, column=0, padx=10, pady=10)

        self.credit_entry = tk.Entry(root)
        self.credit_entry.grid(row=3, column=1, padx=10, pady=10)

        self.grade_label = tk.Label(root, text="Grade:")
        self.grade_label.grid(row=4, column=0, padx=10, pady=10)

        grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
        self.grade_var = tk.StringVar(root)
        self.grade_var.set(grades[0])

        self.grade_menu = tk.OptionMenu(root, self.grade_var, *grades)
        self.grade_menu.grid(row=4, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Course", command=self.add_course)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=10, column=0, columnspan=2, pady=10)

        self.course_listbox = tk.Listbox(root, width=50, height=10)
        self.course_listbox.grid(row=6, column=0, columnspan=2, pady=10)

        self.total_credit_label = tk.Label(root, text="Total Credit Hours:")
        self.total_credit_label.grid(row=7, column=0, padx=10, pady=10)

        self.total_credit_value = tk.Label(root, text="0")
        self.total_credit_value.grid(row=7, column=1, padx=10, pady=10)

        self.overall_gpa_label = tk.Label(root, text="Overall GPA:")
        self.overall_gpa_label.grid(row=8, column=0, padx=10, pady=10)

        self.overall_gpa_value = tk.Label(root, text="0.0")
        self.overall_gpa_value.grid(row=8, column=1, padx=10, pady=10)

        self.export_button = tk.Button(root, text="Export to PDF", command=self.export_to_pdf)
        self.export_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.total_credit_hours = 0
        self.total_grade_points = 0

    def add_course(self):
        try:
            course_name = self.course_name_entry.get()
            credit = float(self.credit_entry.get())
            grade = self.grade_var.get()

            grade_points = self.convert_grade_to_points(grade) * credit
            self.total_credit_hours += credit
            self.total_grade_points += grade_points

            course_info = f"Course: {course_name}, Credit: {credit}, Grade: {grade}"
            self.course_listbox.insert(tk.END, course_info)

            self.total_credit_value.config(text=str(self.total_credit_hours))
            self.calculate_gpa()

            # Clear entry fields
            self.course_name_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.grade_var.set("A+")  # Set default grade to 'A+'
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid values for credit hours.")

    def calculate_gpa(self):
        # Calculate overall GPA
        if self.total_credit_hours > 0:
            overall_gpa = self.total_grade_points / self.total_credit_hours
            self.overall_gpa_value.config(text="{:.2f}".format(overall_gpa))

    def clear_all(self):
        # Clear all entry fields, labels, and course list
        self.student_name_entry.delete(0, tk.END)
        self.university_name_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        self.credit_entry.delete(0, tk.END)
        self.grade_var.set("A+")
        self.course_listbox.delete(0, tk.END)
        self.total_credit_hours = 0
        self.total_grade_points = 0
        self.total_credit_value.config(text="0")
        self.overall_gpa_value.config(text="0.0")

    def convert_grade_to_points(self, grade):
        grade_mapping = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D+": 1.3,
            "D": 1.0,
            "F": 0.0
        }
        return grade_mapping.get(grade, 0.0)

    def export_to_pdf(self):
        try:
            # Ask user for file name and location
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return  # User canceled the file dialog

            student_name = self.student_name_entry.get()
            university_name = self.university_name_entry.get()

            c = canvas.Canvas(file_path, pagesize=letter)

            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(300, 750, "GPA Report")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 720, "Student Name: {}".format(student_name))
            c.drawString(100, 700, "University Name: {}".format(university_name))
            c.drawString(100, 680, "Total Credit Hours: {}".format(self.total_credit_hours))
            c.drawString(100, 660, "Overall GPA: {:.2f}".format(self.total_grade_points / self.total_credit_hours))
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 620, "Course")
            c.drawString(250, 620, "Credit")
            c.drawString(400, 620, "Grade")

            c.setFont("Helvetica", 12)
            y_position = 600
            for course_info in self.course_listbox.get(0, tk.END):
                # Split the course info string to extract course name, credit, and grade
                course_name, credit, grade = [info.strip().split(":")[1] for info in course_info.split(",")]

                # Write course details to the PDF
                c.drawString(100, y_position, course_name)
                c.drawString(250, y_position, credit)
                c.drawString(400, y_position, grade)
                
                y_position -= 20

            c.save()

            messagebox.showinfo("Export Successful", "GPA report exported to {}".format(file_path))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while exporting to PDF: {}".format(str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = GPA_Calculator(root)
    root.mainloop()
