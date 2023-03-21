from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, \
    PasswordField, EmailField, DateField, MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange


class YoutubeSearchForm(FlaskForm):
    url = StringField(
        '유튜브 주소를 복사해서 붙여넣어 주세요',
        validators=[DataRequired('유튜브 주소는 필수 입력 사항입니다.'), Length(min=2, max=25)]
    )