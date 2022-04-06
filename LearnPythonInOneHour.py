






def main():
    grades = []
    grade = float(input('Enter grade'))
    while grade != -1:
        grades.append((grade))
        grade = float(input('Enter grade: '))
    avg = sum(grades) / len(grades)
    print(f'The Average is: {avg}')
    print(grades)


if __name__ == '__main__':
    main()