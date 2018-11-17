from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

#Form for posting to the blog. Requires title and body
class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Post")
