# QA Documentation

The Question Answer Project Documentation

## Models

### LANGUAGE_SKILLS

- QAUser

  It's the QAuser which holds it's own fields.

  Important Fields:

  - is_activate: is `true` if has activated the link which has been sent to the mail.
  - level: level of the user, which is determined base on the user answers and level detection question set which has to answer after registeration.
  - other fields are for user profile which will be complete in the register level.

- QAGroup

  Group for the users for TextWriting correction by admins.

  Important Fields:

  - name: name of group.
  - users: users of group.
  - admins: admins of the group which can correct users's writings.

- Multiple Choice Question Models

  - MultipleChoiceQuestion

    A multiple choice Question including its full text, options, origin text and answer.

    Important Fields:

    - text: Sentence question including /&&**question**&&/ which is a placeholder for answer.
    - whole_text: Whole paragraph question (including sentence question) including /&&**question**&&/ which is a placeholder for answer.
    - level: level of question (A is easy, C is Hard).
    - origin_text: Foreign key to the origin text(it is not a question).

  - SelectedMCQuestion

    Instance of a MultipleChoiceQuestion and it is a connection between a question set and a question. MCQuestionSet includes multiple SelectedMCQuestion items to make a set of questions.

    Important Fields:

    - answer: user's answer.

  - MCQuestionSet

    Set of questions

    Important Fields:

    - question_count: number of questions.
    - right_answers: number of right answers for this set.
    - answer_percentage: score of this question set in percentage.
    - user: user which has answered this set.

- Blank Question Models

  - BlankQuestion

    A Blank Question including its full text, origin text and answer.

    Important Fields:

    - text: Sentence question including /&&**question**&&/ which is a placeholder for answer.
    - whole_text: Whole paragraph question (including sentence question) including /&&**question**&&/ which is a placeholder for answer.
    - level: level of question (A is easy, C is Hard).
    - origin_text: Foreign key to the origin text(it is not a question).

  - SelectedBlankQuestion

    Instance of a BlankQuestion and it is a connection between a question set and a question. BlankQuestionSet includes multiple SelectedBlankQuestion items to make a set of questions.

    Important Fields:

    - answer: user's answer.

  - BlankQuestionSet

    Set of questions

    Important Fields:

    - question_count: number of questions.
    - right_answers: number of right answers for this set.
    - answer_percentage: score of this question set in percentage.
    - user: user which has answered this set.

- Blocked

  This table includes words which are not valid for answer. So when the questions are made they won't be considered as an answer. For example `,` is not a valid answer and is added to this table.

- PrePosition

  List of prepositions. This table is used for MultipleChoice options.

- VerbInfo, VerbForm

  List of verbs. This table is used for MultipleChoice options.

- Config

  `Configs` used in the project.

- LevelDetectionQuestion

  Set of questions that are used for level detection. It includes both multiple choice and blank questions.

- TextWriting

  This table contains texts are written by users and admins need to correct them.

  Important Fields:

  - text: correct version of user's text.
  - modified_text: correct version of user's text.
  - is_done: if correction is complete and done.

## Views:

### language_skills:

All the below functions and classes are in the `language_skills/views.py` file.

- Create Questions:
  - CreateQuestions: This is a `View Class` which will create both Blank questions from files in the `data` directory of the project.
  - CreateMCQuestions: This is a `View Class` which will create both Multiple Choice questions from files in the `data` directory of the project.
  - email: a function which will send email. parameter are(by order): `subject`,`message` and `dest`. `dist` is email of the receiver of the message.
  - `svm_req`, `rf_req`, `logistic_req`: check `svm`, `random forrest` and `logistic regression` for the models of questions.
