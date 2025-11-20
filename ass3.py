import random
import datetime
import os

USERS_FILE = "users.txt"
QUESTIONS_FILE = "questions.txt"
SCORES_FILE = "scores.txt"


def ensure_file(path):
    if not os.path.exists(path):
        open(path, 'w', encoding='utf-8').close()


def registration():
    print('\n--- Registration ---')
    enroll = input('Enter Enrollment: ').strip()
    name = input('Enter Name: ').strip()
    email = input('Enter Email: ').strip()
    branch = input('Enter Branch: ').strip()
    year = input('Enter Year: ').strip()
    password = input('Enter Password: ').strip()

    ensure_file(USERS_FILE)

    # check duplicate
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts and parts[0] == enroll:
                print('User already exists!')
                return

    with open(USERS_FILE, 'a', encoding='utf-8') as f:
        f.write(enroll + ',' + name + ',' + email + ',' + branch + ',' + year + ',' + password + '\n')

    print('Registration Successful!')


def login():
    print('\n--- Login ---')
    enroll = input('Enter Enrollment: ').strip()
    password = input('Enter Password: ').strip()

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 6 and parts[0] == enroll and parts[5] == password:
                    print('Login Successful!')
                    user_menu(enroll)
                    return
    except FileNotFoundError:
        pass

    print('Invalid Enrollment or Password!')


def read_questions():
    ensure_file(QUESTIONS_FILE)
    qs = []
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 7:
                subject = parts[0].strip()
                q = parts[1].strip()
                a = parts[2].strip()
                b = parts[3].strip()
                c = parts[4].strip()
                d = parts[5].strip()
                ans = parts[6].strip().lower()
                if ans in ['a', 'b', 'c', 'd']:
                    qs.append((subject, q, a, b, c, d, ans))
    return qs


def attempt_quiz_random(enroll='GUEST'):
    qs = read_questions()
    if not qs:
        print('No questions available!')
        return

   
    if len(qs) <= 5:
        selected = qs
    else:
        selected = random.sample(qs, 5)

    score = 0
    answers = []  

    for i, item in enumerate(selected, 1):
        subject, q, a, b, c, d, ans = item
        print('\nQ' + str(i) + '. (' + subject + ') ' + q)
        print('a) ' + a)
        print('b) ' + b)
        print('c) ' + c)
        print('d) ' + d)
        user_ans = input('Enter answer (a/b/c/d): ').strip().lower()
        if user_ans == ans:
            score = score + 1
            is_correct = True
        else:
            is_correct = False

       
        your_text = {'a': a, 'b': b, 'c': c, 'd': d}.get(user_ans, 'Invalid')
        correct_text = {'a': a, 'b': b, 'c': c, 'd': d}.get(ans, 'Unknown')
        answers.append((q, your_text, correct_text, is_correct, user_ans, ans))

   
    print('\nYour Score: ' + str(score) + '/' + str(len(selected)))

   
    print('\n--- Score Card ---')
    for idx, it in enumerate(answers, 1):
        qtext, your_text, correct_text, is_correct, your_letter, correct_letter = it
        status = 'Correct' if is_correct else 'Wrong'
        print(str(idx) + '. ' + qtext)
        print('   Your answer   : (' + (your_letter if your_letter else '-') + ') ' + your_text)
        print('   Correct answer: (' + correct_letter + ') ' + correct_text)
        print('   Result        : ' + status + '\n')

   
    if enroll and enroll != 'GUEST':
        ensure_file(SCORES_FILE)
        with open(SCORES_FILE, 'a', encoding='utf-8') as f:
            f.write(enroll + ',RANDOM,' + str(score) + ',' + str(len(selected)) + ',' + datetime.datetime.now().isoformat() + '\n')


def update_profile(enroll):
    print('\n--- Update Profile ---')
    name = input('Enter new name: ').strip()
    email = input('Enter new email: ').strip()
    branch = input('Enter new branch: ').strip()
    year = input('Enter new year: ').strip()

    ensure_file(USERS_FILE)
    lines = []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        for line in lines:
            parts = line.strip().split(',')
            if parts and parts[0] == enroll:
                
                pwd = parts[5] if len(parts) >= 6 else ''
                f.write(enroll + ',' + name + ',' + email + ',' + branch + ',' + year + ',' + pwd + '\n')
            else:
                f.write(line)

    print('Profile Updated!')


def view_profile(enroll):
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts and parts[0] == enroll:
                    print('\n--- Profile ---')
                    print('Enrollment: ' + parts[0])
                    print('Name: ' + parts[1])
                    print('Email: ' + parts[2])
                    print('Branch: ' + parts[3])
                    print('Year: ' + parts[4])
                    return
    except FileNotFoundError:
        pass
    print('Profile not found.')


def user_menu(enroll):
    while True:
        print('\n--- User Menu ---')
        print('1. Attempt Quiz (Random from all subjects)')
        print('2. Update Profile')
        print('3. View Profile')
        print('4. Logout')

        ch = input('Enter choice: ').strip()
        if ch == '1':
            attempt_quiz_random(enroll)
        elif ch == '2':
            update_profile(enroll)
        elif ch == '3':
            view_profile(enroll)
        elif ch == '4':
            break
        else:
            print('Invalid choice!')


if __name__ == '__main__':
    ensure_file(USERS_FILE)
    ensure_file(QUESTIONS_FILE)
    ensure_file(SCORES_FILE)

    while True:
        print('\n=== QUIZ APP ===')
        print('1. Registration')
        print('2. Login')
        print('3. Quiz')
        print('4. Exit')

        choice = input('Enter choice: ').strip()
        if choice == '1':
            registration()
        elif choice == '2':
            login()
        elif choice == '3':
            attempt_quiz_random('GUEST')
        elif choice == '4':
            print('Thank you!')
            break
        else:
            print('Invalid choice!')
