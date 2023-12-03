import csv
import random

MIN_VALUE = 1
MAX_VALUE = 100
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPISODES = 1000
Q_TABLE_FILE = 'q_table.csv'  

def load_q_table():
    q_table = dict()
    try:
        with open(Q_TABLE_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                state = int(row['State'])
                q_table[state] = {
                    'higher': float(row['Higher']),
                    'lower': float(row['Lower'])
                }
        return q_table
    except FileNotFoundError:
        return None

def save_q_table(q_table):
    with open(Q_TABLE_FILE, 'w', newline='') as file:
        fieldnames = ['State', 'Higher', 'Lower']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for state, actions in q_table.items():
            writer.writerow({
                'State': str(state),
                'Higher': str(actions['higher']),
                'Lower': str(actions['lower'])
            })

q_table = load_q_table() or {state: {'higher': random.uniform(0, 1), 'lower': random.uniform(0, 1)} for state in range(MIN_VALUE, MAX_VALUE + 1)}

def guess_number():
    state = random.randint(MIN_VALUE, MAX_VALUE)
    attempts = 0  # Contador de tentativas

    while attempts < EPISODES:
        action = max(q_table[state], key=q_table[state].get)
        if action == 'higher':
            if state == MAX_VALUE:
                next_state = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                next_state = random.randint(state + 1, MAX_VALUE)
        else:
            if state == MIN_VALUE:
                next_state = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                next_state = random.randint(MIN_VALUE, state - 1)
        
        reward = 1 if next_state == state else -1
        q_table[state][action] = (1 - LEARNING_RATE) * q_table[state][action] + \
                                 LEARNING_RATE * (reward + DISCOUNT_FACTOR * max(q_table[next_state].values()))
        state = next_state

        attempts += 1  # Incrementa o número de tentativas

    return state

def autonomous_guessing_game():
    print("Pense em um número entre 1 e 100.")
    input("Pressione Enter quando estiver pronto.")

    number = None
    while True:
        number = guess_number()
        print(f"O número que você pensou é {number}!")
        if int(input("O número está correto? (Digite 1 para sim, 0 para não): ")) == 1:
            break

    save_q_table(q_table)

autonomous_guessing_game()
