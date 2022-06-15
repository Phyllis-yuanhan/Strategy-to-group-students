from course import *
from course import *
from survey import *
from criterion import *
from grouper import *

import pytest
from typing import List, Set, FrozenSet
from example_usage import *
from hypothesis import given

@pytest.fixture
def create_student() -> List[Student]:
    student1 = Student(1, 'kiki')
    student2 = Student(2, 'sam')
    student3 = Student(3, 'black')
    student4 = Student(1, 'manbaike')
    return [student1, student2, student3, student4]

@pytest.fixture
def create_student2() -> List[Student]:
    student1 = Student(1, 'sam')
    student2 = Student(4, 'sam')
    student3 = Student(6, 'black')
    student4 = Student(5, 'manbaike')
    student5 = Student(7, 'sisi')

    return [student1, student2, student3, student4, student5]

@pytest.fixture
def create_questions() -> Tuple[
    MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, CheckboxQuestion]:
    multi_question = MultipleChoiceQuestion(1, "multi question",
                                            ['a', 'b', 'c'])
    num_question = NumericQuestion(2, "number question", 10, 15)
    yesno_question = YesNoQuestion(3, "yesno question")
    check_box_question = CheckboxQuestion(4, "check box question",
                                          ['a', 'b', 'c', 'd'])
    return multi_question, num_question, yesno_question, check_box_question

@pytest.fixture
def create_multi_answers():
    multi_ans = Answer('c')
    multi_ans2 = Answer('a')
    multi_ans3 = Answer('b')
    multi_ans4 = Answer('a')
    return [multi_ans, multi_ans2, multi_ans3, multi_ans4]

@pytest.fixture
def create_multi_answers_not_lonely():
    multi_ans = Answer('c')
    multi_ans2 = Answer('a')
    multi_ans3 = Answer('c')
    multi_ans4 = Answer('a')
    return [multi_ans, multi_ans2, multi_ans3, multi_ans4]

@pytest.fixture
def create_groups(create_student, create_student2):
    group1 = Group(create_student[0:3])
    group2 = Group(create_student2[0:3])
    group3 = Group(create_student2[1:])
    return group1, group2, group3

@pytest.fixture
def create_survey_group_one(create_questions):
    student1 = Student(1, 'kiki')
    student2 = Student(2, 'sam')
    student3 = Student(3, 'black')
    students = [student1, student2, student3]
    questions = create_questions[:3]
    multi_answers = ['a', 'd', 'a']
    number_answers = [12, 13, 14]
    yesno_answers = [True, False, True]
    for si in range(len(students)):
        students[si].set_answer(questions[0], Answer(multi_answers[si]))
        students[si].set_answer(questions[1], Answer(number_answers[si]))
        students[si].set_answer(questions[2], Answer(yesno_answers[si]))
    group1 = Group(students)
    return group1

@pytest.fixture
def create_survey_group_two(create_questions):
    student1 = Student(4, 'Jack')
    student2 = Student(5, 'Nickii')
    student3 = Student(6, 'Obama')
    students = [student1, student2, student3]
    questions = create_questions[:3]
    multi_answers = ['b', 'b', 'b']
    number_answers = [11, 12, 14]
    yesno_answers = [False, False, True]
    for si in range(len(students)):
        students[si].set_answer(questions[0], Answer(multi_answers[si]))
        students[si].set_answer(questions[1], Answer(number_answers[si]))
        students[si].set_answer(questions[2], Answer(yesno_answers[si]))
    group2 = Group(students)
    return group2



@pytest.fixture
def create_surveys(create_student):
    student1, student2, student3 = tuple(create_student[:3])
    multi_question = MultipleChoiceQuestion(1, "multi question",
                                            ['a', 'b', 'c'])
    num_question = NumericQuestion(2, "number question", 10, 15)
    yesno_question = YesNoQuestion(3, "yesno question")
    survey = Survey([multi_question, num_question, yesno_question])
    survey.set_weight(2, multi_question)
    survey.set_criterion(HeterogeneousCriterion(), num_question)
    student1.set_answer(multi_question, Answer('a'))
    student2.set_answer(multi_question, Answer('d'))
    student3.set_answer(multi_question, Answer('a'))

    return survey

@pytest.fixture
def create_example_surveys():
    sur_file = 'example_survey.json'
    sur_data = load_data(sur_file)
    return load_survey(sur_data)

@pytest.fixture
def create_example_course():
    c_file = 'example_course.json'
    c_data = load_data(c_file)
    return load_course(c_data)


def get_group_students(grouping: Grouping) -> FrozenSet[FrozenSet[str]]:
    groups = grouping.get_groups()
    result = []
    for group in groups:
        result.append(frozenset([member.name for member in group.get_members()]))
    return frozenset(result)

class Testcourse:
    def test_get_answer(self, create_student, create_questions) -> None:
        student1 = create_student[0]
        q1 = create_questions[0]
        yesno = create_questions[2]
        assert student1.get_answer(q1) is None
        assert student1.has_answer(q1) is False
        a1 = Answer('a')
        a2 = Answer(True)
        student1.set_answer(q1, a1)
        student1.set_answer(yesno, a2)
        assert student1.get_answer(q1) == a1
        assert student1.has_answer(q1) is True
        assert student1.has_answer(yesno) is True


class TestSurvey:
    def test_vaildate_answer(self, create_questions):
        multi_question = create_questions[0]
        num_question = create_questions[1]
        check_box_question = create_questions[3]
        multi_answer_out, wrong_check_answer1, wrong_check_answer2 = Answer(
            'd'), Answer([]), Answer(['a', 'a', 'c'])
        correct_check_answer3 = Answer(['a', 'b', 'c', 'd'])
        wrong_check_answer4 = Answer(['a', 'b', 'c', 'd', 'e'])
        assert multi_question.validate_answer(multi_answer_out) is False
        assert num_question.validate_answer(multi_answer_out) is False
        assert multi_question.validate_answer(wrong_check_answer1) is False
        assert check_box_question.validate_answer(wrong_check_answer1) is False
        assert check_box_question.validate_answer(wrong_check_answer2) is False
        assert check_box_question.validate_answer(correct_check_answer3) is True
        assert check_box_question.validate_answer(wrong_check_answer4) is False

    def test_similarity(self, create_questions):
        num_question = create_questions[1]
        check_question = create_questions[3]
        num_answer1 = Answer(10)
        num_answer2 = Answer(15)
        assert num_question.get_similarity(num_answer1, num_answer2) == 0
        check_answer1 = Answer(['a', 'b'])
        check_answer2 = Answer(['c'])
        assert check_question.get_similarity(check_answer1, check_answer1) == 1
        assert check_question.get_similarity(check_answer2, check_answer1) == 0

    def test_add_grouping(self, create_survey_group_one):
        grouping = Grouping()
        assert grouping.add_group(create_survey_group_one) is True
        assert grouping.add_group(create_survey_group_one) is False

    def test_score_students_error(self, create_surveys, create_survey_group_one):
        assert create_surveys.score_students(
            create_survey_group_one.get_members()) == 0.0

    def test_score_students_good(self, create_surveys, create_survey_group_two):
        assert create_surveys.score_students(
            create_survey_group_two.get_members()) == 0.9111111111111111

    def test_score_grouping(self, create_surveys, create_survey_group_two, create_survey_group_one):
        grouping = Grouping()
        assert create_surveys.score_grouping(grouping) == 0.0
        grouping.add_group(create_survey_group_two)
        grouping.add_group(create_survey_group_one)
        assert create_surveys.score_grouping(grouping) == 0.45555555555555555

class TestCritertion:
    def test_score_answers(self, create_questions, create_multi_answers):
        multi_q = create_questions[0]
        num_ans = Answer(12)
        multi_ans = create_multi_answers[0]
        multi_ans2 = create_multi_answers[1]
        multi_ans3 = create_multi_answers[2]
        multi_ans4 = create_multi_answers[3]
        homo_crit = HomogeneousCriterion()
        heter_crit = HeterogeneousCriterion()
        with pytest.raises(InvalidAnswerError):
            homo_crit.score_answers(multi_q, [num_ans, multi_ans])
        with pytest.raises(InvalidAnswerError):
            heter_crit.score_answers(multi_q, [num_ans, multi_ans])
        assert homo_crit.score_answers(multi_q, [multi_ans]) == 1.0
        assert heter_crit.score_answers(multi_q, [multi_ans]) == 0.0
        assert homo_crit.score_answers(multi_q, [multi_ans, multi_ans2,
                                                 multi_ans3, multi_ans4]) == 1/6
        assert heter_crit.score_answers(multi_q, [multi_ans, multi_ans2,
                                                 multi_ans3,
                                                 multi_ans4]) == 5 / 6

    def test_lone_answers(self, create_questions, create_multi_answers,
                          create_multi_answers_not_lonely):
        multi_q = create_questions[0]
        lone_crit = LonelyMemberCriterion()
        assert lone_crit.score_answers(multi_q, create_multi_answers) == 0.0
        assert lone_crit.score_answers(multi_q, create_multi_answers_not_lonely) == 1.0



class TestGrouper:
    def test_grouping(self, create_groups):
        grouping = Grouping()
        assert grouping.add_group(create_groups[0]) is True
        assert grouping.add_group(create_groups[2]) is True
        assert '\n' in str(grouping)
        assert 'kiki' in str(grouping)

    def test_empty_group(self):
        grouping = Grouping()
        empty_group = Group([])
        assert grouping.add_group(empty_group) is False

    def test_duplicate_grouping(self, create_groups):
        grouping = Grouping()
        assert grouping.add_group(create_groups[0]) is True
        assert grouping.add_group(create_groups[1]) is False

    def test_get_group(self, create_groups):
        grouping = Grouping()
        assert grouping.add_group(create_groups[0]) is True
        assert grouping._groups is not grouping.get_groups()
        assert grouping._groups[0] is grouping.get_groups()[0]


class TestHelper:
    def test_slice_list(self):
        assert slice_list(['a', 'b', 'c', 'd'], 2) == [['a', 'b'], ['c', 'd']]
        assert slice_list(['a', 'b', 'c', 'd'], 3) == [['a', 'b', 'c'], ['d']]
        assert slice_list(['a', 'b', 'c', 'd'], 4) == [['a', 'b', 'c', 'd']]

    def test_window(self):
        assert windows([3, 4, 6, 2, 3], 3) == [[3, 4, 6], [4, 6, 2], [6, 2, 3]]
        assert windows([2, 3, 4], 3) == [[2,3,4]]


class TestGrouping:
    def test_alpha_grouping(self, create_example_surveys, create_example_course):
        survey1 = create_example_surveys
        alpha = AlphaGrouper(2)
        grouping1 = alpha.make_grouping(create_example_course, survey1)
        assert get_group_students(grouping1) == frozenset({frozenset({"Billy Gilbert", "Otis Harlan"}) , frozenset({"Pinto Colvig",
                                                "Roy Atwell"}), frozenset({"Scotty Mattraw"})})
        alpha.group_size = 6
        grouping1 = alpha.make_grouping(create_example_course, survey1)
        assert get_group_students(grouping1) == frozenset({frozenset({"Billy Gilbert", "Otis Harlan", "Pinto Colvig",
                                                "Roy Atwell", "Scotty Mattraw"})})

    def test_greed_grouper(self, create_surveys, create_survey_group_two, create_survey_group_one):
        survey1 = create_surveys
        students = list(set(create_survey_group_one.get_members()).union(set((create_survey_group_two.get_members()))))
        greedy = GreedyGrouper(3)
        course1 = Course('good course')
        course1.enroll_students(students)
        grouping2 = greedy.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'Obama', 'kiki', 'black'}), frozenset({'sam', 'Nickii', 'Jack'})})
        greedy.group_size = 2
        grouping2 = greedy.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'black', 'kiki'}), frozenset({'sam', 'Jack'}), frozenset({'Obama', 'Nickii'})})
        greedy.group_size = 4
        grouping2 = greedy.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'Jack', 'Obama', 'black', 'kiki'}), frozenset({'Nickii', 'sam'})})

    def test_window_grouper(self, create_surveys, create_survey_group_two, create_survey_group_one):
        survey1 = create_surveys
        students = list(set(create_survey_group_one.get_members()).union(
            set((create_survey_group_two.get_members()))))
        window = WindowGrouper(3)
        course1 = Course('good course')
        course1.enroll_students(students)
        grouping2 = window.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'sam', 'kiki', 'black'}), frozenset({'Nickii', 'Jack', 'Obama'})})
        window.group_size = 2
        grouping2 = window.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'sam', 'kiki'}), frozenset({'Nickii', 'Jack'}), frozenset({'black', 'Obama'})})
        window.group_size = 4
        grouping2 = window.make_grouping(course1, survey1)
        assert get_group_students(grouping2) == frozenset({frozenset({'sam', 'kiki', 'Jack', 'black'}), frozenset({'Nickii', 'Obama'})})

if __name__ == '__main__':
    pytest.main(['a1_pytest.py'])
