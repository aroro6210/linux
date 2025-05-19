import pandas as pd
import random

EXCEL_FILE = '리눅스 6, 7 DB.xlsx'

def get_category_list(df):
    return sorted(df['category'].unique())

def select_category(category_list):
    print("""
╔════════════════════════════════════════════╗
║      🐧 Welcome to the Linux Quiz! 🐧     ║
║                                            ║
║    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓      ║
║    ┃   지식을 향한 모험에 오신 걸    ┃      ║
║    ┃         환영합니다!            ┃      ║
║    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛      ║
║                                            ║
║   💡 실력을 테스트하고 성장하세요! 💡      ║
║   🚀 문제를 풀 준비가 되셨나요? 🚀        ║
╚════════════════════════════════════════════╝
""")
    print("주제 목록:")
    for idx, cat in enumerate(category_list, 1):
        print(f"{idx}. {cat}")
    while True:
        choice = input(f"공부할 주제 번호를 입력하세요 (1~{len(category_list)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(category_list):
            return category_list[int(choice)-1]
        else:
            print(f"잘못된 입력입니다. 1~{len(category_list)} 중에 선택해주세요.")

def generate_problems(df, category):
    filtered = df[df['category'] == category].copy().sample(frac=1, random_state=random.randint(0,10000)).reset_index(drop=True)
    # 객관식 15문제, 주관식 5문제 분리
    objective_sample = filtered.iloc[:15]
    subjective_sample = filtered.iloc[15:20]
    return objective_sample, subjective_sample

def generate_choices(df, correct_answer):
    candidates = df['answer'].unique().tolist()
    candidates = [ans for ans in candidates if ans != correct_answer]
    # 오답이 3개보다 적으면 최대한 뽑기
    choices = random.sample(candidates, min(3, len(candidates)))
    choices.append(correct_answer)
    random.shuffle(choices)
    return choices

def ask_objective_question(row, df):
    print("\n문제(객관식):")
    print(row['question'])
    choices = generate_choices(df, row['answer'])
    for idx, choice in enumerate(choices, 1):
        print(f"{idx}. {choice}")
    user_input = input("정답 번호를 입력하세요: ").strip()
    try:
        user_choice = int(user_input)
        if choices[user_choice - 1] == row['answer']:
            print("정답입니다!\n")
        else:
            print(f"오답입니다. 정답: {row['answer']}\n")
    except:
        print(f"입력이 올바르지 않습니다. 정답: {row['answer']}\n")

def ask_subjective_question(row):
    print("\n문제(주관식):")
    print(row['question'])
    user_answer = input("답을 입력하세요: ").strip()
    if user_answer.lower() == str(row['answer']).strip().lower():
        print("정답입니다.\n")
    else:
        print(f"오답입니다. 정답: {row['answer']}\n")

def main():
    df = pd.read_excel(EXCEL_FILE)
    category_list = get_category_list(df)
    category = select_category(category_list)
    objective, subjective = generate_problems(df, category)
    
    print(f"\n--- {category} 객관식 15문제 ---")
    for _, row in objective.iterrows():
        ask_objective_question(row, df)
    print(f"\n--- {category} 주관식 5문제 ---")
    for _, row in subjective.iterrows():
        ask_subjective_question(row)

if __name__ == '__main__':
    main()
