from django.db import migrations, transaction
from django.utils import timezone
from datetime import datetime
import pytz


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_test_data_book_subsubject_subject"),
        ("users", "0002_users_test_data"),
    ]

    def generate_data(apps, schema_editor):
        from django.contrib.auth.models import User
        from home.models import Subject, Sub_Subject, Book, Question
        from users.models import Profile

        question_test_data = [
            (
                "Rebecca",
                "question from math course",
                "Hey , Can someome help me solve the equation 1+1?",
                timezone.now(),
                "Math",
                "Algebra",
                "7",
                "Benny-Goren",
                14,
                True,
            ),
            (
                "Rebecca",
                "question from bible course",
                "Does god exist?",
                timezone.now(),
                "Bible",
                "Prophecies",
                "7",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "Question",
                "Was Alessandro Volta a professor of chemistry?",
                timezone.now(),
                "Chemistry",
                "",
                "11",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "question about ants",
                "Do the ants eat plants, meats, or both?	both",
                timezone.now(),
                "Biology",
                "Cell Biology",
                "10",
                "Benny-Goren",
                50,
                False,
            ),
            (
                "Ido",
                "Need help",
                "Is Hebrew the largest member of the Semitic language family??",
                timezone.now(),
                "Hebrew",
                "Writing",
                "10",
                "Modern Hebrew for Beginners",
                23,
                False,
            ),
            (
                "Ido",
                "question",
                "Where is the Berliner Dom located?",
                timezone.now(),
                "Geography",
                "Atmosphere",
                "12",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "Novel price",
                "Did Tesla win the Nobel Prize??",
                timezone.now(),
                "History",
                "Ancient history‎",
                "12",
                "Sapiens: A Brief History of Humankind",
                23,
                False,
            ),
            (
                "Danit",
                "Question from  Benny Goren Book",
                "Can you help me solve this equation 2X=8?",
                timezone.now(),
                "Math",
                "Algebra",
                "7",
                "Benny-Goren",
                100,
                False,
            ),
            (
                "Danit",
                "1984",
                "Who is the author of the book 1984?",
                timezone.now(),
                "Literature",
                "20th Century",
                "7",
                "1984",
                None,
                False,
            ),
            (
                "Rebecca",
                "where he was. He must have tried it a hundred time",
                " than half past, more like quarter \
to seven. Had the alarm clock not rung? He could see from the bed that it had been set for four oclock \
as it should have been; it certainly must have rung. Yes, but was it possible to quietly sleep through \
that furniture-ra",
                datetime(2019, 5, 3, 9, 40, 35, tzinfo=pytz.UTC),
                "Math",
                "Geometry",
                "8",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "iar walls. A collection of textile samples lay spr",
                "t and seemed ready to slide off any\
moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly\
as he looked. Whats happened to me? he thought. It wasnt a dream. His room, a proper human room although \
a little too small, lay  be",
                datetime(2020, 2, 23, 9, 1, 21, tzinfo=pytz.UTC),
                "Hebrew",
                "Text analysis",
                "11",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "to see the five oclock train",
                "Well, theres still some hope; once Ive got the money togeth\
er to pay off my parents debt to him - another five or six years I suppose - thats definitely what Ill\
do. Thats when Ill make the big change. First of all though, Ive got to get up, my train leaves at five",
                datetime(2019, 5, 4, 20, 49, 24, tzinfo=pytz.UTC),
                "Math",
                "Algebra",
                "10",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "ck? But that would be extreme",
                "ch more effort than doing your own business at home, and on \
top of that theres the curse of travelling, worries about making train connections, bad and irregul",
                datetime(2019, 3, 10, 8, 6, 36, tzinfo=pytz.UTC),
                "History",
                "Ancient history‎",
                "9",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "g forwards, it was even later than",
                "e always rolled back to where he was. He must have tr\
ied it a hundred times, shut his eyes so that he wouldnt have to look at the floundering legs, and only \
stopped when he began to feel a mild, ",
                datetime(2021, 4, 28, 23, 14, 34, tzinfo=pytz.UTC),
                "History",
                "Ancient history‎",
                "12",
                "",
                None,
                True,
            ),
            (
                "Danit",
                "r it is that Ive chosen! Travelling day in an",
                "mour-like back, and if he lifted his head \
a little he could see his brown belly, slightly",
                datetime(2020, 11, 19, 14, 18, 28, tzinfo=pytz.UTC),
                "Geography",
                "Human Geography",
                "8",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "t being there a long time ago. The",
                "like mad and the collection of samples was still not pa\
cked, and he did not at all feel particularly fresh and lively And even if he did catch the train he would\
not avoi",
                datetime(2019, 12, 27, 9, 50, 22, tzinfo=pytz.UTC),
                "Geography",
                "Physical Geography",
                "11",
                "",
                None,
                False,
            ),
            (
                "Admin",
                "orwards, it was even later tha",
                "s about making train connections, bad and irregular food,\
contact with different people all the time so that you can never get to know anyone or become friendly \
with them.",
                datetime(2021, 2, 19, 20, 34, 50, tzinfo=pytz.UTC),
                "Biology",
                "Genetics",
                "11",
                "",
                None,
                True,
            ),
            (
                "Rebecca",
                "r and forget all this nonsense, he tho",
                "owever hard he threw himself onto his right, he\
always rolled back to where he was. He must have tried it a hundred times, shut his eyes so that ",
                datetime(2019, 12, 13, 16, 53, 50, tzinfo=pytz.UTC),
                "Hebrew",
                "",
                "10",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "itted out with a fur hat and fur boa who sat uprig",
                "doctor from the medical insurance com\
pany, accuse his parents of having a lazy son, and accept the doctors recommendation not to make any claim\
as the doctor believed that no-one was ever ill but that many were workshy. And whats more, wo",
                datetime(2019, 3, 18, 23, 17, 19, tzinfo=pytz.UTC),
                "Physics",
                "",
                "9",
                "",
                None,
                True,
            ),
            (
                "Admin",
                "arents to think about Id have g",
                "tract, these gentlemen are always still sitting there ea\
ting their breakfasts. I ought to just try that wi",
                datetime(2020, 9, 19, 23, 48, 21, tzinfo=pytz.UTC),
                "Bible",
                "",
                "10",
                "",
                None,
                False,
            ),
            (
                "Admin",
                " day in and day out. Doing business like",
                "m the medical insurance company, accuse his par\
ents of having a lazy son, and accept the doctors recommendation not to make any claim as the doctor believed\
that no-one was ever ill but that many were workshy. And whats more, would he have bee",
                datetime(2019, 11, 4, 10, 39, 6, tzinfo=pytz.UTC),
                "Math",
                "Geometry",
                "10",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "to me? he thought. It wasnt a dream",
                "to the guest house during the morning to copy out the\
contract, these gentlemen are always still sitting the",
                datetime(2019, 11, 23, 12, 49, 4, tzinfo=pytz.UTC),
                "Math",
                "Geometry",
                "11",
                "",
                None,
                False,
            ),
            (
                "Danit",
                " like quarter to seven. Had the alarm ",
                "g salesman - and above it there hung a picture th\
at he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady\
fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole\
of her lower arm toward",
                datetime(2021, 3, 3, 8, 12, 26, tzinfo=pytz.UTC),
                "Hebrew",
                "",
                "9",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "d and divided by arches into st",
                "k out the window at the dull weather. Drops of rain co\
uld be heard hitting the pane, which made him feel quite sad. How about if I sleep a little bit longer\
and forget al",
                datetime(2021, 1, 1, 11, 56, 19, tzinfo=pytz.UTC),
                "Bible",
                "",
                "12",
                "",
                None,
                True,
            ),
            (
                "Admin",
                "r Samsa woke from troubled dreams, he found hi",
                "ite spots which he didnt know what to mak\
e of; and when he tried to feel the place with one of his legs he drew it quickly back because as soon as\
he  it he was overcome by a cold shudder. He slid back into his former position. Getting up earl",
                datetime(2020, 6, 13, 23, 11, 27, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "9",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "ons. The bedding was hardly ab",
                "ing legs, and only stopped when he began to feel a mild, dull\
pain there that he had never felt before. Oh, God, he thought, what a strenuous career it is that Ive chosen!\
Travelling day in and day out. Doing business like this takes much more effort than ",
                datetime(2021, 2, 4, 9, 53, 41, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "12",
                "",
                None,
                False,
            ),
            (
                "Ido",
                " should have been; it certainly must have rung. ",
                "thought, but that was something he was un\
able to do because he was used to sleeping on his right, and in his present state couldnt get into that\
position. However hard he threw himself onto his right, he always rolled back to where he was. He mus",
                datetime(2019, 5, 2, 14, 51, 6, tzinfo=pytz.UTC),
                "Chemistry",
                "Periodic Table",
                "11",
                "",
                None,
                False,
            ),
            (
                "Ido",
                "efully between its four familiar walls. A ",
                "ely strained and suspicious as in fifteen years\
of service Gregor had never once yet been ill. His boss would certainly come round with the doctor from\
the medical insurance company, accuse his parents of having",
                datetime(2020, 8, 13, 8, 2, 28, tzinfo=pytz.UTC),
                "History",
                "Ancient history‎",
                "10",
                "",
                None,
                True,
            ),
            (
                "Lior",
                "e had recently cut out of an illustrated magazine",
                "ing up early all the time, he thought, \
it makes you stupid. Youve got to get enough sleep. Other travelling salesmen live a life of luxury. For\
instance, whenever I go back to the guest house during the morning to copy out the contract, t",
                datetime(2020, 4, 2, 8, 31, 31, tzinfo=pytz.UTC),
                "Literature",
                "Medieval",
                "12",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "at and fur boa who sat upright, raising a hea",
                "e was used to sleeping on his right, and in\
his present state couldnt g",
                datetime(2020, 7, 14, 15, 35, 18, tzinfo=pytz.UTC),
                "Literature",
                "20th Century",
                "11",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "be extremely strained and suspicious as ",
                "n the spot. But who knows, maybe that would be the \
best thing for me. If I didnt have my parents to think about Id have given in my notice a long time ago,\
Id have gone up to the boss and told him just what I think, tell him everything I ",
                datetime(2020, 1, 14, 7, 3, 9, tzinfo=pytz.UTC),
                "History",
                "",
                "8",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "er human room although a little too sma",
                " past, more like quarter to seven. Had the alarm c\
lock not rung? He could see from the bed that it had been set for four oclock as it should have been; \
            it certainly must have rung. Yes, but was it possible to quietly sleep through that ",
                datetime(2021, 2, 28, 22, 56, 55, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "12",
                "",
                None,
                False,
            ),
            (
                "Lior",
                "rches into stiff sections. The bedding was hardl",
                "hough a little too small, lay peacefully\
 between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa wasa travelling\
 salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and hous",
                datetime(2019, 11, 10, 22, 59, 27, tzinfo=pytz.UTC),
                "Literature",
                "17th Century",
                "11",
                "",
                None,
                True,
            ),
            (
                "Aviv",
                "t. It wasnt a dream. His room, a proper human room",
                "g there a long time ago. The office as\
 sistant was the bosss man, spineless, and with no understanding. What about if he reported sick? But that would be \
 extremely strained and suspicious as in fifteen years of service Gregor had never once yet been ill. His boss would\
 certainly come round with",
                datetime(2020, 6, 26, 23, 22, 45, tzinfo=pytz.UTC),
                "Geography",
                "Physical Geography",
                "8",
                "",
                None,
                False,
            ),
            (
                "Ido",
                "mall, lay peacefully between its four familiar wa",
                "f slowly up on his back towards the head\
 board so that he could lift his head better; found where the itch was, and saw that it was covered with\
 lots of little white spots which he didnt know what to make of; and when h",
                datetime(2021, 3, 13, 16, 19, 35, tzinfo=pytz.UTC),
                "Geography",
                "",
                "9",
                "",
                None,
                True,
            ),
            (
                "Aviv",
                "towards the headboard so that he could lift his he",
                "of; and when he tried to feel the place\
 with one of his legs he drew it quickly back because as soon as he touched it he was overcome by a cold shudder.",
                datetime(2019, 4, 8, 22, 24, 4, tzinfo=pytz.UTC),
                "Geography",
                "Atmosphere",
                "12",
                "",
                None,
                True,
            ),
            (
                "Lior",
                "e tried it a hundred times, shu",
                "oss would certainly come round with the doctor from the \
            medical insurance company, accuse his parents of having a lazy son",
                datetime(2021, 3, 15, 15, 56, 17, tzinfo=pytz.UTC),
                "Bible",
                "Prophecies",
                "12",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "iff sections. The bedding was hardly a",
                "n; if he were to catch that he would have to rush\
like mad a",
                datetime(2020, 1, 6, 13, 24, 24, tzinfo=pytz.UTC),
                "History",
                "Ancient history‎",
                "10",
                "",
                None,
                False,
            ),
            (
                "Ido",
                "ck train go, he would have put in his report a",
                "hats definitely what Ill do. Thats when Ill\
            make the big change. First of all though, Ive got to get up, my train leave",
                datetime(2020, 8, 11, 16, 46, 43, tzinfo=pytz.UTC),
                "Physics",
                "",
                "7",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "ully between its four familiar w",
                "t he could lift his head better; found where the itch was\
            , and saw that",
                datetime(2019, 3, 20, 14, 38, 30, tzinfo=pytz.UTC),
                "English",
                "English - Oral",
                "8",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                " there, especially when you have to go right up cl",
                "nnections, bad and irregular food, \
 contact with different people all the time so that you can never get to know anyone or become friendly with them. \
 It can all go to Hell! He felt a slight itch up on his belly; pushed himself slowly up on his back towards the\
 headboard so that he could lift",
                datetime(2020, 11, 18, 23, 40, 56, tzinfo=pytz.UTC),
                "Biology",
                "Cell Biology",
                "12",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "ather. Drops of rain could be h",
                "ifferent people all the time so that you can never get\
 to know anyone or become friendly with them. It can all go to Hell! He felt a slight itch up on his belly; pushed\
 himself slowly up on hi",
                datetime(2019, 2, 15, 20, 20, 6, tzinfo=pytz.UTC),
                "Math",
                "",
                "11",
                "",
                None,
                True,
            ),
            (
                "Ido",
                "ed when he began to feel a",
                "t helplessly as he looked. Whats happened to me? he thought. It\
 wasnt a dream. His room, a proper human room although a little too small, lay peacefully be",
                datetime(2021, 3, 17, 7, 14, 56, tzinfo=pytz.UTC),
                "History",
                "The Middle Ages",
                "12",
                "",
                None,
                False,
            ),
            (
                "Ido",
                "rries about making train connecti",
                " doing your own business at home, and on top of that \
 theres the curse of travelling, worries about making train connections, bad and irregular food, contact with \
 different people all the time so that you can never get to know anyone or become friendly with them. \
 It can all go to Hell!",
                datetime(2021, 1, 4, 20, 30, 28, tzinfo=pytz.UTC),
                "Hebrew",
                "Writing",
                "10",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "nitely what Ill do. Thats when Ill make the b",
                " the time, he thought, it makes you stupid\
 Youve got to get enough sleep. Other travelling salesmen live a life of luxury. For instance, whenever\
 I go back to the guest house during the morning to copy out the contract, these gentlemen are always \
 still sitting there eating",
                datetime(2020, 2, 19, 7, 39, 17, tzinfo=pytz.UTC),
                "Literature",
                "",
                "10",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                " between its four familiar walls. A collection of",
                ", these gentlemen are always still sitting\
 there eating their breakfasts. I ought to just try that with my boss; Id get kicked out",
                datetime(2021, 3, 16, 12, 11, 23, tzinfo=pytz.UTC),
                "English",
                "Grammer",
                "8",
                "",
                None,
                False,
            ),
            (
                "Lior",
                "ow just what I feel. Hed fall right off his desk",
                "uickly back because as soon as he touched\
 it he was overcome by a cold shudder. He slid back into his former position. Getting up early all the time,\
 he thought, it makes you stupid. Youve got to get enough sleep. Other travelling salesmen live a life of\
 luxury. For instance, whene",
                datetime(2019, 6, 19, 9, 29, 49, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "7",
                "",
                None,
                True,
            ),
            (
                "Danit",
                "y fresh and lively. And e",
                "e table - Samsa was a travelling salesman - and above it there\
 hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame.\
 It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that cov",
                datetime(2019, 2, 23, 18, 46, 7, tzinfo=pytz.UTC),
                "English",
                "English - Oral",
                "11",
                "",
                None,
                True,
            ),
            (
                "Lior",
                "nd where the itch was, and saw that it was cover",
                "g on the chest of drawers. God in Heaven\
 ! he thought. It was half past six and the hands were quietly moving forwards, it was even later than \
 half past, more like quarter to seven. Had the alarm clock not rung? He c",
                datetime(2020, 10, 3, 8, 29, 23, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "12",
                "",
                None,
                True,
            ),
            (
                "Danit",
                "boss; Id get kicked out o",
                "o be sitting up there at your desk, talking down at your \
 subordinates from up there, especially when you have to go right up close because the boss is hard \
 of hearing. Well, theres still some hope; once Ive got the money together to pay off my parents de",
                datetime(2020, 9, 10, 7, 13, 25, tzinfo=pytz.UTC),
                "Literature",
                "20th Century",
                "8",
                "",
                None,
                True,
            ),
            (
                "Admin",
                "that it had been set for four oclock as it should ",
                "t should have been; it certainly must\
 have rung. Yes, but was it possi",
                datetime(2020, 6, 17, 22, 30, 32, tzinfo=pytz.UTC),
                "Physics",
                "",
                "9",
                "",
                None,
                True,
            ),
            (
                "Lior",
                " many legs, pitifully thin compared with th",
                "lower arm towards the viewer. Gregor then \
 turned to look out the window at the dull weather. Drops of rain could be heard hitting the pane,\
 which made him feel quite sad. How about if I sleep a little bit longer and forget all this nonsense,\
 he thought, but that was someth",
                datetime(2021, 3, 22, 10, 10, 25, tzinfo=pytz.UTC),
                "History",
                "Roman period",
                "9",
                "",
                None,
                True,
            ),
            (
                "Admin",
                "e a life of luxury. For instance, whenever I go ba",
                "uietly sleep through that furniture-\
            rattling noise? True, he had not slept peacefully, but probably all the more deeply because of that.\
 What should he do now? Th",
                datetime(2019, 11, 17, 15, 12, 10, tzinfo=pytz.UTC),
                "Hebrew",
                "Writing",
                "11",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                " medical insurance company, accuse his paren",
                "particularly fresh and lively. And even if\
 he did catch the train he would not avoid his bosss anger as the office assist",
                datetime(2020, 11, 14, 15, 24, 46, tzinfo=pytz.UTC),
                "Bible",
                "Gensis",
                "8",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "imself slowly up on his back towards the headb",
                " to look at the floundering legs, and only\
 stopped when he began to feel a ",
                datetime(2021, 2, 17, 18, 9, 8, tzinfo=pytz.UTC),
                "History",
                "Ancient history‎",
                "8",
                "",
                None,
                True,
            ),
            (
                "Danit",
                "d have to rush like mad and the collection of s",
                "e the five oclock train go, he would have\
 put in his report about Gregors not being",
                datetime(2019, 1, 2, 10, 22, 27, tzinfo=pytz.UTC),
                "Biology",
                "Anatomy",
                "10",
                "",
                None,
                True,
            ),
            (
                "Aviv",
                "n half past, more like quart",
                "s a travelling salesman - and above it there hung a picture th",
                datetime(2020, 7, 9, 11, 41, 50, tzinfo=pytz.UTC),
                "Biology",
                "Anatomy",
                "8",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                " rung. Yes, but was it possible to ",
                "en its four familiar walls. A collection of textile \
 samples lay spread out on the table - Samsa was a travelling salesman - an",
                datetime(2019, 1, 17, 22, 16, 14, tzinfo=pytz.UTC),
                "Geography",
                "Atmosphere",
                "10",
                "",
                None,
                True,
            ),
            (
                "Rebecca",
                "leaves at five. And he loo",
                "tle too small, lay peacefully between its four familiar walls.\
 A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there\
 hung a picture that ",
                datetime(2019, 1, 20, 15, 6, 30, tzinfo=pytz.UTC),
                "Literature",
                "17th Century",
                "10",
                "",
                None,
                False,
            ),
            (
                "Ido",
                "e boss is hard of hearing. Well,",
                "one or become friendly with them. It can all go to Hell! \
 He felt a slight itch up on his belly; pushed himself slowly up on his back towards the headboard so that he could\
 lift his head better; found wher",
                datetime(2019, 3, 4, 21, 7, 38, tzinfo=pytz.UTC),
                "Chemistry",
                "Atomic Structure",
                "9",
                "",
                None,
                True,
            ),
            (
                "Danit",
                "im everything I would, let him know j",
                " no-one was ever ill but that many were workshy. \
 And whats more, would he have be",
                datetime(2019, 10, 20, 11, 36, 4, tzinfo=pytz.UTC),
                "Math",
                "Probability",
                "7",
                "",
                None,
                True,
            ),
            (
                "Ido",
                " years of service Gregor had never once yet be",
                "looked. Whats happened to me? he thought. \
 It wasnt a dream. His room, a proper human room although a little too small, lay peacefully between its",
                datetime(2020, 2, 22, 12, 40, 56, tzinfo=pytz.UTC),
                "Chemistry",
                "Units and Measurement",
                "11",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "ched it he was overcome by a cold shudder. H",
                "oubled dreams, he found himself transformed\
 in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could\
 see his brown belly, ",
                datetime(2019, 5, 5, 8, 36, 35, tzinfo=pytz.UTC),
                "English",
                "Grammer",
                "10",
                "",
                None,
                True,
            ),
            (
                "Rebecca",
                "out if I sleep a little bit longer a",
                " moment. His many legs, pitifully thin compared \
 with the size of the rest of him, waved about helplessly as he looked. Whats happened to me? he thought.\
 It wasnt a dream. His room, a proper human room although a little too small, lay peacefully between its four\
 familiar walls. A c",
                datetime(2020, 1, 25, 16, 6, 19, tzinfo=pytz.UTC),
                "English",
                "English - Oral",
                "9",
                "",
                None,
                False,
            ),
            (
                "Danit",
                "ou have to go right up close because the",
                "former position. Getting up early all the time,\
 he thought, it makes you stupid. Youve got to get enough sleep. Other travelling salesmen live a life of luxury.\
 For instance, whenever I go back to the guest house during the morning to copy out the contract, these gen",
                datetime(2019, 6, 5, 13, 52, 9, tzinfo=pytz.UTC),
                "Chemistry",
                "Atomic Structure",
                "7",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "e chest of drawers. God in",
                "icture that he had recently cut out of an illustrated\
 magazine and housed in a nice, gilded frame. It showed a lady fitt",
                datetime(2019, 9, 24, 18, 18, 29, tzinfo=pytz.UTC),
                "Math",
                "Algebra",
                "9",
                "",
                None,
                True,
            ),
            (
                "Lior",
                "you have to go right up close becaus",
                "s and told him just what I think, tell him everything\
 I would, let him know jus",
                datetime(2020, 4, 2, 12, 59, 30, tzinfo=pytz.UTC),
                "Physics",
                "",
                "10",
                "",
                None,
                True,
            ),
            (
                "Admin",
                "e like quarter to seven. Had the alarm clock not",
                "nto a horrible vermin. He lay on his \
 armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by \
 arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment.\
 His many leg",
                datetime(2020, 6, 10, 16, 6, 20, tzinfo=pytz.UTC),
                "Chemistry",
                "Units and Measurement",
                "9",
                "",
                None,
                True,
            ),
            (
                "Admin",
                " about Gregors not being there a lon",
                "t the alarm clock, ticking on the chest of drawers.\
God in Heaven! he thought. It was half past six and the hands were quietly moving forwards, it ",
                datetime(2021, 1, 21, 9, 3, 28, tzinfo=pytz.UTC),
                "Hebrew",
                "",
                "9",
                "",
                None,
                False,
            ),
        ]

        with transaction.atomic():
            for (
                username,
                title,
                content,
                publish_date,
                subject_name,
                sub_subject_name,
                grade,
                book_name,
                book_page,
                is_edited,
            ) in question_test_data:
                curr_subject = Subject.objects.get(subject_name=subject_name)
                if sub_subject_name != "":
                    curr_sub_subject = Sub_Subject.objects.filter(
                        sub_subject_name=sub_subject_name
                    ).first()
                if book_name != "":
                    curr_book = Book.objects.get(book_name=book_name)
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                Question(
                    profile=profile,
                    title=title,
                    content=content,
                    publish_date=publish_date,
                    subject=curr_subject,
                    sub_subject=curr_sub_subject,
                    grade=grade,
                    book=curr_book,
                    book_page=book_page,
                    is_edited=is_edited,
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
