from course import sort_students, Student, Course
from criterion import InvalidAnswerError, Criterion, HomogeneousCriterion, \
    HeterogeneousCriterion, LonelyMemberCriterion
from survey import Question, MultipleChoiceQuestion, NumericQuestion, \
    YesNoQuestion, CheckboxQuestion, Answer, Survey
from grouper import Group, Grouper, GreedyGrouper, AlphaGrouper, Grouping, \
    WindowGrouper, RandomGrouper
from grouper import slice_list, windows
import pytest
from typing import List, Set, FrozenSet

# Students
s1 = Student(1, 'John')
s2 = Student(2, 'Mary')
s3 = Student(3, 'Tom')
s4 = Student(4, 'Clara')
s5 = Student(5, 'Bob')
s6 = Student(6, 'Joanna')
student_list = [s1, s2, s3, s4]
student_list2 = [s5, s6, s4]

# Courses
c1 = Course('csc148')
c2 = Course('csc165')

# Questions
mcq1 = MultipleChoiceQuestion(1, 'Pick One', ['a', 'b', 'c'])
mcq2 = MultipleChoiceQuestion(2, 'Pick One', ['a', 'b', 'c'])
nq1 = NumericQuestion(1, 'Calculate 5 + 5', 0, 100)
ynq1 = YesNoQuestion(1, 'Is the sky blue?')
cq1 = CheckboxQuestion(1, 'Which of the following are less than 5?',
                       ['1', '2', '3', '4', '5'])
question_list = [mcq1, nq1, ynq1, cq1]
single_question = [mcq1]

# Answers
a01 = Answer('a')
a02 = Answer('b')
a03 = Answer('a')
a11 = Answer(10)
a12 = Answer(20)
a21 = Answer(True)
a22 = Answer(False)
a31 = Answer(['1', '2', '3', '4'])
a32 = Answer(['1', '2'])

answer_list = [a01, a02, a03]

# Survey
survey0 = Survey(single_question)
survey1 = Survey(question_list)

# Grouping
g = Grouping()
gg = Grouping()

# Group
group1 = Group([s1, s2])


def test_sort_students_id() -> None:
    assert sort_students(student_list, 'id') == [s1, s2, s3, s4]


def test_sort_students_name() -> None:
    assert sort_students(student_list, 'name') == [s4, s1, s2, s3]


class TestStudent:
    def test__str__(self) -> None:
        s = student_list[1]
        assert s.name == str(s)

    def test_has_answer_true(self) -> None:
        s1.set_answer(mcq1, a01)
        assert s1.has_answer(mcq1) is True

    def test_has_answer_false(self) -> None:
        assert s2.has_answer(mcq1) is False

    def test_set_answer(self) -> None:
        s2.set_answer(mcq1, a01)
        assert s2.has_answer(mcq1) is True

    def test_get_answer_empty(self) -> None:
        assert s3.get_answer(mcq1) is None

    def test_get_answer_not_empty(self) -> None:
        assert s2.get_answer(mcq1) == a01


class TestCourse:
    def test_enroll_students(self) -> None:
        c1.enroll_students(student_list)
        assert len(c1.students) == len(student_list)

    def test_enroll_students_violation(self) -> None:
        c = Course('cs')
        c.enroll_students(student_list2)
        assert len(c.students) == len(student_list2)

    def test_all_answered(self) -> None:
        s3.set_answer(mcq1, a01)
        s4.set_answer(mcq1, a01)
        assert c1.all_answered(survey0) is True

    def test_get_students(self) -> None:
        assert len(c1.get_students()) == len(tuple(student_list))


class TestMultipleChoiceQuestion:
    def test__str__(self) -> None:
        assert str(mcq1) == 'Question: Pick One. Options: a, b, c'

    def test_validate_answer(self) -> None:
        assert mcq1.validate_answer(a01) is True

    def test_get_similarity_zero(self) -> None:
        assert mcq1.get_similarity(a01, a02) == 0

    def test_get_similarity_one(self) -> None:
        assert mcq1.get_similarity(a01, a03) == 1


class TestNumericQuestion:
    def test__str__(self) -> None:
        assert str(nq1) == 'Question: Calculate 5 + 5. The answer is between 0'\
                           ' and 100'

    def test_validate_answer(self) -> None:
        assert nq1.validate_answer(a11) is True

    def test_get_similarity(self) -> None:
        assert nq1.get_similarity(a11, a12) == 0.9


class TestYesNoQuestion:
    def test__str__(self) -> None:
        assert str(ynq1) == 'Question: Is the sky blue? The possible answer ' \
                            'is True or False'

    def test_validate_answer(self) -> None:
        assert ynq1.validate_answer(a21) is True

    def test_get_similarity(self) -> None:
        assert ynq1.get_similarity(a21, a22) == 0


class TestCheckboxQuestions:
    def test__str__(self) -> None:
        assert str(cq1) == 'Question: Which of the following are less than 5?' \
                           ' Options: 1, 2, 3, 4, 5'

    def test_validate_answer(self) -> None:
        assert cq1.validate_answer(a31) is True

    def test_get_similarity(self) -> None:
        assert cq1.get_similarity(a31, a32) == 0.5


class TestAnswer:
    def test_is_valid(self) -> None:
        assert a01.is_valid(mcq1)


class TestSurvey:
    def test__len__(self) -> None:
        assert len(survey0) == 1

    def test__contains__(self) -> None:
        assert mcq1 in survey0

    def test__str__(self) -> None:
        assert str(survey1) == 'Question: Which ' \
                               'of the following are less than 5? '

    def test_get_questions(self) -> None:
        s = Survey([mcq1])
        assert s.get_questions()[0] == mcq1

    def test__get_criterion(self) -> None:
        survey1.set_criterion(LonelyMemberCriterion, mcq1)
        assert survey1._get_criterion(mcq1) == LonelyMemberCriterion

    def test__get_weight(self) -> None:
        survey1.set_weight(2, mcq1)
        assert survey1._get_weight(mcq1) == 2

    def test_set_criterion(self) -> None:
        survey1.set_criterion(HomogeneousCriterion, mcq1)
        assert survey1._get_criterion(mcq1) == HomogeneousCriterion

    def test_set_weight(self) -> None:
        survey1.set_weight(3, mcq1)
        assert survey1._get_weight(mcq1) == 3

    def test_score_students(self) -> None:
        assert survey0.score_students(student_list) == 1.0

    def test_score_grouping(self) -> None:
        s = Survey([mcq1, mcq2])
        g1 = Group([s1, s2])
        g2 = Group([s3, s4])
        g.add_group(g1)
        g.add_group(g2)
        s1.set_answer(mcq2, a01)
        s2.set_answer(mcq2, a02)
        s3.set_answer(mcq2, a02)
        s4.set_answer(mcq2, a03)
        assert s.score_grouping(g) == 0.5


class TestHomogeneousCriterion:
    def test_score_answers(self) -> None:
        x = HomogeneousCriterion()
        assert round(x.score_answers(mcq1, answer_list), 5) == 0.33333


class TestHeterogeneousCriterion:
    def test_score_answer(self) -> None:
        y = HeterogeneousCriterion()
        assert round(y.score_answers(mcq1, answer_list), 5) == 0.66667


class TestLonelyMemberCriterion:
    def test_score_answer(self) -> None:
        z = LonelyMemberCriterion()
        assert round(z.score_answers(mcq1, answer_list), 5) == 0


def test_slice_list_middle() -> None:
    num_list = [1, 2, 3]
    assert slice_list(num_list, 1) == [[1], [2], [3]]


def test_slice_list_zero() -> None:
    num_list = [1, 2, 3]
    assert slice_list(num_list, 0) == []


def test_windows_zero() -> None:
    num_list = [1, 2, 3]
    assert windows(num_list, 0) == []


def test_windows_middle() -> None:
    num_list = [1, 2, 3]
    assert windows(num_list, 2) == [[1, 2], [2, 3]]


class TestAlphaGrouper:
    def test_make_grouping(self) -> None:
        alpha_group = AlphaGrouper(2)
        c10 = Course('math')
        c10.enroll_students(student_list)
        assert len(alpha_group.make_grouping(c10, survey1)) == 2
        a = alpha_group.make_grouping(c10, survey1).get_groups()[0]
        assert s4, s1 in a


class TestRandomGrouper:
    def test_make_grouping(self) -> None:
        random_group = RandomGrouper(3)
        c10 = Course('math')
        c10.enroll_students(student_list)
        assert len(random_group.make_grouping(c10, survey1)) == 2


class TestGreedyGrouper:
    def test_make_grouping(self) -> None:
        c8 = Course('psy')
        c8.enroll_students(student_list)
        s1.set_answer(mcq1, Answer('a'))
        s2.set_answer(mcq1, Answer('b'))
        s3.set_answer(mcq1, Answer('c'))
        s4.set_answer(mcq1, Answer('d'))
        greedy_group = GreedyGrouper(2)
        assert len(greedy_group.make_grouping(c8, survey0)) == 2


class TestWindowGrouper:
    def test_make_grouping(self) -> None:
        c9 = Course('eco')
        c9.enroll_students(student_list)
        s1.set_answer(mcq1, Answer('a'))
        s2.set_answer(mcq1, Answer('b'))
        s3.set_answer(mcq1, Answer('c'))
        s4.set_answer(mcq1, Answer('d'))
        window_group = WindowGrouper(2)
        assert len(window_group.make_grouping(c9, survey0)) == 2


class TestGroup:
    def test__len__(self) -> None:
        assert len(group1) == 2

    def test__contains__(self) -> None:
        assert s1 in group1

    def test__str__(self) -> None:
        assert str(group1) == 'John, Mary'

    def test_get_members(self) -> None:
        assert group1.get_members() == [s1, s2]


class TestGrouping:
    def test__len__(self) -> None:
        g1 = Group([s1, s2])
        g2 = Group([s3])
        assert len(gg) == 0
        gg.add_group(g1)
        gg.add_group(g2)
        assert len(gg) == 2

    def test__str__(self) -> None:
        assert str(gg) == 'John, Mary\nTom'

    def test_add_group(self) -> None:
        assert len(gg) == 2
        g3 = Group([s5])
        g4 = Group([s3])
        gg.add_group(g3)
        gg.add_group(g4)
        assert len(gg) == 3

    def test_get_groups(self) -> None:
        g1 = Group([s1, s2])
        ggg = Grouping()
        ggg.add_group(g1)
        assert ggg.get_groups()[0] == g1


if __name__ == '__main__':
    pytest.main(['tests2.py'])
