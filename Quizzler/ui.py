from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0)
        self.question_text = self.canvas.create_text(150, 125,
                                                     text="",
                                                     font=("Arial", 20, "italic"),
                                                     fill=THEME_COLOR,
                                                     width=280)
        self.canvas.grid(column=0, row=1, columnspan=2)

        true_image = PhotoImage(file="images/true.png")
        false_image = PhotoImage(file="images/false.png")

        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_button)
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_button)
        self.true_button.grid(column=0, row=2, pady=20)
        self.false_button.grid(column=1, row=2, pady=20)

        self.word_label = Label(
            text=f"Score: 0",
            font=("Arial", 15),
            bg=THEME_COLOR,
            fg="white",
            pady=20
        )
        self.word_label.grid(column=1, row=0)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.word_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="Quiz ended.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_button(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def false_button(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

